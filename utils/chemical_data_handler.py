import sys
import os
import pandas as pd
import requests
import json
from typing import Dict, List, Optional
import streamlit as st

# Fix TradChem import path - Add correct path to real database
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tradchem_path = os.path.join(project_root, 'Trad-Chem')
sys.path.insert(0, tradchem_path)

# @author Anu Gamage

class ChemicalDataHandler:
    """Handler for integrating TradChem chemical database with LLM"""
    
    def __init__(self, repo_url: str = None, package_name: str = None):
        """Initialize chemical data handler with TradChem integration
        
        Args:
            repo_url: URL of the TradChem git repository (not used anymore)
            package_name: Name of the TradChem package (not used anymore)
        """
        self.repo_url = repo_url
        self.package_name = package_name
        self.data_cache = {}
        self.is_loaded = False
        self.tradchem_available = self._check_tradchem_availability()
        
    def _check_tradchem_availability(self):
        """Check if real TradChem database is available"""
        try:
            # Try to import real TradChem module
            from tradchem import llm_query, get_database_stats
            stats = get_database_stats()
            st.success(f"✅ Real TradChem database connected! Contains {stats['total_medicines']} traditional medicines")
            return True
        except ImportError as e:
            st.warning(f"⚠️ Unable to connect to real TradChem database: {str(e)}")
            st.info("💡 Using sample database. Please ensure Trad-Chem directory exists for complete database.")
            return False
        except Exception as e:
            st.error(f"❌ Error connecting to TradChem: {str(e)}")
            return False
        
    def load_chemical_data(self):
        """Load chemical data from real TradChem database"""
        try:
            if self.tradchem_available:
                # Import real TradChem functions
                from tradchem import get_database_stats, get_all_medicines
                
                st.info("🔄 Loading real TradChem database...")
                
                # Get database statistics
                stats = get_database_stats()
                st.success(f"✅ Real TradChem loaded: {stats['total_medicines']} medicines from {len(stats['traditional_systems'])} traditional medical systems")
                
                # Load all medicines for caching, including SMILES chemical formulas
                all_medicines = get_all_medicines(include_smiles=True)
                
                # Organize data into our internal format
                self.data_cache = {
                    'plants': {},
                    'compounds': {},
                    'stats': stats,
                    'raw_medicines': all_medicines
                }
                
                # Process medicine data into plant and compound format
                self._process_tradchem_data(all_medicines)
                
                self.is_loaded = True
                return True
            else:
                # Fallback to enhanced sample data
                return self._load_enhanced_sample_data()
                
        except Exception as e:
            st.error(f"❌ Failed to load TradChem data: {str(e)}")
            return self._load_enhanced_sample_data()
    
    def _process_tradchem_data(self, medicines_data):
        """Process TradChem data into our internal format"""
        plants = {}
        compounds = {}
        
        for medicine in medicines_data:
            plant_name = medicine.get('product_name', '').lower().replace(' ', '_')
            if not plant_name:
                continue
            
            # Process plant data
            plants[plant_name] = {
                'scientific_name': medicine.get('scientific_name', ''),
                'traditional_system': medicine.get('traditional_system', ''),
                'geographic_origin': medicine.get('geographic_origin', ''),
                'compounds': [],
                'benefits': medicine.get('benefits', []),
                'diseases': medicine.get('diseases', []),
                'raw_data': medicine
            }
            
            # Process chemical composition
            if 'chemical_composition' in medicine and 'ingredients' in medicine['chemical_composition']:
                ingredients = medicine['chemical_composition']['ingredients']
                for compound_name, compound_data in ingredients.items():
                    compound_key = compound_name.lower().replace(' ', '_')
                    plants[plant_name]['compounds'].append(compound_key)
                    
                    # Add to compounds dictionary
                    if compound_key not in compounds:
                        compounds[compound_key] = {
                            'smiles': compound_data.get('smiles', ''),
                            'molecular_formula': compound_data.get('molecular_formula', ''),
                            'molecular_weight': compound_data.get('molecular_weight', ''),
                            'source_plants': [],
                            'raw_data': compound_data
                        }
                    
                    compounds[compound_key]['source_plants'].append(plant_name)
        
        self.data_cache['plants'] = plants
        self.data_cache['compounds'] = compounds
        
        st.info(f"📊 Processed: {len(plants)} plants, {len(compounds)} compounds")
    
    def _load_enhanced_sample_data(self):
        """Load enhanced sample data when TradChem is not available"""
        st.info("📊 Loading enhanced sample chemical database...")
        
        # Enhanced sample data with more comprehensive information
        sample_data = {
            'plants': {
                'turmeric_extract': {
                    'scientific_name': 'Curcuma longa',
                    'traditional_system': 'Ayurveda',
                    'geographic_origin': 'India, Southeast Asia',
                    'compounds': ['curcumin', 'demethoxycurcumin', 'bisdemethoxycurcumin'],
                    'benefits': ['Anti-inflammatory', 'Antioxidant', 'Digestive aid', 'Hepatoprotective'],
                    'diseases': ['Arthritis', 'Digestive disorders', 'Inflammation', 'Liver disorders']
                },
                'ginger_extract': {
                    'scientific_name': 'Zingiber officinale',
                    'traditional_system': 'Traditional Chinese Medicine',
                    'geographic_origin': 'Asia, India',
                    'compounds': ['gingerol', 'shogaol', 'zingerone'],
                    'benefits': ['Digestive', 'Anti-nausea', 'Anti-inflammatory', 'Warming'],
                    'diseases': ['Nausea', 'Indigestion', 'Motion sickness', 'Cold symptoms']
                },
                'ashwagandha_extract': {
                    'scientific_name': 'Withania somnifera',
                    'traditional_system': 'Ayurveda',
                    'geographic_origin': 'India, Middle East',
                    'compounds': ['withanolide_a', 'withanolide_d'],
                    'benefits': ['Adaptogenic', 'Stress reduction', 'Immune support', 'Energy'],
                    'diseases': ['Stress', 'Anxiety', 'Fatigue', 'Insomnia']
                },
                'ginkgo_extract': {
                    'scientific_name': 'Ginkgo biloba',
                    'traditional_system': 'Traditional Chinese Medicine',
                    'geographic_origin': 'China',
                    'compounds': ['ginkgolide_a', 'ginkgolide_b', 'bilobalide'],
                    'benefits': ['Cognitive enhancement', 'Circulatory support', 'Antioxidant'],
                    'diseases': ['Memory loss', 'Circulation disorders', 'Tinnitus']
                }
            },
            'compounds': {
                'curcumin': {
                    'smiles': 'COC1=CC(\\C=C\\C(=O)CC(=O)\\C=C\\C2=CC(OC)=C(O)C=C2)=CC(OC)=C1O',
                    'molecular_formula': 'C21H20O6',
                    'molecular_weight': 368.38,
                    'source_plants': ['turmeric_extract']
                },
                'gingerol': {
                    'smiles': 'CCCCCC(O)CC(=O)CCc1ccc(O)c(OC)c1',
                    'molecular_formula': 'C17H26O4',
                    'molecular_weight': 294.39,
                    'source_plants': ['ginger_extract']
                },
                'withanolide_a': {
                    'smiles': 'CC1C2C(CC3C1(CCC4C3(CCC(C4)C5C(=O)OC6C5(CC(C(C6O)O)O)C)C)C)(C(=O)C7C2(C(CC(O7)(C)C=C)O)C)O',
                    'molecular_formula': 'C28H38O6',
                    'molecular_weight': 470.6,
                    'source_plants': ['ashwagandha_extract']
                },
                'ginkgolide_a': {
                    'smiles': 'CC(C)(C1C2C3C(C4C1(C(=O)C5C(C4O)C(C(O5)C(C)(C)O)O)O)OC(O2)(C6C3OC(O6)C(C)(C)O)C)O',
                    'molecular_formula': 'C20H24O9',
                    'molecular_weight': 408.4,
                    'source_plants': ['ginkgo_extract']
                }
            },
            'stats': {
                'total_medicines': 4,
                'traditional_systems': ['Ayurveda', 'Traditional Chinese Medicine'],
                'geographic_regions': ['India', 'Asia', 'China'],
                'description': 'Enhanced sample database (Full TradChem database not available)'
            }
        }
        
        self.data_cache = sample_data
        self.is_loaded = True
        st.success("✅ Enhanced sample data loaded!")
        return True
    
    def search_plants_via_tradchem(self, query: str) -> Dict:
        """Search plants through real TradChem database"""
        if not self.tradchem_available:
            return self.search_plants(query)
            
        try:
            from tradchem import llm_query
            
            # 使用TradChem的智能搜索功能
            results = llm_query(query, context_limit=5, include_smiles=True)
            
            formatted_results = {
                'total_found': results['total_found'],
                'results': []
            }
            
            for item in results.get('context_data', []):
                formatted_results['results'].append({
                    'name': item.get('product_name', ''),
                    'scientific_name': item.get('scientific_name', ''),
                    'system': item.get('traditional_system', ''),
                    'benefits': item.get('benefits', []),
                    'compounds': [comp for comp in item.get('chemical_composition', {}).get('ingredients', {}).keys()]
                })
            
            return formatted_results
            
        except Exception as e:
            st.error(f"TradChem搜索错误: {str(e)}")
            return self.search_plants(query)
    
    def search_compounds_via_tradchem(self, query: str) -> Dict:
        """Search compounds using TradChem"""
        if not self.tradchem_available:
            return self.search_compounds(query)
        
        try:
            from tradchem import llm_query
            
            # Search with focus on chemical compounds
            response = llm_query(f"chemical compounds {query}", context_limit=10, include_smiles=True)
            
            results = {}
            for medicine in response.get('context_data', []):
                if 'chemical_composition' in medicine:
                    comp = medicine['chemical_composition']
                    if 'ingredients' in comp:
                        for compound_name, compound_data in comp['ingredients'].items():
                            if query.lower() in compound_name.lower():
                                compound_key = compound_name.lower().replace(' ', '_')
                                results[compound_key] = compound_data
            
            return results
            
        except Exception:
            return self.search_compounds(query)
    
    def search_by_benefits_tradchem(self, benefits: str) -> Dict:
        """Search by benefits using TradChem"""
        if not self.tradchem_available:
            return self.search_by_disease(benefits)  # Fallback
        
        try:
            from tradchem import search_by_benefits
            
            results = search_by_benefits(benefits, limit=10)
            formatted_results = {}
            
            for medicine in results:
                plant_name = medicine.get('product_name', '').lower().replace(' ', '_')
                if plant_name:
                    formatted_results[plant_name] = medicine
            
            return formatted_results
            
        except Exception:
            return self.search_by_disease(benefits)
    
    def search_by_disease_tradchem(self, disease: str) -> Dict:
        """Search by disease using TradChem"""
        if not self.tradchem_available:
            return self.search_by_disease(disease)
        
        try:
            from tradchem import search_by_disease
            
            results = search_by_disease(disease, limit=10)
            formatted_results = {}
            
            for medicine in results:
                plant_name = medicine.get('product_name', '').lower().replace(' ', '_')
                if plant_name:
                    formatted_results[plant_name] = medicine
            
            return formatted_results
            
        except Exception:
            return self.search_by_disease(disease)
    
    def search_by_traditional_system_tradchem(self, system: str) -> Dict:
        """Search by traditional medicine system using TradChem"""
        if not self.tradchem_available:
            return self.search_by_traditional_system(system)
        
        try:
            from tradchem import search_by_system
            
            results = search_by_system(system, limit=10)
            formatted_results = {}
            
            for medicine in results:
                plant_name = medicine.get('product_name', '').lower().replace(' ', '_')
                if plant_name:
                    formatted_results[plant_name] = medicine
            
            return formatted_results
            
        except Exception:
            return self.search_by_traditional_system(system)
    
    def enhance_llm_prompt(self, user_query: str) -> str:
        """Enhance LLM prompt with relevant chemical data using TradChem"""
        if not self.is_loaded:
            self.load_chemical_data()
        
        enhanced_context = []
        
        if self.tradchem_available:
            try:
                from tradchem import llm_query
                
                # Use TradChem's intelligent query function
                response = llm_query(user_query, context_limit=5, include_smiles=True)
                
                enhanced_context.append("🌿 TRADCHEM DATABASE RESULTS:")
                enhanced_context.append(f"Database: {response['database_context']['total_medicines']} traditional medicines")
                enhanced_context.append(f"Query: {response['query']}")
                enhanced_context.append(f"Found: {response['total_found']} relevant medicines")
                enhanced_context.append("")
                
                for i, medicine in enumerate(response['context_data'], 1):
                    enhanced_context.append(f"{i}. {medicine['product_name']}")
                    
                    if medicine.get('scientific_name'):
                        enhanced_context.append(f"   Scientific name: {medicine['scientific_name']}")
                    
                    if medicine.get('traditional_system'):
                        enhanced_context.append(f"   Traditional system: {medicine['traditional_system']}")
                    
                    if medicine.get('geographic_origin'):
                        enhanced_context.append(f"   Origin: {medicine['geographic_origin']}")
                    
                    if medicine.get('benefits'):
                        enhanced_context.append(f"   Benefits: {', '.join(medicine['benefits'][:5])}")
                    
                    if medicine.get('diseases'):
                        enhanced_context.append(f"   Treats: {', '.join(medicine['diseases'][:5])}")
                    
                    # Add chemical composition if available
                    if medicine.get('chemical_composition'):
                        comp = medicine['chemical_composition']
                        if 'ingredients' in comp:
                            compounds = list(comp['ingredients'].keys())[:3]
                            enhanced_context.append(f"   Key compounds: {', '.join(compounds)}")
                    
                    enhanced_context.append("")
                
                return "\n".join(enhanced_context)
                
            except Exception as e:
                st.warning(f"TradChem query failed: {str(e)}")
        
        # Fallback to cached data search
        plants = self.data_cache.get('plants', {})
        compounds = self.data_cache.get('compounds', {})
        
        query_lower = user_query.lower()
        relevant_items = []
        
        # Search plants
        for plant_name, plant_data in plants.items():
            if (any(term in plant_name for term in query_lower.split()) or
                any(term in plant_data.get('scientific_name', '').lower() for term in query_lower.split()) or
                any(term in ' '.join(plant_data.get('benefits', [])).lower() for term in query_lower.split())):
                relevant_items.append(('plant', plant_name, plant_data))
        
        # Search compounds
        for compound_name, compound_data in compounds.items():
            if any(term in compound_name for term in query_lower.split()):
                relevant_items.append(('compound', compound_name, compound_data))
        
        if relevant_items:
            enhanced_context.append("🧪 CHEMICAL DATABASE CONTEXT:")
            for item_type, name, data in relevant_items[:5]:
                if item_type == 'plant':
                    enhanced_context.append(f"• Plant: {name.replace('_', ' ').title()}")
                    enhanced_context.append(f"  Scientific: {data.get('scientific_name', 'N/A')}")
                    enhanced_context.append(f"  System: {data.get('traditional_system', 'N/A')}")
                    enhanced_context.append(f"  Benefits: {', '.join(data.get('benefits', [])[:3])}")
                elif item_type == 'compound':
                    enhanced_context.append(f"• Compound: {name.replace('_', ' ').title()}")
                    enhanced_context.append(f"  Formula: {data.get('molecular_formula', 'N/A')}")
                    enhanced_context.append(f"  SMILES: {data.get('smiles', 'N/A')}")
                enhanced_context.append("")
        
        return "\n".join(enhanced_context) if enhanced_context else ""

    # Include all the original search methods as fallbacks
    def search_plants(self, query: str) -> Dict:
        """Search for plants by name or scientific name (fallback method)"""
        if not self.is_loaded:
            self.load_chemical_data()
        
        results = {}
        plants = self.data_cache.get('plants', {})
        
        query = query.lower()
        for plant_name, plant_data in plants.items():
            if (query in plant_name.lower() or 
                query in plant_data.get('scientific_name', '').lower()):
                results[plant_name] = plant_data
        
        return results
    
    def search_compounds(self, query: str) -> Dict:
        """Search for chemical compounds (fallback method)"""
        if not self.is_loaded:
            self.load_chemical_data()
        
        results = {}
        compounds = self.data_cache.get('compounds', {})
        
        query = query.lower()
        for compound_name, compound_data in compounds.items():
            if query in compound_name.lower():
                results[compound_name] = compound_data
        
        return results
    
    def search_by_disease(self, disease: str) -> Dict:
        """Search plants by disease treatment (fallback method)"""
        if not self.is_loaded:
            self.load_chemical_data()
        
        results = {}
        plants = self.data_cache.get('plants', {})
        
        disease = disease.lower()
        for plant_name, plant_data in plants.items():
            diseases = plant_data.get('diseases', [])
            if any(disease in d.lower() for d in diseases):
                results[plant_name] = plant_data
        
        return results
    
    def search_by_traditional_system(self, system: str) -> Dict:
        """Search plants by traditional medicine system (fallback method)"""
        if not self.is_loaded:
            self.load_chemical_data()
        
        results = {}
        plants = self.data_cache.get('plants', {})
        
        system = system.lower()
        for plant_name, plant_data in plants.items():
            if system in plant_data.get('traditional_system', '').lower():
                results[plant_name] = plant_data
        
        return results
    
    def get_database_stats_display(self) -> Dict:
        """Get database statistics for display"""
        if self.tradchem_available:
            try:
                from tradchem import get_database_stats
                return get_database_stats()
            except:
                pass
        
        return self.data_cache.get('stats', {
            'total_medicines': len(self.data_cache.get('plants', {})),
            'traditional_systems': ['Sample data'],
            'description': 'Sample database'
        })