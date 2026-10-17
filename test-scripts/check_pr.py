#!/usr/bin/env python3
"""
Pull-request quality check for Trad-Chem-LLM (standard library only; submitted code is never run).

Run it yourself from the repository root before opening a pull request:
    python3 test-scripts/check_pr.py

GitHub Actions runs it on every pull request and replies on the PR if something needs fixing:
    python3 test-scripts/check_pr.py --root pr --changed-files changed.txt --report report.md
"""
import argparse
import re
import sys
from pathlib import Path, PurePosixPath

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_checks import check_chemical_folder, code  # noqa: E402

DATA = PurePosixPath("tradchem/data")
CHEMICAL_DEPTH = 5  # <system>/formulations/<formulation>/<sub-component>/<chemical>
LAYOUT = "`tradchem/data/<system>/formulations/<formulation>/<sub-component>/<chemical>/`"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MARKER = "<!-- tradchem-pr-check -->"
DEFAULT_GUIDE = "contributions/CONTRIBUTING.md"


def where(location):
    return code(location, limit=300)


def check_structure(root, changed):
    """Check folder layout and naming for the changed files.

    Returns (errors by folder, warnings, notes, chemical folders to check).
    """
    errors, warnings, notes, chemical_folders = {}, [], [], set()

    def error(location, message):
        errors.setdefault(location, [])
        if message not in errors[location]:
            errors[location].append(message)

    for name in changed:
        path = PurePosixPath(name)
        if path.name == ".DS_Store" or path.suffix in (".db", ".sqlite", ".sqlite3"):
            warnings.append(f"{where(name)}: please remove this file from the pull request")
            continue
        if DATA not in path.parents:
            if name != "CONTRIBUTORS.md":
                notes.append(f"{where(name)} is outside `tradchem/data/`; a maintainer will review this change")
            continue

        dirs, filename = path.relative_to(DATA).parts[:-1], path.name
        location = str(DATA.joinpath(*dirs))
        if len(dirs) >= 2 and dirs[1] != "formulations":
            error(location, f"the folder after `{dirs[0]}` must be `formulations` (found {code(dirs[1])})")
        for i, folder in enumerate(dirs):
            if i != 1 and not NAME_RE.match(folder):
                error(location, f"folder name {code(folder)} must be lower-case words joined by `-` (e.g. `gallic-acid`)")
        if len(dirs) > CHEMICAL_DEPTH:
            error(location, f"folders are nested too deeply; use {LAYOUT}")
        elif len(dirs) == CHEMICAL_DEPTH:
            chemical = dirs[-1]
            chemical_folders.add(location)
            allowed = {"__init__.py"} | {f"{chemical}.{ext}" for ext in ("csv", "json", "py")}
            if filename not in allowed:
                error(location, f"unexpected file {code(filename)}; a chemical folder holds only `__init__.py`, "
                                f"`{chemical}.csv`, `{chemical}.json` and `{chemical}.py`")
        elif filename != "__init__.py":
            error(location, f"{code(filename)} is in the wrong place; data files go in {LAYOUT}")

        for depth in range(1, min(len(dirs), CHEMICAL_DEPTH) + 1):
            folder = DATA.joinpath(*dirs[:depth])
            if not (root / folder / "__init__.py").is_file():
                error(str(folder), "missing empty `__init__.py` file in this folder")
    return errors, warnings, notes, chemical_folders


def build_report(errors, warnings, notes, checked, author, guide_url):
    count = sum(len(v) for v in errors.values())
    hello = f"Hi @{author}" if author else "Hi"
    lines = [MARKER]
    if count:
        lines += [f"## TradChem PR check: {count} problem(s) to fix", "",
                  f"{hello}, thanks for your contribution! The automatic check found some problems. "
                  "Please fix them and push to the same branch; the check will run again automatically.", ""]
        for location, messages in sorted(errors.items()):
            lines.append(f"**{where(location)}**")
            lines += [f"- [ ] {m}" for m in messages]
            lines.append("")
    else:
        lines += ["## TradChem PR check: passed", "",
                  f"{hello}, all automatic checks passed. A maintainer will review your pull request.", ""]
    if checked:
        lines += ["Checked chemical folders: " + ", ".join(where(c) for c in checked), ""]
    if warnings:
        lines += ["### Warnings (these do not block the pull request)"] + [f"- {w}" for w in warnings] + [""]
    if notes:
        lines += ["### Notes"] + [f"- {n}" for n in notes] + [""]
    lines.append(f"See the [contribution guide]({guide_url}) for the folder layout and field formats. "
                 "You can run this check yourself with `python3 test-scripts/check_pr.py`.")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1],
                    help="repository folder to check (default: this repository)")
    ap.add_argument("--changed-files", type=Path,
                    help="text file with one changed path per line (default: every file under tradchem/data)")
    ap.add_argument("--report", type=Path, help="write the Markdown report to this file")
    ap.add_argument("--author", default="", help="GitHub user name to greet in the report")
    ap.add_argument("--guide-url", default=DEFAULT_GUIDE)
    args = ap.parse_args()

    root = args.root.resolve()
    if args.changed_files:
        changed = [line.strip() for line in args.changed_files.read_text().splitlines() if line.strip()]
    else:
        changed = sorted(p.relative_to(root).as_posix() for p in (root / DATA).rglob("*")
                         if p.is_file() and not p.name.startswith("."))

    errors, warnings, notes, chemical_folders = check_structure(root, changed)
    checked = []
    for location in sorted(chemical_folders):
        folder = root / location
        if folder.is_symlink() or not folder.resolve().is_relative_to(root):
            errors.setdefault(location, []).append("this folder must be a normal folder, not a link")
            continue
        if not folder.is_dir():
            continue
        if any(part.startswith("example-") for part in PurePosixPath(location).parts):
            notes.append(f"{where(location)} is an example folder; its data was not checked")
            continue
        folder_errors, folder_warnings = check_chemical_folder(folder)
        for message in folder_errors:
            if message not in errors.setdefault(location, []):
                errors[location].append(message)
        warnings += [f"{where(location)}: {w}" for w in folder_warnings]
        checked.append(location)

    if args.changed_files and checked and "CONTRIBUTORS.md" not in changed:
        warnings.append("remember to add your row to `CONTRIBUTORS.md`")

    report = build_report(errors, warnings, notes, checked, args.author, args.guide_url)
    print(report)
    if args.report:
        args.report.write_text(report, encoding="utf-8")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
