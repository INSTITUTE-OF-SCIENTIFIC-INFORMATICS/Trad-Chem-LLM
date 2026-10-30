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
    "chemical_name": "Vanillin",
    "smiles": "COc1cc(C=O)ccc1O",
    "pubchem_cid": "1183",
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
        uniprot_id="O15164", protein_name="Transcription intermediary factor 1-alpha", protein_acronym="TRIM24",
        species="Homo sapiens", taxon_id=9606,
        cell_types=[],
        best_structure="AlphaFold:AF-O15164-F1", other_structures=[],
        go_terms=['GO:0000785 chromatin', 'GO:0005737 cytoplasm', 'GO:0005829 cytosol', 'GO:0000791 euchromatin', 'GO:0005739 mitochondrion', 'GO:0005654 nucleoplasm', 'GO:0005634 nucleus', 'GO:0005726 perichromatin fibrils', 'GO:0003682 chromatin binding', 'GO:0034056 estrogen response element binding', 'GO:0140118 histone H3K23ac reader activity', 'GO:0016922 nuclear receptor binding', 'GO:0002039 p53 binding', 'GO:0004672 protein kinase activity', 'GO:0005102 signaling receptor binding', 'GO:0003713 transcription coactivator activity', 'GO:0061630 ubiquitin protein ligase activity', 'GO:0008270 zinc ion binding', 'GO:0071391 cellular response to estrogen stimulus', 'GO:0030163 protein catabolic process', 'GO:0016567 protein ubiquitination', 'GO:0042981 regulation of apoptotic process', 'GO:0031647 regulation of protein stability', 'GO:0043434 response to peptide hormone', 'GO:0006366 transcription by RNA polymerase II'],
        protein_diseases=[],
        method="ChEMBL", score=6.79, source_ref="ChEMBL ID: CHEMBL13883"
    ),
    slot(
        uniprot_id="Q9UPN9", protein_name="E3 ubiquitin-protein ligase TRIM33", protein_acronym="TRIM33",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Expressed in stem cells at the bottom of the crypts of the colon (at protein level). Expressed in colon adenomas and adenocarcinomas (at protein level). Expressed in brain, lung, liver, spleen, thymus, prostate, kidney, testis, heart, placenta, pancreas, small intestine, ovary, colon, skeletal muscle and hematopoietic progenitors'],
        best_structure="AlphaFold:AF-Q9UPN9-F1", other_structures=[],
        go_terms=['GO:0000785 chromatin', 'GO:0005654 nucleoplasm', 'GO:0005634 nucleus', 'GO:0070410 co-SMAD binding', 'GO:0070412 R-SMAD binding', 'GO:0061630 ubiquitin protein ligase activity', 'GO:0004842 ubiquitin-protein transferase activity', 'GO:0008270 zinc ion binding', 'GO:0030514 negative regulation of BMP signaling pathway', 'GO:0045892 negative regulation of DNA-templated transcription', 'GO:0000122 negative regulation of transcription by RNA polymerase II', 'GO:0016567 protein ubiquitination', 'GO:0017015 regulation of transforming growth factor beta receptor signaling pathway'],
        protein_diseases=['Developmental dysplasia of the hip 4'],
        method="ChEMBL", score=6.49, source_ref="ChEMBL ID: CHEMBL13883"
    ),
    slot(
        uniprot_id="Q9NUW8", protein_name="Tyrosyl-DNA phosphodiesterase 1", protein_acronym="TDP1",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Ubiquitously expressed. Similar expression throughout the central nervous system (whole brain, amygdala, caudate nucleus, cerebellum, cerebral cortex, frontal lobe, hippocampus, medulla oblongata, occipital lobe, putamen, substantia nigra, temporal lobe, thalamus, nucleus accumbens and spinal cord) and increased expression in testis and thymus'],
        best_structure="AlphaFold:AF-Q9NUW8-F1", other_structures=[],
        go_terms=['GO:0005737 cytoplasm', 'GO:0070421 DNA ligase III-XRCC1 complex', 'GO:0005654 nucleoplasm', 'GO:0005634 nucleus', 'GO:0090734 site of DNA damage', "GO:0017005 3'-tyrosyl-DNA phosphodiesterase activity", 'GO:0003690 double-stranded DNA binding', 'GO:0003697 single-stranded DNA binding', 'GO:0006281 DNA repair', 'GO:0006302 double-strand break repair', 'GO:0006282 regulation of DNA repair', 'GO:0000012 single strand break repair'],
        protein_diseases=['Spinocerebellar ataxia, autosomal recessive, with axonal neuropathy 1'],
        method="ChEMBL", score=5.3, source_ref="ChEMBL ID: CHEMBL13883"
    ),
    slot(
        uniprot_id="P00352", protein_name="Aldehyde dehydrogenase 1A1", protein_acronym="ALDH1A1",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Expressed by erythrocytes (at protein level)'],
        best_structure="AlphaFold:AF-P00352-F1", other_structures=[],
        go_terms=['GO:0030424 axon', 'GO:0005737 cytoplasm', 'GO:0005829 cytosol', 'GO:0070062 extracellular exosome', 'GO:0045202 synapse', 'GO:0106373 3-deoxyglucosone dehydrogenase activity', 'GO:0140087 acetaldehyde dehydrogenase (NAD+) activity', 'GO:0004029 aldehyde dehydrogenase (NAD+) activity', 'GO:0019145 aminobutyraldehyde dehydrogenase (NAD+) activity', 'GO:0005497 androgen binding', 'GO:0018479 benzaldehyde dehydrogenase (NAD+) activity', 'GO:0005096 GTPase activator activity', 'GO:0052814 medium-chain fatty aldehyde dehydrogenase (NAD+) activity', 'GO:0051287 NAD binding', 'GO:0070403 NAD+ binding', 'GO:0001758 retinal dehydrogenase (NAD+) activity', 'GO:0042904 9-cis-retinoic acid biosynthetic process', 'GO:0006081 aldehyde metabolic process', 'GO:0110095 cellular detoxification of aldehyde', 'GO:0030392 fructosamine catabolic process', 'GO:0006540 GABA shunt', 'GO:0036438 maintenance of lens transparency', 'GO:0120163 negative regulation of cold-induced thermogenesis', 'GO:0001523 retinoid metabolic process', 'GO:0042572 retinol metabolic process'],
        protein_diseases=[],
        method="ChEMBL", score=4.85, source_ref="ChEMBL ID: CHEMBL13883"
    ),
    slot(
        uniprot_id="P51649", protein_name="Succinate-semialdehyde dehydrogenase, mitochondrial", protein_acronym="ALDH5A1",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Brain, pancreas, heart, liver, skeletal muscle and kidney. Lower in placenta'],
        best_structure="AlphaFold:AF-P51649-F1", other_structures=[],
        go_terms=['GO:0005759 mitochondrial matrix', 'GO:0005739 mitochondrion', 'GO:0042802 identical protein binding', 'GO:0004777 succinate-semialdehyde dehydrogenase (NAD+) activity', 'GO:0007417 central nervous system development', 'GO:0009450 GABA catabolic process', 'GO:0006540 GABA shunt', 'GO:0006536 glutamate metabolic process', 'GO:0006105 succinate metabolic process'],
        protein_diseases=['Succinic semialdehyde dehydrogenase deficiency'],
        method="ChEMBL", score=4.81, source_ref="ChEMBL ID: CHEMBL13883"
    ),
    slot(
        uniprot_id="P80404", protein_name="4-aminobutyrate aminotransferase, mitochondrial", protein_acronym="ABAT",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Liver > pancreas > brain > kidney > heart > placenta'],
        best_structure="AlphaFold:AF-P80404-F1", other_structures=[],
        go_terms=['GO:0032144 4-aminobutyrate transaminase complex', 'GO:0005759 mitochondrial matrix', 'GO:0005739 mitochondrion', 'GO:0047298 (S)-3-amino-2-methylpropionate:2-oxoglutarate transaminase activity', 'GO:0034386 4-aminobutyrate:2-oxoglutarate transaminase activity', 'GO:0030170 pyridoxal phosphate binding', 'GO:0032145 succinate-semialdehyde dehydrogenase binding', 'GO:0021549 cerebellum development', 'GO:0007620 copulation', 'GO:0035640 exploration behavior', 'GO:0009450 GABA catabolic process', 'GO:0006540 GABA shunt', 'GO:0007626 locomotory behavior', 'GO:0045776 negative regulation of blood pressure', 'GO:0033602 negative regulation of dopamine secretion', 'GO:0014053 negative regulation of gamma-aminobutyric acid secretion', 'GO:0050877 nervous system process', 'GO:1904450 positive regulation of aspartate secretion', 'GO:0045964 positive regulation of dopamine metabolic process', 'GO:0031652 positive regulation of heat generation', 'GO:0097151 positive regulation of inhibitory postsynaptic potential', 'GO:0032024 positive regulation of insulin secretion', 'GO:1902722 positive regulation of prolactin secretion', 'GO:0070474 positive regulation of uterine smooth muscle contraction', 'GO:0042220 response to cocaine', 'GO:0045471 response to ethanol', 'GO:0001666 response to hypoxia', 'GO:0010039 response to iron ion', 'GO:0035094 response to nicotine', 'GO:0009410 response to xenobiotic stimulus'],
        protein_diseases=['GABA-transaminase deficiency'],
        method="ChEMBL", score=4.77, source_ref="ChEMBL ID: CHEMBL13883"
    ),
    slot(
        uniprot_id="P15428", protein_name="15-hydroxyprostaglandin dehydrogenase [NAD(+)]", protein_acronym="HPGD",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Detected in colon epithelium (at protein level)'],
        best_structure="AlphaFold:AF-P15428-F1", other_structures=[],
        go_terms=['GO:0016323 basolateral plasma membrane', 'GO:0005737 cytoplasm', 'GO:0005829 cytosol', 'GO:0070062 extracellular exosome', 'GO:0047034 15-hydroxyicosatetraenoate dehydrogenase activity', 'GO:0016404 15-hydroxyprostaglandin dehydrogenase (NAD+) activity', 'GO:0042802 identical protein binding', 'GO:0051287 NAD binding', 'GO:0070403 NAD+ binding', 'GO:0016616 oxidoreductase activity, acting on the CH-OH group of donors, NAD or NADP as acceptor', 'GO:0004957 prostaglandin E receptor activity', 'GO:0097070 ductus arteriosus closure', 'GO:0007565 female pregnancy', 'GO:0001822 kidney development', 'GO:2001301 lipoxin biosynthetic process', 'GO:0019372 lipoxygenase pathway', 'GO:0045786 negative regulation of cell cycle', 'GO:0030728 ovulation', 'GO:0007567 parturition', 'GO:0043065 positive regulation of apoptotic process', 'GO:1904707 positive regulation of vascular associated smooth muscle cell proliferation', 'GO:1905344 prostaglandin catabolic process', 'GO:0006693 prostaglandin metabolic process', 'GO:1905828 regulation of prostaglandin catabolic process', 'GO:0032355 response to estradiol', 'GO:0045471 response to ethanol', 'GO:0032496 response to lipopolysaccharide', 'GO:0070493 thrombin-activated receptor signaling pathway', 'GO:0007179 transforming growth factor beta receptor signaling pathway'],
        protein_diseases=['Hypertrophic osteoarthropathy, primary, autosomal recessive, 1', 'Cranioosteoarthropathy', 'Digital clubbing, isolated congenital'],
        method="ChEMBL", score=4.4, source_ref="ChEMBL ID: CHEMBL13883"
    ),
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
