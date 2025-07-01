# Clean TradChem Handler - @author Anu Gamage
# Direct database access to avoid null bytes issues

import json
import os
import streamlit as st
from typing import Dict, List, Optional

class CleanTradChemHandler:
    """Clean TradChem handler with direct JSON database access"""
    
    def __init__(self):
        """Initialize handler with direct database access"""
        self.database_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'Trad-Chem', 'tradchem', 'data', 'tradchem_database.json'
        )
        self.data_cache = {}
        self.is_loaded = False
        self.tradchem_available = self._check_database_availability()
        
    def _check_database_availability(self):
        """Check if TradChem database JSON file is available"""
        try:
            if os.path.exists(self.database_path):
                with open(self.database_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                st.success(f"✅ TradChem database connected! Contains {len(data)} traditional medicines")
                return True
            else:
                st.warning("⚠️ TradChem database file not found")
                return False
        except Exception as e:
            st.error(f"❌ Error accessing TradChem database: {str(e)}")
            return False
    
    def load_database(self):
        """Load chemical data from TradChem JSON database"""
        try:
            if self.tradchem_available:
                st.info("🔄 Loading TradChem database...")
                
                with open(self.database_path, 'r', encoding='utf-8') as f:
                    raw_data = json.load(f)
                
                # Get statistics
                stats = self._calculate_stats(raw_data)
                st.success(f"✅ TradChem loaded: {stats['total_medicines']} medicines from {len(stats['traditional_systems'])} traditional systems")
                
                # Organize data
                self.data_cache = {
                    'plants': {},
                    'compounds': {},
                    'stats': stats,
                    'raw_medicines': raw_data
                }
                
                # Process medicine data
                self._process_medicines_data(raw_data)
                
                self.is_loaded = True
                return True
            else:
                return self._load_sample_data()
                
        except Exception as e:
            st.error(f"❌ Failed to load TradChem database: {str(e)}")
            return self._load_sample_data()
    
    def _calculate_stats(self, medicines_data):
        """Calculate database statistics"""
        traditional_systems = set()
        geographic_regions = set()
        total_benefits = 0
        total_diseases = 0
        
        for medicine in medicines_data:
            if medicine.get('traditional_system'):
                traditional_systems.add(medicine['traditional_system'])
            if medicine.get('geographic_origin'):
                geographic_regions.add(medicine['geographic_origin'])
            if medicine.get('benefits'):
                total_benefits += len(medicine['benefits'])
            if medicine.get('diseases'):
                total_diseases += len(medicine['diseases'])
        
        return {
            'total_medicines': len(medicines_data),
            'traditional_systems': sorted(list(traditional_systems)),
            'geographic_regions': sorted(list(geographic_regions)),
            'total_benefits': total_benefits,
            'total_diseases': total_diseases
        }
    
    def _process_medicines_data(self, medicines_data):
        """Process medicine data into plants and compounds format"""
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
                for ingredient_name, compound_data in ingredients.items():
                    compound_key = ingredient_name.lower().replace(' ', '_')
                    plants[plant_name]['compounds'].append(compound_key)
                    
                    # Add to compounds dictionary
                    if compound_key not in compounds:
                        compounds[compound_key] = {
                            'smiles': {},
                            'molecular_data': {},
                            'source_plants': [],
                            'raw_data': compound_data
                        }
                    
                    # Process individual compounds
                    if isinstance(compound_data, dict):
                        for compound_name, smiles_or_data in compound_data.items():
                            if isinstance(smiles_or_data, str):
                                compounds[compound_key]['smiles'][compound_name] = smiles_or_data
                            else:
                                compounds[compound_key]['molecular_data'][compound_name] = smiles_or_data
                    
                    compounds[compound_key]['source_plants'].append(plant_name)
        
        self.data_cache['plants'] = plants
        self.data_cache['compounds'] = compounds
        
        st.info(f"📊 Processed: {len(plants)} plants, {len(compounds)} compound groups")
    
    def _load_sample_data(self):
        """Load sample data when TradChem database is not available"""
        st.info("📊 Loading sample chemical database...")
        
        sample_data = {
            'plants': {
                'turmeric_complex': {
                    'scientific_name': 'Curcuma longa',
                    'traditional_system': 'Ayurveda',
                    'geographic_origin': 'India, Southeast Asia',
                    'compounds': ['curcumin_compounds'],
                    'benefits': ['Anti-inflammatory', 'Antioxidant', 'Digestive aid'],
                    'diseases': ['Arthritis', 'Digestive disorders', 'Inflammation']
                }
            },
            'compounds': {
                'curcumin_compounds': {
                    'smiles': {
                        'curcumin': 'COC1=CC(\\C=C\\C(=O)CC(=O)\\C=C\\C2=CC(OC)=C(O)C=C2)=CC(OC)=C1O'
                    },
                    'source_plants': ['turmeric_complex']
                }
            },
            'stats': {
                'total_medicines': 1,
                'traditional_systems': ['Ayurveda'],
                'geographic_regions': ['India'],
                'description': 'Sample database (TradChem database not available)'
            }
        }
        
        self.data_cache = sample_data
        self.is_loaded = True
        return True
    
    def query_for_llm(self, query: str, context_limit: int = 5) -> str:
        """Generate LLM-ready context from TradChem data"""
        if not self.is_loaded:
            self.load_database()
        
        if not self.data_cache.get('raw_medicines'):
            return "No traditional medicine data available."
        
        # Search through raw medicines data with improved algorithm
        query_lower = query.lower()
        relevant_medicines = []
        
        # Keywords for broader matching
        search_terms = query_lower.split()
        
        for medicine in self.data_cache['raw_medicines']:
            score = 0
            matched_fields = []
            
            # Product name search (exact and partial matches)
            product_name = medicine.get('product_name', '').lower()
            if any(term in product_name for term in search_terms):
                score += 10
                matched_fields.append('product_name')
            
            # Benefits search (more flexible)
            if 'benefits' in medicine:
                benefits_text = ' '.join(medicine['benefits']).lower()
                for term in search_terms:
                    if term in benefits_text:
                        score += 5
                        matched_fields.append('benefits')
                        break
            
            # Disease search (more flexible)
            if 'diseases' in medicine:
                diseases_text = ' '.join(medicine['diseases']).lower()
                for term in search_terms:
                    if term in diseases_text:
                        score += 5
                        matched_fields.append('diseases')
                        break
            
            # Chemical composition search (enhanced)
            if 'chemical_composition' in medicine:
                comp = medicine['chemical_composition']
                if 'ingredients' in comp:
                    for ingredient_name, compounds in comp['ingredients'].items():
                        # Search ingredient names
                        if any(term in ingredient_name.lower() for term in search_terms):
                            score += 4
                            matched_fields.append('chemical_composition')
                            break
                        
                        # Search compound names
                        if isinstance(compounds, dict):
                            compound_names = ' '.join(compounds.keys()).lower()
                            if any(term in compound_names for term in search_terms):
                                score += 3
                                matched_fields.append('chemical_compounds')
                                break
            
            # Traditional system search
            if 'traditional_system' in medicine:
                system_text = medicine.get('traditional_system', '').lower()
                if any(term in system_text for term in search_terms):
                    score += 3
                    matched_fields.append('traditional_system')
            
            # Semantic matches for common queries
            semantic_matches = {
                'stress': ['weakness', 'fatigue'],
                'energy': ['vitality', 'enhances'],
                'immune': ['immunity', 'boosts'],
                'digestive': ['honey', 'ghee'],
                'anti-inflammatory': ['cannabis'],
                'natural': ['traditional', 'medicine'],
                'healing': ['benefits', 'treatment']
            }
            
            for query_concept, related_terms in semantic_matches.items():
                if query_concept in query_lower:
                    medicine_text = (product_name + ' ' + 
                                   ' '.join(medicine.get('benefits', [])) + ' ' +
                                   ' '.join(medicine.get('diseases', []))).lower()
                    if any(term in medicine_text for term in related_terms):
                        score += 2
                        matched_fields.append('semantic_match')
            
            if score > 0:
                medicine_copy = medicine.copy()
                medicine_copy['_relevance_score'] = score
                medicine_copy['_matched_fields'] = matched_fields
                relevant_medicines.append(medicine_copy)
        
        # Sort by relevance and limit results
        relevant_medicines.sort(key=lambda x: x['_relevance_score'], reverse=True)
        relevant_medicines = relevant_medicines[:context_limit]
        
        if not relevant_medicines:
            return self._generate_helpful_suggestions(query)
        
        # Format context for LLM
        context_parts = [
            f"TRADITIONAL MEDICINE DATABASE CONTEXT for '{query}':",
            f"Found {len(relevant_medicines)} relevant medicines:",
            ""
        ]
        
        for i, medicine in enumerate(relevant_medicines, 1):
            context_parts.extend([
                f"{i}. {medicine.get('product_name', 'Unknown Medicine')}",
                f"   Benefits: {', '.join(medicine.get('benefits', []))}",
                f"   Treats: {', '.join(medicine.get('diseases', []))}",
                f"   Relevance Score: {medicine.get('_relevance_score', 0)}",
                f"   Matched Fields: {', '.join(medicine.get('_matched_fields', []))}",
                ""
            ])
            
            # Include chemical composition
            if 'chemical_composition' in medicine:
                comp = medicine['chemical_composition']
                if 'ingredients' in comp:
                    context_parts.append("   Chemical Composition:")
                    for ingredient_name, compounds in comp['ingredients'].items():
                        if isinstance(compounds, dict):
                            compound_names = list(compounds.keys())
                            context_parts.append(f"     - {ingredient_name}: {', '.join(compound_names[:3])}")
                            if len(compound_names) > 3:
                                context_parts.append(f"       (and {len(compound_names) - 3} more compounds)")
                    context_parts.append("")
        
        stats = self.data_cache['stats']
        context_parts.extend([
            f"Database Summary: {stats['total_medicines']} total medicines",
            f"Traditional Systems: {', '.join(stats['traditional_systems'])}",
            ""
        ])
        
        return "\n".join(context_parts)
    
    def _generate_helpful_suggestions(self, query: str) -> str:
        """Generate helpful suggestions when no data is found"""
        suggestions = [
            f"No specific traditional medicine data found for '{query}'.",
            "",
            "📊 AVAILABLE DATA IN TRADCHEM DATABASE:",
            "",
            "🌿 **Kameshwari Rasayanaya** (Ayurvedic Medicine)",
            "   • Benefits: Enhances vitality, Boosts immunity",
            "   • Treats: Weakness, Fatigue", 
            "   • Ingredients: Cannabis, Bee Honey, Ghee",
            "   • Chemical compounds: 10+ compounds with SMILES notations",
            "",
            "🔍 **TRY THESE QUERIES INSTEAD:**",
            "   • 'cannabis compounds in traditional medicine'",
            "   • 'kameshwari rasayanaya benefits'",
            "   • 'bee honey glucose in ayurveda'",
            "   • 'ghee fatty acids traditional use'",
            "   • 'vitality and immunity herbs'",
            "   • 'weakness and fatigue treatment'",
            "",
            "💡 **KEYWORDS THAT WORK:**",
            "cannabis, cannabigerol, bee honey, glucose, fructose, ghee, butyric acid,",
            "vitality, immunity, weakness, fatigue, kameshwari, rasayanaya",
            "",
            "🚀 **DATABASE EXPANSION:**",
            "The TradChem database is designed to grow over time.",
            "Currently contains 3 medicines with detailed chemical compositions.",
            "More traditional medicines will be added to expand coverage."
        ]
        
        return "\n".join(suggestions)
    
    def get_database_info(self):
        """Get database information"""
        if self.is_loaded:
            return self.data_cache.get('stats', {})
        return {}
    
    def test_integration(self):
        """Test integration functionality"""
        results = {
            'database_file_exists': os.path.exists(self.database_path),
            'database_loaded': self.is_loaded,
            'sample_query_works': False
        }
        
        try:
            if self.load_database():
                test_context = self.query_for_llm("test", context_limit=1)
                results['sample_query_works'] = len(test_context) > 50
        except Exception:
            pass
        
        return results 