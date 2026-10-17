"""Self-tests for the PR checker:  python3 -m unittest discover -s test-scripts -v"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from check_pr import MARKER, check_structure  # noqa: E402
from data_checks import CHEM_FIELDS, LIST_FIELDS, TARGET_FIELDS, check_chemical_folder  # noqa: E402

CHECK_PR = HERE / "check_pr.py"

EXAMPLE = (HERE.parent / "tradchem/data/ayurvedha/formulations/example-formulation-1"
           / "example-sub-component-1/curcumin")
CHEMICAL_PATH = "tradchem/data/ayurvedha/formulations/triphala/terminalia-chebula/gallic-acid"

CHEMICAL = {"medicine": "Triphala", "system": "Ayurveda", "plant": "Terminalia chebula", "plant_type": "tree",
            "part_used": "fruit", "family": "Combretaceae", "common_name": "Haritaki",
            "chemical_name": "gallic acid", "smiles": "C1=C(C=C(C(=C1O)O)O)C(=O)O", "pubchem_cid": "370",
            "diseases": ["inflammation"]}
TARGET = {"uniprot_id": "P35354", "protein_name": "Prostaglandin G/H synthase 2", "protein_acronym": "PTGS2",
          "species": "Homo sapiens", "taxon_id": 9606, "cell_types": ["macrophage"],
          "best_structure": "PDB:5IKR", "other_structures": ["AlphaFold:AF-P35354-F1"],
          "go_terms": ["GO:0006954 inflammatory response"], "protein_diseases": ["inflammation"],
          "method": "literature", "score": "", "source_ref": "doi:10.1000/test"}


def cell(field, value):
    return "; ".join(value) if field in LIST_FIELDS else str(value)


def write_submission(root, chemical=CHEMICAL, targets=(TARGET,)):
    folder = Path(root) / CHEMICAL_PATH
    folder.mkdir(parents=True)
    data = Path(root) / "tradchem/data"
    for path in [folder, *folder.parents]:
        (path / "__init__.py").touch()
        if path == data:
            break
    name = folder.name

    header = list(CHEM_FIELDS) + ["rank"] + list(TARGET_FIELDS)
    rows = [",".join(f'"{cell(f, chemical[f])}"' for f in CHEM_FIELDS) + f",{rank},"
            + ",".join(f'"{cell(f, t[f])}"' for f in TARGET_FIELDS) for rank, t in enumerate(targets, 1)]
    (folder / f"{name}.csv").write_text("\n".join([",".join(header)] + rows) + "\n")
    (folder / f"{name}.json").write_text(json.dumps(dict(chemical, targets=list(targets)), indent=2))
    slots = "".join("    slot(" + ", ".join(f"{k}={v!r}" for k, v in t.items()) + "),\n" for t in targets)
    (folder / f"{name}.py").write_text(f"CHEMICAL = {chemical!r}\n\ndef slot(**kw):\n    return kw\n\n"
                                       f"TARGETS = [\n{slots}]\n")
    return folder


def changed_files(folder, root):
    return sorted({p.relative_to(root).as_posix() for p in Path(root, "tradchem").rglob("*") if p.is_file()})


def run_check_pr(root, changed, author="octocat"):
    (Path(root) / "changed.txt").write_text("\n".join(changed) + "\n")
    report = Path(root) / "report.md"
    result = subprocess.run([sys.executable, str(CHECK_PR), "--root", str(root), "--changed-files",
                             str(Path(root) / "changed.txt"), "--report", str(report), "--author", author],
                            capture_output=True, text=True)
    return result.returncode, report.read_text()


class SubmissionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_valid_submission_passes(self):
        folder = write_submission(self.root)
        errors, _ = check_chemical_folder(folder)
        self.assertEqual(errors, [])
        structure_errors, _, _, chemical_folders = check_structure(self.root, changed_files(folder, self.root))
        self.assertEqual(structure_errors, {})
        self.assertEqual(chemical_folders, {CHEMICAL_PATH})

    def test_files_must_agree(self):
        folder = write_submission(self.root)
        data = json.loads((folder / "gallic-acid.json").read_text())
        data["targets"][0]["best_structure"] = "PDB:1ABC"
        (folder / "gallic-acid.json").write_text(json.dumps(data))
        errors, _ = check_chemical_folder(folder)
        self.assertTrue(any("same data" in e and "best_structure" in e for e in errors), errors)

    def test_bad_ids_are_reported(self):
        bad = dict(TARGET, uniprot_id="XYZ", best_structure="5IKR", go_terms=["GO:123"], source_ref="")
        errors, _ = check_chemical_folder(write_submission(self.root, targets=(bad,)))
        for text in ("UniProt", "PDB:5IKR", "GO:", "source_ref"):
            self.assertTrue(any(text in e for e in errors), f"{text} not in {errors}")

    def test_too_many_targets(self):
        targets = [dict(TARGET, uniprot_id=f"P{n:05d}") for n in range(11)]
        errors, _ = check_chemical_folder(write_submission(self.root, targets=targets))
        self.assertTrue(any("keep only the top 10" in e for e in errors), errors)

    def test_duplicate_csv_rank(self):
        folder = write_submission(self.root, targets=(TARGET, dict(TARGET, uniprot_id="P03372")))
        csv_path = folder / "gallic-acid.csv"
        csv_path.write_text(csv_path.read_text().replace('",2,"', '",1,"'))
        errors, _ = check_chemical_folder(folder)
        self.assertTrue(any("same `rank`" in e for e in errors), errors)

    def test_bom_json_and_annotated_python_are_accepted(self):
        folder = write_submission(self.root)
        json_path, py_path = folder / "gallic-acid.json", folder / "gallic-acid.py"
        json_path.write_text(json_path.read_text(), encoding="utf-8-sig")
        py_path.write_text(py_path.read_text().replace("CHEMICAL = ", "CHEMICAL: dict = "))
        errors, _ = check_chemical_folder(folder)
        self.assertEqual(errors, [])

    def test_missing_file(self):
        folder = write_submission(self.root)
        (folder / "gallic-acid.py").unlink()
        errors, _ = check_chemical_folder(folder)
        self.assertTrue(any("missing `gallic-acid.py`" in e for e in errors), errors)

    def test_python_file_is_never_executed(self):
        folder = write_submission(self.root)
        marker = self.root / "executed"
        (folder / "gallic-acid.py").write_text(
            f"import pathlib\nCHEMICAL = pathlib.Path({str(marker)!r}).touch()\nTARGETS = []\n")
        errors, _ = check_chemical_folder(folder)
        self.assertFalse(marker.exists())
        self.assertTrue(any("plain values" in e for e in errors), errors)

    def test_wrong_layout(self):
        errors, _, _, _ = check_structure(self.root, ["tradchem/data/ayurvedha/Triphala/gallic.csv"])
        messages = [m for msgs in errors.values() for m in msgs]
        self.assertTrue(any("formulations" in m for m in messages), messages)
        self.assertTrue(any("wrong place" in m for m in messages), messages)

    def test_missing_init_and_unexpected_file(self):
        folder = write_submission(self.root)
        (folder.parent / "__init__.py").unlink()
        (folder / "notes.txt").write_text("x")
        errors, _, _, _ = check_structure(self.root, changed_files(folder, self.root))
        messages = [m for msgs in errors.values() for m in msgs]
        self.assertTrue(any("__init__.py" in m for m in messages), messages)
        self.assertTrue(any("unexpected file" in m for m in messages), messages)

    def test_cli_good_pull_request_passes(self):
        folder = write_submission(self.root)
        code, report = run_check_pr(self.root, changed_files(folder, self.root) + ["CONTRIBUTORS.md"])
        self.assertEqual(code, 0, report)
        self.assertIn("passed", report)
        self.assertIn(CHEMICAL_PATH, report)
        self.assertNotIn("CONTRIBUTORS.md", report)

    def test_cli_bad_pull_request_replies_to_author(self):
        bad = dict(TARGET, uniprot_id="XYZ")
        folder = write_submission(self.root, targets=(bad,))
        code, report = run_check_pr(self.root, changed_files(folder, self.root) + ["README.md"])
        self.assertEqual(code, 1)
        self.assertTrue(report.startswith(MARKER))
        self.assertIn("@octocat", report)
        self.assertIn(f"**`{CHEMICAL_PATH}`**", report)
        self.assertIn("UniProt", report)
        self.assertIn("CONTRIBUTORS.md", report)
        self.assertIn("outside `tradchem/data/`", report)

    def test_cli_skips_example_folders(self):
        folder = self.root / "tradchem/data/ayurvedha/formulations/example-x/example-y/chem"
        folder.mkdir(parents=True)
        for path in [folder, *folder.parents][:6]:
            (path / "__init__.py").touch()
        code, report = run_check_pr(self.root, changed_files(folder, self.root))
        self.assertEqual(code, 0, report)
        self.assertIn("example folder", report)

    def test_repo_example_only_fails_on_placeholders(self):
        errors, _ = check_chemical_folder(EXAMPLE)
        self.assertTrue(errors)
        self.assertTrue(all("example" in e.lower() for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
