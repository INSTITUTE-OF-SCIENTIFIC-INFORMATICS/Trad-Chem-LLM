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
    "part_used": "buds, leaves, and stems",
    "family": "Myrtaceae",
    "common_name": "Clove",
    "chemical_name": "Eugenyl acetate",
    "smiles": "C=CCc1ccc(OC(C)=O)c(OC)c1",
    "pubchem_cid": "7136",
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
        uniprot_id="P23219", protein_name="Prostaglandin G/H synthase 1", protein_acronym="PTGS1",
        species="Homo sapiens", taxon_id=9606,
        cell_types=[],
        best_structure="AlphaFold:AF-P23219-F1", other_structures=[],
        go_terms=['GO:0005737 cytoplasm', 'GO:0005788 endoplasmic reticulum lumen', 'GO:0005789 endoplasmic reticulum membrane', 'GO:0070062 extracellular exosome', 'GO:0043005 neuron projection', 'GO:0001750 photoreceptor outer segment', 'GO:0020037 heme binding', 'GO:0004601 peroxidase activity', 'GO:0004666 prostaglandin-endoperoxide synthase activity', 'GO:0019371 cyclooxygenase pathway', 'GO:0001516 prostaglandin biosynthetic process', 'GO:0008217 regulation of blood pressure', 'GO:0006979 response to oxidative stress'],
        protein_diseases=[],
        method="ChEMBL", score=5.52, source_ref="ChEMBL ID: CHEMBL108299"
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
