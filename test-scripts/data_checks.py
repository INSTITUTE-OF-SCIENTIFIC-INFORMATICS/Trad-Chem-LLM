"""
Read and validate one chemical folder (<chemical>.csv, .json, .py).

Submitted files are only parsed (csv / json / ast), never executed.
"""
import ast
import csv
import json
import re
from pathlib import Path

CHEM_FIELDS = ("medicine", "system", "plant", "plant_type", "part_used", "family", "common_name",
               "chemical_name", "smiles", "pubchem_cid", "diseases")
TARGET_FIELDS = ("uniprot_id", "protein_name", "protein_acronym", "species", "taxon_id", "cell_types",
                 "best_structure", "other_structures", "go_terms", "protein_diseases", "method", "score",
                 "source_ref")
LIST_FIELDS = {"diseases", "cell_types", "other_structures", "go_terms", "protein_diseases"}
SYSTEMS = {"Ayurveda", "Siddha", "Unani", "TCM", "Other"}
METHODS = {"literature", "docking", "assay", "SwissTargetPrediction", "NetInfer", "TrackMyPDB"}
MAX_TARGETS = 10

UNIPROT_RE = re.compile(r"^([OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2})$")
STRUCTURE_RE = re.compile(r"^(PDB:[0-9][A-Za-z0-9]{3}|AlphaFold:AF-[A-Z0-9]+-F[0-9]+|SWISS-MODEL:\S+)$")
GO_RE = re.compile(r"^GO:[0-9]{7}(\s|$)")
SMILES_RE = re.compile(r"^[A-Za-z0-9@+\-\[\]()=#$:/\\.%*]+$")
PLANT_RE = re.compile(r"^[A-Z][a-z]+ [a-z]")


def code(value, limit=80):
    """Show a submitted value safely inside a Markdown comment."""
    text = "; ".join(value) if isinstance(value, tuple) else str(value)
    if not text:
        return "(empty)"
    text = text.replace("`", "'").replace("\n", " ")
    return f"`{text[:limit]}{'...' if len(text) > limit else ''}`"


def _norm(field, value):
    if field in LIST_FIELDS:
        if value is None:
            return ()
        items = value.split(";") if isinstance(value, str) else value
        if not isinstance(items, (list, tuple)):
            items = [items]
        return tuple(sorted({str(v).strip() for v in items if str(v).strip()}))
    if value is None:
        return ""
    text = str(value).strip()
    if field == "score" and text:
        try:
            return repr(float(text))
        except ValueError:
            return text
    return text


def _record(raw, fields):
    return {f: _norm(f, raw.get(f)) for f in fields}


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError("the file has no data rows")
    chemicals = {tuple(_record(r, CHEM_FIELDS).items()) for r in rows}
    if len(chemicals) > 1:
        raise ValueError("the medicine / plant / chemical columns must be identical on every row")
    ranked = []
    for line, row in enumerate(rows, 2):
        target = _record(row, TARGET_FIELDS)
        if not target["uniprot_id"]:
            continue
        rank = (row.get("rank") or "").strip()
        if not rank.isdigit() or not 1 <= int(rank) <= MAX_TARGETS:
            raise ValueError(f"line {line}: `rank` must be a whole number from 1 to {MAX_TARGETS} (found {code(rank)})")
        ranked.append((int(rank), target))
    ranks = [r for r, _ in ranked]
    if len(set(ranks)) != len(ranks):
        raise ValueError("two proteins share the same `rank`")
    return dict(chemicals.pop()), [t for _, t in sorted(ranked, key=lambda x: x[0])]


def read_json(path):
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict) or not isinstance(data.get("targets", []), list):
        raise ValueError("expected one object with the chemical fields and a `targets` list")
    if not all(isinstance(t, dict) for t in data.get("targets", [])):
        raise ValueError("every item in `targets` must be an object { ... }")
    targets = [_record(t, TARGET_FIELDS) for t in data.get("targets", [])]
    return _record(data, CHEM_FIELDS), [t for t in targets if t["uniprot_id"]]


def read_py(path):
    tree = ast.parse(Path(path).read_text(encoding="utf-8-sig"), filename=str(path))
    found = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            target = node.target
        else:
            continue
        if isinstance(target, ast.Name) and target.id in ("CHEMICAL", "TARGETS"):
            found[target.id] = node.value
    if set(found) != {"CHEMICAL", "TARGETS"}:
        raise ValueError("it must define `CHEMICAL = {...}` and `TARGETS = [...]` (copy the example curcumin.py)")
    try:
        chemical = ast.literal_eval(found["CHEMICAL"])
    except (ValueError, TypeError, SyntaxError):
        raise ValueError("`CHEMICAL` must contain plain values only (text, numbers, lists)") from None
    if not isinstance(chemical, dict):
        raise ValueError("`CHEMICAL` must be a dictionary { ... }")
    if not isinstance(found["TARGETS"], ast.List):
        raise ValueError("`TARGETS` must be a list of `slot(...)` entries")
    targets = []
    for i, item in enumerate(found["TARGETS"].elts, 1):
        if not (isinstance(item, ast.Call) and isinstance(item.func, ast.Name)
                and item.func.id == "slot" and not item.args):
            raise ValueError(f"`TARGETS` entry {i} must be written as `slot(name=value, ...)`")
        try:
            values = {kw.arg: ast.literal_eval(kw.value) for kw in item.keywords if kw.arg}
        except (ValueError, TypeError, SyntaxError):
            raise ValueError(f"`TARGETS` entry {i} must contain plain values only (text, numbers, lists)") from None
        if any(kw.arg is None for kw in item.keywords):
            raise ValueError(f"`TARGETS` entry {i} must be written as `slot(name=value, ...)`")
        targets.append(_record(values, TARGET_FIELDS))
    return _record(chemical, CHEM_FIELDS), [t for t in targets if t["uniprot_id"]]


def compare(label_a, a, label_b, b, errors, limit=5):
    (chem_a, targets_a), (chem_b, targets_b) = a, b
    diffs = [f"chemical `{f}` is {code(chem_a[f])} in {label_a} but {code(chem_b[f])} in {label_b}"
             for f in CHEM_FIELDS if chem_a[f] != chem_b[f]]
    ids_a = tuple(t["uniprot_id"] for t in targets_a)
    ids_b = tuple(t["uniprot_id"] for t in targets_b)
    if ids_a != ids_b:
        diffs.append(f"proteins in rank order are {code(ids_a)} in {label_a} but {code(ids_b)} in {label_b}")
    else:
        for rank, (ta, tb) in enumerate(zip(targets_a, targets_b), 1):
            diffs += [f"rank {rank} `{f}` is {code(ta[f])} in {label_a} but {code(tb[f])} in {label_b}"
                      for f in TARGET_FIELDS if ta[f] != tb[f]]
    errors += [f"the three files must hold the same data: {d}" for d in diffs[:limit]]
    if len(diffs) > limit:
        errors.append(f"...and {len(diffs) - limit} more difference(s) between {label_a} and {label_b}")


def validate(chemical, targets, errors, warnings):
    for field in ("chemical_name", "smiles"):
        if not chemical[field]:
            errors.append(f"`{field}` is required")
    if chemical["smiles"] and not SMILES_RE.match(chemical["smiles"]):
        errors.append(f"`smiles` {code(chemical['smiles'])} is not a valid SMILES string (copy it from PubChem)")
    if chemical["pubchem_cid"] and not chemical["pubchem_cid"].isdigit():
        errors.append(f"`pubchem_cid` must be a number (found {code(chemical['pubchem_cid'])})")
    if chemical["system"] and chemical["system"] not in SYSTEMS:
        warnings.append(f"`system` {code(chemical['system'])} is not one of {', '.join(sorted(SYSTEMS))}")
    if chemical["plant"] and not PLANT_RE.match(chemical["plant"]):
        warnings.append(f"`plant` {code(chemical['plant'])} should be a scientific name, e.g. `Curcuma longa`")
    for field in CHEM_FIELDS:
        if "example" in " ".join(chemical[field] if isinstance(chemical[field], tuple) else [chemical[field]]).lower():
            errors.append(f"`{field}` still has example text {code(chemical[field])}; replace it with real data")

    if not targets:
        errors.append("no target proteins found: add at least one protein with a `uniprot_id`")
    elif len(targets) > MAX_TARGETS:
        errors.append(f"{len(targets)} target proteins found; keep only the top {MAX_TARGETS}")
    elif len(targets) < MAX_TARGETS:
        warnings.append(f"{len(targets)} target protein(s) found; the project aims for the top {MAX_TARGETS}")

    seen = set()
    for rank, t in enumerate(targets, 1):
        uid = t["uniprot_id"]
        tag = f"rank {rank} ({code(uid)})"
        if not UNIPROT_RE.match(uid):
            errors.append(f"{tag}: `uniprot_id` is not a valid UniProt accession (e.g. `P35354`)")
        if uid in seen:
            errors.append(f"{tag}: this UniProt ID is listed more than once")
        seen.add(uid)
        if not t["best_structure"]:
            errors.append(f"{tag}: `best_structure` is required (e.g. `PDB:5IKR` or `AlphaFold:AF-P35354-F1`)")
        for s in ((t["best_structure"],) if t["best_structure"] else ()) + t["other_structures"]:
            if not STRUCTURE_RE.match(s):
                errors.append(f"{tag}: structure {code(s)} must look like `PDB:5IKR`, "
                              "`AlphaFold:AF-P35354-F1` or `SWISS-MODEL:<id>`")
        for go in t["go_terms"]:
            if not GO_RE.match(go):
                errors.append(f"{tag}: GO term {code(go)} must start with `GO:` and 7 digits, "
                              "e.g. `GO:0006954 inflammatory response`")
        if not t["method"]:
            errors.append(f"{tag}: `method` is required (e.g. `literature`, `SwissTargetPrediction`, `docking`)")
        elif t["method"] not in METHODS:
            warnings.append(f"{tag}: `method` {code(t['method'])} is not one of {', '.join(sorted(METHODS))}")
        if t["score"]:
            try:
                float(t["score"])
            except ValueError:
                errors.append(f"{tag}: `score` must be a number (found {code(t['score'])})")
        if not t["source_ref"]:
            errors.append(f"{tag}: `source_ref` is required (DOI, PMID, or tool name + date)")
        elif "example" in t["source_ref"].lower():
            errors.append(f"{tag}: `source_ref` still has the example text; add a real citation")
        if t["taxon_id"] and not t["taxon_id"].isdigit():
            errors.append(f"{tag}: `taxon_id` must be a number, e.g. `9606`")
        if t["species"] and not t["taxon_id"]:
            warnings.append(f"{tag}: add `taxon_id` for species {code(t['species'])} (e.g. `9606` for Homo sapiens)")


def check_chemical_folder(folder):
    """Return (errors, warnings) for one chemical folder."""
    folder = Path(folder)
    name = folder.name
    errors, warnings, loaded = [], [], {}
    for ext, reader in (("csv", read_csv), ("json", read_json), ("py", read_py)):
        path = folder / f"{name}.{ext}"
        if path.is_symlink():
            errors.append(f"`{name}.{ext}` must be a normal file, not a link")
        elif not path.is_file():
            errors.append(f"missing `{name}.{ext}` (every chemical needs a .csv, .json and .py file)")
        else:
            try:
                loaded[ext] = reader(path)
            except (ValueError, SyntaxError, UnicodeDecodeError, csv.Error) as e:
                errors.append(f"`{name}.{ext}` could not be read: {e}")
    if not (folder / "__init__.py").is_file():
        errors.append("missing empty `__init__.py` file in this folder")
    if "json" in loaded:
        for ext in ("csv", "py"):
            if ext in loaded:
                compare(".json", loaded["json"], f".{ext}", loaded[ext], errors)
    reference = loaded.get("json") or loaded.get("csv") or loaded.get("py")
    if reference:
        validate(*reference, errors, warnings)
    return errors, warnings
