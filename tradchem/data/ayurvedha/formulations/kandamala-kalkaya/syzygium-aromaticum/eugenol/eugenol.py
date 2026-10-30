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
    "chemical_name": "Eugenol",
    "smiles": "C=CCc1ccc(O)c(OC)c1",
    "pubchem_cid": "3314",
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
        uniprot_id="P08684", protein_name="Cytochrome P450 3A4", protein_acronym="CYP3A4",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Expressed in prostate and liver. According to some authors, it is not expressed in brain (PubMed:19094056). According to others, weak levels of expression are measured in some brain locations (PubMed:18545703, PubMed:19359404). Also expressed in epithelium of the small intestine and large intestine, bile duct, nasal mucosa, kidney, adrenal cortex, epithelium of the gastric mucosa with intestinal metaplasia, gallbladder, intercalated ducts of the pancreas, chief cells of the parathyroid and the corpus luteum of the ovary (at protein level)'],
        best_structure="AlphaFold:AF-P08684-F1", other_structures=[],
        go_terms=['GO:0005737 cytoplasm', 'GO:0005789 endoplasmic reticulum membrane', 'GO:0043231 intracellular membrane-bounded organelle', 'GO:0102320 1,8-cineole 2-exo-monooxygenase activity', 'GO:0062181 1-alpha,25-dihydroxyvitamin D3 23-hydroxylase activity', 'GO:0062188 anandamide 11,12 epoxidase activity', 'GO:0062189 anandamide 14,15 epoxidase activity', 'GO:0062187 anandamide 8,9 epoxidase activity', 'GO:0008404 arachidonate 14,15-epoxygenase activity', 'GO:0034875 caffeine oxidase activity', 'GO:0019899 enzyme binding', 'GO:0101020 estrogen 16-alpha-hydroxylase activity', 'GO:0101021 estrogen 2-hydroxylase activity', 'GO:0020037 heme binding', 'GO:0005506 iron ion binding', 'GO:0004497 monooxygenase activity', 'GO:0016491 oxidoreductase activity', 'GO:0016712 oxidoreductase activity, acting on paired donors, with incorporation or reduction of molecular oxygen, reduced flavin or flavoprotein as one donor, and incorporation of one atom of oxygen', 'GO:0019825 oxygen binding', 'GO:0050591 quinine 3-monooxygenase activity', 'GO:0008401 retinoic acid 4-hydroxylase activity', 'GO:0005496 steroid binding', 'GO:0008395 steroid hydroxylase activity', 'GO:0050649 testosterone 6-beta-hydroxylase activity', 'GO:0070576 vitamin D 24-hydroxylase activity', 'GO:0030343 vitamin D 25-hydroxylase activity', 'GO:0046222 aflatoxin metabolic process', 'GO:0009822 alkaloid catabolic process', 'GO:0008203 cholesterol metabolic process', 'GO:0008210 estrogen metabolic process', 'GO:0002933 lipid hydroxylation', 'GO:0006629 lipid metabolic process', 'GO:0042759 long-chain fatty acid biosynthetic process', 'GO:0016098 monoterpenoid metabolic process', 'GO:0070989 oxidative demethylation', 'GO:0042573 retinoic acid metabolic process', 'GO:0042572 retinol metabolic process', 'GO:0006706 steroid catabolic process', 'GO:0008202 steroid metabolic process', 'GO:0042369 vitamin D catabolic process', 'GO:0042359 vitamin D metabolic process', 'GO:0042178 xenobiotic catabolic process', 'GO:0006805 xenobiotic metabolic process'],
        protein_diseases=['Vitamin D-dependent rickets 3'],
        method="ChEMBL", score=5.4, source_ref="ChEMBL ID: CHEMBL42710"
    ),
    slot(
        uniprot_id="P23219", protein_name="Prostaglandin G/H synthase 1", protein_acronym="PTGS1",
        species="Homo sapiens", taxon_id=9606,
        cell_types=[],
        best_structure="AlphaFold:AF-P23219-F1", other_structures=[],
        go_terms=['GO:0005737 cytoplasm', 'GO:0005788 endoplasmic reticulum lumen', 'GO:0005789 endoplasmic reticulum membrane', 'GO:0070062 extracellular exosome', 'GO:0043005 neuron projection', 'GO:0001750 photoreceptor outer segment', 'GO:0020037 heme binding', 'GO:0004601 peroxidase activity', 'GO:0004666 prostaglandin-endoperoxide synthase activity', 'GO:0019371 cyclooxygenase pathway', 'GO:0001516 prostaglandin biosynthetic process', 'GO:0008217 regulation of blood pressure', 'GO:0006979 response to oxidative stress'],
        protein_diseases=[],
        method="ChEMBL", score=4.96, source_ref="ChEMBL ID: CHEMBL42710"
    ),
    slot(
        uniprot_id="P00352", protein_name="Aldehyde dehydrogenase 1A1", protein_acronym="ALDH1A1",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Expressed by erythrocytes (at protein level)'],
        best_structure="AlphaFold:AF-P00352-F1", other_structures=[],
        go_terms=['GO:0030424 axon', 'GO:0005737 cytoplasm', 'GO:0005829 cytosol', 'GO:0070062 extracellular exosome', 'GO:0045202 synapse', 'GO:0106373 3-deoxyglucosone dehydrogenase activity', 'GO:0140087 acetaldehyde dehydrogenase (NAD+) activity', 'GO:0004029 aldehyde dehydrogenase (NAD+) activity', 'GO:0019145 aminobutyraldehyde dehydrogenase (NAD+) activity', 'GO:0005497 androgen binding', 'GO:0018479 benzaldehyde dehydrogenase (NAD+) activity', 'GO:0005096 GTPase activator activity', 'GO:0052814 medium-chain fatty aldehyde dehydrogenase (NAD+) activity', 'GO:0051287 NAD binding', 'GO:0070403 NAD+ binding', 'GO:0001758 retinal dehydrogenase (NAD+) activity', 'GO:0042904 9-cis-retinoic acid biosynthetic process', 'GO:0006081 aldehyde metabolic process', 'GO:0110095 cellular detoxification of aldehyde', 'GO:0030392 fructosamine catabolic process', 'GO:0006540 GABA shunt', 'GO:0036438 maintenance of lens transparency', 'GO:0120163 negative regulation of cold-induced thermogenesis', 'GO:0001523 retinoid metabolic process', 'GO:0042572 retinol metabolic process'],
        protein_diseases=[],
        method="ChEMBL", score=4.85, source_ref="ChEMBL ID: CHEMBL42710"
    ),
    slot(
        uniprot_id="P10275", protein_name="Androgen receptor", protein_acronym="AR",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Mainly expressed in heart and skeletal muscle', 'Expressed in basal and stromal cells of the prostate (at protein level)'],
        best_structure="AlphaFold:AF-P10275-F1", other_structures=[],
        go_terms=['GO:0000785 chromatin', 'GO:0005737 cytoplasm', 'GO:0005829 cytosol', 'GO:0016607 nuclear speck', 'GO:0005654 nucleoplasm', 'GO:0005634 nucleus', 'GO:0005886 plasma membrane', 'GO:0032991 protein-containing complex', 'GO:0017053 transcription repressor complex', 'GO:0005497 androgen binding', 'GO:0051117 ATPase binding', 'GO:0008013 beta-catenin binding', 'GO:0003682 chromatin binding', 'GO:0001228 DNA-binding transcription activator activity, RNA polymerase II-specific', 'GO:0003700 DNA-binding transcription factor activity', 'GO:0000981 DNA-binding transcription factor activity, RNA polymerase II-specific', 'GO:0019899 enzyme binding', 'GO:0034056 estrogen response element binding', 'GO:0060090 molecular adaptor activity', 'GO:0140693 molecular condensate scaffold activity', 'GO:0004879 nuclear receptor activity', 'GO:0003707 nuclear steroid receptor activity', 'GO:0070974 POU domain binding', 'GO:0000978 RNA polymerase II cis-regulatory region sequence-specific DNA binding', 'GO:0000979 RNA polymerase II core promoter sequence-specific DNA binding', 'GO:0001091 RNA polymerase II general transcription initiation factor binding', 'GO:0000977 RNA polymerase II transcription regulatory region sequence-specific DNA binding', 'GO:0061629 RNA polymerase II-specific DNA-binding transcription factor binding', 'GO:0005102 signaling receptor binding', 'GO:0005496 steroid binding', 'GO:0000976 transcription cis-regulatory region binding', 'GO:0001223 transcription coactivator binding', 'GO:0008270 zinc ion binding', 'GO:0030521 androgen receptor signaling pathway', 'GO:0007267 cell-cell signaling', 'GO:0071391 cellular response to estrogen stimulus', 'GO:0071383 cellular response to steroid hormone stimulus', 'GO:0071394 cellular response to testosterone stimulus', 'GO:0030520 estrogen receptor signaling pathway', 'GO:0030522 intracellular receptor signaling pathway', 'GO:0008584 male gonad development', 'GO:0140694 membraneless organelle assembly', 'GO:0008285 negative regulation of cell population proliferation', 'GO:2001237 negative regulation of extrinsic apoptotic signaling pathway', 'GO:0000122 negative regulation of transcription by RNA polymerase II', 'GO:0045597 positive regulation of cell differentiation', 'GO:0008284 positive regulation of cell population proliferation', 'GO:0045893 positive regulation of DNA-templated transcription', 'GO:0010628 positive regulation of gene expression', 'GO:0045726 positive regulation of integrin biosynthetic process', 'GO:1902895 positive regulation of miRNA transcription', 'GO:0045944 positive regulation of transcription by RNA polymerase II', 'GO:0045945 positive regulation of transcription by RNA polymerase III', 'GO:1903076 regulation of protein localization to plasma membrane', 'GO:0033574 response to testosterone', 'GO:0007165 signal transduction', 'GO:0007283 spermatogenesis'],
        protein_diseases=['Androgen insensitivity syndrome', 'Spinal and bulbar muscular atrophy X-linked 1', 'Prostate cancer, hereditary, X-linked 3', 'Androgen insensitivity, partial', 'Hypospadias 1, X-linked'],
        method="ChEMBL", score=4.72, source_ref="ChEMBL ID: CHEMBL42710"
    ),
    slot(
        uniprot_id="P09917", protein_name="Polyunsaturated fatty acid 5-lipoxygenase", protein_acronym="ALOX5",
        species="Homo sapiens", taxon_id=9606,
        cell_types=[],
        best_structure="AlphaFold:AF-P09917-F1", other_structures=[],
        go_terms=['GO:0005737 cytoplasm', 'GO:0005829 cytosol', 'GO:0005576 extracellular region', 'GO:1904813 ficolin-1-rich granule lumen', 'GO:0005635 nuclear envelope', 'GO:0005641 nuclear envelope lumen', 'GO:0016363 nuclear matrix', 'GO:0031965 nuclear membrane', 'GO:0005654 nucleoplasm', 'GO:0048471 perinuclear region of cytoplasm', 'GO:0034774 secretory granule lumen', 'GO:0004052 arachidonate 12(S)-lipoxygenase activity', 'GO:0004051 arachidonate 5-lipoxygenase activity', 'GO:0036403 arachidonate 8(S)-lipoxygenase activity', 'GO:0005506 iron ion binding', 'GO:0016491 oxidoreductase activity', 'GO:0016701 oxidoreductase activity, acting on single donors with incorporation of molecular oxygen', 'GO:0019369 arachidonate metabolic process', 'GO:0036336 dendritic cell migration', 'GO:0042593 glucose homeostasis', 'GO:0006959 humoral immune response', 'GO:0002232 leukocyte chemotaxis involved in inflammatory response', 'GO:0002523 leukocyte migration involved in inflammatory response', 'GO:1901753 leukotriene A4 biosynthetic process', 'GO:0019370 leukotriene biosynthetic process', 'GO:0006691 leukotriene metabolic process', 'GO:0034440 lipid oxidation', 'GO:2001301 lipoxin biosynthetic process', 'GO:0019372 lipoxygenase pathway', 'GO:0042759 long-chain fatty acid biosynthetic process', 'GO:0016525 negative regulation of angiogenesis', 'GO:0001937 negative regulation of endothelial cell proliferation', 'GO:0050728 negative regulation of inflammatory response', 'GO:1903573 negative regulation of response to endoplasmic reticulum stress', 'GO:1903671 negative regulation of sprouting angiogenesis', 'GO:0061044 negative regulation of vascular wound healing', 'GO:0061045 negative regulation of wound healing', 'GO:0030501 positive regulation of bone mineralization', 'GO:1904999 positive regulation of leukocyte adhesion to arterial endothelial cell', 'GO:1900407 regulation of cellular response to oxidative stress', 'GO:1900015 regulation of cytokine production involved in inflammatory response', 'GO:0045598 regulation of fat cell differentiation', 'GO:0050727 regulation of inflammatory response', 'GO:0106014 regulation of inflammatory response to wounding', 'GO:0050796 regulation of insulin secretion', 'GO:1903426 regulation of reactive oxygen species biosynthetic process'],
        protein_diseases=[],
        method="ChEMBL", score=4.58, source_ref="ChEMBL ID: CHEMBL42710"
    ),
    slot(
        uniprot_id="Q7Z2W7", protein_name="Transient receptor potential cation channel subfamily M member 8", protein_acronym="TRPM8",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Expressed in prostate. Also expressed in prostate tumors and in non-prostatic primary tumors such as colon, lung, breast and skin tumors'],
        best_structure="AlphaFold:AF-Q7Z2W7-F1", other_structures=[],
        go_terms=['GO:0005789 endoplasmic reticulum membrane', 'GO:0009897 external side of plasma membrane', 'GO:0045121 membrane raft', 'GO:0005886 plasma membrane', 'GO:0044853 plasma membrane raft', 'GO:0005262 calcium channel activity', 'GO:0042802 identical protein binding', 'GO:0099604 ligand-gated calcium channel activity', 'GO:0070588 calcium ion transmembrane transport', 'GO:0120162 positive regulation of cold-induced thermogenesis', 'GO:0009409 response to cold', 'GO:0050955 thermoception'],
        protein_diseases=[],
        method="ChEMBL", score=4.18, source_ref="ChEMBL ID: CHEMBL42710"
    ),
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
