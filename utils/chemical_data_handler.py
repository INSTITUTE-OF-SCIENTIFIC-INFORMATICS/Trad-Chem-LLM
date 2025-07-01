import pandas as pd
import requests
import json
from typing import Dict, List, Optional
import streamlit as st

# @author SaltyHeart

class ChemicalDataHandler:
    """Handler for integrating TradChem chemical database"""
    
    def __init__(self, repo_url: str = None, package_name: str = None):
        """Initialize chemical data handler
        
        Args:
            repo_url: URL of the TradChem git repository
            package_name: Name of the TradChem package ("tradchem")
        """
        self.repo_url = repo_url
        self.package_name = package_name
        self.data_cache = {}
        self.is_loaded = False
        self.tradchem_instance = None
        
    def load_chemical_data(self):
        """Load chemical data from TradChem package"""
        try:
            if self.package_name == "tradchem":
                # Import and initialize TradChem
                from tradchem import TradChem
                self.tradchem_instance = TradChem()
                
                # Load traditional medicine data
                try:
                    # Try to load any available CSV data files
                    medicines_data = self.tradchem_instance.load_data()
                    self.data_cache = self._convert_tradchem_data(medicines_data)
                except:
                    # If no data files available, use TradChem's sample data structure
                    self.data_cache = self._load_tradchem_sample_data()
                
                st.success("✅ TradChem package loaded successfully!")
                
            elif self.repo_url:
                # If it's a repository, fetch data via API
                self.data_cache = self._fetch_data_from_repo()
            else:
                # Load sample data structure for demonstration
                self.data_cache = self._load_sample_data()
            
            self.is_loaded = True
            return True
            
        except ImportError:
            st.warning("⚠️ TradChem package not found. Using sample data. Install with: pip install git+https://github.com/INSTITUTE-OF-SCIENTIFIC-INFORMATICS/Trad-Chem.git")
            self.data_cache = self._load_sample_data()
            self.is_loaded = True
            return True
            
        except Exception as e:
            st.error(f"Error loading TradChem data: {str(e)}")
            # Fallback to sample data
            self.data_cache = self._load_sample_data()
            self.is_loaded = True
            return True
    
    def _extract_data_from_module(self, module):
        """Extract data from imported Python module"""
        data = {}
        
        # Common attributes to look for in chemical data modules
        attributes = ['plants', 'compounds', 'smiles', 'benefits', 'diseases']
        
        for attr in attributes:
            if hasattr(module, attr):
                data[attr] = getattr(module, attr)
        
        return data
    
    def _fetch_data_from_repo(self):
        """Fetch data from repository API"""
        # This would implement GitHub API or direct file access
        # For now, return empty structure
        return {}
    
    def _convert_tradchem_data(self, medicines_data):
        """Convert TradChem data format to our internal format"""
        converted_data = {'plants': {}, 'compounds': {}}
        
        if isinstance(medicines_data, (list, pd.DataFrame)):
            # Handle DataFrame or list of medicine records
            if isinstance(medicines_data, pd.DataFrame):
                medicines_data = medicines_data.to_dict('records')
            
            for medicine in medicines_data:
                plant_name = medicine.get('product_name', '').lower().replace(' ', '_')
                if not plant_name:
                    continue
                
                # Extract plant information
                converted_data['plants'][plant_name] = {
                    'scientific_name': medicine.get('scientific_name', ''),
                    'traditional_system': medicine.get('traditional_system', ''),
                    'geographic_origin': medicine.get('geographic_origin', ''),
                    'compounds': [],
                    'benefits': medicine.get('benefits', []) if isinstance(medicine.get('benefits'), list) else medicine.get('benefits', '').split(','),
                    'diseases': medicine.get('diseases', []) if isinstance(medicine.get('diseases'), list) else medicine.get('diseases', '').split(',')
                }
                
                # Extract chemical composition
                chem_comp = medicine.get('chemical_composition', {})
                if isinstance(chem_comp, dict) and 'ingredients' in chem_comp:
                    ingredients = chem_comp['ingredients']
                    for compound_name, compound_data in ingredients.items():
                        compound_key = compound_name.lower().replace(' ', '_')
                        converted_data['plants'][plant_name]['compounds'].append(compound_key)
                        
                        # Add compound to compounds dict
                        converted_data['compounds'][compound_key] = {
                            'smiles': compound_data.get('smiles', ''),
                            'molecular_formula': compound_data.get('formula', ''),
                            'molecular_weight': compound_data.get('molecular_weight', ''),
                            'source_plants': [plant_name]
                        }
        
        return converted_data
    
    def _load_tradchem_sample_data(self):
        """Load TradChem-compatible sample data"""
        return {
            'plants': {
                'turmeric_extract': {
                    'scientific_name': 'Curcuma longa',
                    'traditional_system': 'Ayurveda',
                    'geographic_origin': 'India',
                    'compounds': ['curcumin', 'demethoxycurcumin', 'bisdemethoxycurcumin'],
                    'benefits': ['Anti-inflammatory', 'Antioxidant', 'Digestive aid'],
                    'diseases': ['Arthritis', 'Digestive disorders', 'Inflammation']
                },
                'ginger_extract': {
                    'scientific_name': 'Zingiber officinale',
                    'traditional_system': 'Traditional Chinese Medicine',
                    'geographic_origin': 'Asia',
                    'compounds': ['gingerol', 'shogaol', 'zingerone'],
                    'benefits': ['Digestive', 'Anti-nausea', 'Anti-inflammatory'],
                    'diseases': ['Nausea', 'Indigestion', 'Motion sickness']
                },
                'neem_extract': {
                    'scientific_name': 'Azadirachta indica',
                    'traditional_system': 'Ayurveda',
                    'geographic_origin': 'India',
                    'compounds': ['azadirachtin', 'nimbin', 'salannin'],
                    'benefits': ['Antimicrobial', 'Anti-inflammatory', 'Insecticidal'],
                    'diseases': ['Skin disorders', 'Infections', 'Fever']
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
                'azadirachtin': {
                    'smiles': 'CC1C2C(C(C1O)OC(=O)C)OC3C4C(=CC(=O)O3)C5C(C6C(C5(C4(C2=O)O)O)OC(=O)C7=C6C(=O)C=CO7)(C)O',
                    'molecular_formula': 'C35H44O16',
                    'molecular_weight': 720.71,
                    'source_plants': ['neem_extract']
                }
            }
        }
    
    def _load_sample_data(self):
        """Load basic sample chemical data structure"""
        return self._load_tradchem_sample_data()
    
    def search_plants(self, query: str) -> Dict:
        """Search for plants by name or scientific name"""
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
        """Search for chemical compounds"""
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
        """Search plants that treat specific diseases"""
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
    
    def get_smiles_notation(self, compound: str) -> Optional[str]:
        """Get SMILES notation for a compound"""
        if not self.is_loaded:
            self.load_chemical_data()
        
        compounds = self.data_cache.get('compounds', {})
        compound_data = compounds.get(compound.lower(), {})
        return compound_data.get('smiles')
    
    def get_plant_composition(self, plant_name: str) -> Dict:
        """Get chemical composition of a plant"""
        if not self.is_loaded:
            self.load_chemical_data()
        
        plants = self.data_cache.get('plants', {})
        return plants.get(plant_name.lower(), {})
    
    def format_search_results(self, results: Dict, search_type: str) -> str:
        """Format TradChem search results for LLM consumption"""
        if not results:
            return f"No {search_type} found matching your query."
        
        formatted = f"Found {len(results)} {search_type}:\n\n"
        
        for name, data in results.items():
            formatted += f"**{name.replace('_', ' ').title()}**\n"
            
            if search_type == "plants":
                formatted += f"- Scientific name: {data.get('scientific_name', 'N/A')}\n"
                
                # Traditional medicine system info
                if data.get('traditional_system'):
                    formatted += f"- Traditional system: {data.get('traditional_system')}\n"
                
                # Geographic origin info
                if data.get('geographic_origin'):
                    formatted += f"- Geographic origin: {data.get('geographic_origin')}\n"
                
                # Chemical compounds
                compounds = data.get('compounds', [])
                if compounds:
                    formatted += f"- Active compounds: {', '.join(compounds)}\n"
                
                # Therapeutic benefits
                benefits = data.get('benefits', [])
                if benefits:
                    formatted += f"- Therapeutic benefits: {', '.join(benefits)}\n"
                
                # Diseases treated
                diseases = data.get('diseases', [])
                if diseases:
                    formatted += f"- Traditional uses for: {', '.join(diseases)}\n"
            
            elif search_type == "compounds":
                formatted += f"- Molecular formula: {data.get('molecular_formula', 'N/A')}\n"
                
                # Molecular weight if available
                if data.get('molecular_weight'):
                    formatted += f"- Molecular weight: {data.get('molecular_weight')} g/mol\n"
                
                # SMILES notation
                smiles = data.get('smiles', 'N/A')
                if smiles and smiles != 'N/A':
                    formatted += f"- SMILES notation: {smiles}\n"
                
                # Source plants
                source_plants = data.get('source_plants', [])
                if source_plants:
                    formatted += f"- Found in plants: {', '.join(source_plants)}\n"
            
            formatted += "\n"
        
        return formatted
    
    def search_by_traditional_system(self, system: str) -> Dict:
        """Search plants by traditional medicine system"""
        if not self.is_loaded:
            self.load_chemical_data()
        
        results = {}
        plants = self.data_cache.get('plants', {})
        
        system = system.lower()
        for plant_name, plant_data in plants.items():
            traditional_system = plant_data.get('traditional_system', '').lower()
            if system in traditional_system:
                results[plant_name] = plant_data
        
        return results
    
    def search_by_geographic_origin(self, origin: str) -> Dict:
        """Search plants by geographic origin"""
        if not self.is_loaded:
            self.load_chemical_data()
        
        results = {}
        plants = self.data_cache.get('plants', {})
        
        origin = origin.lower()
        for plant_name, plant_data in plants.items():
            geographic_origin = plant_data.get('geographic_origin', '').lower()
            if origin in geographic_origin:
                results[plant_name] = plant_data
        
        return results
    
    def enhance_llm_prompt(self, user_query: str) -> str:
        """Enhance user query with relevant TradChem chemical data"""
        enhanced_info = ""
        
        # Search for relevant data based on query keywords
        query_lower = user_query.lower()
        
        # Check if query mentions specific plants
        plants_found = self.search_plants(user_query)
        if plants_found:
            enhanced_info += "🌿 RELEVANT PLANT DATA FROM TRADCHEM DATABASE:\n"
            enhanced_info += self.format_search_results(plants_found, "plants")
            enhanced_info += "\n"
        
        # Check if query mentions chemical compounds
        compounds_found = self.search_compounds(user_query)
        if compounds_found:
            enhanced_info += "🧪 RELEVANT CHEMICAL COMPOUNDS:\n"
            enhanced_info += self.format_search_results(compounds_found, "compounds")
            enhanced_info += "\n"
        
        # Check for disease mentions
        common_diseases = ['diabetes', 'cancer', 'arthritis', 'inflammation', 'infection', 'nausea', 'indigestion', 'fever', 'skin disorders']
        for disease in common_diseases:
            if disease in query_lower:
                disease_plants = self.search_by_disease(disease)
                if disease_plants:
                    enhanced_info += f"💊 TRADITIONAL PLANTS FOR {disease.upper()}:\n"
                    enhanced_info += self.format_search_results(disease_plants, "plants")
                    enhanced_info += "\n"
        
        # Check for traditional medicine system mentions
        traditional_systems = ['ayurveda', 'traditional chinese medicine', 'tcm', 'unani', 'homeopathy']
        for system in traditional_systems:
            if system in query_lower:
                system_plants = self.search_by_traditional_system(system)
                if system_plants:
                    enhanced_info += f"🏛️ {system.upper()} TRADITIONAL MEDICINES:\n"
                    enhanced_info += self.format_search_results(system_plants, "plants")
                    enhanced_info += "\n"
        
        # Check for geographic mentions
        geographic_regions = ['india', 'china', 'asia', 'africa', 'america', 'europe']
        for region in geographic_regions:
            if region in query_lower:
                regional_plants = self.search_by_geographic_origin(region)
                if regional_plants:
                    enhanced_info += f"🌍 TRADITIONAL MEDICINES FROM {region.upper()}:\n"
                    enhanced_info += self.format_search_results(regional_plants, "plants")
                    enhanced_info += "\n"
        
        if enhanced_info:
            enhanced_info = "📚 TRADCHEM DATABASE CONTEXT:\n\n" + enhanced_info
            enhanced_info += "\nPlease use this traditional medicine database information to provide accurate, evidence-based responses about plant chemistry, SMILES notations, therapeutic benefits, and traditional uses.\n\n"
        
        return enhanced_info