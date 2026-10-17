#!/usr/bin/env python3
"""
Trad-Chem-LLM submission checker.

Every contribution must come as THREE files with the same base name and identical content:
    contributions/curcumin_top10.csv
    contributions/curcumin_top10.json
    contributions/curcumin_top10.py

Check them (give the path WITHOUT the extension, or give the three files):
    python3 check_submission.py contributions/curcumin_top10
    python3 check_submission.py a.csv b.json c.py

What it does
  1. confirms all three files exist
  2. loads each one into its own throw-away database (your real tradmed.db is never touched)
  3. confirms the three databases hold exactly the same data
  4. flags leftover example rows, missing sources, and chemicals without 10 proteins

Maintainers only:  add --import to load a passing submission into tradmed.db
    python3 check_submission.py contributions/curcumin_top10 --import

NOTE for maintainers: the .py file is executed to read it. Read a stranger's .py before checking it.
"""
import argparse, importlib.util, os, sqlite3, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from import_data import import_record, run as run_import, DB_DEFAULT  # noqa: E402

SCHEMA = os.path.join(HERE, "schema.sql")

# name-based (not id-based) views of everything a contribution can contain
QUERIES = {
    "chemical":          "SELECT chemical_name, smiles, pubchem_cid FROM chemical",
    "medicine/plant":    """SELECT tm.name, tm.system, p.scientific_name, p.plant_type, p.part_used, p.family,
                                  p.common_name, c.chemical_name
                           FROM plant p
                           JOIN plant_chemical pc USING(plant_id) JOIN chemical c USING(chemical_id)
                           LEFT JOIN medicine_plant mp USING(plant_id)
                           LEFT JOIN traditional_medicine tm USING(medicine_id)""",
    "chemical->protein": """SELECT c.chemical_name, cp.target_rank, cp.uniprot_id, cp.method, cp.score, cp.source_ref
                           FROM chemical_protein cp JOIN chemical c USING(chemical_id)""",
    "protein":           """SELECT p.uniprot_id, p.protein_name, p.acronym, s.taxon_id, s.scientific_name
                           FROM protein p LEFT JOIN species s USING(taxon_id)""",
    "structure":         "SELECT uniprot_id, source_db, structure_id, is_best FROM structure",
    "GO":                "SELECT pg.uniprot_id, g.go_id, g.name FROM protein_go pg JOIN go_term g USING(go_id)",
    "cell type":         """SELECT pc.uniprot_id, ct.name FROM protein_cell_type pc
                           JOIN cell_type ct USING(cell_type_id)""",
    "protein disease":   "SELECT pd.uniprot_id, d.name FROM protein_disease pd JOIN disease d USING(disease_id)",
    "chemical disease":  """SELECT c.chemical_name, d.name FROM chemical_disease cd
                           JOIN chemical c USING(chemical_id) JOIN disease d USING(disease_id)""",
}


def new_db(folder, name):
    path = os.path.join(folder, name + ".db")
    con = sqlite3.connect(path)
    con.executescript(open(SCHEMA).read())
    con.commit()
    con.close()
    return path


def load_py(db, path):
    spec = importlib.util.spec_from_file_location("submitted_py", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "CHEMICAL") or not hasattr(mod, "TARGETS"):
        raise ValueError("the .py file must define CHEMICAL and TARGETS (copy add_top10.py)")
    con = sqlite3.connect(db)
    con.execute("PRAGMA foreign_keys=ON")
    try:
        import_record(con, dict(mod.CHEMICAL, targets=mod.TARGETS))
        con.commit()
    finally:
        con.close()


def snapshot(db):
    con = sqlite3.connect(db)
    snap = {}
    for name, q in QUERIES.items():
        snap[name] = {tuple("" if v is None else str(v) for v in row) for row in con.execute(q)}
    con.close()
    return snap


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", help="base path without extension, or the three files")
    ap.add_argument("--import", dest="do_import", action="store_true",
                    help="maintainers: load a passing submission into tradmed.db")
    ap.add_argument("--db", default=DB_DEFAULT)
    a = ap.parse_args()

    if len(a.paths) == 1:
        base = a.paths[0]
        for ext in (".csv", ".json", ".py"):
            if base.lower().endswith(ext):
                base = base[: -len(ext)]
        files = {"csv": base + ".csv", "json": base + ".json", "py": base + ".py"}
    else:
        files = {}
        for p in a.paths:
            ext = os.path.splitext(p)[1].lower().lstrip(".")
            if ext not in ("csv", "json", "py") or ext in files:
                sys.exit("Give exactly one .csv, one .json and one .py file.")
            files[ext] = p
    errors, warnings = [], []

    missing = [k for k in ("csv", "json", "py") if k not in files or not os.path.exists(files[k])]
    if missing:
        for k in missing:
            errors.append(f"missing .{k} file (every contribution needs CSV + JSON + Python)")
        return report(errors, warnings)

    snaps = {}
    with tempfile.TemporaryDirectory() as tmp:
        for kind in ("csv", "json", "py"):
            db = new_db(tmp, kind)
            print(f"Loading {files[kind]} ...")
            try:
                if kind == "py":
                    load_py(db, files[kind])
                else:
                    if run_import(db, "flat" if kind == "csv" else "json", files[kind]) != 0:
                        errors.append(f".{kind} file has rows that failed to import (see messages above)")
            except Exception as e:
                errors.append(f".{kind} file could not be loaded: {e}")
            snaps[kind] = snapshot(db)

    if not errors:
        base_snap = snaps["csv"]
        for kind in ("json", "py"):
            for table, rows in base_snap.items():
                other = snaps[kind][table]
                for label, diff in ((f"in CSV but not in .{kind}", rows - other),
                                    (f"in .{kind} but not in CSV", other - rows)):
                    if diff:
                        errors.append(f"[{table}] {len(diff)} row(s) {label}, e.g. {sorted(diff)[0]}")

        hits = snaps["csv"]["chemical->protein"]
        if not hits:
            errors.append("no chemical->protein hits found: add at least one protein")
        by_chem = {}
        for chem, rank, uid, method, score, src in hits:
            by_chem.setdefault(chem, []).append((rank, uid, src, method))
            if "example" in src.lower():
                errors.append(f"{chem}/{uid}: example source_ref still present; replace with a real citation")
            elif not src:
                errors.append(f"{chem}/{uid}: source_ref is empty (every protein hit needs a source)")
            if not rank:
                errors.append(f"{chem}/{uid}: rank is missing")
            if not method:
                warnings.append(f"{chem}/{uid}: method is empty")
        for chem, rows in by_chem.items():
            if len(rows) != 10:
                warnings.append(f"{chem} has {len(rows)} protein(s); the project expects the top 10")
        structs = snaps["csv"]["structure"]
        for (uid,) in {(h[2],) for h in hits}:
            if not any(s[0] == uid and s[3] == "1" for s in structs):
                warnings.append(f"{uid}: no best structure marked")
        if not snaps["csv"]["GO"]:
            warnings.append("no GO terms found")
        if not (snaps["csv"]["protein disease"] or snaps["csv"]["chemical disease"]):
            warnings.append("no diseases found")

    code = report(errors, warnings)
    if code == 0 and a.do_import:
        print(f"\nImporting into {a.db} ...")
        return run_import(a.db, "json", files["json"])
    return code


def report(errors, warnings):
    print()
    for w in warnings:
        print("  warning:", w)
    for e in errors:
        print("  ERROR:  ", e)
    if errors:
        print(f"\nFAILED: {len(errors)} error(s). Fix them and run the check again.")
        return 1
    print("\nPASSED: the CSV, JSON and Python files agree and are valid." +
          (f" ({len(warnings)} warning(s) to look at)" if warnings else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
