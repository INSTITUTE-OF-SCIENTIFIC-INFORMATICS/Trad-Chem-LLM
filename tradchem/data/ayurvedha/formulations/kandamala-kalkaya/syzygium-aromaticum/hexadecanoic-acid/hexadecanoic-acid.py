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
    "chemical_name": "Hexadecanoic acid",
    "smiles": "CCCCCCCCCCCCCCCC(=O)O",
    "pubchem_cid": "985",
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
        uniprot_id="Q9H255", protein_name="Olfactory receptor 51E2", protein_acronym="OR51E2",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Highly expressed in the prostate (PubMed:11707321). Also expressed in spleen, liver, olfactory epithelium, retinal pigment epithelium and medulla oblongata (PubMed:11707321, PubMed:16491480, PubMed:29249973). In the retinal pigment epithelium expression is restricted to the pigment cells and choroid (at protein level) (PubMed:29249973). Expressed in epidermal melanocytes (at protein level) (PubMed:27226631)'],
        best_structure="AlphaFold:AF-Q9H255-F1", other_structures=[],
        go_terms=['GO:0031901 early endosome membrane', 'GO:0005886 plasma membrane', 'GO:0004930 G protein-coupled receptor activity', 'GO:0003707 nuclear steroid receptor activity', 'GO:0004984 olfactory receptor activity', 'GO:0038023 signaling receptor activity', 'GO:0007189 adenylate cyclase-activating G protein-coupled receptor signaling pathway', 'GO:0016477 cell migration', 'GO:0071398 cellular response to fatty acid', 'GO:0050911 detection of chemical stimulus involved in sensory perception of smell', 'GO:0030318 melanocyte differentiation', 'GO:0097325 melanocyte proliferation', 'GO:0045777 positive regulation of blood pressure', 'GO:1900135 positive regulation of renin secretion into blood stream', 'GO:0043401 steroid hormone receptor signaling pathway'],
        protein_diseases=[],
        method="ChEMBL", score=8.01, source_ref="ChEMBL ID: CHEMBL82293"
    ),
    slot(
        uniprot_id="P15090", protein_name="Fatty acid-binding protein, adipocyte", protein_acronym="FABP4",
        species="Homo sapiens", taxon_id=9606,
        cell_types=[],
        best_structure="AlphaFold:AF-P15090-F1", other_structures=[],
        go_terms=['GO:0005737 cytoplasm', 'GO:0005829 cytosol', 'GO:0070062 extracellular exosome', 'GO:0005811 lipid droplet', 'GO:0005634 nucleus', 'GO:0005504 fatty acid binding', 'GO:0051427 hormone receptor binding', 'GO:0060229 lipase activator activity', 'GO:0005319 lipid carrier activity', 'GO:0036041 long-chain fatty acid binding', 'GO:0005324 long-chain fatty acid transmembrane transporter activity', 'GO:0015908 fatty acid transport', 'GO:0015909 long-chain fatty acid transport', 'GO:0120162 positive regulation of cold-induced thermogenesis', 'GO:0019433 triglyceride catabolic process', 'GO:0070343 white fat cell proliferation'],
        protein_diseases=[],
        method="ChEMBL", score=6.47, source_ref="ChEMBL ID: CHEMBL82293"
    ),
    slot(
        uniprot_id="Q01469", protein_name="Fatty acid-binding protein 5", protein_acronym="FABP5",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Keratinocytes', 'highly expressed in psoriatic skin (PubMed:8092987). Expressed in brain gray matter (PubMed:21395585)'],
        best_structure="AlphaFold:AF-Q01469-F1", other_structures=[],
        go_terms=['GO:0035578 azurophil granule lumen', 'GO:0005737 cytoplasm', 'GO:0005829 cytosol', 'GO:0070062 extracellular exosome', 'GO:0005576 extracellular region', 'GO:0098978 glutamatergic synapse', 'GO:0005654 nucleoplasm', 'GO:0005634 nucleus', 'GO:0005886 plasma membrane', 'GO:0099524 postsynaptic cytosol', 'GO:0014069 postsynaptic density', 'GO:0099092 postsynaptic density, intracellular component', 'GO:0030667 secretory granule membrane', 'GO:0045202 synapse', 'GO:0005504 fatty acid binding', 'GO:0042802 identical protein binding', 'GO:0008289 lipid binding', 'GO:0005319 lipid carrier activity', 'GO:0005324 long-chain fatty acid transmembrane transporter activity', 'GO:0001972 retinoic acid binding', 'GO:0008544 epidermis development', 'GO:0015908 fatty acid transport', 'GO:0006629 lipid metabolic process', 'GO:1990379 lipid transport across blood-brain barrier', 'GO:0015909 long-chain fatty acid transport', 'GO:0120162 positive regulation of cold-induced thermogenesis', 'GO:0035360 positive regulation of peroxisome proliferator activated receptor signaling pathway', 'GO:0031392 regulation of prostaglandin biosynthetic process', 'GO:0099178 regulation of retrograde trans-synaptic signaling by endocanabinoid', 'GO:0051930 regulation of sensory perception of pain', 'GO:0098921 retrograde trans-synaptic signaling by endocannabinoid', 'GO:0019433 triglyceride catabolic process'],
        protein_diseases=[],
        method="ChEMBL", score=6.1, source_ref="ChEMBL ID: CHEMBL82293"
    ),
    slot(
        uniprot_id="Q96DB2", protein_name="Histone deacetylase 11", protein_acronym="HDAC11",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Weakly expressed in most tissues. Strongly expressed in brain, heart, skeletal muscle, kidney and testis'],
        best_structure="AlphaFold:AF-Q96DB2-F1", other_structures=[],
        go_terms=['GO:0000118 histone deacetylase complex', 'GO:0005654 nucleoplasm', 'GO:0005634 nucleus', 'GO:0005886 plasma membrane', 'GO:0140297 DNA-binding transcription factor binding', 'GO:0141221 histone deacetylase activity, hydrolytic mechanism', 'GO:0006325 chromatin organization'],
        protein_diseases=[],
        method="ChEMBL", score=6.05, source_ref="ChEMBL ID: CHEMBL82293"
    ),
    slot(
        uniprot_id="Q07869", protein_name="Peroxisome proliferator-activated receptor alpha", protein_acronym="PPARA",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Skeletal muscle, liver, heart and kidney. Expressed in monocytes (PubMed:28167758)'],
        best_structure="AlphaFold:AF-Q07869-F1", other_structures=[],
        go_terms=['GO:0000785 chromatin', 'GO:0001650 fibrillar center', 'GO:0016604 nuclear body', 'GO:0005654 nucleoplasm', 'GO:0005634 nucleus', 'GO:0090575 RNA polymerase II transcription regulator complex', 'GO:0003677 DNA binding', 'GO:0001216 DNA-binding transcription activator activity', 'GO:0001228 DNA-binding transcription activator activity, RNA polymerase II-specific', 'GO:0003700 DNA-binding transcription factor activity', 'GO:0000981 DNA-binding transcription factor activity, RNA polymerase II-specific', 'GO:0001227 DNA-binding transcription repressor activity, RNA polymerase II-specific', 'GO:0008289 lipid binding', 'GO:0097371 MDM2/MDM4 family protein binding', 'GO:0031435 mitogen-activated protein kinase kinase kinase binding', 'GO:0051525 NFAT protein binding', 'GO:0004879 nuclear receptor activity', 'GO:0003707 nuclear steroid receptor activity', 'GO:0019902 phosphatase binding', 'GO:0019904 protein domain specific binding', 'GO:0044877 protein-containing complex binding', 'GO:0000978 RNA polymerase II cis-regulatory region sequence-specific DNA binding', 'GO:0061629 RNA polymerase II-specific DNA-binding transcription factor binding', 'GO:0043565 sequence-specific DNA binding', 'GO:0001223 transcription coactivator binding', 'GO:0031624 ubiquitin conjugating enzyme binding', 'GO:0008270 zinc ion binding', 'GO:0035095 behavioral response to nicotine', 'GO:0030154 cell differentiation', 'GO:0071332 cellular response to fructose stimulus', 'GO:0009267 cellular response to starvation', 'GO:0032922 circadian regulation of gene expression', 'GO:0051607 defense response to virus', 'GO:0006631 fatty acid metabolic process', 'GO:0007507 heart development', 'GO:0009755 hormone-mediated signaling pathway', 'GO:0030522 intracellular receptor signaling pathway', 'GO:0007595 lactation', 'GO:0042157 lipoprotein metabolic process', 'GO:0032099 negative regulation of appetite', 'GO:0045776 negative regulation of blood pressure', 'GO:0061052 negative regulation of cell growth involved in cardiac muscle cell development', 'GO:0010887 negative regulation of cholesterol storage', 'GO:1900016 negative regulation of cytokine production involved in inflammatory response', 'GO:0045820 negative regulation of glycolytic process', 'GO:1903944 negative regulation of hepatocyte apoptotic process', 'GO:0050728 negative regulation of inflammatory response', 'GO:1903038 negative regulation of leukocyte cell-cell adhesion', 'GO:0010745 negative regulation of macrophage derived foam cell differentiation', 'GO:1902894 negative regulation of miRNA transcription', 'GO:0051898 negative regulation of phosphatidylinositol 3-kinase/protein kinase B signal transduction', 'GO:1903427 negative regulation of reactive oxygen species biosynthetic process', 'GO:0000122 negative regulation of transcription by RNA polymerase II', 'GO:0030512 negative regulation of transforming growth factor beta receptor signaling pathway', 'GO:0046209 nitric oxide metabolic process', 'GO:0035357 peroxisome proliferator activated receptor signaling pathway', 'GO:2001171 positive regulation of ATP biosynthetic process', 'GO:0045893 positive regulation of DNA-templated transcription', 'GO:0032000 positive regulation of fatty acid beta-oxidation', 'GO:0045923 positive regulation of fatty acid metabolic process', 'GO:0046321 positive regulation of fatty acid oxidation', 'GO:0046889 positive regulation of lipid biosynthetic process', 'GO:0045944 positive regulation of transcription by RNA polymerase II', 'GO:0042752 regulation of circadian rhythm', 'GO:0019217 regulation of fatty acid metabolic process', 'GO:2000191 regulation of fatty acid transport', 'GO:0010565 regulation of ketone metabolic process', 'GO:0045471 response to ethanol', 'GO:0001666 response to hypoxia', 'GO:0032868 response to insulin', 'GO:0007584 response to nutrient'],
        protein_diseases=[],
        method="ChEMBL", score=5.82, source_ref="ChEMBL ID: CHEMBL82293"
    ),
    slot(
        uniprot_id="P12104", protein_name="Fatty acid-binding protein, intestinal", protein_acronym="FABP2",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Expressed in the small intestine and at much lower levels in the large intestine. Highest expression levels in the jejunum'],
        best_structure="AlphaFold:AF-P12104-F1", other_structures=[],
        go_terms=['GO:0045179 apical cortex', 'GO:0005829 cytosol', 'GO:0005902 microvillus', 'GO:0005634 nucleus', 'GO:0005504 fatty acid binding', 'GO:0005319 lipid carrier activity', 'GO:0036041 long-chain fatty acid binding', 'GO:0005324 long-chain fatty acid transmembrane transporter activity', 'GO:0006631 fatty acid metabolic process', 'GO:0015908 fatty acid transport', 'GO:0098856 intestinal lipid absorption', 'GO:0019433 triglyceride catabolic process'],
        protein_diseases=[],
        method="ChEMBL", score=5.77, source_ref="ChEMBL ID: CHEMBL82293"
    ),
    slot(
        uniprot_id="P05413", protein_name="Fatty acid-binding protein, heart", protein_acronym="FABP3",
        species="Homo sapiens", taxon_id=9606,
        cell_types=[],
        best_structure="AlphaFold:AF-P05413-F1", other_structures=[],
        go_terms=['GO:0005829 cytosol', 'GO:0070062 extracellular exosome', 'GO:0005576 extracellular region', 'GO:0005634 nucleus', 'GO:0016528 sarcoplasm', 'GO:0008092 cytoskeletal protein binding', 'GO:0050543 icosatetraenoic acid binding', 'GO:0005319 lipid carrier activity', 'GO:0036041 long-chain fatty acid binding', 'GO:0005324 long-chain fatty acid transmembrane transporter activity', 'GO:0070538 oleic acid binding', 'GO:0042632 cholesterol homeostasis', 'GO:0006631 fatty acid metabolic process', 'GO:0032365 intracellular lipid transport', 'GO:0015909 long-chain fatty acid transport', 'GO:0008285 negative regulation of cell population proliferation', 'GO:0055091 phospholipid homeostasis', 'GO:0140214 positive regulation of long-chain fatty acid import into cell', 'GO:0071073 positive regulation of phospholipid biosynthetic process', 'GO:0046320 regulation of fatty acid oxidation', 'GO:0070542 response to fatty acid', 'GO:0032868 response to insulin', 'GO:0009410 response to xenobiotic stimulus', 'GO:0019433 triglyceride catabolic process'],
        protein_diseases=[],
        method="ChEMBL", score=5.58, source_ref="ChEMBL ID: CHEMBL82293"
    ),
    slot(
        uniprot_id="O60603", protein_name="Toll-like receptor 2", protein_acronym="TLR2",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Highly expressed in peripheral blood leukocytes, in particular in monocytes, in bone marrow, lymph node and in spleen. Also detected in lung and in fetal liver. Levels are low in other tissues'],
        best_structure="AlphaFold:AF-O60603-F1", other_structures=[],
        go_terms=['GO:0009986 cell surface', 'GO:0005737 cytoplasm', 'GO:0005794 Golgi apparatus', 'GO:0016020 membrane', 'GO:0045121 membrane raft', 'GO:0030670 phagocytic vesicle membrane', 'GO:0005886 plasma membrane', 'GO:0044853 plasma membrane raft', 'GO:0030667 secretory granule membrane', 'GO:0043235 signaling receptor complex', 'GO:0035354 Toll-like receptor 1-Toll-like receptor 2 protein complex', 'GO:0035355 Toll-like receptor 2-Toll-like receptor 6 protein complex', 'GO:0001540 amyloid-beta binding', 'GO:0042802 identical protein binding', 'GO:0001530 lipopolysaccharide binding', 'GO:0001875 lipopolysaccharide immune receptor activity', 'GO:0038187 pattern recognition receptor activity', 'GO:0042834 peptidoglycan binding', 'GO:0044877 protein-containing complex binding', 'GO:0038023 signaling receptor activity', 'GO:0035325 Toll-like receptor binding', 'GO:0004888 transmembrane signaling receptor activity', 'GO:0042497 triacyl lipopeptide binding', 'GO:0140367 antibacterial innate immune response', 'GO:0071221 cellular response to bacterial lipopeptide', 'GO:0071726 cellular response to diacyl bacterial lipopeptide', 'GO:0071223 cellular response to lipoteichoic acid', 'GO:0071727 cellular response to triacyl bacterial lipopeptide', 'GO:0071346 cellular response to type II interferon', 'GO:0050830 defense response to Gram-positive bacterium', 'GO:0051607 defense response to virus', 'GO:0042496 detection of diacyl bacterial lipopeptide', 'GO:0042495 detection of triacyl bacterial lipopeptide', 'GO:0006954 inflammatory response', 'GO:0045087 innate immune response', 'GO:0007612 learning', 'GO:0014005 microglia development', 'GO:0050765 negative regulation of phagocytosis', 'GO:0051964 negative regulation of synapse assembly', 'GO:0043123 positive regulation of canonical NF-kappaB signal transduction', 'GO:1903974 positive regulation of cellular response to macrophage colony-stimulating factor stimulus', 'GO:0032722 positive regulation of chemokine production', 'GO:0010628 positive regulation of gene expression', 'GO:0050729 positive regulation of inflammatory response', 'GO:0032728 positive regulation of interferon-beta production', 'GO:0032735 positive regulation of interleukin-12 production', 'GO:0032741 positive regulation of interleukin-18 production', 'GO:0032755 positive regulation of interleukin-6 production', 'GO:0032757 positive regulation of interleukin-8 production', 'GO:1904466 positive regulation of matrix metallopeptidase secretion', 'GO:0045944 positive regulation of transcription by RNA polymerase II', 'GO:0032760 positive regulation of tumor necrosis factor production', 'GO:0030177 positive regulation of Wnt signaling pathway', 'GO:0034134 toll-like receptor 2 signaling pathway', 'GO:0002224 toll-like receptor signaling pathway', 'GO:0038123 toll-like receptor TLR1:TLR2 signaling pathway', 'GO:0038124 toll-like receptor TLR6:TLR2 signaling pathway'],
        protein_diseases=[],
        method="ChEMBL", score=5.3, source_ref="ChEMBL ID: CHEMBL82293"
    ),
    slot(
        uniprot_id="Q03181", protein_name="Peroxisome proliferator-activated receptor delta", protein_acronym="PPARD",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Ubiquitous with maximal levels in placenta and skeletal muscle'],
        best_structure="AlphaFold:AF-Q03181-F1", other_structures=[],
        go_terms=['GO:0000785 chromatin', 'GO:0005654 nucleoplasm', 'GO:0005634 nucleus', 'GO:0090575 RNA polymerase II transcription regulator complex', 'GO:0003677 DNA binding', 'GO:0003700 DNA-binding transcription factor activity', 'GO:0000981 DNA-binding transcription factor activity, RNA polymerase II-specific', 'GO:0001227 DNA-binding transcription repressor activity, RNA polymerase II-specific', 'GO:0070539 linoleic acid binding', 'GO:0008289 lipid binding', 'GO:0051059 NF-kappaB binding', 'GO:0004879 nuclear receptor activity', 'GO:0003707 nuclear steroid receptor activity', 'GO:0000978 RNA polymerase II cis-regulatory region sequence-specific DNA binding', 'GO:1990837 sequence-specific double-stranded DNA binding', 'GO:0001223 transcription coactivator binding', 'GO:0008270 zinc ion binding', 'GO:0006915 apoptotic process', 'GO:0097190 apoptotic signaling pathway', 'GO:0008366 axon ensheathment', 'GO:0030154 cell differentiation', 'GO:0008283 cell population proliferation', 'GO:0071222 cellular response to lipopolysaccharide', 'GO:0031669 cellular response to nutrient levels', 'GO:0008203 cholesterol metabolic process', 'GO:1904659 D-glucose transmembrane transport', 'GO:0046697 decidualization', 'GO:0007566 embryo implantation', 'GO:0097009 energy homeostasis', 'GO:0006635 fatty acid beta-oxidation', 'GO:0009062 fatty acid catabolic process', 'GO:0006631 fatty acid metabolic process', 'GO:0015908 fatty acid transport', 'GO:0006091 generation of precursor metabolites and energy', 'GO:0006006 glucose metabolic process', 'GO:0007507 heart development', 'GO:0009755 hormone-mediated signaling pathway', 'GO:0030522 intracellular receptor signaling pathway', 'GO:0006629 lipid metabolic process', 'GO:0043066 negative regulation of apoptotic process', 'GO:0030308 negative regulation of cell growth', 'GO:0010887 negative regulation of cholesterol storage', 'GO:0032966 negative regulation of collagen biosynthetic process', 'GO:0045892 negative regulation of DNA-templated transcription', 'GO:0050728 negative regulation of inflammatory response', 'GO:1902894 negative regulation of miRNA transcription', 'GO:0045662 negative regulation of myoblast differentiation', 'GO:0014912 negative regulation of smooth muscle cell migration', 'GO:0048662 negative regulation of smooth muscle cell proliferation', 'GO:0000122 negative regulation of transcription by RNA polymerase II', 'GO:0008654 phospholipid biosynthetic process', 'GO:0045893 positive regulation of DNA-templated transcription', 'GO:0045684 positive regulation of epidermis development', 'GO:0045600 positive regulation of fat cell differentiation', 'GO:0045923 positive regulation of fatty acid metabolic process', 'GO:0046321 positive regulation of fatty acid oxidation', 'GO:0010628 positive regulation of gene expression', 'GO:0035774 positive regulation of insulin secretion involved in cellular response to glucose stimulus', 'GO:2000288 positive regulation of myoblast proliferation', 'GO:0043415 positive regulation of skeletal muscle tissue regeneration', 'GO:0045944 positive regulation of transcription by RNA polymerase II', 'GO:0006029 proteoglycan metabolic process', 'GO:0014842 regulation of skeletal muscle satellite cell proliferation', 'GO:0006357 regulation of transcription by RNA polymerase II', 'GO:0014823 response to activity', 'GO:0009749 response to glucose', 'GO:0033189 response to vitamin A', 'GO:0042311 vasodilation'],
        protein_diseases=[],
        method="ChEMBL", score=5.13, source_ref="ChEMBL ID: CHEMBL82293"
    ),
    slot(
        uniprot_id="P18031", protein_name="Tyrosine-protein phosphatase non-receptor type 1", protein_acronym="PTPN1",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Expressed in keratinocytes (at protein level)'],
        best_structure="AlphaFold:AF-P18031-F1", other_structures=[],
        go_terms=['GO:0005737 cytoplasm', 'GO:0098554 cytoplasmic side of endoplasmic reticulum membrane', 'GO:0005829 cytosol', 'GO:0005769 early endosome', 'GO:0005783 endoplasmic reticulum', 'GO:0005789 endoplasmic reticulum membrane', 'GO:0031904 endosome lumen', 'GO:0098978 glutamatergic synapse', 'GO:0030061 mitochondrial crista', 'GO:0005759 mitochondrial matrix', 'GO:0098794 postsynapse', 'GO:0032991 protein-containing complex', 'GO:0097443 sorting endosome', 'GO:0045296 cadherin binding', 'GO:0019899 enzyme binding', 'GO:0046875 ephrin receptor binding', 'GO:0005158 insulin receptor binding', 'GO:0004726 non-membrane spanning protein tyrosine phosphatase activity', 'GO:0004721 phosphoprotein phosphatase activity', 'GO:0019901 protein kinase binding', 'GO:0051721 protein phosphatase 2A binding', 'GO:0004725 protein tyrosine phosphatase activity', 'GO:0030971 receptor tyrosine kinase binding', 'GO:0003723 RNA binding', 'GO:0008270 zinc ion binding', 'GO:0030036 actin cytoskeleton organization', 'GO:1904385 cellular response to angiotensin', 'GO:0044344 cellular response to fibroblast growth factor stimulus', 'GO:0071456 cellular response to hypoxia', 'GO:0032869 cellular response to insulin stimulus', 'GO:1990090 cellular response to nerve growth factor stimulus', 'GO:0071732 cellular response to nitric oxide', 'GO:0036120 cellular response to platelet-derived growth factor stimulus', 'GO:0034620 cellular response to unfolded protein', 'GO:0030968 endoplasmic reticulum unfolded protein response', 'GO:0060397 growth hormone receptor signaling pathway via JAK-STAT', 'GO:0038020 insulin receptor recycling', 'GO:0036498 IRE1-mediated unfolded protein response', 'GO:0008285 negative regulation of cell population proliferation', 'GO:0010812 negative regulation of cell-substrate adhesion', 'GO:1902236 negative regulation of endoplasmic reticulum stress-induced intrinsic apoptotic signaling pathway', 'GO:0070373 negative regulation of ERK1 and ERK2 cascade', 'GO:0046627 negative regulation of insulin receptor signaling pathway', 'GO:0043407 negative regulation of MAP kinase activity', 'GO:0010977 negative regulation of neuron projection development', 'GO:1903898 negative regulation of PERK-mediated unfolded protein response', 'GO:0051898 negative regulation of phosphatidylinositol 3-kinase/protein kinase B signal transduction', 'GO:0009968 negative regulation of signal transduction', 'GO:1904753 negative regulation of vascular associated smooth muscle cell migration', 'GO:0030948 negative regulation of vascular endothelial growth factor receptor signaling pathway', 'GO:0035335 peptidyl-tyrosine dephosphorylation', 'GO:0035791 platelet-derived growth factor receptor-beta signaling pathway', 'GO:0010666 positive regulation of cardiac muscle cell apoptotic process', 'GO:2000353 positive regulation of endothelial cell apoptotic process', 'GO:0010460 positive regulation of heart rate', 'GO:1903896 positive regulation of IRE1-mediated unfolded protein response', 'GO:0046330 positive regulation of JNK cascade', 'GO:2000646 positive regulation of receptor catabolic process', 'GO:0003084 positive regulation of systemic arterial blood pressure', 'GO:0030100 regulation of endocytosis', 'GO:1902202 regulation of hepatocyte growth factor receptor signaling pathway', 'GO:0033157 regulation of intracellular protein transport', 'GO:0150052 regulation of postsynapse assembly', 'GO:0030162 regulation of proteolysis', 'GO:0009966 regulation of signal transduction', 'GO:0060338 regulation of type I interferon-mediated signaling pathway', 'GO:0031667 response to nutrient levels', 'GO:0097706 vascular endothelial cell response to oscillatory fluid shear stress'],
        protein_diseases=[],
        method="ChEMBL", score=5.06, source_ref="ChEMBL ID: CHEMBL82293"
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
