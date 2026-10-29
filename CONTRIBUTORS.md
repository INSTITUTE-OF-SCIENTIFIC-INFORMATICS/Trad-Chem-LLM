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
| 1 | Janith Madhusanka | Not specified | @janithmadhu277-cmyk | Ayurveda | pathpadagam | Mollugo cerviana | 2-5-di-tert-butylhydroquinone | 1/10 | ✅ | ✅ | ✅ | doi:10.1073/pnas.0506222102 | 2026-10-29 |  |
| 2 | Janith Madhusanka | Not specified | @janithmadhu277-cmyk | Ayurveda | pathpadagam | Mollugo cerviana | 4-vinylguaiacol | 2/10 | ✅ | ✅ | ✅ | doi:10.1007/s10529-017-2475-2 | 2026-10-29 |  |
| 3 | Janith Madhusanka | Not specified | @janithmadhu277-cmyk | Ayurveda | pathpadagam | Mollugo cerviana | 4-vinylphenol | 2/10 | ✅ | ✅ | ✅ | PMID:14675903 | 2026-10-29 |  |
| 4 | Janith Madhusanka | Not specified | @janithmadhu277-cmyk | Ayurveda | pathpadagam | Mollugo cerviana | capric-acid | 1/10 | ✅ | ✅ | ✅ | doi:10.1038/s41467-023-38985-6 | 2026-10-29 |  |
| 5 | Janith Madhusanka | Not specified | @janithmadhu277-cmyk | Ayurveda | pathpadagam | Mollugo cerviana | di-n-octyl-phthalate | 8/10 | ✅ | ✅ | ✅ | PMID:40243467 | 2026-10-29 |  |
| 6 | Janith Madhusanka | Not specified | @janithmadhu277-cmyk | Ayurveda | pathpadagam | Mollugo cerviana | diethyl-phthalate | 7/10 | ✅ | ✅ | ✅ | PMID:40243467 | 2026-10-29 |  |
| 7 | Janith Madhusanka | Not specified | @janithmadhu277-cmyk | Ayurveda | pathpadagam | Mollugo cerviana | guaiacol | 1/10 | ✅ | ✅ | ✅ | PMID:40503524 | 2026-10-29 |  |
| 8 | Janith Madhusanka | Not specified | @janithmadhu277-cmyk | Ayurveda | pathpadagam | Mollugo cerviana | lauric-acid | 1/10 | ✅ | ✅ | ✅ | doi:10.1038/s41467-023-38985-6 | 2026-10-29 |  |
| 9 | Janith Madhusanka | Not specified | @janithmadhu277-cmyk | Ayurveda | pathpadagam | Mollugo cerviana | neophytadiene | 1/10 | ✅ | ✅ | ✅ | PMID:38386097 | 2026-10-29 |  |
| 10 | Janith Madhusanka | Not specified | @janithmadhu277-cmyk | Ayurveda | pathpadagam | Mollugo cerviana | phytol | 1/10 | ✅ | ✅ | ✅ | PMID:16202384 | 2026-10-29 |  |
| 11 | Janith Madhusanka | Not specified | @janithmadhu277-cmyk | Ayurveda | pathpadagam | Mollugo cerviana | squalene | 1/10 | ✅ | ✅ | ✅ | UniProt:Q14534 | 2026-10-29 |  |

## Contribution declaration

By adding your name above you confirm that:

- the data in your three files is your own work or properly cited from the stated sources,
- `python3 contributions/check_submission.py <path-to-chemical-folder>/<chemical>` reported **PASSED**,
- you have removed all example rows from the templates,
- you are happy for the data to be released under the project licence: **[add licence]**.
