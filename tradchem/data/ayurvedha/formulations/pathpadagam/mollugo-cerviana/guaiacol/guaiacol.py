#!/usr/bin/env python3
# Data-only contribution; no network calls or computation.
CHEMICAL = {'medicine': '',
 'system': 'Ayurveda',
 'plant': 'Mollugo cerviana',
 'plant_type': 'herb',
 'part_used': 'whole plant',
 'family': 'Molluginaceae',
 'common_name': 'Pathpadagam (පත්පාඩගම්)',
 'chemical_name': 'guaiacol',
 'smiles': 'COC1=CC=CC=C1O',
 'pubchem_cid': '460',
 'diseases': []}

def slot(**kwargs):
    return kwargs

TARGETS = [
    slot(uniprot_id='Q8NGN3', protein_name='Olfactory receptor 10G4', protein_acronym='OR10G4', species='Homo sapiens', taxon_id=9606, cell_types=[], best_structure='AlphaFold:AF-Q8NGN3-F1', other_structures=[], go_terms=['GO:0004984'], protein_diseases=[], method='docking', score=-4.15, source_ref='PMID:40503524'),
]
