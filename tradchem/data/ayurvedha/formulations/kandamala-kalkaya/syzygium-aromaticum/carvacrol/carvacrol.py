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
    "chemical_name": "Carvacrol",
    "smiles": "Cc1ccc(C(C)C)cc1O",
    "pubchem_cid": "10364",
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
        method="ChEMBL", score=5.4, source_ref="ChEMBL ID: CHEMBL281202"
    ),
    slot(
        uniprot_id="O75762", protein_name="Transient receptor potential cation channel subfamily A member 1", protein_acronym="TRPA1",
        species="Homo sapiens", taxon_id=9606,
        cell_types=[],
        best_structure="AlphaFold:AF-O75762-F1", other_structures=[],
        go_terms=['GO:0016324 apical plasma membrane', 'GO:0030424 axon', 'GO:0005886 plasma membrane', 'GO:0032421 stereocilium bundle', 'GO:0005262 calcium channel activity', 'GO:0015267 channel activity', 'GO:0042802 identical protein binding', 'GO:0015278 intracellularly gated calcium channel activity', 'GO:1990760 osmolarity-sensing monoatomic cation channel activity', 'GO:0097604 temperature-gated cation channel activity', 'GO:0005245 voltage-gated calcium channel activity', 'GO:0097553 calcium ion transmembrane import into cytosol', 'GO:0070588 calcium ion transmembrane transport', 'GO:0007166 cell surface receptor signaling pathway', 'GO:0071313 cellular response to caffeine', 'GO:0071244 cellular response to carbon dioxide', 'GO:0070417 cellular response to cold', 'GO:0071240 cellular response to food', 'GO:0034605 cellular response to heat', 'GO:0070301 cellular response to hydrogen peroxide', 'GO:0097237 cellular response to toxic substance', 'GO:0050968 detection of chemical stimulus involved in sensory perception of pain', 'GO:0050974 detection of mechanical stimulus involved in sensory perception', 'GO:0006874 intracellular calcium ion homeostasis', 'GO:0006811 monoatomic ion transport', 'GO:0035774 positive regulation of insulin secretion involved in cellular response to glucose stimulus', 'GO:1903793 positive regulation of monoatomic anion transport', 'GO:0051289 protein homotetramerization', 'GO:1903522 regulation of blood circulation', 'GO:0098908 regulation of neuronal action potential', 'GO:0009409 response to cold', 'GO:0019233 sensory perception of pain', 'GO:0050955 thermoception', 'GO:0072105 ureteric peristalsis', 'GO:0014832 urinary bladder smooth muscle contraction', 'GO:0042311 vasodilation'],
        protein_diseases=['Episodic pain syndrome, familial, 1'],
        method="ChEMBL", score=5.16, source_ref="ChEMBL ID: CHEMBL281202"
    ),
    slot(
        uniprot_id="Q13936", protein_name="Voltage-dependent L-type calcium channel subunit alpha-1C", protein_acronym="CACNA1C",
        species="Homo sapiens", taxon_id=9606,
        cell_types=['Detected throughout the brain, including hippocampus, cerebellum and amygdala, throughout the heart and vascular system, including ductus arteriosus, in urinary bladder, and in retina and sclera in the eye (PubMed:15454078). Expressed in brain, heart, jejunum, ovary, pancreatic beta-cells and vascular smooth muscle. Overall expression is reduced in atherosclerotic vascular smooth muscle'],
        best_structure="AlphaFold:AF-Q13936-F1", other_structures=[],
        go_terms=['GO:0005737 cytoplasm', 'GO:0030425 dendrite', 'GO:1990454 L-type voltage-gated calcium channel complex', 'GO:0016020 membrane', 'GO:0043204 perikaryon', 'GO:0005886 plasma membrane', 'GO:0014069 postsynaptic density', 'GO:0098839 postsynaptic density membrane', 'GO:0005891 voltage-gated calcium channel complex', 'GO:0030018 Z disc', 'GO:0051393 alpha-actinin binding', 'GO:0005516 calmodulin binding', 'GO:0008331 high voltage-gated calcium channel activity', 'GO:0005245 voltage-gated calcium channel activity', 'GO:0086056 voltage-gated calcium channel activity involved in AV node cell action potential', 'GO:0086007 voltage-gated calcium channel activity involved in cardiac muscle cell action potential', 'GO:0098703 calcium ion import across plasma membrane', 'GO:0070588 calcium ion transmembrane transport', 'GO:0061577 calcium ion transmembrane transport via high voltage-gated calcium channel', 'GO:0060402 calcium ion transport into cytosol', 'GO:0043010 camera-type eye development', 'GO:0061337 cardiac conduction', 'GO:0086002 cardiac muscle cell action potential involved in contraction', 'GO:0086064 cell communication by electrical coupling involved in cardiac conduction', 'GO:0035115 embryonic forelimb morphogenesis', 'GO:0007507 heart development', 'GO:0002520 immune system development', 'GO:0098912 membrane depolarization during atrial cardiac muscle cell action potential', 'GO:0086045 membrane depolarization during AV node cell action potential', 'GO:0086012 membrane depolarization during cardiac muscle cell action potential', 'GO:0045762 positive regulation of adenylate cyclase activity', 'GO:0007204 positive regulation of cytosolic calcium ion concentration', 'GO:0045933 positive regulation of muscle contraction', 'GO:0010881 regulation of cardiac muscle contraction by regulation of the release of sequestered calcium ion', 'GO:0086091 regulation of heart rate by cardiac conduction', 'GO:0098911 regulation of ventricular cardiac muscle cell action potential'],
        protein_diseases=['Timothy syndrome', 'Brugada syndrome 3', 'Long QT syndrome 8', 'Neurodevelopmental disorder with hypotonia, language delay, and skeletal defects with or without seizures'],
        method="ChEMBL", score=4.01, source_ref="ChEMBL ID: CHEMBL281202"
    ),
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
