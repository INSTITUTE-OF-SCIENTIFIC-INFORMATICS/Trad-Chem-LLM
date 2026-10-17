#!/usr/bin/env python3
"""
Add ONE chemical with its TOP 10 target proteins (UniProt IDs), each with its best
structure, GO terms, diseases, method and score.

1. Edit CHEMICAL (the compound + where it comes from).
2. Edit TARGETS: fill slot(...) for each protein, best hit first. Order = rank 1..10.
   Leave unused slots as slot() or delete them. More than 10 is rejected.
3. Run:   python3 add_top10.py
   (keep this file next to import_data.py and tradmed.db)

For another chemical: copy this file, or change CHEMICAL and TARGETS and run again.
Everything for the chemical is saved together: if any protein has a mistake,
nothing for that chemical is saved and the error says which protein.
"""
import sqlite3
from import_data import import_record, DB_DEFAULT

# ------------------------------------------------------------------ the chemical
CHEMICAL = {
    "medicine": "Example Medicine A",
    "system": "Ayurveda",                  # Ayurveda / Siddha / Unani / TCM / Other
    "plant": "Curcuma longa",              # scientific name
    "plant_type": "herb",
    "part_used": "rhizome",
    "family": "Zingiberaceae",
    "common_name": "Turmeric",
    "chemical_name": "curcumin",
    "smiles": "COC1=C(C=CC(=C1)C=CC(=O)CC(=O)C=CC2=CC(=C(C=C2)O)OC)O",
    "pubchem_cid": "969516",
    "diseases": ["colorectal cancer", "arthritis"],   # diseases linked to the CHEMICAL
}


# ------------------------------------------------------------------ one protein slot
def slot(uniprot_id="", protein_name="", protein_acronym="", species="", taxon_id="",
         cell_types=(), best_structure="", other_structures=(), go_terms=(),
         protein_diseases=(), method="", score="", source_ref=""):
    """best_structure / other_structures look like  PDB:5IKR  |  AlphaFold:AF-P35354-F1  |  SWISS-MODEL:xxxx
    go_terms look like  "GO:0006954 inflammatory response"
    method: docking / assay / SwissTargetPrediction / literature     score: affinity or probability"""
    return dict(uniprot_id=uniprot_id, protein_name=protein_name, protein_acronym=protein_acronym,
                species=species, taxon_id=taxon_id, cell_types=list(cell_types),
                best_structure=best_structure, other_structures=list(other_structures),
                go_terms=list(go_terms), protein_diseases=list(protein_diseases),
                method=method, score=score, source_ref=source_ref)


# ------------------------------------------------------------------ top 10 proteins, best first
TARGETS = [
    slot(  # rank 1   (EXAMPLE ONLY: replace with verified data)
        uniprot_id="P35354", protein_name="Prostaglandin G/H synthase 2", protein_acronym="PTGS2",
        species="Homo sapiens", taxon_id=9606,
        cell_types=["macrophage", "epithelial cell"],
        best_structure="PDB:5IKR", other_structures=["AlphaFold:AF-P35354-F1"],
        go_terms=["GO:0006954 inflammatory response", "GO:0005737 cytoplasm"],
        protein_diseases=["inflammation"],
        method="literature", score="", source_ref="EXAMPLE ONLY - replace with real citation / DOI"),
    slot(  # rank 2   (EXAMPLE ONLY)
        uniprot_id="P03372", protein_name="Estrogen receptor", protein_acronym="ESR1",
        species="Homo sapiens", taxon_id=9606,
        cell_types=["epithelial cell"],
        best_structure="AlphaFold:AF-P03372-F1",
        go_terms=["GO:0005634 nucleus"],
        protein_diseases=["breast cancer"],
        method="docking", score=-8.1, source_ref="EXAMPLE ONLY"),
    slot(),  # rank 3
    slot(),  # rank 4
    slot(),  # rank 5
    slot(),  # rank 6
    slot(),  # rank 7
    slot(),  # rank 8
    slot(),  # rank 9
    slot(),  # rank 10
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
