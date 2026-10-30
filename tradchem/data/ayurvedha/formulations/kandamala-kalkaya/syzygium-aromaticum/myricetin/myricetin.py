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
    "chemical_name": "Myricetin",
    "smiles": "O=c1c(O)c(-c2cc(O)c(O)c(O)c2)oc2cc(O)cc(O)c12",
    "pubchem_cid": "5281672",
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
        uniprot_id="Q9NR56", protein_name="Muscleblind-like protein 1", protein_acronym="MBNL1",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Highly expressed in cardiac, skeletal muscle and during myoblast differentiation. Weakly expressed in other tissues (at protein level). Expressed in heart, brain, placenta, lung, liver, skeletal muscle, kidney and pancreas'],
        best_structure="AlphaFold:AF-Q9NR56-F1", other_structures=[],
        go_terms=['GO:0005737 cytoplasm', 'GO:0010494 cytoplasmic stress granule', 'GO:0005829 cytosol', 'GO:0005654 nucleoplasm', 'GO:0005634 nucleus', 'GO:0003725 double-stranded RNA binding', 'GO:0046872 metal ion binding', 'GO:0003723 RNA binding', 'GO:0030326 embryonic limb morphogenesis', 'GO:0001701 in utero embryonic development', 'GO:0045445 myoblast differentiation', 'GO:0007399 nervous system development', 'GO:0043484 regulation of RNA splicing', 'GO:0008380 RNA splicing'],
        protein_diseases=['Dystrophia myotonica 1', 'Corneal dystrophy, Fuchs endothelial, 3'],
        method="ChEMBL", score=9.6, source_ref="ChEMBL ID: CHEMBL164"
    ),
    slot(
        uniprot_id="P14618", protein_name="Pyruvate kinase PKM", protein_acronym="PKM",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Specifically expressed in proliferating cells, such as embryonic stem cells, embryonic carcinoma cells, as well as cancer cells', 'Expressed in adult tissues (PubMed:18337823). Not expressed in tumor cells (PubMed:18337823)'],
        best_structure="AlphaFold:AF-P14618-F1", other_structures=[],
        go_terms=['GO:0005929 cilium', 'GO:0005737 cytoplasm', 'GO:0005829 cytosol', 'GO:0070062 extracellular exosome', 'GO:0005576 extracellular region', 'GO:1903561 extracellular vesicle', 'GO:1904813 ficolin-1-rich granule lumen', 'GO:0005739 mitochondrion', 'GO:0005654 nucleoplasm', 'GO:0005634 nucleus', 'GO:0005791 rough endoplasmic reticulum', 'GO:0034774 secretory granule lumen', 'GO:0031982 vesicle', 'GO:0045296 cadherin binding', 'GO:0035402 histone H3T11 kinase activity', 'GO:0000287 magnesium ion binding', 'GO:0023026 MHC class II protein complex binding', 'GO:0003729 mRNA binding', 'GO:0004715 non-membrane spanning protein tyrosine kinase activity', 'GO:0030955 potassium ion binding', 'GO:0042803 protein homodimerization activity', 'GO:0004674 protein serine/threonine kinase activity', 'GO:0004713 protein tyrosine kinase activity', 'GO:0004743 pyruvate kinase activity', 'GO:0003723 RNA binding', 'GO:0003713 transcription coactivator activity', 'GO:0061621 canonical glycolysis', 'GO:0032869 cellular response to insulin stimulus', 'GO:0006096 glycolytic process', 'GO:2000767 positive regulation of cytoplasmic translation', 'GO:1903672 positive regulation of sprouting angiogenesis', 'GO:0045944 positive regulation of transcription by RNA polymerase II', 'GO:0012501 programmed cell death', 'GO:0042866 pyruvate biosynthetic process'],
        protein_diseases=[],
        method="ChEMBL", score=9.29, source_ref="ChEMBL ID: CHEMBL164"
    ),
    slot(
        uniprot_id="P22303", protein_name="Acetylcholinesterase", protein_acronym="ACHE",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Isoform H is highly expressed in erythrocytes'],
        best_structure="AlphaFold:AF-P22303-F1", other_structures=[],
        go_terms=['GO:0005604 basement membrane', 'GO:0009986 cell surface', 'GO:0005576 extracellular region', 'GO:0005794 Golgi apparatus', 'GO:0016020 membrane', 'GO:0031594 neuromuscular junction', 'GO:0005634 nucleus', 'GO:0048471 perinuclear region of cytoplasm', 'GO:0005886 plasma membrane', 'GO:0045202 synapse', 'GO:0043083 synaptic cleft', 'GO:0042166 acetylcholine binding', 'GO:0003990 acetylcholinesterase activity', 'GO:0001540 amyloid-beta binding', 'GO:0004104 cholinesterase activity', 'GO:0005518 collagen binding', 'GO:0016787 hydrolase activity', 'GO:0043236 laminin binding', 'GO:0042803 protein homodimerization activity', 'GO:0017171 serine hydrolase activity', 'GO:0006581 acetylcholine catabolic process', 'GO:0001507 acetylcholine catabolic process in synaptic cleft', 'GO:0042982 amyloid precursor protein metabolic process', 'GO:0007155 cell adhesion', 'GO:0032223 negative regulation of synaptic transmission, cholinergic', 'GO:0007399 nervous system development', 'GO:0002076 osteoblast development', 'GO:0120162 positive regulation of cold-induced thermogenesis', 'GO:0050714 positive regulation of protein secretion', 'GO:0007416 synapse assembly'],
        protein_diseases=[],
        method="ChEMBL", score=7.92, source_ref="ChEMBL ID: CHEMBL164"
    ),
    slot(
        uniprot_id="Q16678", protein_name="Cytochrome P450 1B1", protein_acronym="CYP1B1",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Expressed in heart, brain, lung, skeletal muscle, kidney, spleen, thymus, prostate, testis, ovary, small intestine, colon, and peripheral blood leukocytes (PubMed:8175734). Expressed in retinal endothelial cells and umbilical vein endothelial cells (at protein level) (PubMed:19005183)'],
        best_structure="AlphaFold:AF-Q16678-F1", other_structures=[],
        go_terms=['GO:0005789 endoplasmic reticulum membrane', 'GO:0005739 mitochondrion', 'GO:0008405 arachidonate 11,12-epoxygenase activity', 'GO:0008404 arachidonate 14,15-epoxygenase activity', 'GO:0106302 arachidonate 8,9-epoxygenase activity', 'GO:0101020 estrogen 16-alpha-hydroxylase activity', 'GO:0101021 estrogen 2-hydroxylase activity', 'GO:0020037 heme binding', 'GO:0106256 hydroperoxy icosatetraenoate dehydratase activity', 'GO:0005506 iron ion binding', 'GO:0004497 monooxygenase activity', 'GO:0016709 oxidoreductase activity, acting on paired donors, with incorporation or reduction of molecular oxygen, NAD(P)H as one donor, and incorporation of one atom of oxygen', 'GO:0016712 oxidoreductase activity, acting on paired donors, with incorporation or reduction of molecular oxygen, reduced flavin or flavoprotein as one donor, and incorporation of one atom of oxygen', 'GO:0008395 steroid hydroxylase activity', 'GO:0050649 testosterone 6-beta-hydroxylase activity', 'GO:0019369 arachidonate metabolic process', 'GO:0048514 blood vessel morphogenesis', 'GO:0007155 cell adhesion', 'GO:0070301 cellular response to hydrogen peroxide', 'GO:0030199 collagen fibril organization', 'GO:0043542 endothelial cell migration', 'GO:0019373 epoxygenase P450 pathway', 'GO:0008210 estrogen metabolic process', 'GO:0008631 intrinsic apoptotic signaling pathway in response to oxidative stress', 'GO:0016042 lipid catabolic process', 'GO:0033629 negative regulation of cell adhesion mediated by integrin', 'GO:0030336 negative regulation of cell migration', 'GO:0008285 negative regulation of cell population proliferation', 'GO:0006809 nitric oxide biosynthetic process', 'GO:0097267 omega-hydroxylase P450 pathway', 'GO:0045766 positive regulation of angiogenesis', 'GO:0043065 positive regulation of apoptotic process', 'GO:0046427 positive regulation of receptor signaling pathway via JAK-STAT', 'GO:0010575 positive regulation of vascular endothelial growth factor production', 'GO:2000377 regulation of reactive oxygen species metabolic process', 'GO:0061304 retinal blood vessel morphogenesis', 'GO:0042574 retinal metabolic process', 'GO:0042572 retinol metabolic process', 'GO:0006706 steroid catabolic process', 'GO:0008202 steroid metabolic process', 'GO:0016125 sterol metabolic process', 'GO:0009404 toxin metabolic process', 'GO:0002930 trabecular meshwork development', 'GO:0042178 xenobiotic catabolic process', 'GO:0006805 xenobiotic metabolic process'],
        protein_diseases=['Anterior segment dysgenesis 6', 'Glaucoma 3, primary congenital, A', 'Glaucoma 1, open angle, A'],
        method="ChEMBL", score=7.57, source_ref="ChEMBL ID: CHEMBL164"
    ),
    slot(
        uniprot_id="Q99714", protein_name="3-hydroxyacyl-CoA dehydrogenase type-2", protein_acronym="HSD17B10",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Ubiquitously expressed in normal tissues but is overexpressed in neurons affected in AD'],
        best_structure="AlphaFold:AF-Q99714-F1", other_structures=[],
        go_terms=['GO:1902494 catalytic complex', 'GO:0005737 cytoplasm', 'GO:1902555 endoribonuclease complex', 'GO:0005759 mitochondrial matrix', 'GO:0042645 mitochondrial nucleoid', 'GO:0030678 mitochondrial ribonuclease P complex', 'GO:0005739 mitochondrion', 'GO:0005886 plasma membrane', 'GO:0043527 tRNA methyltransferase complex', 'GO:0003857 (3S)-3-hydroxyacyl-CoA dehydrogenase (NAD+) activity', 'GO:0044594 17-beta-hydroxysteroid dehydrogenase (NAD+) activity', 'GO:0047015 3-hydroxy-2-methylbutyryl-CoA dehydrogenase activity', 'GO:0047044 androstan-3-alpha,17-beta-diol dehydrogenase (NAD+) activity', 'GO:0160241 cardiolipin dehydrogenase (NAD+) activity', 'GO:0106281 chenodeoxycholate 7-alpha-dehydrogenase (NAD+) activity', 'GO:0008709 cholate 7-alpha-dehydrogenase (NAD+) activity', 'GO:0004303 estradiol 17-beta-dehydrogenase [NAD(P)+] activity', 'GO:0106282 isoursodeoxycholate 7-beta-dehydrogenase (NAD+) activity', 'GO:0016509 long-chain (3S)-3-hydroxyacyl-CoA dehydrogenase (NAD+) activity', 'GO:0003723 RNA binding', 'GO:0047035 testosterone dehydrogenase (NAD+) activity', 'GO:0000049 tRNA binding', 'GO:0106283 ursodeoxycholate 7-beta-dehydrogenase (NAD+) activity', 'GO:0008209 androgen metabolic process', 'GO:0006699 bile acid biosynthetic process', 'GO:0062173 brexanolone metabolic process', 'GO:0008207 C21-steroid hormone metabolic process', 'GO:0008210 estrogen metabolic process', 'GO:0006635 fatty acid beta-oxidation', 'GO:0006631 fatty acid metabolic process', 'GO:0006550 L-isoleucine catabolic process', 'GO:0006629 lipid metabolic process', "GO:1990180 mitochondrial tRNA 3'-end processing", "GO:0097745 mitochondrial tRNA 5'-end processing", 'GO:0070901 mitochondrial tRNA methylation', 'GO:0007005 mitochondrion organization', 'GO:0051289 protein homotetramerization', "GO:0042780 tRNA 3'-end processing", "GO:0001680 tRNA 3'-terminal CCA addition"],
        protein_diseases=['HSD10 mitochondrial disease'],
        method="ChEMBL", score=6.9, source_ref="ChEMBL ID: CHEMBL164"
    ),
    slot(
        uniprot_id="Q9NUW8", protein_name="Tyrosyl-DNA phosphodiesterase 1", protein_acronym="TDP1",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Ubiquitously expressed. Similar expression throughout the central nervous system (whole brain, amygdala, caudate nucleus, cerebellum, cerebral cortex, frontal lobe, hippocampus, medulla oblongata, occipital lobe, putamen, substantia nigra, temporal lobe, thalamus, nucleus accumbens and spinal cord) and increased expression in testis and thymus'],
        best_structure="AlphaFold:AF-Q9NUW8-F1", other_structures=[],
        go_terms=['GO:0005737 cytoplasm', 'GO:0070421 DNA ligase III-XRCC1 complex', 'GO:0005654 nucleoplasm', 'GO:0005634 nucleus', 'GO:0090734 site of DNA damage', "GO:0017005 3'-tyrosyl-DNA phosphodiesterase activity", 'GO:0003690 double-stranded DNA binding', 'GO:0003697 single-stranded DNA binding', 'GO:0006281 DNA repair', 'GO:0006302 double-strand break repair', 'GO:0006282 regulation of DNA repair', 'GO:0000012 single strand break repair'],
        protein_diseases=['Spinocerebellar ataxia, autosomal recessive, with axonal neuropathy 1'],
        method="ChEMBL", score=6.8, source_ref="ChEMBL ID: CHEMBL164"
    ),
    slot(
        uniprot_id="P42336", protein_name="Phosphatidylinositol 4,5-bisphosphate 3-kinase catalytic subunit alpha isoform", protein_acronym="PIK3CA",
        species="Homo sapiens", taxon_id=9606,
        cell_types=[],
        best_structure="AlphaFold:AF-P42336-F1", other_structures=[],
        go_terms=['GO:0005829 cytosol', 'GO:0014704 intercalated disc', 'GO:0030027 lamellipodium', 'GO:0048471 perinuclear region of cytoplasm', 'GO:0005942 phosphatidylinositol 3-kinase complex', 'GO:0005943 phosphatidylinositol 3-kinase complex, class IA', 'GO:0005944 phosphatidylinositol 3-kinase complex, class IB', 'GO:0005886 plasma membrane', 'GO:0016303 1-phosphatidylinositol-3-kinase activity', 'GO:0046934 1-phosphatidylinositol-4,5-bisphosphate 3-kinase activity', 'GO:0035005 1-phosphatidylinositol-4-phosphate 3-kinase activity', 'GO:0043560 insulin receptor substrate binding', 'GO:0030295 protein kinase activator activity', 'GO:0106310 protein serine kinase activity', 'GO:0004674 protein serine/threonine kinase activity', 'GO:0030036 actin cytoskeleton organization', 'GO:0043276 anoikis', 'GO:0086003 cardiac muscle cell contraction', 'GO:0060048 cardiac muscle contraction', 'GO:0016477 cell migration', 'GO:0071464 cellular response to hydrostatic pressure', 'GO:0032869 cellular response to insulin stimulus', 'GO:0043542 endothelial cell migration', 'GO:0007173 epidermal growth factor receptor signaling pathway', 'GO:0008286 insulin receptor signaling pathway', 'GO:0048009 insulin-like growth factor receptor signaling pathway', 'GO:0030835 negative regulation of actin filament depolymerization', 'GO:2000811 negative regulation of anoikis', 'GO:0010629 negative regulation of gene expression', 'GO:0016242 negative regulation of macroautophagy', 'GO:0043491 phosphatidylinositol 3-kinase/protein kinase B signal transduction', 'GO:0046854 phosphatidylinositol phosphate biosynthetic process', 'GO:0036092 phosphatidylinositol-3-phosphate biosynthetic process', 'GO:0048015 phosphatidylinositol-mediated signaling', 'GO:0030168 platelet activation', 'GO:0010592 positive regulation of lamellipodium assembly', 'GO:0051897 positive regulation of phosphatidylinositol 3-kinase/protein kinase B signal transduction', 'GO:0045860 positive regulation of protein kinase activity', 'GO:1905477 positive regulation of protein localization to membrane', 'GO:0048661 positive regulation of smooth muscle cell proliferation', 'GO:0032008 positive regulation of TOR signaling', 'GO:0110053 regulation of actin filament organization', 'GO:0055119 relaxation of cardiac muscle', 'GO:0014823 response to activity', 'GO:1903544 response to butyrate', 'GO:0071548 response to dexamethasone', 'GO:0043201 response to L-leucine', 'GO:0014870 response to muscle inactivity', 'GO:0035994 response to muscle stretch', 'GO:0050852 T cell receptor signaling pathway', 'GO:0038203 TORC2 signaling', 'GO:0038084 vascular endothelial growth factor signaling pathway', 'GO:0001944 vasculature development'],
        protein_diseases=['Colorectal cancer', 'Breast cancer', 'Ovarian cancer', 'Hepatocellular carcinoma', 'Keratosis, seborrheic', 'Megalencephaly-capillary malformation-polymicrogyria syndrome', 'Congenital lipomatous overgrowth, vascular malformations, and epidermal nevi', 'Cowden syndrome 5', 'CLAPO syndrome', 'Macrodactyly', 'Cerebral cavernous malformations 4', 'Hemifacial myohyperplasia'],
        method="ChEMBL", score=6.77, source_ref="ChEMBL ID: CHEMBL164"
    ),
    slot(
        uniprot_id="P06746", protein_name="DNA polymerase beta", protein_acronym="POLB",
        species="Homo sapiens", taxon_id=9606,
        cell_types=[],
        best_structure="AlphaFold:AF-P06746-F1", other_structures=[],
        go_terms=['GO:0005737 cytoplasm', 'GO:0005829 cytosol', 'GO:0070421 DNA ligase III-XRCC1 complex', 'GO:0005874 microtubule', 'GO:0005654 nucleoplasm', 'GO:0005634 nucleus', 'GO:0032991 protein-containing complex', 'GO:0090734 site of DNA damage', 'GO:0005876 spindle microtubule', "GO:0051575 5'-deoxyribose-5-phosphate lyase activity", 'GO:0140078 class I DNA-(apurinic or apyrimidinic site) endonuclease activity', 'GO:0003684 damaged DNA binding', 'GO:0003906 DNA-(apurinic or apyrimidinic site) endonuclease activity', 'GO:0003887 DNA-directed DNA polymerase activity', 'GO:0019899 enzyme binding', 'GO:0016829 lyase activity', 'GO:0046872 metal ion binding', 'GO:0008017 microtubule binding', 'GO:0006284 base-excision repair', 'GO:0006287 base-excision repair, gap-filling', 'GO:0006974 DNA damage response', 'GO:0006281 DNA repair', 'GO:0006261 DNA-templated DNA replication', 'GO:0006290 pyrimidine dimer repair', 'GO:0006282 regulation of DNA repair', 'GO:0045471 response to ethanol', 'GO:0010332 response to gamma radiation', 'GO:0055093 response to hyperoxia'],
        protein_diseases=[],
        method="ChEMBL", score=6.7, source_ref="ChEMBL ID: CHEMBL164"
    ),
    slot(
        uniprot_id="P37840", protein_name="Alpha-synuclein", protein_acronym="SNCA",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Highly expressed in presynaptic terminals in the central nervous system. Expressed principally in brain'],
        best_structure="AlphaFold:AF-P37840-F1", other_structures=[],
        go_terms=['GO:0015629 actin cytoskeleton', 'GO:0030424 axon', 'GO:0043679 axon terminus', 'GO:0005938 cell cortex', 'GO:0005737 cytoplasm', 'GO:0005829 cytosol', 'GO:0005576 extracellular region', 'GO:0030426 growth cone', 'GO:0016234 inclusion body', 'GO:0097413 Lewy body', 'GO:0005764 lysosome', 'GO:0016020 membrane', 'GO:0005743 mitochondrial inner membrane', 'GO:0005759 mitochondrial matrix', 'GO:0005741 mitochondrial outer membrane', 'GO:0005739 mitochondrion', 'GO:0043025 neuronal cell body', 'GO:0005640 nuclear outer membrane', 'GO:0005634 nucleus', 'GO:0048471 perinuclear region of cytoplasm', 'GO:0005886 plasma membrane', 'GO:0032991 protein-containing complex', 'GO:0005840 ribosome', 'GO:0099512 supramolecular fiber', 'GO:0045202 synapse', 'GO:0030672 synaptic vesicle membrane', 'GO:0043195 terminal bouton', 'GO:0003779 actin binding', 'GO:0043014 alpha-tubulin binding', 'GO:0048487 beta-tubulin binding', 'GO:0005509 calcium ion binding', 'GO:0005507 copper ion binding', 'GO:1903136 cuprous ion binding', 'GO:0004869 cysteine-type endopeptidase inhibitor activity', 'GO:0070840 dynein complex binding', 'GO:0008047 enzyme activator activity', 'GO:0019899 enzyme binding', 'GO:0004857 enzyme inhibitor activity', 'GO:0008198 ferrous iron binding', 'GO:0042393 histone binding', 'GO:0030544 Hsp70 protein binding', 'GO:0042802 identical protein binding', 'GO:0019894 kinesin binding', 'GO:0008289 lipid binding', 'GO:0000287 magnesium ion binding', 'GO:0008017 microtubule binding', 'GO:0016491 oxidoreductase activity', 'GO:0043274 phospholipase binding', 'GO:0005543 phospholipid binding', 'GO:0051219 phosphoprotein binding', 'GO:0019904 protein domain specific binding', 'GO:0004860 protein kinase inhibitor activity', 'GO:0140311 protein sequestering activity', 'GO:0000149 SNARE binding', 'GO:0048156 tau protein binding', 'GO:0000976 transcription cis-regulatory region binding', 'GO:0141108 transporter regulator activity', 'GO:0015631 tubulin binding', 'GO:0008270 zinc ion binding', 'GO:1990000 amyloid fibril formation', 'GO:0048148 behavioral response to cocaine', 'GO:0071280 cellular response to copper ion', 'GO:0071872 cellular response to epinephrine stimulus', 'GO:0044344 cellular response to fibroblast growth factor stimulus', 'GO:0034599 cellular response to oxidative stress', 'GO:0042416 dopamine biosynthetic process', 'GO:0051583 dopamine uptake involved in synaptic transmission', 'GO:0006749 glutathione metabolic process', 'GO:0001774 microglial cell activation', 'GO:0043066 negative regulation of apoptotic process', 'GO:1904715 negative regulation of chaperone-mediated autophagy', 'GO:0045963 negative regulation of dopamine metabolic process', 'GO:0051585 negative regulation of dopamine uptake involved in synaptic transmission', 'GO:0045920 negative regulation of exocytosis', 'GO:0031115 negative regulation of microtubule polymerization', 'GO:1902957 negative regulation of mitochondrial electron transport, NADH to ubiquinone', 'GO:0043524 negative regulation of neuron apoptotic process', 'GO:0051622 negative regulation of norepinephrine uptake', 'GO:0010642 negative regulation of platelet-derived growth factor receptor signaling pathway', 'GO:0051612 negative regulation of serotonin uptake', 'GO:0070495 negative regulation of thrombin-activated receptor signaling pathway', 'GO:0000122 negative regulation of transcription by RNA polymerase II', 'GO:0043065 positive regulation of apoptotic process', 'GO:0045807 positive regulation of endocytosis', 'GO:0045921 positive regulation of exocytosis', 'GO:1903285 positive regulation of hydrogen peroxide catabolic process', 'GO:0050729 positive regulation of inflammatory response', 'GO:0060732 positive regulation of inositol phosphate biosynthetic process', 'GO:1904377 positive regulation of protein localization to cell periphery', 'GO:0001921 positive regulation of receptor recycling', 'GO:0051281 positive regulation of release of sequestered calcium ion into cytosol', 'GO:0035543 positive regulation of SNARE complex assembly', 'GO:0031648 protein destabilization', 'GO:0051262 protein tetramerization', 'GO:0031623 receptor internalization', 'GO:0014059 regulation of dopamine secretion', 'GO:0070507 regulation of microtubule cytoskeleton organization', 'GO:0051621 regulation of norepinephrine uptake', 'GO:1905606 regulation of presynapse assembly', 'GO:1903426 regulation of reactive oxygen species biosynthetic process', 'GO:1903421 regulation of synaptic vesicle recycling', 'GO:1904307 response to desipramine', 'GO:0070555 response to interleukin-1', 'GO:0010040 response to iron(II) ion', 'GO:0032496 response to lipopolysaccharide', 'GO:0032026 response to magnesium ion', 'GO:0034341 response to type II interferon', 'GO:0035493 SNARE complex assembly', 'GO:0097435 supramolecular fiber organization', 'GO:0050808 synapse organization', 'GO:0001963 synaptic transmission, dopaminergic', 'GO:0048488 synaptic vesicle endocytosis', 'GO:0016079 synaptic vesicle exocytosis', 'GO:0016082 synaptic vesicle priming', 'GO:0048489 synaptic vesicle transport'],
        protein_diseases=['Parkinson disease 1, autosomal dominant', 'Parkinson disease 4, autosomal dominant', 'Dementia, Lewy body'],
        method="ChEMBL", score=6.66, source_ref="ChEMBL ID: CHEMBL164"
    ),
    slot(
        uniprot_id="P27695", protein_name="DNA repair nuclease/redox regulator APEX1", protein_acronym="APEX1",
        species="Homo sapiens", taxon_id=9606,
        cell_types=[],
        best_structure="AlphaFold:AF-P27695-F1", other_structures=[],
        go_terms=['GO:0000785 chromatin', 'GO:0000781 chromosome, telomeric region', 'GO:0005737 cytoplasm', 'GO:0005783 endoplasmic reticulum', 'GO:0005739 mitochondrion', 'GO:0016607 nuclear speck', 'GO:0005730 nucleolus', 'GO:0005654 nucleoplasm', 'GO:0005634 nucleus', 'GO:0048471 perinuclear region of cytoplasm', 'GO:0005840 ribosome', "GO:0008408 3'-5' exonuclease activity", "GO:0008296 3'-5'-DNA exonuclease activity", 'GO:0031490 chromatin DNA binding', 'GO:0052720 class II DNA-(apurinic or apyrimidinic site) endonuclease activity', 'GO:0003684 damaged DNA binding', 'GO:0033892 deoxyribonuclease (pyrimidine dimer) activity', 'GO:0003677 DNA binding', 'GO:0004520 DNA endonuclease activity', 'GO:0140431 DNA-(abasic site) binding', 'GO:0003906 DNA-(apurinic or apyrimidinic site) endonuclease activity', "GO:0008311 double-stranded DNA 3'-5' DNA exonuclease activity", 'GO:0008309 double-stranded DNA exodeoxyribonuclease activity', 'GO:0003691 double-stranded telomeric DNA binding', 'GO:0004519 endonuclease activity', 'GO:0046872 metal ion binding', 'GO:0016491 oxidoreductase activity', "GO:0090580 phosphodiesterase activity, acting on 3'-phosphoglycolate-terminated DNA strands", 'GO:0004528 phosphodiesterase I activity', 'GO:0008081 phosphoric diester hydrolase activity', 'GO:0003723 RNA binding', 'GO:0004523 RNA-DNA hybrid ribonuclease activity', 'GO:0003713 transcription coactivator activity', 'GO:0003714 transcription corepressor activity', 'GO:0004844 uracil DNA N-glycosylase activity', 'GO:0006284 base-excision repair', 'GO:0006287 base-excision repair, gap-filling', 'GO:0006308 DNA catabolic process', 'GO:0006281 DNA repair', 'GO:0008626 granzyme-mediated apoptotic signaling pathway', 'GO:0044029 positive regulation of gene expression via chromosomal CpG island demethylation', 'GO:0045944 positive regulation of transcription by RNA polymerase II', 'GO:0042981 regulation of apoptotic process', 'GO:0043488 regulation of mRNA stability', 'GO:0000723 telomere maintenance', 'GO:0097698 telomere maintenance via base-excision repair'],
        protein_diseases=[],
        method="ChEMBL", score=6.5, source_ref="ChEMBL ID: CHEMBL164"
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
