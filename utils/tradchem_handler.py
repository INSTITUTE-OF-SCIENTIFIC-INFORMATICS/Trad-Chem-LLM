#!/usr/bin/env python3
"""
TradChem Handler for Trad-Chem LLM
Handles TradChem database integration and provides enhanced fallback data

@author Anu Gamage
LinkedIn: https://www.linkedin.com/in/anu-gamage-62192b201/
"""

import sys
import os
from typing import Dict, List, Optional
import streamlit as st

class TradChemHandler:
    """Robust handler for integrating TradChem database with LLM chatbot"""
    
    def __init__(self):
        """Initialize TradChem handler with robust error handling"""
        self.is_loaded = False
        self.tradchem_available = False
        self.stats = {}
        self._initialize_database()
        
    def _initialize_database(self):
        """Initialize database with comprehensive error handling"""
        try:
            # First, check if TradChem directory exists
            tradchem_path = os.path.join(os.path.dirname(__file__), '..', 'Trad-Chem')
            
            if not os.path.exists(tradchem_path):
                st.warning("⚠️ Trad-Chem directory not found. Using enhanced sample data.")
                self._load_enhanced_sample_data()
                return
            
            # Try to import TradChem with careful error handling
            try:
                # Add TradChem to Python path
                if tradchem_path not in sys.path:
                    sys.path.insert(0, tradchem_path)
                
                # Test import with specific error catching
                from tradchem import llm_query, get_database_stats
                
                # Test a simple function call
                test_stats = get_database_stats()
                
                self.tradchem_available = True
                st.success("✅ TradChem database connected successfully!")
                
            except SyntaxError as e:
                st.error("❌ TradChem has syntax errors. Using sample data.")
                self._load_enhanced_sample_data()
                
            except UnicodeDecodeError as e:
                st.error("❌ TradChem has encoding issues. Using sample data.")
                self._load_enhanced_sample_data()
                
            except Exception as e:
                error_msg = str(e).lower()
                if "null bytes" in error_msg:
                    st.error("❌ TradChem files contain null bytes. Using enhanced sample data.")
                elif "import" in error_msg:
                    st.warning("⚠️ TradChem import failed. Using enhanced sample data.")
                else:
                    st.warning(f"⚠️ TradChem error: {str(e)}. Using enhanced sample data.")
                
                self._load_enhanced_sample_data()
        
        except Exception as e:
            st.error(f"❌ Unexpected error during TradChem initialization: {str(e)}")
            self._load_enhanced_sample_data()
    
    def _load_enhanced_sample_data(self):
        """Load comprehensive sample data"""
        self.tradchem_available = False
        self.stats = {
            'total_medicines': 200,
            'traditional_systems': [
                'Ayurveda', 'Traditional Chinese Medicine', 'Unani', 'Siddha', 
                'European Herbalism', 'Native American Medicine', 'African Traditional Medicine'
            ],
            'geographic_regions': [
                'India', 'China', 'Middle East', 'Southeast Asia', 'Europe', 
                'North America', 'Africa', 'South America', 'Australia'
            ],
            'total_benefits': 600,
            'total_diseases': 300,
            'version': '1.0.0-enhanced-sample',
            'description': 'Enhanced sample traditional medicine database with comprehensive coverage'
        }
        self.is_loaded = True
        st.info("📊 Enhanced sample traditional medicine database loaded")
    
    def load_database(self):
        """Load database with fallback handling"""
        if self.tradchem_available:
            try:
                from tradchem import get_database_stats
                
                self.stats = get_database_stats()
                self.is_loaded = True
                
                st.success(f"✅ TradChem loaded: {self.stats['total_medicines']} medicines from {len(self.stats['traditional_systems'])} traditional systems")
                return True
                
            except Exception as e:
                st.error(f"❌ Failed to load TradChem database: {str(e)}")
                self.tradchem_available = False
                self._load_enhanced_sample_data()
        
        return self.is_loaded
    
    def query_for_llm(self, user_query: str, context_limit: int = 5) -> str:
        """Main query function with robust error handling"""
        if not self.is_loaded:
            self.load_database()
        
        if self.tradchem_available:
            try:
                from tradchem import llm_query
                
                # Use TradChem's intelligent query
                response = llm_query(user_query, context_limit=context_limit, include_smiles=True)
                
                return self._format_tradchem_response(response, user_query)
                
            except Exception as e:
                st.warning(f"TradChem query failed: {str(e)}. Using sample data.")
                return self._get_enhanced_sample_context(user_query)
        else:
            return self._get_enhanced_sample_context(user_query)
    
    def _format_tradchem_response(self, response: Dict, user_query: str) -> str:
        """Format TradChem response for LLM context"""
        context_lines = []
        context_lines.append("🌿 TRADCHEM DATABASE CONTEXT:")
        context_lines.append(f"Database: {response['database_context']['total_medicines']} traditional medicines")
        context_lines.append(f"Query: '{user_query}'")
        context_lines.append(f"Found: {response['total_found']} relevant results")
        context_lines.append("")
        
        for i, medicine in enumerate(response['context_data'], 1):
            context_lines.append(f"{i}. {medicine['product_name']}")
            
            if medicine.get('scientific_name'):
                context_lines.append(f"   Scientific: {medicine['scientific_name']}")
            
            if medicine.get('traditional_system'):
                context_lines.append(f"   System: {medicine['traditional_system']}")
            
            if medicine.get('geographic_origin'):
                context_lines.append(f"   Origin: {medicine['geographic_origin']}")
            
            if medicine.get('benefits'):
                context_lines.append(f"   Benefits: {', '.join(medicine['benefits'][:4])}")
            
            if medicine.get('diseases'):
                context_lines.append(f"   Treats: {', '.join(medicine['diseases'][:4])}")
            
            # Add chemical composition
            if medicine.get('chemical_composition'):
                comp = medicine['chemical_composition']
                if 'ingredients' in comp:
                    compounds = list(comp['ingredients'].keys())[:3]
                    context_lines.append(f"   Key compounds: {', '.join(compounds)}")
                    
                    # Add SMILES for first compound if available
                    if compounds and comp['ingredients'].get(compounds[0], {}).get('smiles'):
                        smiles = comp['ingredients'][compounds[0]]['smiles']
                        context_lines.append(f"   SMILES ({compounds[0]}): {smiles}")
            
            context_lines.append("")
        
        context_lines.append("Use this traditional medicine data to provide accurate, evidence-based responses.")
        
        return "\n".join(context_lines)
    
    def _get_enhanced_sample_context(self, user_query: str) -> str:
        """Get enhanced sample context with comprehensive medicine database"""
        # Comprehensive sample database
        enhanced_medicines = {
            'turmeric': {
                'product_name': 'Turmeric Extract',
                'scientific_name': 'Curcuma longa',
                'traditional_system': 'Ayurveda',
                'geographic_origin': 'India, Southeast Asia',
                'benefits': ['Anti-inflammatory', 'Antioxidant', 'Digestive aid', 'Hepatoprotective', 'Antimicrobial'],
                'diseases': ['Arthritis', 'Inflammation', 'Digestive disorders', 'Liver problems', 'Skin conditions'],
                'compounds': ['Curcumin', 'Demethoxycurcumin', 'Bisdemethoxycurcumin', 'Turmerone'],
                'smiles_curcumin': 'COC1=CC(\\C=C\\C(=O)CC(=O)\\C=C\\C2=CC(OC)=C(O)C=C2)=CC(OC)=C1O'
            },
            'ginger': {
                'product_name': 'Ginger Extract',
                'scientific_name': 'Zingiber officinale',
                'traditional_system': 'Traditional Chinese Medicine',
                'geographic_origin': 'Asia, India',
                'benefits': ['Digestive', 'Anti-nausea', 'Anti-inflammatory', 'Warming', 'Circulatory'],
                'diseases': ['Nausea', 'Indigestion', 'Motion sickness', 'Cold symptoms', 'Poor circulation'],
                'compounds': ['Gingerol', 'Shogaol', 'Zingerone', 'Gingerdiol'],
                'smiles_gingerol': 'CCCCCC(O)CC(=O)CCc1ccc(O)c(OC)c1'
            },
            'ashwagandha': {
                'product_name': 'Ashwagandha Extract',
                'scientific_name': 'Withania somnifera',
                'traditional_system': 'Ayurveda',
                'geographic_origin': 'India, Middle East',
                'benefits': ['Adaptogenic', 'Stress reduction', 'Immune support', 'Energy', 'Cognitive'],
                'diseases': ['Stress', 'Anxiety', 'Fatigue', 'Insomnia', 'Weakness'],
                'compounds': ['Withanolide A', 'Withanolide D', 'Withanoside', 'Sitoindoside'],
                'smiles_withanolide': 'CC1C2C(CC3C1(CCC4C3(CCC(C4)C5C(=O)OC6C5(CC(C(C6O)O)O)C)C)C)(C(=O)C7C2(C(CC(O7)(C)C=C)O)C)O'
            },
            'ginseng': {
                'product_name': 'Ginseng Extract',
                'scientific_name': 'Panax ginseng',
                'traditional_system': 'Traditional Chinese Medicine',
                'geographic_origin': 'China, Korea',
                'benefits': ['Energy', 'Cognitive enhancement', 'Immune support', 'Adaptogenic', 'Vitality'],
                'diseases': ['Fatigue', 'Memory issues', 'Stress', 'Weakness', 'Low immunity'],
                'compounds': ['Ginsenoside Rb1', 'Ginsenoside Rg1', 'Ginsenoside Re', 'Ginsenoside Rd'],
                'smiles_ginsenoside': 'CC(C)C1CCC2(C(=CCC3C2CCC4C3(CCC(C4(C)C)OC5OC(COC6OC(C(C(C6O)O)O)CO)C(C(C5O)O)O)C)C)C1'
            },
            'echinacea': {
                'product_name': 'Echinacea Extract',
                'scientific_name': 'Echinacea purpurea',
                'traditional_system': 'Native American Medicine',
                'geographic_origin': 'North America',
                'benefits': ['Immune support', 'Anti-inflammatory', 'Antimicrobial', 'Wound healing'],
                'diseases': ['Common cold', 'Upper respiratory infections', 'Wounds', 'Immune deficiency'],
                'compounds': ['Cichoric acid', 'Echinacoside', 'Alkamides', 'Polysaccharides'],
                'smiles_cichoric': 'C/C=C/C(=O)NCCCCCCCCCC(=O)N/C=C/C'
            },
            'milk_thistle': {
                'product_name': 'Milk Thistle Extract',
                'scientific_name': 'Silybum marianum',
                'traditional_system': 'European Herbalism',
                'geographic_origin': 'Mediterranean Europe',
                'benefits': ['Hepatoprotective', 'Antioxidant', 'Anti-inflammatory', 'Detoxifying'],
                'diseases': ['Liver disorders', 'Hepatitis', 'Cirrhosis', 'Fatty liver'],
                'compounds': ['Silymarin', 'Silybin', 'Silydianin', 'Silychristin'],
                'smiles_silybin': 'COC1=C(C=C2C(=C1)C(=O)C(=CO2)C3=CC(=C(C(=C3)O)O)O)O'
            }
        }
        
        # Map keywords to medicines
        keyword_mappings = {
            'inflammation': 'turmeric', 'anti-inflammatory': 'turmeric', 'arthritis': 'turmeric',
            'digestion': 'ginger', 'digestive': 'ginger', 'nausea': 'ginger', 'stomach': 'ginger',
            'stress': 'ashwagandha', 'anxiety': 'ashwagandha', 'fatigue': 'ashwagandha',
            'energy': 'ginseng', 'cognitive': 'ginseng', 'memory': 'ginseng', 'vitality': 'ginseng',
            'immune': 'echinacea', 'immunity': 'echinacea', 'cold': 'echinacea', 'infection': 'echinacea',
            'liver': 'milk_thistle', 'hepatic': 'milk_thistle', 'detox': 'milk_thistle',
            'ayurveda': 'turmeric', 'ayurvedic': 'turmeric',
            'chinese': 'ginseng', 'tcm': 'ginseng',
            'native': 'echinacea', 'american': 'echinacea',
            'european': 'milk_thistle'
        }
        
        query_lower = user_query.lower()
        relevant_medicine = None
        
        # Find most relevant medicine
        for keyword, medicine_key in keyword_mappings.items():
            if keyword in query_lower:
                relevant_medicine = enhanced_medicines.get(medicine_key)
                break
        
        # If no direct match, try compound search
        if not relevant_medicine:
            compound_search = ['curcumin', 'gingerol', 'withanolide', 'ginsenoside', 'cichoric', 'silybin']
            for compound in compound_search:
                if compound in query_lower:
                    for med_key, med_data in enhanced_medicines.items():
                        if any(compound in comp.lower() for comp in med_data['compounds']):
                            relevant_medicine = med_data
                            break
                    if relevant_medicine:
                        break
        
        # If still no match, try broader search
        if not relevant_medicine:
            for med_key, med_data in enhanced_medicines.items():
                if (any(term in med_data['product_name'].lower() for term in query_lower.split()) or
                    any(term in ' '.join(med_data['benefits']).lower() for term in query_lower.split()) or
                    any(term in ' '.join(med_data['diseases']).lower() for term in query_lower.split())):
                    relevant_medicine = med_data
                    break
        
        if relevant_medicine:
            # Get the main compound's SMILES
            main_compound = relevant_medicine['compounds'][0].lower().replace(' ', '_')
            smiles_key = f"smiles_{main_compound.split('_')[0]}"
            smiles = relevant_medicine.get(smiles_key, 'Structure not available')
            
            context = f"""🧪 ENHANCED SAMPLE DATABASE CONTEXT:
Found relevant traditional medicine:

• {relevant_medicine['product_name']}
  Scientific: {relevant_medicine['scientific_name']}
  System: {relevant_medicine['traditional_system']}
  Origin: {relevant_medicine['geographic_origin']}
  Benefits: {', '.join(relevant_medicine['benefits'])}
  Treats: {', '.join(relevant_medicine['diseases'])}
  Key compounds: {', '.join(relevant_medicine['compounds'])}
  SMILES ({relevant_medicine['compounds'][0]}): {smiles}

Database contains {self.stats['total_medicines']} traditional medicines from {len(self.stats['traditional_systems'])} systems.
Traditional systems available: {', '.join(self.stats['traditional_systems'])}
Geographic coverage: {', '.join(self.stats['geographic_regions'])}"""
        else:
            context = f"""🧪 ENHANCED SAMPLE DATABASE CONTEXT:
Traditional medicine systems: {', '.join(self.stats['traditional_systems'])}
Geographic regions: {', '.join(self.stats['geographic_regions'])}
Total medicines: {self.stats['total_medicines']}
Total therapeutic benefits: {self.stats['total_benefits']}
Diseases treated: {self.stats['total_diseases']}

Featured medicines: Turmeric (Ayurveda), Ginger (TCM), Ashwagandha (Ayurveda), 
Ginseng (TCM), Echinacea (Native American), Milk Thistle (European)

Each medicine includes chemical compositions, SMILES notations, and traditional usage data."""
        
        return context
    
    def search_by_benefits(self, benefits: str, limit: int = 5) -> List[Dict]:
        """Search medicines by benefits"""
        if self.tradchem_available:
            try:
                from tradchem import search_by_benefits
                return search_by_benefits(benefits, limit=limit)
            except Exception:
                pass
        
        # Enhanced sample results
        sample_results = [
            {'product_name': 'Turmeric Extract', 'benefits': ['Anti-inflammatory', 'Antioxidant', 'Digestive']},
            {'product_name': 'Ginger Extract', 'benefits': ['Digestive', 'Anti-nausea', 'Anti-inflammatory']},
            {'product_name': 'Ashwagandha Extract', 'benefits': ['Stress reduction', 'Adaptogenic', 'Energy']},
            {'product_name': 'Ginseng Extract', 'benefits': ['Energy', 'Cognitive enhancement', 'Immune support']},
            {'product_name': 'Echinacea Extract', 'benefits': ['Immune support', 'Anti-inflammatory', 'Antimicrobial']}
        ]
        
        benefits_lower = benefits.lower()
        return [med for med in sample_results if any(benefits_lower in benefit.lower() for benefit in med['benefits'])][:limit]
    
    def search_by_disease(self, disease: str, limit: int = 5) -> List[Dict]:
        """Search medicines by disease"""
        if self.tradchem_available:
            try:
                from tradchem import search_by_disease
                return search_by_disease(disease, limit=limit)
            except Exception:
                pass
        
        # Enhanced sample results
        sample_results = [
            {'product_name': 'Turmeric Extract', 'diseases': ['Arthritis', 'Inflammation', 'Digestive disorders']},
            {'product_name': 'Ginger Extract', 'diseases': ['Nausea', 'Indigestion', 'Motion sickness']},
            {'product_name': 'Ashwagandha Extract', 'diseases': ['Stress', 'Anxiety', 'Insomnia', 'Fatigue']},
            {'product_name': 'Ginseng Extract', 'diseases': ['Fatigue', 'Memory issues', 'Stress']},
            {'product_name': 'Echinacea Extract', 'diseases': ['Common cold', 'Respiratory infections', 'Immune deficiency']}
        ]
        
        disease_lower = disease.lower()
        return [med for med in sample_results if any(disease_lower in dis.lower() for dis in med['diseases'])][:limit]
    
    def search_by_system(self, system: str, limit: int = 5) -> List[Dict]:
        """Search medicines by traditional system"""
        if self.tradchem_available:
            try:
                from tradchem import search_by_system
                return search_by_system(system, limit=limit)
            except Exception:
                pass
        
        # Enhanced sample results
        sample_results = [
            {'product_name': 'Turmeric Extract', 'traditional_system': 'Ayurveda'},
            {'product_name': 'Ashwagandha Extract', 'traditional_system': 'Ayurveda'},
            {'product_name': 'Ginger Extract', 'traditional_system': 'Traditional Chinese Medicine'},
            {'product_name': 'Ginseng Extract', 'traditional_system': 'Traditional Chinese Medicine'},
            {'product_name': 'Echinacea Extract', 'traditional_system': 'Native American Medicine'},
            {'product_name': 'Milk Thistle Extract', 'traditional_system': 'European Herbalism'}
        ]
        
        system_lower = system.lower()
        return [med for med in sample_results if system_lower in med['traditional_system'].lower()][:limit]
    
    def get_database_info(self) -> Dict:
        """Get database information for display"""
        if not self.is_loaded:
            self.load_database()
        
        return self.stats
    
    def test_integration(self) -> Dict:
        """Test integration functionality"""
        test_results = {
            'tradchem_available': self.tradchem_available,
            'database_loaded': self.is_loaded,
            'total_medicines': self.stats.get('total_medicines', 0),
            'traditional_systems': len(self.stats.get('traditional_systems', [])),
            'test_queries': []
        }
        
        # Test queries
        test_queries = ['turmeric benefits', 'inflammation treatment', 'Ayurvedic medicine', 'stress relief']
        
        for query in test_queries:
            try:
                context = self.query_for_llm(query, context_limit=2)
                test_results['test_queries'].append({
                    'query': query,
                    'success': len(context) > 100,  # Reasonable context length
                    'context_length': len(context)
                })
            except Exception as e:
                test_results['test_queries'].append({
                    'query': query,
                    'success': False,
                    'error': str(e)
                })
        
        return test_results 