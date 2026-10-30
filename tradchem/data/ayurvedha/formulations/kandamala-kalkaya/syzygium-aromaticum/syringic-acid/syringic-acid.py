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
    "chemical_name": "Syringic acid",
    "smiles": "COc1cc(C(=O)O)cc(OC)c1O",
    "pubchem_cid": "10742",
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
        uniprot_id="P00918", protein_name="Carbonic anhydrase 2", protein_acronym="CA2",
        species="Homo sapiens", taxon_id=9606,
        cell_types=[],
        best_structure="AlphaFold:AF-P00918-F1", other_structures=[],
        go_terms=['GO:0045177 apical part of cell', 'GO:0005737 cytoplasm', 'GO:0005829 cytosol', 'GO:0070062 extracellular exosome', 'GO:0043209 myelin sheath', 'GO:0005886 plasma membrane', 'GO:0004064 arylesterase activity', 'GO:0004089 carbonate dehydratase activity', 'GO:0018820 cyanamide hydratase activity', 'GO:0008270 zinc ion binding', 'GO:0038166 angiotensin-activated signaling pathway', 'GO:2001150 positive regulation of dipeptide transmembrane transport', 'GO:0051453 regulation of intracellular pH', 'GO:0044070 regulation of monoatomic anion transport'],
        protein_diseases=['Osteopetrosis, autosomal recessive 3'],
        method="ChEMBL", score=5.5, source_ref="ChEMBL ID: CHEMBL1414"
    ),
    slot(
        uniprot_id="P00915", protein_name="Carbonic anhydrase 1", protein_acronym="CA1",
        species="Homo sapiens", taxon_id=9606,
        cell_types=[],
        best_structure="AlphaFold:AF-P00915-F1", other_structures=[],
        go_terms=['GO:0005737 cytoplasm', 'GO:0005829 cytosol', 'GO:0070062 extracellular exosome', 'GO:0004064 arylesterase activity', 'GO:0004089 carbonate dehydratase activity', 'GO:0018820 cyanamide hydratase activity', 'GO:0016836 hydro-lyase activity', 'GO:0008270 zinc ion binding', 'GO:0009750 response to fructose'],
        protein_diseases=[],
        method="ChEMBL", score=5.38, source_ref="ChEMBL ID: CHEMBL1414"
    ),
    slot(
        uniprot_id="P35218", protein_name="Carbonic anhydrase 5A, mitochondrial", protein_acronym="CA5A",
        species="Homo sapiens", taxon_id=9606,
        cell_types=[],
        best_structure="AlphaFold:AF-P35218-F1", other_structures=[],
        go_terms=['GO:0005737 cytoplasm', 'GO:0005759 mitochondrial matrix', 'GO:0005739 mitochondrion', 'GO:0004089 carbonate dehydratase activity', 'GO:0008270 zinc ion binding'],
        protein_diseases=['Hyperammonemia due to carbonic anhydrase VA deficiency'],
        method="ChEMBL", score=5.2, source_ref="ChEMBL ID: CHEMBL1414"
    ),
    slot(
        uniprot_id="P23280", protein_name="Carbonic anhydrase 6", protein_acronym="CA6",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Major constituent of saliva'],
        best_structure="AlphaFold:AF-P23280-F1", other_structures=[],
        go_terms=['GO:0005829 cytosol', 'GO:0070062 extracellular exosome', 'GO:0005576 extracellular region', 'GO:0004089 carbonate dehydratase activity', 'GO:0008270 zinc ion binding', 'GO:0001580 detection of chemical stimulus involved in sensory perception of bitter taste'],
        protein_diseases=[],
        method="ChEMBL", score=5.12, source_ref="ChEMBL ID: CHEMBL1414"
    ),
    slot(
        uniprot_id="P43166", protein_name="Carbonic anhydrase 7", protein_acronym="CA7",
        species="Homo sapiens", taxon_id=9606,
        cell_types=[],
        best_structure="AlphaFold:AF-P43166-F1", other_structures=[],
        go_terms=['GO:0005737 cytoplasm', 'GO:0005829 cytosol', 'GO:0004089 carbonate dehydratase activity', 'GO:0008270 zinc ion binding'],
        protein_diseases=[],
        method="ChEMBL", score=5.11, source_ref="ChEMBL ID: CHEMBL1414"
    ),
    slot(
        uniprot_id="Q16790", protein_name="Carbonic anhydrase 9", protein_acronym="CA9",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Expressed primarily in carcinoma cells lines. Expression is restricted to very few normal tissues and the most abundant expression is found in the epithelial cells of gastric mucosa'],
        best_structure="AlphaFold:AF-Q16790-F1", other_structures=[],
        go_terms=['GO:0016323 basolateral plasma membrane', 'GO:0016020 membrane', 'GO:0031528 microvillus membrane', 'GO:0005730 nucleolus', 'GO:0005886 plasma membrane', 'GO:0004089 carbonate dehydratase activity', 'GO:0140677 molecular function activator activity', 'GO:0008270 zinc ion binding', 'GO:0001666 response to hypoxia', 'GO:0033574 response to testosterone', 'GO:0009410 response to xenobiotic stimulus'],
        protein_diseases=[],
        method="ChEMBL", score=5.09, source_ref="ChEMBL ID: CHEMBL1414"
    ),
    slot(
        uniprot_id="P07451", protein_name="Carbonic anhydrase 3", protein_acronym="CA3",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Muscle specific'],
        best_structure="AlphaFold:AF-P07451-F1", other_structures=[],
        go_terms=['GO:0005737 cytoplasm', 'GO:0005829 cytosol', 'GO:0005634 nucleus', 'GO:0030017 sarcomere', 'GO:0004089 carbonate dehydratase activity', 'GO:0016151 nickel cation binding', 'GO:0016791 phosphatase activity', 'GO:0008270 zinc ion binding', 'GO:0071456 cellular response to hypoxia', 'GO:0032869 cellular response to insulin stimulus', 'GO:0044320 cellular response to leptin stimulus', 'GO:0097421 liver regeneration', 'GO:1903751 negative regulation of intrinsic apoptotic signaling pathway in response to hydrogen peroxide', 'GO:1903427 negative regulation of reactive oxygen species biosynthetic process', 'GO:0008284 positive regulation of cell population proliferation', 'GO:0045471 response to ethanol', 'GO:0033993 response to lipid', 'GO:0006979 response to oxidative stress', 'GO:0003009 skeletal muscle contraction'],
        protein_diseases=[],
        method="ChEMBL", score=5.07, source_ref="ChEMBL ID: CHEMBL1414"
    ),
    slot(
        uniprot_id="Q9ULX7", protein_name="Carbonic anhydrase 14", protein_acronym="CA14",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['High expression in all parts of the central nervous system and lower expression in adult liver, heart, small intestine, colon, kidney, urinary bladder and skeletal muscle'],
        best_structure="AlphaFold:AF-Q9ULX7-F1", other_structures=[],
        go_terms=['GO:0016324 apical plasma membrane', 'GO:0016323 basolateral plasma membrane', 'GO:0016020 membrane', 'GO:0005886 plasma membrane', 'GO:0004089 carbonate dehydratase activity', 'GO:0008270 zinc ion binding'],
        protein_diseases=[],
        method="ChEMBL", score=5.04, source_ref="ChEMBL ID: CHEMBL1414"
    ),
    slot(
        uniprot_id="O43570", protein_name="Carbonic anhydrase 12", protein_acronym="CA12",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Highly expressed in colon, kidney, prostate, intestine and activated lymphocytes. Expressed at much higher levels in the renal cell cancers than in surrounding normal kidney tissue. Moderately expressed in pancreas, ovary and testis. Expressed in sweat glands and bronchiolar epithelium (PubMed:26911677)'],
        best_structure="AlphaFold:AF-O43570-F1", other_structures=[],
        go_terms=['GO:0016324 apical plasma membrane', 'GO:0016323 basolateral plasma membrane', 'GO:0016020 membrane', 'GO:0005886 plasma membrane', 'GO:0004089 carbonate dehydratase activity', 'GO:0008270 zinc ion binding', 'GO:0055064 chloride ion homeostasis', 'GO:0044849 estrous cycle'],
        protein_diseases=['Hyperchlorhidrosis, isolated'],
        method="ChEMBL", score=5.04, source_ref="ChEMBL ID: CHEMBL1414"
    ),
    slot(
        uniprot_id="P22748", protein_name="Carbonic anhydrase 4", protein_acronym="CA4",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Expressed in the endothelium of the choriocapillaris in eyes (at protein level). Not expressed in the retinal epithelium at detectable levels'],
        best_structure="AlphaFold:AF-P22748-F1", other_structures=[],
        go_terms=['GO:0016324 apical plasma membrane', 'GO:0031526 brush border membrane', 'GO:0009986 cell surface', 'GO:0005793 endoplasmic reticulum-Golgi intermediate compartment', 'GO:0009897 external side of plasma membrane', 'GO:0070062 extracellular exosome', 'GO:0005794 Golgi apparatus', 'GO:0016020 membrane', 'GO:0048471 perinuclear region of cytoplasm', 'GO:0005886 plasma membrane', 'GO:0005791 rough endoplasmic reticulum', 'GO:0030667 secretory granule membrane', 'GO:0005802 trans-Golgi network', 'GO:0030658 transport vesicle membrane', 'GO:0004089 carbonate dehydratase activity', 'GO:0008270 zinc ion binding', 'GO:0015701 bicarbonate transport'],
        protein_diseases=['Retinitis pigmentosa 17'],
        method="ChEMBL", score=4.97, source_ref="ChEMBL ID: CHEMBL1414"
    ),
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
