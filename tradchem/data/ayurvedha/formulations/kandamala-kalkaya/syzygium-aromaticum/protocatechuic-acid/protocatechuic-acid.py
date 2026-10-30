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
    "chemical_name": "Protocatechuic acid",
    "smiles": "O=C(O)c1ccc(O)c(O)c1",
    "pubchem_cid": "72",
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
        method="ChEMBL", score=6.33, source_ref="ChEMBL ID: CHEMBL37537"
    ),
    slot(
        uniprot_id="Q9ULX7", protein_name="Carbonic anhydrase 14", protein_acronym="CA14",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['High expression in all parts of the central nervous system and lower expression in adult liver, heart, small intestine, colon, kidney, urinary bladder and skeletal muscle'],
        best_structure="AlphaFold:AF-Q9ULX7-F1", other_structures=[],
        go_terms=['GO:0016324 apical plasma membrane', 'GO:0016323 basolateral plasma membrane', 'GO:0016020 membrane', 'GO:0005886 plasma membrane', 'GO:0004089 carbonate dehydratase activity', 'GO:0008270 zinc ion binding'],
        protein_diseases=[],
        method="ChEMBL", score=6.16, source_ref="ChEMBL ID: CHEMBL37537"
    ),
    slot(
        uniprot_id="P00915", protein_name="Carbonic anhydrase 1", protein_acronym="CA1",
        species="Homo sapiens", taxon_id=9606,
        cell_types=[],
        best_structure="AlphaFold:AF-P00915-F1", other_structures=[],
        go_terms=['GO:0005737 cytoplasm', 'GO:0005829 cytosol', 'GO:0070062 extracellular exosome', 'GO:0004064 arylesterase activity', 'GO:0004089 carbonate dehydratase activity', 'GO:0018820 cyanamide hydratase activity', 'GO:0016836 hydro-lyase activity', 'GO:0008270 zinc ion binding', 'GO:0009750 response to fructose'],
        protein_diseases=[],
        method="ChEMBL", score=5.97, source_ref="ChEMBL ID: CHEMBL37537"
    ),
    slot(
        uniprot_id="P22748", protein_name="Carbonic anhydrase 4", protein_acronym="CA4",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Expressed in the endothelium of the choriocapillaris in eyes (at protein level). Not expressed in the retinal epithelium at detectable levels'],
        best_structure="AlphaFold:AF-P22748-F1", other_structures=[],
        go_terms=['GO:0016324 apical plasma membrane', 'GO:0031526 brush border membrane', 'GO:0009986 cell surface', 'GO:0005793 endoplasmic reticulum-Golgi intermediate compartment', 'GO:0009897 external side of plasma membrane', 'GO:0070062 extracellular exosome', 'GO:0005794 Golgi apparatus', 'GO:0016020 membrane', 'GO:0048471 perinuclear region of cytoplasm', 'GO:0005886 plasma membrane', 'GO:0005791 rough endoplasmic reticulum', 'GO:0030667 secretory granule membrane', 'GO:0005802 trans-Golgi network', 'GO:0030658 transport vesicle membrane', 'GO:0004089 carbonate dehydratase activity', 'GO:0008270 zinc ion binding', 'GO:0015701 bicarbonate transport'],
        protein_diseases=['Retinitis pigmentosa 17'],
        method="ChEMBL", score=5.61, source_ref="ChEMBL ID: CHEMBL37537"
    ),
    slot(
        uniprot_id="P10636", protein_name="Microtubule-associated protein tau", protein_acronym="MAPT",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Expressed in neurons. Isoform PNS-tau is expressed in the peripheral nervous system while the others are expressed in the central nervous system'],
        best_structure="AlphaFold:AF-P10636-F1", other_structures=[],
        go_terms=['GO:0030673 axolemma', 'GO:0030424 axon', 'GO:1904115 axon cytoplasm', 'GO:0044297 cell body', 'GO:0005737 cytoplasm', 'GO:0036464 cytoplasmic ribonucleoprotein granule', 'GO:0005829 cytosol', 'GO:0030425 dendrite', 'GO:0043197 dendritic spine', 'GO:0005576 extracellular region', 'GO:0097386 glial cell projection', 'GO:0030426 growth cone', 'GO:0044304 main axon', 'GO:0045121 membrane raft', 'GO:0015630 microtubule cytoskeleton', 'GO:0005739 mitochondrion', 'GO:0097418 neurofibrillary tangle', 'GO:0043025 neuronal cell body', 'GO:0034399 nuclear periphery', 'GO:0005634 nucleus', 'GO:0005886 plasma membrane', 'GO:0036477 somatodendritic compartment', 'GO:0045298 tubulin complex', 'GO:0003779 actin binding', 'GO:0034185 apolipoprotein binding', 'GO:0003677 DNA binding', 'GO:0003690 double-stranded DNA binding', 'GO:0034452 dynactin binding', 'GO:0019899 enzyme binding', 'GO:0004857 enzyme inhibitor activity', 'GO:0099077 histone-dependent DNA binding', 'GO:0051879 Hsp90 protein binding', 'GO:0042802 identical protein binding', 'GO:0071813 lipoprotein particle binding', 'GO:0008017 microtubule binding', 'GO:0099609 microtubule lateral binding', 'GO:0140778 microtubule stabilizing activity', 'GO:0003680 minor groove of adenine-thymine-rich DNA binding', 'GO:0035091 phosphatidylinositol binding', 'GO:1902936 phosphatidylinositol bisphosphate binding', 'GO:0019901 protein kinase binding', 'GO:0051721 protein phosphatase 2A binding', 'GO:0051087 protein-folding chaperone binding', 'GO:0030674 protein-macromolecule adaptor activity', 'GO:0003723 RNA binding', 'GO:0043565 sequence-specific DNA binding', 'GO:0017124 SH3 domain binding', 'GO:0003697 single-stranded DNA binding', 'GO:1990000 amyloid fibril formation', 'GO:0048143 astrocyte activation', 'GO:0061564 axon development', 'GO:0098930 axonal transport', 'GO:0019896 axonal transport of mitochondrion', 'GO:0007267 cell-cell signaling', 'GO:1990416 cellular response to brain-derived neurotrophic factor stimulus', 'GO:0034605 cellular response to heat', 'GO:1990090 cellular response to nerve growth factor stimulus', 'GO:0034614 cellular response to reactive oxygen species', 'GO:0021954 central nervous system neuron development', 'GO:0031122 cytoplasmic microtubule organization', 'GO:0006974 DNA damage response', 'GO:0048699 generation of neurons', 'GO:0048312 intracellular distribution of mitochondria', 'GO:0007611 learning or memory', 'GO:0007613 memory', 'GO:0001774 microglial cell activation', 'GO:0000226 microtubule cytoskeleton organization', 'GO:0046785 microtubule polymerization', 'GO:0010629 negative regulation of gene expression', 'GO:0090258 negative regulation of mitochondrial fission', 'GO:0010917 negative regulation of mitochondrial membrane potential', 'GO:1903748 negative regulation of protein localization to mitochondrion', 'GO:1902988 neurofibrillary tangle assembly', 'GO:0031175 neuron projection development', 'GO:0072386 plus-end-directed organelle transport along microtubule', 'GO:0045773 positive regulation of axon extension', 'GO:0031116 positive regulation of microtubule polymerization', 'GO:1903829 positive regulation of protein localization', 'GO:1902474 positive regulation of protein localization to synapse', 'GO:0032930 positive regulation of superoxide anion generation', 'GO:0051260 protein homooligomerization', 'GO:0051258 protein polymerization', 'GO:0010506 regulation of autophagy', 'GO:0050848 regulation of calcium-mediated signaling', 'GO:1900034 regulation of cellular response to heat', 'GO:0033044 regulation of chromosome organization', 'GO:1900452 regulation of long-term synaptic depression', 'GO:0070507 regulation of microtubule cytoskeleton organization', 'GO:0031113 regulation of microtubule polymerization', 'GO:0031110 regulation of microtubule polymerization or depolymerization', 'GO:0060632 regulation of microtubule-based movement', 'GO:0090140 regulation of mitochondrial fission', 'GO:0048167 regulation of synaptic plasticity', 'GO:0010288 response to lead ion', 'GO:0016072 rRNA metabolic process', 'GO:0034063 stress granule assembly', 'GO:0097435 supramolecular fiber organization', 'GO:0007416 synapse assembly', 'GO:0050808 synapse organization'],
        protein_diseases=['Frontotemporal dementia 1', 'Pick disease of the brain', 'Progressive supranuclear palsy 1', 'Parkinson-dementia syndrome'],
        method="ChEMBL", score=5.55, source_ref="ChEMBL ID: CHEMBL37537"
    ),
    slot(
        uniprot_id="O43570", protein_name="Carbonic anhydrase 12", protein_acronym="CA12",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Highly expressed in colon, kidney, prostate, intestine and activated lymphocytes. Expressed at much higher levels in the renal cell cancers than in surrounding normal kidney tissue. Moderately expressed in pancreas, ovary and testis. Expressed in sweat glands and bronchiolar epithelium (PubMed:26911677)'],
        best_structure="AlphaFold:AF-O43570-F1", other_structures=[],
        go_terms=['GO:0016324 apical plasma membrane', 'GO:0016323 basolateral plasma membrane', 'GO:0016020 membrane', 'GO:0005886 plasma membrane', 'GO:0004089 carbonate dehydratase activity', 'GO:0008270 zinc ion binding', 'GO:0055064 chloride ion homeostasis', 'GO:0044849 estrous cycle'],
        protein_diseases=['Hyperchlorhidrosis, isolated'],
        method="ChEMBL", score=5.39, source_ref="ChEMBL ID: CHEMBL37537"
    ),
    slot(
        uniprot_id="Q16790", protein_name="Carbonic anhydrase 9", protein_acronym="CA9",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Expressed primarily in carcinoma cells lines. Expression is restricted to very few normal tissues and the most abundant expression is found in the epithelial cells of gastric mucosa'],
        best_structure="AlphaFold:AF-Q16790-F1", other_structures=[],
        go_terms=['GO:0016323 basolateral plasma membrane', 'GO:0016020 membrane', 'GO:0031528 microvillus membrane', 'GO:0005730 nucleolus', 'GO:0005886 plasma membrane', 'GO:0004089 carbonate dehydratase activity', 'GO:0140677 molecular function activator activity', 'GO:0008270 zinc ion binding', 'GO:0001666 response to hypoxia', 'GO:0033574 response to testosterone', 'GO:0009410 response to xenobiotic stimulus'],
        protein_diseases=[],
        method="ChEMBL", score=5.35, source_ref="ChEMBL ID: CHEMBL37537"
    ),
    slot(
        uniprot_id="P23280", protein_name="Carbonic anhydrase 6", protein_acronym="CA6",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Major constituent of saliva'],
        best_structure="AlphaFold:AF-P23280-F1", other_structures=[],
        go_terms=['GO:0005829 cytosol', 'GO:0070062 extracellular exosome', 'GO:0005576 extracellular region', 'GO:0004089 carbonate dehydratase activity', 'GO:0008270 zinc ion binding', 'GO:0001580 detection of chemical stimulus involved in sensory perception of bitter taste'],
        protein_diseases=[],
        method="ChEMBL", score=5.33, source_ref="ChEMBL ID: CHEMBL37537"
    ),
    slot(
        uniprot_id="P10253", protein_name="Lysosomal alpha-glucosidase", protein_acronym="GAA",
        species="Homo sapiens", taxon_id=9606,
        cell_types=[],
        best_structure="AlphaFold:AF-P10253-F1", other_structures=[],
        go_terms=['GO:0120282 autolysosome lumen', 'GO:0035577 azurophil granule membrane', 'GO:0070062 extracellular exosome', 'GO:0101003 ficolin-1-rich granule membrane', 'GO:0043202 lysosomal lumen', 'GO:0005765 lysosomal membrane', 'GO:0005764 lysosome', 'GO:0016020 membrane', 'GO:0005886 plasma membrane', 'GO:0070821 tertiary granule membrane', 'GO:0004558 alpha-1,4-glucosidase activity', 'GO:0090599 alpha-glucosidase activity', 'GO:0030246 carbohydrate binding', 'GO:0043896 glucan 1,6-alpha-glucosidase activity', 'GO:0002086 diaphragm contraction', 'GO:0006006 glucose metabolic process', 'GO:0005980 glycogen catabolic process', 'GO:0061723 glycophagy', 'GO:0007040 lysosome organization', 'GO:0000023 maltose metabolic process', 'GO:0005985 sucrose metabolic process'],
        protein_diseases=['Pompe disease, infantile-onset', 'Pompe disease, late-onset'],
        method="ChEMBL", score=5.3, source_ref="ChEMBL ID: CHEMBL37537"
    ),
    slot(
        uniprot_id="P43166", protein_name="Carbonic anhydrase 7", protein_acronym="CA7",
        species="Homo sapiens", taxon_id=9606,
        cell_types=[],
        best_structure="AlphaFold:AF-P43166-F1", other_structures=[],
        go_terms=['GO:0005737 cytoplasm', 'GO:0005829 cytosol', 'GO:0004089 carbonate dehydratase activity', 'GO:0008270 zinc ion binding'],
        protein_diseases=[],
        method="ChEMBL", score=5.1, source_ref="ChEMBL ID: CHEMBL37537"
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
