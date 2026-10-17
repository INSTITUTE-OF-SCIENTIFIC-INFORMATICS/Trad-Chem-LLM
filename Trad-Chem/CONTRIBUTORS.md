# Trad-Chem-LLM Contributors

Everyone who adds data signs here. **Add one row per chemical you contribute**, in the same
pull request as your chemical folder (`<chemical>.csv`, `.json`, `.py`). Never delete or edit anyone else's row.

## How to sign

1. Copy the last empty row of the table.
2. Fill every column. Use your real name (or the name you want credited).
3. Tick **CSV / JSON / PY** only when that file is in your chemical folder
   (`tradchem/data/<system>/formulations/<formulation>/<sub-component>/<chemical>/`).
4. Leave **Reviewed by** blank; the maintainer fills it after checking.

| # | Contributor name | Team | GitHub / email (optional) | System | Formulation | Sub-component (plant) | Chemical | Proteins (n/10) | CSV | JSON | PY | Main source (DOI / PMID) | Date | Reviewed by |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| – | *Example: Your Name* | *Team A* | *@yourhandle* | *Ayurveda* | *example-formulation-1* | *Curcuma longa* | *curcumin* | *10/10* | ✅ | ✅ | ✅ | *doi:10.xxxx/xxxxx* | *YYYY-MM-DD* | |
| 1 | | | | | | | | /10 | ☐ | ☐ | ☐ | | | |
| 2 | | | | | | | | /10 | ☐ | ☐ | ☐ | | | |
| 3 | | | | | | | | /10 | ☐ | ☐ | ☐ | | | |
| 4 | | | | | | | | /10 | ☐ | ☐ | ☐ | | | |
| 5 | | | | | | | | /10 | ☐ | ☐ | ☐ | | | |
| 6 | | | | | | | | /10 | ☐ | ☐ | ☐ | | | |
| 7 | | | | | | | | /10 | ☐ | ☐ | ☐ | | | |
| 8 | | | | | | | | /10 | ☐ | ☐ | ☐ | | | |
| 9 | | | | | | | | /10 | ☐ | ☐ | ☐ | | | |
| 10 | | | | | | | | /10 | ☐ | ☐ | ☐ | | | |

## Contribution declaration

By adding your name above you confirm that:

- the data in your three files is your own work or properly cited from the stated sources,
- `python3 contributions/check_submission.py <path-to-chemical-folder>/<chemical>` reported **PASSED**,
- you have removed all example rows from the templates,
- you are happy for the data to be released under the project licence: **[add licence]**.
