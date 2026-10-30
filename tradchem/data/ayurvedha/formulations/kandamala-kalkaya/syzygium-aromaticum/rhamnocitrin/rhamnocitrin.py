#!/usr/bin/env python3
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[7] / "contributions"))
from import_data import import_record, DB_DEFAULT  # noqa: E402

CHEMICAL = {
    "medicine": "kandamala-kalkaya",
    "system": "Ayurveda",
    "plant": "Syzygium aromaticum",
    "plant_type": "tree",
    "part_used": "flower buds",
    "family": "Myrtaceae",
    "common_name": "Clove",
    "chemical_name": "Rhamnocitrin",
    "smiles": "COc1cc(O)c2c(=O)c(O)c(-c3ccc(O)cc3)oc2c1",
    "pubchem_cid": "5320946",
    "diseases": [],
}

def slot(uniprot_id="", protein_name="", protein_acronym="", species="", taxon_id="",
         cell_types=(), best_structure="", other_structures=(), go_terms=(),
         protein_diseases=(), method="", score="", source_ref=""):
    return dict(uniprot_id=uniprot_id, protein_name=protein_name, protein_acronym=protein_acronym,
                species=species, taxon_id=taxon_id, cell_types=list(cell_types),
                best_structure=best_structure, other_structures=list(other_structures),
                go_terms=list(go_terms), protein_diseases=list(protein_diseases),
                method=method, score=score, source_ref=source_ref)

TARGETS = [
    slot(
        uniprot_id="P21397", protein_name="Amine oxidase [flavin-containing] A", protein_acronym="MAOA",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Heart, liver, duodenum, blood vessels and kidney'],
        best_structure="AlphaFold:AF-P21397-F1", other_structures=[],
        go_terms=['GO:0005741 mitochondrial outer membrane', 'GO:0005739 mitochondrion', 'GO:0097621 monoamine oxidase activity', 'GO:0008131 primary methylamine oxidase activity', 'GO:0006576 biogenic amine metabolic process', 'GO:0042420 dopamine catabolic process', 'GO:0019607 phenylethylamine catabolic process', 'GO:0042429 serotonin catabolic process', 'GO:0042428 serotonin metabolic process'],
        protein_diseases=['Brunner syndrome'],
        method="ChEMBL", score=7.29, source_ref="ChEMBL ID: CHEMBL442289"
    ),
    slot(),
    slot(),
    slot(),
    slot(),
    slot(),
    slot(),
    slot(),
    slot(),
    slot(),
]

def main():
    record = dict(CHEMICAL, targets=TARGETS)
    conn = sqlite3.connect(DB_DEFAULT)
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        conn.execute("SAVEPOINT chem")
        import_record(conn, record)
        conn.execute("RELEASE chem")
        conn.commit()
        n = sum(1 for t in TARGETS if t["uniprot_id"])
        print(f"Saved {CHEMICAL['chemical_name']} with {n} target protein(s).")
    except Exception as e:
        conn.execute("ROLLBACK TO chem")
        conn.execute("RELEASE chem")
        print(f"Nothing saved for {CHEMICAL['chemical_name']}: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
