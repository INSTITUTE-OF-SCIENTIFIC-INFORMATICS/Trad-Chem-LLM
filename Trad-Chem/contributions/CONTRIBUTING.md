# Contributing to Trad-Chem-LLM

Thank you for adding data. This guide takes you from an empty template to a checked submission.
You do not need to know SQL.

## The rule: every contribution uses all three file types

For **each chemical** you contribute, submit **three files with the same base name and the same content**:

```
contributions/curcumin_top10.csv
contributions/curcumin_top10.json
contributions/curcumin_top10.py
```

- File names: lower-case, underscores, `<chemical>_top10.<ext>` (example: `gallic_acid_top10.csv`).
- One chemical per submission, with **up to 10 target proteins** (aim for exactly 10).
- A submission with only one or two of the three files will be rejected by the checker.
- After checking, **sign your name in [CONTRIBUTORS.md](CONTRIBUTORS.md)**.

---

## Step by step

### 1. Prepare
Put these in one folder: `import_data.py`, `check_submission.py`, `schema.sql`, `tradmed.db`,
`top10_template.csv`, `top10_template.json`, `add_top10.py`. You need Python 3.8+ and nothing else.

### 2. Collect your data first
For your chemical, gather in a notebook or spreadsheet:
- medicine, plant (scientific name), chemical name and SMILES
- the top 10 proteins, ranked, with UniProt ID, acronym, species, cell types
- for each protein: best structure, GO terms, diseases, method, score, source

Filling the CSV (a spreadsheet) first is the quickest; then copy the same values into the JSON and Python files.

### 3. Fill the CSV
```bash
cp top10_template.csv contributions/<chemical>_top10.csv
```
- Keep the header row. **One row per protein**, up to 10 rows.
- **Repeat the medicine, plant and chemical columns on every row.**
- Put the protein's rank (1 to 10) in `rank`. Separate multiple values in one cell with `;`.
- Save as **CSV UTF-8**.
- Delete the example rows.

### 4. Fill the JSON
```bash
cp top10_template.json contributions/<chemical>_top10.json
```
- Chemical details **once** at the top; protein details inside `targets`.
- **The order of `targets` is the rank.** Put the best hit first.
- Multi-value fields (`cell_types`, `go_terms`, `protein_diseases`, `other_structures`, `diseases`) are lists: `["a", "b"]`.
- Remove the example proteins; delete or leave empty any unused slots.

### 5. Fill the Python file
```bash
cp add_top10.py contributions/<chemical>_top10.py
```
- Edit the `CHEMICAL = {...}` block.
- Fill one `slot(...)` per protein inside `TARGETS`, best hit first (order = rank).
- Unused slots can stay as `slot()`.
- You do not need to run it yourself; the checker loads it for you.

### 6. Check your three files
```bash
python3 check_submission.py contributions/<chemical>_top10
```

Fix every `ERROR` and re-run until you see **PASSED**. Read the `warning` lines too.
The checker never touches the real database.

### 7. Submit
Send or open a pull request with **only your three files in `contributions/`** and your row in `CONTRIBUTORS.md`:
**[add pull-request or email instructions here]**.

Please do **not** submit your own copy of `tradmed.db`; the maintainer imports accepted files.

---

## Field reference

Chemical-level fields are written once in JSON/Python and repeated on every CSV row.

### Chemical level

| Field | Required | Example | Notes |
|---|---|---|---|
| `chemical_name` | **yes** | `curcumin` | One spelling per compound |
| `smiles` | **yes** | `COC1=C(C=CC(=C1)...)O` | Copy from PubChem / ChEMBL |
| `pubchem_cid` | no | `969516` | |
| `medicine` | recommended | `Triphala` | Traditional medicine name |
| `system` | recommended | `Ayurveda` | Ayurveda / Siddha / Unani / TCM / Other |
| `plant` | recommended | `Curcuma longa` | **Scientific name** |
| `plant_type` | recommended | `herb` | herb / shrub / tree / climber / fungus … |
| `part_used` | no | `rhizome` | leaf / root / bark … |
| `family`, `common_name` | no | `Zingiberaceae`, `Turmeric` | |
| `diseases` | no | `colorectal cancer; arthritis` | Diseases linked to the **chemical** |

### Protein level (one CSV row, JSON object or `slot` per protein)

| Field | Required | Example | Notes |
|---|---|---|---|
| `rank` | CSV: yes | `1` | 1–10, unique per chemical. JSON/Python use list order |
| `uniprot_id` | **yes** | `P35354` | UniProtKB accession |
| `protein_name` | recommended | `Prostaglandin G/H synthase 2` | |
| `protein_acronym` | recommended | `PTGS2` | |
| `species` | recommended | `Homo sapiens` | |
| `taxon_id` | first use of a species | `9606` | NCBI Taxonomy ID |
| `cell_types` | recommended | `macrophage; epithelial cell` | |
| `best_structure` | **yes** | `PDB:5IKR` | Exactly one per protein |
| `other_structures` | no | `AlphaFold:AF-P35354-F1` | |
| `go_terms` | recommended | `GO:0006954 inflammatory response` | ID, then name |
| `protein_diseases` | recommended | `inflammation` | Diseases tied to **this protein** |
| `method` | **yes** | `docking` | docking / assay / SwissTargetPrediction / literature |
| `score` | no | `-8.1` | A number |
| `source_ref` | **yes** | `doi:10.xxxx/xxxxx` | DOI, PMID, or database + date |

**Structure format:** `DB:ID` where DB is exactly `PDB`, `AlphaFold` or `SWISS-MODEL`
(`PDB:5IKR`, `AlphaFold:AF-P35354-F1`, `SWISS-MODEL:<id>`).
Pick the best structure as: experimental PDB with the best resolution that covers the binding region;
otherwise AlphaFold or SWISS-MODEL.

---

## Quality checklist (tick before submitting)

- [ ] Three files exist: `.csv`, `.json`, `.py`, same base name
- [ ] `check_submission.py` says **PASSED**
- [ ] No example rows left (PTGS2 / ESR1 / "EXAMPLE ONLY")
- [ ] Every protein has a real `source_ref`
- [ ] SMILES copied from a trusted database
- [ ] UniProt, PDB, GO IDs verified on the live databases
- [ ] Ranked 1–10, and the ranking method is in `method` / `score`
- [ ] One `best_structure` per protein in `DB:ID` format
- [ ] Plant names are scientific names
- [ ] Disease, cell-type and chemical spellings match existing entries where possible
- [ ] Your name and row added to `CONTRIBUTORS.md`

---

## What the checker tells you

| Message | Meaning / fix |
|---|---|
| `missing .json file …` | Add the missing file type. All three are required |
| `N row(s) in CSV but not in .json` | The files disagree; make them identical |
| `example source_ref still present` | Replace the sample citation with a real one |
| `source_ref is empty` | Add a DOI/PMID/database source |
| `chemical_name and smiles are required` | Fill both |
| `already stored with a different SMILES` | Same name, different structure; verify |
| `has 11 targets; the limit is 10` | Keep the top 10 only |
| `rank N … already used by …` | Two proteins share a rank |
| `unknown structure source` | Use `PDB`, `AlphaFold` or `SWISS-MODEL` |
| `species '…' needs taxon_id` | Add the taxon ID, e.g. 9606 |
| `GO term '…' must start with GO:#######` | `GO:` + 7 digits, then the name |
| warning: `has 2 protein(s); the project expects the top 10` | Add the remaining proteins |
| warning: `no best structure marked` | Fill `best_structure` |

---

## For maintainers

1. Read the submitted `.py` before running anything: the checker executes it to read its data.
2. Run `python3 check_submission.py contributions/<name>`.
3. Spot-check a few IDs and sources against UniProt, RCSB PDB / AlphaFold DB, and the cited paper.
4. Import: `python3 check_submission.py contributions/<name> --import` (only works if the check passes).
5. Confirm the contributor's row in `CONTRIBUTORS.md` and fill the **Reviewed by** column.

---

## Starting over (local copy only)

```bash
rm tradmed.db
python3 -c "import sqlite3; sqlite3.connect('tradmed.db').executescript(open('schema.sql').read())"
```
