#!/usr/bin/env python3
# Data-only contribution; no network calls or computation.
CHEMICAL = {'medicine': '',
 'system': 'Ayurveda',
 'plant': 'Mollugo cerviana',
 'plant_type': 'herb',
 'part_used': 'whole plant',
 'family': 'Molluginaceae',
 'common_name': 'Pathpadagam (පත්පාඩගම්)',
 'chemical_name': 'Neophytadiene',
 'smiles': 'CC(C)CCCC(C)CCCC(C)CCCC(=C)C=C',
 'pubchem_cid': '10446',
 'diseases': []}

def slot(**kwargs):
    return kwargs

TARGETS = [
    slot(uniprot_id='P12821', protein_name='Angiotensin-converting enzyme', protein_acronym='ACE', species='Homo sapiens', taxon_id=9606, cell_types=[], best_structure='PDB:1O8A', other_structures=[], go_terms=[], protein_diseases=[], method='docking', score='', source_ref='PMID:38386097'),
]
