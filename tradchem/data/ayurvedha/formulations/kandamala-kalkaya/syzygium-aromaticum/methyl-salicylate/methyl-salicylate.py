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
    "chemical_name": "Methyl salicylate",
    "smiles": "COC(=O)c1ccccc1O",
    "pubchem_cid": "4133",
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
        uniprot_id="P02545", protein_name="Prelamin-A/C", protein_acronym="LMNA",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['In the arteries, prelamin-A/C accumulation is not observed in young healthy vessels but is prevalent in medial vascular smooth muscle cells (VSMCs) from aged individuals and in atherosclerotic lesions, where it often colocalizes with senescent and degenerate VSMCs. Prelamin-A/C expression increases with age and disease. In normal aging, the accumulation of prelamin-A/C is caused in part by the down-regulation of ZMPSTE24/FACE1 in response to oxidative stress'],
        best_structure="AlphaFold:AF-P02545-F1", other_structures=[],
        go_terms=['GO:0005829 cytosol', 'GO:0005882 intermediate filament', 'GO:0005638 lamin filament', 'GO:0005635 nuclear envelope', 'GO:0005652 nuclear lamina', 'GO:0016363 nuclear matrix', 'GO:0031965 nuclear membrane', 'GO:0016607 nuclear speck', 'GO:0005654 nucleoplasm', 'GO:0005634 nucleus', 'GO:0048471 perinuclear region of cytoplasm', 'GO:0035861 site of double-strand break', 'GO:0042802 identical protein binding', 'GO:0005200 structural constituent of cytoskeleton', 'GO:0160123 structural constituent of nuclear lamina', 'GO:0005198 structural molecule activity', 'GO:0071456 cellular response to hypoxia', 'GO:0090398 cellular senescence', 'GO:1990683 DNA double-strand break attachment to nuclear envelope', 'GO:0006303 double-strand break repair via nonhomologous end joining', 'GO:0030951 establishment or maintenance of microtubule cytoskeleton polarity', 'GO:0031507 heterochromatin formation', 'GO:0008104 intracellular protein localization', 'GO:0007517 muscle organ development', 'GO:1903243 negative regulation of cardiac muscle hypertrophy in response to stress', 'GO:0008285 negative regulation of cell population proliferation', 'GO:0006998 nuclear envelope organization', 'GO:0007097 nuclear migration', 'GO:0051664 nuclear pore localization', 'GO:0090435 protein localization to nuclear envelope', 'GO:0034504 protein localization to nucleus', 'GO:0030334 regulation of cell migration', 'GO:0032204 regulation of telomere maintenance'],
        protein_diseases=['Emery-Dreifuss muscular dystrophy 2, autosomal dominant', 'Emery-Dreifuss muscular dystrophy 3, autosomal recessive', 'Cardiomyopathy, dilated, 1A', 'Lipodystrophy, familial partial, 2', 'Charcot-Marie-Tooth disease, axonal, type 2B1', 'Hutchinson-Gilford progeria syndrome', 'Cardiomyopathy, dilated, with hypergonadotropic hypogonadism', 'Mandibuloacral dysplasia with type A lipodystrophy', 'Restrictive dermopathy 2', 'Heart-hand syndrome Slovenian type', 'Muscular dystrophy congenital LMNA-related'],
        method="ChEMBL", score=6.1, source_ref="ChEMBL ID: CHEMBL108545"
    ),
    slot(
        uniprot_id="P16473", protein_name="Thyrotropin receptor", protein_acronym="TSHR",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Expressed in thyroide cells (at protein level) (PubMed:11847099). Expressed in the thyroid (PubMed:2610690)'],
        best_structure="AlphaFold:AF-P16473-F1", other_structures=[],
        go_terms=['GO:0016323 basolateral plasma membrane', 'GO:0009986 cell surface', 'GO:0005886 plasma membrane', 'GO:0043235 signaling receptor complex', 'GO:0008528 G protein-coupled peptide receptor activity', 'GO:0004930 G protein-coupled receptor activity', 'GO:0044877 protein-containing complex binding', 'GO:0038023 signaling receptor activity', 'GO:0004996 thyroid-stimulating hormone receptor activity', 'GO:0007189 adenylate cyclase-activating G protein-coupled receptor signaling pathway', 'GO:0007166 cell surface receptor signaling pathway', 'GO:0007267 cell-cell signaling', 'GO:1904588 cellular response to glycoprotein', 'GO:1905229 cellular response to thyrotropin-releasing hormone', 'GO:0007186 G protein-coupled receptor signaling pathway', 'GO:0007187 G protein-coupled receptor signaling pathway, coupled to cyclic nucleotide second messenger', 'GO:0009755 hormone-mediated signaling pathway', 'GO:0008284 positive regulation of cell population proliferation', 'GO:0120162 positive regulation of cold-induced thermogenesis', 'GO:0038194 thyroid-stimulating hormone signaling pathway'],
        protein_diseases=['Hypothyroidism, congenital, non-goitrous, 1', 'Familial gestational hyperthyroidism', 'Hyperthyroidism, non-autoimmune'],
        method="ChEMBL", score=5.4, source_ref="ChEMBL ID: CHEMBL108545"
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
