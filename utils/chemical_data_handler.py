#!/usr/bin/env python3
"""
Chemical Data Handler for TradChem LLM Integration
Handles traditional medicine database operations using direct JSON access

@author SaltyHeart
"""

import json
import os
from typing import Dict, List, Any, Optional

class ChemicalDataHandler:
    """Handler for TradChem database operations using direct JSON access"""
    
    def __init__(self):
        """Initialize chemical data handler with TradChem database"""
        self.database_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'Trad-Chem', 'tradchem', 'data', 'tradchem_database.json'
        )
        self.data = self.load_database()
        self.status = "Connected" if self.data else "Disconnected"
    
    def load_database(self) -> List[Dict]:
        """Load TradChem database from JSON file"""
        try:
            if os.path.exists(self.database_path):
                with open(self.database_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data if isinstance(data, list) else []
            else:
                print(f"Database file not found: {self.database_path}")
                return []
        except Exception as e:
            print(f"Error loading database: {e}")
            return []
    
    def get_status(self) -> Dict[str, Any]:
        """Get current database status"""
        return {
            "status": self.status,
            "database_path": self.database_path,
            "medicines_count": len(self.data),
            "database_exists": os.path.exists(self.database_path)
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive database statistics"""
        if not self.data:
            return {
                "total_medicines": 0,
                "traditional_systems": [],
                "geographic_regions": [],
                "error": "No data loaded"
            }
        
        systems = set()
        regions = set()
        benefits_count = 0
        diseases_count = 0
        
        for medicine in self.data:
            if medicine.get('traditional_system'):
                systems.add(medicine['traditional_system'])
            if medicine.get('geographic_origin'):
                regions.add(medicine['geographic_origin'])
            if medicine.get('benefits'):
                benefits_count += len(medicine['benefits'])
            if medicine.get('diseases'):
                diseases_count += len(medicine['diseases'])
        
        return {
            "total_medicines": len(self.data),
            "traditional_systems": sorted(list(systems)),
            "geographic_regions": sorted(list(regions)),
            "total_benefits": benefits_count,
            "total_diseases": diseases_count,
            "sample_medicines": [m.get('product_name', 'Unknown') for m in self.data[:3]]
        }
    
    def search_medicines(self, query: str, limit: int = 5) -> List[Dict]:
        """Search medicines by query across multiple fields"""
        if not self.data:
            return []
        
        query_lower = query.lower()
        results = []
        
        for medicine in self.data:
            score = 0
            matched_fields = []
            
            # Search in product name
            if 'product_name' in medicine and query_lower in medicine['product_name'].lower():
                score += 10
                matched_fields.append('product_name')
            
            # Search in benefits
            if 'benefits' in medicine:
                for benefit in medicine['benefits']:
                    if query_lower in benefit.lower():
                        score += 5
                        matched_fields.append('benefits')
                        break
            
            # Search in diseases
            if 'diseases' in medicine:
                for disease in medicine['diseases']:
                    if query_lower in disease.lower():
                        score += 5
                        matched_fields.append('diseases')
                        break
            
            # Search in traditional system
            if 'traditional_system' in medicine and query_lower in medicine.get('traditional_system', '').lower():
                score += 3
                matched_fields.append('traditional_system')
            
            # Search in chemical composition
            if 'chemical_composition' in medicine:
                comp = medicine['chemical_composition']
                if 'ingredients' in comp:
                    for ingredient_name in comp['ingredients'].keys():
                        if query_lower in ingredient_name.lower():
                            score += 4
                            matched_fields.append('chemical_composition')
                            break
            
            if score > 0:
                result = medicine.copy()
                result['_relevance_score'] = score
                result['_matched_fields'] = matched_fields
                results.append(result)
        
        # Sort by relevance and limit results
        results.sort(key=lambda x: x['_relevance_score'], reverse=True)
        return results[:limit]
    
    def get_chemical_context(self, query: str, include_smiles: bool = True) -> Dict[str, Any]:
        """Get chemical context for LLM enhancement"""
        results = self.search_medicines(query, limit=3)
        
        context = {
            "query": query,
            "found_medicines": len(results),
            "context_data": []
        }
        
        for result in results:
            medicine_context = {
                "name": result.get('product_name', 'Unknown'),
                "english_name": result.get('english_name', ''),
                "traditional_system": result.get('traditional_system', ''),
                "geographic_origin": result.get('geographic_origin', ''),
                "benefits": result.get('benefits', []),
                "diseases": result.get('diseases', []),
                "relevance_score": result.get('_relevance_score', 0)
            }
            
            # Include chemical composition if requested
            if include_smiles and 'chemical_composition' in result:
                composition = result['chemical_composition']
                medicine_context["chemical_composition"] = composition
            
            context["context_data"].append(medicine_context)
        
        return context

# Initialize the handler instance
chemical_handler = ChemicalDataHandler()