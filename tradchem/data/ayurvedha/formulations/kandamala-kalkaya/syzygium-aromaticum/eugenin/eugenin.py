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
    "chemical_name": "Eugenin",
    "smiles": "COc1cc(O)c2c(=O)cc(C)oc2c1",
    "pubchem_cid": "10189",
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
        method="ChEMBL", score=4.75, source_ref="ChEMBL ID: CHEMBL446974"
    ),
    slot(
        uniprot_id="P35354", protein_name="Prostaglandin G/H synthase 2", protein_acronym="PTGS2",
        species="Homo sapiens", taxon_id=9606,
        cell_types=[],
        best_structure="AlphaFold:AF-P35354-F1", other_structures=[],
        go_terms=['GO:0005737 cytoplasm', 'GO:0005783 endoplasmic reticulum', 'GO:0005788 endoplasmic reticulum lumen', 'GO:0005789 endoplasmic reticulum membrane', 'GO:0043005 neuron projection', 'GO:0005637 nuclear inner membrane', 'GO:0005640 nuclear outer membrane', 'GO:0019899 enzyme binding', 'GO:0020037 heme binding', 'GO:0016701 oxidoreductase activity, acting on single donors with incorporation of molecular oxygen', 'GO:0004601 peroxidase activity', 'GO:0004666 prostaglandin-endoperoxide synthase activity', 'GO:0042803 protein homodimerization activity', 'GO:0050873 brown fat cell differentiation', 'GO:0071456 cellular response to hypoxia', 'GO:0071471 cellular response to non-ionic osmotic stress', 'GO:0019371 cyclooxygenase pathway', 'GO:0019372 lipoxygenase pathway', 'GO:0042759 long-chain fatty acid biosynthetic process', 'GO:1902219 negative regulation of intrinsic apoptotic signaling pathway in response to osmotic stress', 'GO:0090336 positive regulation of brown fat cell differentiation', 'GO:0090050 positive regulation of cell migration involved in sprouting angiogenesis', 'GO:0031622 positive regulation of fever generation', 'GO:0090271 positive regulation of fibroblast growth factor production', 'GO:0045429 positive regulation of nitric oxide biosynthetic process', 'GO:0090362 positive regulation of platelet-derived growth factor production', 'GO:0031394 positive regulation of prostaglandin biosynthetic process', 'GO:0071636 positive regulation of transforming growth factor beta production', 'GO:0010575 positive regulation of vascular endothelial growth factor production', 'GO:0001516 prostaglandin biosynthetic process', 'GO:0008217 regulation of blood pressure', 'GO:0050727 regulation of inflammatory response', 'GO:0150077 regulation of neuroinflammatory response', 'GO:0006979 response to oxidative stress'],
        protein_diseases=[],
        method="ChEMBL", score=4.7, source_ref="ChEMBL ID: CHEMBL446974"
    ),
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
