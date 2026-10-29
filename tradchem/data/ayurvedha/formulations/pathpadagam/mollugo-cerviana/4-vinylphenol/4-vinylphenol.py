#!/usr/bin/env python3
# Data-only contribution; no network calls or computation.
CHEMICAL = {'medicine': '',
 'system': 'Ayurveda',
 'plant': 'Mollugo cerviana',
 'plant_type': 'herb',
 'part_used': 'whole plant',
 'family': 'Molluginaceae',
 'common_name': 'Pathpadagam (පත්පාඩගම්)',
 'chemical_name': '4-vinylphenol',
 'smiles': 'C=CC1=CC=C(C=C1)O',
 'pubchem_cid': '62453',
 'diseases': []}

def slot(**kwargs):
    return kwargs

TARGETS = [
    slot(uniprot_id='Q05421', protein_name='Cytochrome P450 2E1', protein_acronym='CYP2E1', species='Mus musculus', taxon_id=10090, cell_types=[], best_structure='AlphaFold:AF-Q05421-F1', other_structures=[], go_terms=[], protein_diseases=[], method='literature', score='', source_ref='PMID:14675903; PMID:20925585'),
    slot(uniprot_id='P33267', protein_name='Cytochrome P450 2F2', protein_acronym='CYP2F2', species='Mus musculus', taxon_id=10090, cell_types=[], best_structure='AlphaFold:AF-P33267-F1', other_structures=[], go_terms=[], protein_diseases=[], method='literature', score='', source_ref='PMID:14675903; PMID:20925585'),
]
