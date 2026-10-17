# Trad-Chem-LLM

**Trad-Chem-LLM** is a community-built database that connects **traditional medicine** to molecular
science: each traditional medicine is linked to its **plants**, the **chemicals** in those plants
(with SMILES), the **top 10 target proteins** of each chemical, and the biology around those proteins.

> **Want to add data? Read [CONTRIBUTING.md](CONTRIBUTING.md), then sign the table in
> [CONTRIBUTORS.md](CONTRIBUTORS.md).**
> Every contribution must be submitted as **three files: CSV + JSON + Python**.

---

## What the database holds

```
Traditional medicine → Plant (type) → Chemical (name + SMILES)
                                          │
                                          └─ Top 10 proteins (UniProt IDs, ranked, method, score)
                                                 ├─ best structure (PDB / AlphaFold / SWISS-MODEL id)
                                                 ├─ protein acronym
                                                 ├─ cell types
                                                 ├─ species
                                                 ├─ GO terms
                                                 └─ diseases (per protein, and per chemical)
```

| Data | Stored as |
|---|---|
| Traditional medicine, system (Ayurveda, Siddha, Unani, TCM …) | `traditional_medicine` |
| Plant scientific name, plant type, part used | `plant` |
| Chemical name, SMILES, PubChem CID | `chemical` |
| UniProt IDs each chemical hits (rank 1–10, method, score, source) | `chemical_protein` |
| Best PDB / AlphaFold / SWISS-MODEL id for each UniProt | `structure` |
| Protein acronym, species (NCBI taxon) | `protein`, `species` |
| Cell types | `cell_type`, `protein_cell_type` |
| GO terms | `go_term`, `protein_go` |
| Diseases | `disease`, `protein_disease`, `chemical_disease` |

The database is SQLite (`tradmed.db`). `v_full_record` is a ready-made view that flattens everything.

---

## Repository contents

| Path | What it is |
|---|---|
| `README.md` | This file |
| `CONTRIBUTING.md` | Step-by-step contribution rules (**read first**) |
| `CONTRIBUTORS.md` | Table where every contributor signs their name next to their contribution |
| `contributions/` | Submitted data: `<chemical>_top10.csv`, `.json`, `.py` |
| `top10_template.csv` / `.json` / `add_top10.py` | The three templates to copy and fill |
| `check_submission.py` | Checks that your CSV, JSON and Python files are valid and identical |
| `import_data.py` | Importer used by everything above |
| `schema.sql` | Table definitions |
| `tradmed.db` | The master database |
| `templates/` | One empty CSV per table (advanced use) |

---

## Quick start

```bash
# 1. get the files into one folder, then check Python is installed
python3 --version

# 2. copy the three templates, fill them in (see CONTRIBUTING.md)
cp top10_template.csv  contributions/curcumin_top10.csv
cp top10_template.json contributions/curcumin_top10.json
cp add_top10.py        contributions/curcumin_top10.py

# 3. check your three files agree
python3 check_submission.py contributions/curcumin_top10
```

No extra Python packages are needed.

---

## The one rule

**One chemical = one submission = three files with the same content**:

| File | Format |
|---|---|
| `<chemical>_top10.csv` | spreadsheet, one row per protein |
| `<chemical>_top10.json` | JSON, chemical once + a list of up to 10 proteins |
| `<chemical>_top10.py` | Python, `CHEMICAL` + 10 `slot(...)` entries |

`check_submission.py` loads all three into separate throw-away databases and fails if they differ,
if any file is missing, or if example data or sources are left in.

---

## Data standards

- Every protein hit has a **source** (DOI, PMID, or database + date).
- IDs (UniProt, PDB, GO, taxon) are copied from the live databases, never guessed.
- "Top 10" is a **ranked** list; state how it was ranked (`method`, `score`).
- Exactly one **best structure** per protein.

Details and the full field reference are in [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Maintainers

- Contact / issues: **[add maintainer name and contact]**
- Licence: **[add licence for the data and code]**
- How to cite: **[add citation text]**
