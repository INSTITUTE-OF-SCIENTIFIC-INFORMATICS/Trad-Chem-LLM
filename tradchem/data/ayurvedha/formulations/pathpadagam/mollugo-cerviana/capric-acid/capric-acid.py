#!/usr/bin/env python3
# Data-only contribution; no network calls or computation.
CHEMICAL = {'medicine': '',
 'system': 'Ayurveda',
 'plant': 'Mollugo cerviana',
 'plant_type': 'herb',
 'part_used': 'whole plant',
 'family': 'Molluginaceae',
 'common_name': 'Pathpadagam (පත්පාඩගම්)',
 'chemical_name': 'decanoic acid',
 'smiles': 'CCCCCCCCCC(=O)O',
 'pubchem_cid': '2969',
 'diseases': []}

def slot(**kwargs):
    return kwargs

TARGETS = [
    slot(uniprot_id='Q9NQS5', protein_name='G protein-coupled receptor 84', protein_acronym='GPR84', species='Homo sapiens', taxon_id=9606, cell_types=[], best_structure='PDB:8J18', other_structures=[], go_terms=['GO:0004930'], protein_diseases=[], method='literature', score='', source_ref='doi:10.1038/s41467-023-38985-6'),
]
