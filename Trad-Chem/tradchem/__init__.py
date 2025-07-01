"""
TradChem - Traditional Medicine Database for LLM Integration

A comprehensive database for traditional medicine data,
optimized for integration with LLM chatbots and AI applications.

Author: Anu Gamage
Repository: https://github.com/INSTITUTE-OF-SCIENTIFIC-INFORMATICS/Trad-Chem
LLM Chatbot: https://github.com/INSTITUTE-OF-SCIENTIFIC-INFORMATICS/Trad-Chem-LLM
"""

import json
import os
from typing import List, Dict, Any, Optional
from .version import __version__

# Simple TradChem class implementation
class TradChem:
    """
    TradChem - Traditional Medicine Database Access
    Provides access to traditional medicine database
    """
    
    def __init__(self, database_path=None):
        """
        Initialize TradChem with optional database path.
        Sets up database path and loads the medicine data
        """
        self.database_path = database_path or os.path.join(
            os.path.dirname(__file__), "data", "tradchem_database.json"
        )
        self.data = self.load_database()

    def load_database(self):
        """
        Load the traditional medicine database.
        Reads and parses the JSON database file
        """
        try:
            if os.path.exists(self.database_path):
                with open(self.database_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data
            else:
                return []
        except Exception as e:
            print(f"Error loading database: {e}")
            return []

    def get_statistics(self) -> Dict[str, Any]:
        """Get basic statistics - Returns comprehensive database metrics"""
        if not self.data:
            return {"total_medicines": 0}
        
        systems = set()
        regions = set()
        total_benefits = 0
        total_diseases = 0
        
        for medicine in self.data:
            if medicine.get('traditional_system'):
                systems.add(medicine['traditional_system'])
            if medicine.get('geographic_origin'):
                regions.add(medicine['geographic_origin'])
            if medicine.get('benefits'):
                total_benefits += len(medicine['benefits'])
            if medicine.get('diseases'):
                total_diseases += len(medicine['diseases'])
        
        return {
            "total_medicines": len(self.data),
            "traditional_systems": sorted(list(systems)),
            "geographic_regions": sorted(list(regions)),
            "total_benefits": total_benefits,
            "total_diseases": total_diseases,
            "description": "Traditional medicine database with chemical compositions and SMILES notations"
        }


def llm_query(query: str, context_limit: int = 5, include_smiles: bool = False, database_path: str = None):
    """
    Main LLM query function - optimized for AI chatbots.
    Primary function for LLM query processing and intelligent search
    
    Args:
        query: Natural language query - User input for medicine search
        context_limit: Limit of results to return - Maximum number of results
        include_smiles: Whether to include SMILES chemical formulas - Chemical data flag
        database_path: Custom database path - Alternative database location
        
    Returns:
        Structured LLM response - Formatted response for LLM integration
    """
    tc = TradChem(database_path)
    
    query_lower = query.lower()
    results = []
    
    # Multi-field intelligent search - Search across multiple medicine attributes
    for medicine in tc.data:
        score = 0
        matched_fields = []
        
        # Product name search - highest weight - Primary name matching
        if 'product_name' in medicine and query_lower in medicine['product_name'].lower():
            score += 10
            matched_fields.append('product_name')
        
        # Scientific name search - Scientific name matching
        if 'scientific_name' in medicine and query_lower in medicine.get('scientific_name', '').lower():
            score += 8
            matched_fields.append('scientific_name')
        
        # Benefits search - Therapeutic benefits matching
        if 'benefits' in medicine:
            for benefit in medicine['benefits']:
                if query_lower in benefit.lower():
                    score += 5
                    matched_fields.append('benefits')
                    break
        
        # Disease search - Disease treatment matching
        if 'diseases' in medicine:
            for disease in medicine['diseases']:
                if query_lower in disease.lower():
                    score += 5
                    matched_fields.append('diseases')
                    break
        
        # Traditional system search - Medical system matching
        if 'traditional_system' in medicine and query_lower in medicine.get('traditional_system', '').lower():
            score += 3
            matched_fields.append('traditional_system')
        
        # Geographic origin search - Regional origin matching
        if 'geographic_origin' in medicine and query_lower in medicine.get('geographic_origin', '').lower():
            score += 3
            matched_fields.append('geographic_origin')
        
        # Chemical composition search - Chemical component matching
        if 'chemical_composition' in medicine:
            comp = medicine['chemical_composition']
            if 'ingredients' in comp:
                for ingredient_name in comp['ingredients'].keys():
                    if query_lower in ingredient_name.lower():
                        score += 4
                        matched_fields.append('chemical_composition')
                        break
        
        if score > 0:
            result_entry = medicine.copy()
            result_entry['_relevance_score'] = score
            result_entry['_matched_fields'] = matched_fields
            results.append(result_entry)
    
    # Sort by relevance and limit results - Rank and limit search results
    results.sort(key=lambda x: x['_relevance_score'], reverse=True)
    results = results[:context_limit]
    
    # Format as LLM-friendly response - Structure response for LLM context
    response = {
        "query": query,
        "total_found": len(results),
        "context_data": [],
        "database_context": {
            "total_medicines": len(tc.data),
            "description": "Traditional medicine database with chemical compositions and SMILES notations",
            "version": __version__
        }
    }
    
    # Format each search result - Process individual medicine entries
    for result in results:
        context_entry = {
            "product_name": result.get('product_name', 'Unknown'),
            "scientific_name": result.get('scientific_name', ''),
            "traditional_system": result.get('traditional_system', ''),
            "geographic_origin": result.get('geographic_origin', ''),
            "benefits": result.get('benefits', []),
            "diseases": result.get('diseases', []),
            "relevance_score": result.get('_relevance_score', 0),
            "matched_fields": result.get('_matched_fields', [])
        }
        
        # Include chemical composition if requested - Add chemical data when needed
        if include_smiles and 'chemical_composition' in result:
            context_entry["chemical_composition"] = result['chemical_composition']
        
        response["context_data"].append(context_entry)
    
    return response


def get_database_stats():
    """Get database statistics for LLM context - Retrieve comprehensive database metrics for LLM"""
    tc = TradChem()
    stats = tc.get_statistics()
    stats["version"] = __version__
    return stats


def search_by_benefits(benefits_query: str, limit: int = 10):
    """Search traditional medicines by benefits - Find medicines based on therapeutic benefits"""
    tc = TradChem()
    query_lower = benefits_query.lower()
    results = []
    
    for medicine in tc.data:
        if 'benefits' in medicine:
            for benefit in medicine['benefits']:
                if query_lower in benefit.lower():
                    results.append(medicine)
                    break
    
    return results[:limit]


def search_by_disease(disease_query: str, limit: int = 10):
    """Search traditional medicines by disease - Find medicines for specific diseases"""
    tc = TradChem()
    query_lower = disease_query.lower()
    results = []
    
    for medicine in tc.data:
        if 'diseases' in medicine:
            for disease in medicine['diseases']:
                if query_lower in disease.lower():
                    results.append(medicine)
                    break
    
    return results[:limit]


def search_by_system(system_query: str, limit: int = 10):
    """Search medicines by traditional medicine system - Find medicines by medical tradition"""
    tc = TradChem()
    query_lower = system_query.lower()
    results = []
    
    for medicine in tc.data:
        if 'traditional_system' in medicine:
            if query_lower in medicine['traditional_system'].lower():
                results.append(medicine)
    
    return results[:limit]


def get_all_medicines(include_smiles: bool = False):
    """
    Get all medicines in the database.
    Retrieve complete medicine database with optional chemical data
    
    Args:
        include_smiles: Whether to include SMILES notations - Chemical data inclusion flag
        
    Returns:
        List of all medicines - Complete medicine database
    """
    tc = TradChem()
    
    if include_smiles:
        return tc.data
    else:
        # Return without chemical composition to keep response lighter - Remove chemical data for lighter response
        result = []
        for medicine in tc.data:
            filtered_medicine = {k: v for k, v in medicine.items() if k != 'chemical_composition'}
            result.append(filtered_medicine)
        return result


# Export main components - Define public API exports
__all__ = [
    'TradChem',
    'llm_query',
    'get_database_stats', 
    'search_by_benefits',
    'search_by_disease',
    'search_by_system',
    'get_all_medicines',
    '__version__'
]

# Project metadata
__author__ = "Anu Gamage"
__description__ = "Traditional medicine database for LLM integration"
__repository__ = "https://github.com/INSTITUTE-OF-SCIENTIFIC-INFORMATICS/Trad-Chem"
__llm_chatbot__ = "https://github.com/INSTITUTE-OF-SCIENTIFIC-INFORMATICS/Trad-Chem-LLM"