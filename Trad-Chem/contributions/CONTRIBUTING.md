# Contributing to Trad-Chem-LLM

Thank you for adding data! This guide explains, step by step, how to add a formulation to the database.
You do not need to know SQL.

---

## How the data is organised

All data lives in `tradchem/data/`. Each level is a folder:

```
tradchem/data/
└── <system>/                     e.g. ayurvedha
    └── formulations/
        └── <formulation>/        e.g. harithakyadiya-kashaya
            └── <sub-component>/  a plant or other ingredient, e.g. curcuma-longa
                └── <chemical>/   e.g. curcumin
                    ├── __init__.py
                    ├── curcumin.csv
                    ├── curcumin.json
                    └── curcumin.py
```

**One chemical = one folder = three files (`.csv`, `.json`, `.py`) with the same content.**

A complete worked example is in
[tradchem/data/ayurvedha/formulations/example-formulation-1/example-sub-component-1/curcumin/](../tradchem/data/ayurvedha/formulations/example-formulation-1/example-sub-component-1/curcumin/).

**Naming rules**
- Use lower-case and join words with `-` (for example `gallic-acid`, `curcuma-longa`).
- The three files must have the same name as their folder (`gallic-acid/gallic-acid.csv`).
- Every new folder needs an empty `__init__.py`.

---

## Where the data can come from

You can fill the data files using either (or both) of these:

1. **Peer-reviewed literature** – published papers that report the chemical, its targets or its activity.
   Use `method = literature` and put the DOI or PMID in `source_ref`.
2. **Computational prediction tools** – tools that predict the protein targets of a chemical, for example:
   - [SwissTargetPrediction](http://www.swisstargetprediction.ch/)
   - NetInfer
   - TrackMyPDB

   Put the tool name in `method` (e.g. `SwissTargetPrediction`), the tool's score in `score`,
   and the tool name, version / URL and the date you ran it in `source_ref`.

If a target is supported by both a paper and a tool, prefer the paper as the `source_ref`.
Never guess values: if you cannot find something, leave it empty.

---

## Step 1 – Get the repository

```bash
git clone https://github.com/INSTITUTE-OF-SCIENTIFIC-INFORMATICS/Trad-Chem-LLM.git
cd Trad-Chem-LLM
git checkout -b <team-name>/<formulation>
```

Always work on your own branch, never on `main`.

## Step 2 – Choose a formulation (as a team)

- Agree on **one formulation** within your team and check that no other team has taken it.
- Create its folder: `tradchem/data/<system>/formulations/<formulation>/`

## Step 3 – List the sub-components

- List every plant (or other ingredient) in the formulation.
- Create one folder per sub-component inside the formulation folder.
- Record the plant's **scientific name**, type (herb / shrub / tree …), part used, family and common name.

## Step 4 – Find and categorise the chemicals

- For each sub-component, list the chemicals found in the **part used**
  (sources: [IMPPAT](https://cb.imsc.res.in/imppat/), [PubChem](https://pubchem.ncbi.nlm.nih.gov/), literature).
- Group them by class (alkaloids, flavonoids, terpenoids, phenolics, glycosides …).
- Get the **SMILES** and **PubChem CID** from PubChem.
- Create one folder per chemical inside the sub-component folder.

## Step 5 – Find the top 10 UniProt targets for each chemical

- Find the proteins each chemical acts on, using peer-reviewed literature or prediction tools
  (SwissTargetPrediction, NetInfer, TrackMyPDB, [ChEMBL](https://www.ebi.ac.uk/chembl/), [STITCH](http://stitch.embl.de/)).
  See [Where the data can come from](#where-the-data-can-come-from).
- Keep the **best 10**, ranked 1 (best) to 10.
- For each protein, look up on [UniProt](https://www.uniprot.org/): UniProt ID, name, acronym, species, cell types, GO terms, diseases.
- Write down how you found it (`method`, `score`) and the source (`source_ref`: DOI / PMID / database).

## Step 6 – Pick the best structure for each UniProt

- Choose **one** best structure per protein:
  1. an experimental structure from [RCSB PDB](https://www.rcsb.org/) with the best resolution that covers the binding site, or
  2. if there is none, the [AlphaFold](https://alphafold.ebi.ac.uk/) model.
- Write it as `PDB:5IKR` or `AlphaFold:AF-P35354-F1`. Other structures go in `other_structures`.

## Step 7 – Fill the three files

Copy the three example files from the `curcumin` folder into your chemical folder and rename them.

| File | How to fill it |
|---|---|
| `<chemical>.csv` | One row per protein (up to 10). Repeat the medicine / plant / chemical columns on every row. Separate multiple values with `;`. Save as CSV UTF-8. |
| `<chemical>.json` | Chemical details once at the top; proteins inside `targets`, best first. Lists use `["a", "b"]`. |
| `<chemical>.py` | Edit the `CHEMICAL = {...}` block and one `slot(...)` per protein in `TARGETS`, best first. |

Tip: fill the CSV first (in a spreadsheet), then copy the same values into the JSON and Python files.
**Delete all example values** (PTGS2, ESR1, "EXAMPLE ONLY").

## Step 8 – Check your files

From the repository root:

```bash
python3 contributions/check_submission.py tradchem/data/<system>/formulations/<formulation>/<sub-component>/<chemical>/<chemical>
```

Fix every `ERROR` and run again until you see **PASSED**.

## Step 9 – Sign and submit

1. Add your row to [CONTRIBUTORS.md](../CONTRIBUTORS.md).
2. Commit and push your branch:
   ```bash
   git add tradchem/data/<system>/formulations/<formulation> CONTRIBUTORS.md
   git commit -m "Add <formulation> data"
   git push origin <team-name>/<formulation>
   ```
3. Open a **Pull Request** to `main` on GitHub.

Do **not** commit `tradmed.db` or `.DS_Store` files.

---

## Field reference

**Chemical level** (once per chemical)

| Field | Required | Example |
|---|---|---|
| `chemical_name` | **yes** | `curcumin` |
| `smiles` | **yes** | `COC1=C(C=CC(=C1)...)O` |
| `pubchem_cid` | no | `969516` |
| `medicine` | recommended | `Harithakyadiya Kashaya` |
| `system` | recommended | `Ayurveda` / `Siddha` / `Unani` / `TCM` / `Other` |
| `plant` | recommended | `Curcuma longa` (scientific name) |
| `plant_type` | recommended | `herb` |
| `part_used`, `family`, `common_name` | no | `rhizome`, `Zingiberaceae`, `Turmeric` |
| `diseases` | no | `colorectal cancer; arthritis` (linked to the chemical) |

**Protein level** (once per target, up to 10)

| Field | Required | Example |
|---|---|---|
| `rank` | CSV only | `1` to `10` (JSON / Python use list order) |
| `uniprot_id` | **yes** | `P35354` |
| `protein_name`, `protein_acronym` | recommended | `Prostaglandin G/H synthase 2`, `PTGS2` |
| `species`, `taxon_id` | recommended | `Homo sapiens`, `9606` |
| `cell_types` | recommended | `macrophage; epithelial cell` |
| `best_structure` | **yes** | `PDB:5IKR` |
| `other_structures` | no | `AlphaFold:AF-P35354-F1` |
| `go_terms` | recommended | `GO:0006954 inflammatory response` |
| `protein_diseases` | recommended | `inflammation` |
| `method` | **yes** | `literature` / `SwissTargetPrediction` / `NetInfer` / `TrackMyPDB` / `docking` / `assay` |
| `score` | no | `-8.1` |
| `source_ref` | **yes** | `doi:10.xxxx/xxxxx` |

---

## Checklist

- [ ] Working on my own branch
- [ ] Folders follow `system / formulations / formulation / sub-component / chemical`
- [ ] Each chemical folder has `.csv`, `.json`, `.py` (same name) and `__init__.py`
- [ ] No example values left
- [ ] Each protein has a UniProt ID, one best structure and a real `source_ref`
- [ ] `check_submission.py` says **PASSED**
- [ ] My row is added to `CONTRIBUTORS.md`

---

## Common checker messages

| Message | Fix |
|---|---|
| `missing .json file` | Add the missing file; all three are required |
| `row(s) in CSV but not in .json` | Make the three files identical |
| `example source_ref still present` | Replace with a real citation |
| `source_ref is empty` | Add a DOI / PMID / database source |
| `has 11 targets; the limit is 10` | Keep only the top 10 |
| `rank N … already used` | Two proteins share a rank |
| `unknown structure source` | Use `PDB:`, `AlphaFold:` or `SWISS-MODEL:` |
| `species '…' needs taxon_id` | Add the taxon ID (e.g. `9606`) |
| `GO term must start with GO:#######` | Use `GO:` + 7 digits, then the name |
