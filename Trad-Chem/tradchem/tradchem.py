import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Optional, Any, Union
from datetime import datetime
import logging
from collections import Counter, defaultdict

# Import utility modules
from .utils import smiles_utils, data_utils

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TradChem:
    """
    TradChem - Traditional Medicine Chemical Analysis
    
    A comprehensive class for analyzing traditional medicine data, 
    chemical structures, and molecular properties.
    
    Core Components:
    - Data Loading & Validation: Load and validate traditional medicine data
    - Chemical Structure Analysis: Analyze molecular structures and properties
    - Statistical Analysis: Perform comprehensive statistical analysis
    - Traditional Medicine Analysis: Analyze traditional medicine systems
    - Data Processing Tools: Filter, sort, and transform data
    - Visualization Tools: Create comprehensive visualizations
    """
    
    def __init__(self, database_path=None):
        """
        Initialize TradChem with optional database path.
        
        Args:
            database_path: Path to the traditional medicine database
        """
        # Use default database if not provided
        self.database_path = database_path or os.path.join(
            os.path.dirname(__file__), "data", "tradchem_database.json"
        )
        self.data = self.load_database()
        self._validate_database_structure()

        # Initialize analysis results cache
        self._analysis_cache = {}

    # ============================================================================
    # DATA LOADING & VALIDATION COMPONENT
    # ============================================================================
    
    def load_data(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Load traditional medicine data from various file formats.
        
        Args:
            file_path: Path to the data file (CSV, JSON, Excel)
            
        Returns:
            List of medicine dictionaries
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is not supported
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.csv':
            return self._load_csv_data(file_path)
        elif file_ext == '.json':
            return self._load_json_data(file_path)
        elif file_ext in ['.xlsx', '.xls']:
            return self._load_excel_data(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    
    def _load_csv_data(self, file_path: str) -> List[Dict[str, Any]]:
        """Load data from CSV file."""
        try:
            df = pd.read_csv(file_path)
            return df.to_dict('records')
        except Exception as e:
            logger.error(f"Error loading CSV file: {e}")
            return []
    
    def _load_json_data(self, file_path: str) -> List[Dict[str, Any]]:
        """Load data from JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data if isinstance(data, list) else [data]
        except Exception as e:
            logger.error(f"Error loading JSON file: {e}")
            return []
    
    def _load_excel_data(self, file_path: str) -> List[Dict[str, Any]]:
        """Load data from Excel file."""
        try:
            df = pd.read_excel(file_path)
            return df.to_dict('records')
        except Exception as e:
            logger.error(f"Error loading Excel file: {e}")
            return []

    def validate_data(self, medicines: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate traditional medicine data structure and content.
        
        Args:
            medicines: List of medicine dictionaries
            
        Returns:
            Dictionary containing validation results
        """
        validation_results = {
            'total_medicines': len(medicines),
            'valid_medicines': 0,
            'invalid_medicines': 0,
            'missing_fields': {},
            'data_quality_score': 0.0,
            'errors': []
        }
        
        required_fields = ['product_name', 'benefits', 'diseases', 'chemical_composition']
        
        for i, medicine in enumerate(medicines):
            medicine_valid = True
            missing_fields = []
        
        # Check required fields
        for field in required_fields:
                if field not in medicine:
                    missing_fields.append(field)
                    medicine_valid = False
            
            # Check data types
            if 'product_name' in medicine and not isinstance(medicine['product_name'], str):
                validation_results['errors'].append(f"Medicine {i}: product_name must be string")
                medicine_valid = False
            
            if 'benefits' in medicine and not isinstance(medicine['benefits'], list):
                validation_results['errors'].append(f"Medicine {i}: benefits must be list")
                medicine_valid = False
            
            if 'diseases' in medicine and not isinstance(medicine['diseases'], list):
                validation_results['errors'].append(f"Medicine {i}: diseases must be list")
                medicine_valid = False
            
            if 'chemical_composition' in medicine and not isinstance(medicine['chemical_composition'], dict):
                validation_results['errors'].append(f"Medicine {i}: chemical_composition must be dict")
                medicine_valid = False
            
            # Update counters
            if medicine_valid:
                validation_results['valid_medicines'] += 1
            else:
                validation_results['invalid_medicines'] += 1
                validation_results['missing_fields'][i] = missing_fields
        
        # Calculate quality score
        if validation_results['total_medicines'] > 0:
            validation_results['data_quality_score'] = (
                validation_results['valid_medicines'] / validation_results['total_medicines']
            )
        
        return validation_results
    
    def clean_data(self, medicines: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Clean and standardize traditional medicine data.
        
        Args:
            medicines: List of medicine dictionaries
            
        Returns:
            List of cleaned medicine dictionaries
        """
        cleaned_medicines = []
        
        for medicine in medicines:
            cleaned_medicine = medicine.copy()
            
            # Standardize string fields
            if 'product_name' in cleaned_medicine:
                cleaned_medicine['product_name'] = str(cleaned_medicine['product_name']).strip()
            
            if 'scientific_name' in cleaned_medicine:
                cleaned_medicine['scientific_name'] = str(cleaned_medicine['scientific_name']).strip()
            
            if 'description' in cleaned_medicine:
                cleaned_medicine['description'] = str(cleaned_medicine['description']).strip()
            
            # Ensure lists are properly formatted
            if 'benefits' in cleaned_medicine:
                if isinstance(cleaned_medicine['benefits'], str):
                    cleaned_medicine['benefits'] = [b.strip() for b in cleaned_medicine['benefits'].split(',')]
                elif not isinstance(cleaned_medicine['benefits'], list):
                    cleaned_medicine['benefits'] = []
            
            if 'diseases' in cleaned_medicine:
                if isinstance(cleaned_medicine['diseases'], str):
                    cleaned_medicine['diseases'] = [d.strip() for d in cleaned_medicine['diseases'].split(',')]
                elif not isinstance(cleaned_medicine['diseases'], list):
                    cleaned_medicine['diseases'] = []
            
            # Clean chemical composition
            if 'chemical_composition' in cleaned_medicine:
                if isinstance(cleaned_medicine['chemical_composition'], dict):
                    # Clean SMILES notations
                    if 'ingredients' in cleaned_medicine['chemical_composition']:
                        for ingredient_name, ingredient_data in cleaned_medicine['chemical_composition']['ingredients'].items():
                            if isinstance(ingredient_data, dict) and 'smiles' in ingredient_data:
                                # Validate and canonicalize SMILES
                                smiles = ingredient_data['smiles']
                                if smiles_utils.validate_smiles(smiles):
                                    ingredient_data['smiles'] = smiles_utils.canonicalize_smiles(smiles)
            
            cleaned_medicines.append(cleaned_medicine)
        
        return cleaned_medicines

    # ============================================================================
    # CHEMICAL STRUCTURE ANALYSIS COMPONENT
    # ============================================================================
    
    def analyze_chemical_structures(self, medicines: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze molecular structures and properties of compounds.
        
        Args:
            medicines: List of medicine dictionaries
            
        Returns:
            Dictionary containing chemical analysis results
        """
        analysis_results = {
            'total_compounds': 0,
            'valid_smiles': 0,
            'invalid_smiles': 0,
            'avg_molecular_weight': 0.0,
            'unique_formulas': 0,
            'molecular_properties': [],
            'chemical_families': {},
            'smiles_validation': {}
        }
        
        all_molecular_weights = []
        molecular_formulas = set()
        
        for medicine in medicines:
            if 'chemical_composition' in medicine and 'ingredients' in medicine['chemical_composition']:
                for ingredient_name, ingredient_data in medicine['chemical_composition']['ingredients'].items():
                    if isinstance(ingredient_data, dict) and 'smiles' in ingredient_data:
                        analysis_results['total_compounds'] += 1
                        smiles = ingredient_data['smiles']
                        
                        # Validate SMILES
                        if smiles_utils.validate_smiles(smiles):
                            analysis_results['valid_smiles'] += 1
                            
                            # Calculate molecular properties
                            properties = smiles_utils.calculate_molecular_properties(smiles)
                            if properties:
                                all_molecular_weights.append(properties.get('molecular_weight', 0))
                                if 'molecular_formula' in properties:
                                    molecular_formulas.add(properties['molecular_formula'])
                                
                                # Add to molecular properties list
                                properties['ingredient_name'] = ingredient_name
                                properties['medicine_name'] = medicine.get('product_name', 'Unknown')
                                analysis_results['molecular_properties'].append(properties)
                        else:
                            analysis_results['invalid_smiles'] += 1
                            analysis_results['smiles_validation'][ingredient_name] = smiles
        
        # Calculate averages
        if all_molecular_weights:
            analysis_results['avg_molecular_weight'] = sum(all_molecular_weights) / len(all_molecular_weights)
        
        analysis_results['unique_formulas'] = len(molecular_formulas)
        
        return analysis_results
    
    def calculate_molecular_properties(self, chemical_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate detailed molecular properties from chemical analysis.
        
        Args:
            chemical_analysis: Results from analyze_chemical_structures
            
        Returns:
            Dictionary containing molecular property summary
        """
        if not chemical_analysis.get('molecular_properties'):
            return {}
        
        properties = chemical_analysis['molecular_properties']
        
        # Calculate property ranges
        molecular_weights = [p.get('molecular_weight', 0) for p in properties if p.get('molecular_weight')]
        logp_values = [p.get('logp', 0) for p in properties if p.get('logp')]
        
        summary = {
            'min_weight': min(molecular_weights) if molecular_weights else 0,
            'max_weight': max(molecular_weights) if molecular_weights else 0,
            'avg_weight': sum(molecular_weights) / len(molecular_weights) if molecular_weights else 0,
            'min_logp': min(logp_values) if logp_values else 0,
            'max_logp': max(logp_values) if logp_values else 0,
            'avg_logp': sum(logp_values) / len(logp_values) if logp_values else 0,
            'common_formulas': [],
            'unique_compounds': len(set(p.get('smiles', '') for p in properties))
        }
        
        # Find common molecular formulas
        formulas = [p.get('molecular_formula', '') for p in properties if p.get('molecular_formula')]
        formula_counts = Counter(formulas)
        summary['common_formulas'] = [formula for formula, count in formula_counts.most_common(5)]
        
        return summary
    
    def validate_smiles(self, medicines: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate SMILES notations in traditional medicine data.
        
        Args:
            medicines: List of medicine dictionaries
            
        Returns:
            Dictionary containing SMILES validation results
        """
        validation_results = {
            'valid_count': 0,
            'invalid_count': 0,
            'validation_rate': 0.0,
            'invalid_examples': []
        }
        
        total_smiles = 0
        
        for medicine in medicines:
            if 'chemical_composition' in medicine and 'ingredients' in medicine['chemical_composition']:
                for ingredient_name, ingredient_data in medicine['chemical_composition']['ingredients'].items():
                    if isinstance(ingredient_data, dict) and 'smiles' in ingredient_data:
                        total_smiles += 1
                        smiles = ingredient_data['smiles']
                        
                        if smiles_utils.validate_smiles(smiles):
                            validation_results['valid_count'] += 1
                        else:
                            validation_results['invalid_count'] += 1
                            validation_results['invalid_examples'].append(smiles)
        
        # Calculate validation rate
        if total_smiles > 0:
            validation_results['validation_rate'] = validation_results['valid_count'] / total_smiles
        
        return validation_results

    # ============================================================================
    # STATISTICAL ANALYSIS COMPONENT
    # ============================================================================
    
    def statistical_analysis(self, medicines: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Perform statistical analysis on traditional medicine data.
        
        Args:
            medicines: List of medicine dictionaries
            
        Returns:
            Dictionary containing statistical analysis results
        """
        if not medicines:
            return {}
        
        # Basic statistics
        stats = {
            'total_medicines': len(medicines),
            'unique_systems': len(set(m.get('traditional_system', 'Unknown') for m in medicines)),
            'unique_regions': len(set(m.get('geographic_origin', 'Unknown') for m in medicines)),
            'avg_benefits_per_medicine': 0,
            'compounds_with_smiles': 0,
            'system_distribution': {},
            'region_distribution': {},
            'benefit_frequency': {},
            'disease_frequency': {}
        }
        
        # Count compounds with SMILES
        for medicine in medicines:
            if 'chemical_composition' in medicine and 'ingredients' in medicine['chemical_composition']:
                for ingredient_data in medicine['chemical_composition']['ingredients'].values():
                    if isinstance(ingredient_data, dict) and 'smiles' in ingredient_data:
                        stats['compounds_with_smiles'] += 1
        
        # Calculate average benefits per medicine
        total_benefits = sum(len(m.get('benefits', [])) for m in medicines)
        stats['avg_benefits_per_medicine'] = total_benefits / len(medicines) if medicines else 0
        
        # System and region distributions
        for medicine in medicines:
            system = medicine.get('traditional_system', 'Unknown')
            region = medicine.get('geographic_origin', 'Unknown')
            
            stats['system_distribution'][system] = stats['system_distribution'].get(system, 0) + 1
            stats['region_distribution'][region] = stats['region_distribution'].get(region, 0) + 1
        
        # Benefit and disease frequency
        all_benefits = []
        all_diseases = []
        
        for medicine in medicines:
            all_benefits.extend(medicine.get('benefits', []))
            all_diseases.extend(medicine.get('diseases', []))
        
        stats['benefit_frequency'] = dict(Counter(all_benefits))
        stats['disease_frequency'] = dict(Counter(all_diseases))
        
        return stats
    
    def correlation_analysis(self, medicines: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Find correlations between properties in traditional medicine data.
        
        Args:
            medicines: List of medicine dictionaries
            
        Returns:
            Dictionary containing correlation analysis results
        """
        # This is a simplified correlation analysis
        # In a full implementation, you would calculate actual correlations
        # between numerical properties like molecular weights, logP values, etc.
        
        correlations = {
            'correlations': [],
            'strong_correlations': [],
            'correlation_matrix': {}
        }
        
        # Placeholder for correlation analysis
        # In practice, you would extract numerical properties and calculate correlations
        
        return correlations
    
    def pattern_analysis(self, medicines: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Identify patterns in traditional medicine data.
        
        Args:
            medicines: List of medicine dictionaries
            
        Returns:
            Dictionary containing pattern analysis results
        """
        patterns = {
            'patterns': [],
            'common_combinations': {},
            'trends': {}
        }
        
        # Analyze common ingredient combinations
        ingredient_combinations = defaultdict(int)
        
        for medicine in medicines:
            if 'chemical_composition' in medicine and 'ingredients' in medicine['chemical_composition']:
                ingredients = list(medicine['chemical_composition']['ingredients'].keys())
                if len(ingredients) >= 2:
                    # Sort ingredients for consistent combination keys
                    ingredients.sort()
                    combination_key = ' + '.join(ingredients[:3])  # Top 3 ingredients
                    ingredient_combinations[combination_key] += 1
        
        # Find most common combinations
        patterns['common_combinations'] = dict(
            sorted(ingredient_combinations.items(), key=lambda x: x[1], reverse=True)[:10]
        )
        
        return patterns

    # ============================================================================
    # TRADITIONAL MEDICINE ANALYSIS COMPONENT
    # ============================================================================
    
    def analyze_traditional_systems(self, medicines: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze traditional medicine systems and their characteristics.
        
        Args:
            medicines: List of medicine dictionaries
            
        Returns:
            Dictionary containing traditional system analysis
        """
        system_analysis = {}
        
        for medicine in medicines:
            system = medicine.get('traditional_system', 'Unknown')
            
            if system not in system_analysis:
                system_analysis[system] = {
                    'count': 0,
                    'geographic_origins': set(),
                    'common_benefits': [],
                    'common_compounds': [],
                    'chemical_families': set(),
                    'compounds_with_smiles': 0
                }
            
            system_data = system_analysis[system]
            system_data['count'] += 1
            
            # Geographic origins
            if 'geographic_origin' in medicine:
                system_data['geographic_origins'].add(medicine['geographic_origin'])
            
            # Benefits
            system_data['common_benefits'].extend(medicine.get('benefits', []))
            
            # Chemical compounds
            if 'chemical_composition' in medicine and 'ingredients' in medicine['chemical_composition']:
                for ingredient_name, ingredient_data in medicine['chemical_composition']['ingredients'].items():
                    system_data['common_compounds'].append(ingredient_name)
                    
                    if isinstance(ingredient_data, dict) and 'smiles' in ingredient_data:
                        system_data['compounds_with_smiles'] += 1
        
        # Convert sets to lists and calculate frequencies
        for system, data in system_analysis.items():
            data['geographic_origins'] = list(data['geographic_origins'])
            data['chemical_families'] = list(data['chemical_families'])
            
            # Find most common benefits
            benefit_counts = Counter(data['common_benefits'])
            data['common_benefits'] = [benefit for benefit, count in benefit_counts.most_common(5)]
            
            # Find most common compounds
            compound_counts = Counter(data['common_compounds'])
            data['common_compounds'] = [compound for compound, count in compound_counts.most_common(5)]
        
        return system_analysis
    
    def geographic_analysis(self, medicines: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze geographic distributions of traditional medicines.
        
        Args:
            medicines: List of medicine dictionaries
            
        Returns:
            Dictionary containing geographic analysis results
        """
        geographic_analysis = {}
        
        for medicine in medicines:
            region = medicine.get('geographic_origin', 'Unknown')
            
            if region not in geographic_analysis:
                geographic_analysis[region] = {
                    'count': 0,
                    'systems': set(),
                    'common_ingredients': [],
                    'common_benefits': []
                }
            
            region_data = geographic_analysis[region]
            region_data['count'] += 1
            
            # Traditional systems
            if 'traditional_system' in medicine:
                region_data['systems'].add(medicine['traditional_system'])
            
            # Common ingredients
            if 'chemical_composition' in medicine and 'ingredients' in medicine['chemical_composition']:
                region_data['common_ingredients'].extend(
                    medicine['chemical_composition']['ingredients'].keys()
                )
            
            # Common benefits
            region_data['common_benefits'].extend(medicine.get('benefits', []))
        
        # Convert sets to lists and calculate frequencies
        for region, data in geographic_analysis.items():
            data['systems'] = list(data['systems'])
            
            # Find most common ingredients
            ingredient_counts = Counter(data['common_ingredients'])
            data['common_ingredients'] = [ingredient for ingredient, count in ingredient_counts.most_common(5)]
            
            # Find most common benefits
            benefit_counts = Counter(data['common_benefits'])
            data['common_benefits'] = [benefit for benefit, count in benefit_counts.most_common(5)]
        
        return geographic_analysis
    
    def benefit_analysis(self, medicines: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze health benefits and applications of traditional medicines.
        
        Args:
            medicines: List of medicine dictionaries
            
        Returns:
            Dictionary containing benefit analysis results
        """
        benefit_analysis = {
            'unique_benefits': set(),
            'benefit_frequency': {},
            'benefit_by_system': {},
            'benefit_by_region': {}
        }
        
        for medicine in medicines:
            benefits = medicine.get('benefits', [])
            system = medicine.get('traditional_system', 'Unknown')
            region = medicine.get('geographic_origin', 'Unknown')
            
            for benefit in benefits:
                benefit_analysis['unique_benefits'].add(benefit)
                
                # Overall frequency
                benefit_analysis['benefit_frequency'][benefit] = \
                    benefit_analysis['benefit_frequency'].get(benefit, 0) + 1
                
                # By system
                if system not in benefit_analysis['benefit_by_system']:
                    benefit_analysis['benefit_by_system'][system] = {}
                benefit_analysis['benefit_by_system'][system][benefit] = \
                    benefit_analysis['benefit_by_system'][system].get(benefit, 0) + 1
                
                # By region
                if region not in benefit_analysis['benefit_by_region']:
                    benefit_analysis['benefit_by_region'][region] = {}
                benefit_analysis['benefit_by_region'][region][benefit] = \
                    benefit_analysis['benefit_by_region'][region].get(benefit, 0) + 1
        
        # Convert set to list
        benefit_analysis['unique_benefits'] = list(benefit_analysis['unique_benefits'])
        
        return benefit_analysis

    # ============================================================================
    # DATA PROCESSING TOOLS COMPONENT
    # ============================================================================
    
    def filter_data(self, medicines: List[Dict[str, Any]], **filters) -> List[Dict[str, Any]]:
        """
        Filter traditional medicine data based on various criteria.
        
        Args:
            medicines: List of medicine dictionaries
            **filters: Filter criteria (system, region, benefit, etc.)
            
        Returns:
            Filtered list of medicine dictionaries
        """
        filtered_medicines = medicines
        
        for filter_key, filter_value in filters.items():
            if filter_key == 'system':
                filtered_medicines = [
                    m for m in filtered_medicines 
                    if m.get('traditional_system', '').lower() == filter_value.lower()
                ]
            elif filter_key == 'region':
                filtered_medicines = [
                    m for m in filtered_medicines 
                    if m.get('geographic_origin', '').lower() == filter_value.lower()
                ]
            elif filter_key == 'benefit':
                filtered_medicines = [
                    m for m in filtered_medicines 
                    if any(filter_value.lower() in benefit.lower() for benefit in m.get('benefits', []))
                ]
            elif filter_key == 'disease':
                filtered_medicines = [
                    m for m in filtered_medicines 
                    if any(filter_value.lower() in disease.lower() for disease in m.get('diseases', []))
                ]
            elif filter_key == 'ingredient':
                filtered_medicines = [
                    m for m in filtered_medicines 
                    if 'chemical_composition' in m and 'ingredients' in m['chemical_composition']
                    and any(filter_value.lower() in ingredient.lower() 
                           for ingredient in m['chemical_composition']['ingredients'].keys())
                ]
        
        return filtered_medicines
    
    def sort_data(self, medicines: List[Dict[str, Any]], by: str = 'name', 
                  reverse: bool = False) -> List[Dict[str, Any]]:
        """
        Sort traditional medicine data by various properties.
        
        Args:
            medicines: List of medicine dictionaries
            by: Property to sort by ('name', 'system', 'region', 'molecular_weight')
            reverse: Whether to sort in reverse order
            
        Returns:
            Sorted list of medicine dictionaries
        """
        if by == 'name':
            return sorted(medicines, key=lambda x: x.get('product_name', ''), reverse=reverse)
        elif by == 'system':
            return sorted(medicines, key=lambda x: x.get('traditional_system', ''), reverse=reverse)
        elif by == 'region':
            return sorted(medicines, key=lambda x: x.get('geographic_origin', ''), reverse=reverse)
        elif by == 'molecular_weight':
            # Sort by average molecular weight of ingredients
            def get_avg_molecular_weight(medicine):
                if 'chemical_composition' in medicine and 'ingredients' in medicine['chemical_composition']:
                    weights = []
                    for ingredient_data in medicine['chemical_composition']['ingredients'].values():
                        if isinstance(ingredient_data, dict) and 'molecular_weight' in ingredient_data:
                            weights.append(ingredient_data['molecular_weight'])
                    return sum(weights) / len(weights) if weights else 0
                return 0
            
            return sorted(medicines, key=get_avg_molecular_weight, reverse=reverse)
        else:
            return medicines
    
    def export_data(self, data: Union[List[Dict[str, Any]], Dict[str, Any]], 
                   output_path: str, format: str = 'json') -> bool:
        """
        Export data to various formats.
        
        Args:
            data: Data to export
            output_path: Output file path
            format: Export format ('json', 'csv', 'html')
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            if format == 'json':
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
            elif format == 'csv':
                df = pd.DataFrame(data)
                df.to_csv(output_path, index=False)
            elif format == 'html':
                df = pd.DataFrame(data)
                df.to_html(output_path, index=False)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            logger.info(f"Data exported successfully to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            return False

    # ============================================================================
    # VISUALIZATION TOOLS COMPONENT
    # ============================================================================
    
    def plot_chemical_structures(self, medicines: List[Dict[str, Any]], 
                                save_path: Optional[str] = None) -> None:
        """
        Create visualizations of chemical structures.
        
        Args:
            medicines: List of medicine dictionaries
            save_path: Optional path to save the plot
        """
        # This would integrate with RDKit for molecular structure visualization
        # For now, we'll create a basic plot of molecular weight distribution
        
        molecular_weights = []
        compound_names = []
        
        for medicine in medicines:
            if 'chemical_composition' in medicine and 'ingredients' in medicine['chemical_composition']:
                for ingredient_name, ingredient_data in medicine['chemical_composition']['ingredients'].items():
                    if isinstance(ingredient_data, dict) and 'molecular_weight' in ingredient_data:
                        molecular_weights.append(ingredient_data['molecular_weight'])
                        compound_names.append(ingredient_name)
        
        if molecular_weights:
            plt.figure(figsize=(10, 6))
            plt.hist(molecular_weights, bins=20, alpha=0.7, edgecolor='black')
            plt.title('Molecular Weight Distribution of Compounds')
            plt.xlabel('Molecular Weight')
            plt.ylabel('Frequency')
            plt.grid(True, alpha=0.3)
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.show()
    
    def plot_statistics(self, medicines: List[Dict[str, Any]], 
                       save_path: Optional[str] = None) -> None:
        """
        Create statistical plots of traditional medicine data.
        
        Args:
            medicines: List of medicine dictionaries
            save_path: Optional path to save the plot
        """
        # Create multiple subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Traditional Medicine Statistics', fontsize=16, fontweight='bold')
        
        # Plot 1: Traditional systems distribution
        system_counts = {}
        for medicine in medicines:
            system = medicine.get('traditional_system', 'Unknown')
            system_counts[system] = system_counts.get(system, 0) + 1
        
        if system_counts:
            axes[0, 0].pie(system_counts.values(), labels=system_counts.keys(), autopct='%1.1f%%')
            axes[0, 0].set_title('Traditional Medicine Systems Distribution')
        
        # Plot 2: Geographic distribution
        region_counts = {}
        for medicine in medicines:
            region = medicine.get('geographic_origin', 'Unknown')
            region_counts[region] = region_counts.get(region, 0) + 1
        
        if region_counts:
            axes[0, 1].bar(region_counts.keys(), region_counts.values())
            axes[0, 1].set_title('Geographic Distribution')
            axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Plot 3: Benefits frequency
        all_benefits = []
        for medicine in medicines:
            all_benefits.extend(medicine.get('benefits', []))
        
        if all_benefits:
            benefit_counts = Counter(all_benefits)
            top_benefits = dict(benefit_counts.most_common(10))
            axes[1, 0].barh(list(top_benefits.keys()), list(top_benefits.values()))
            axes[1, 0].set_title('Top 10 Health Benefits')
        
        # Plot 4: Benefits per medicine distribution
        benefits_per_medicine = [len(medicine.get('benefits', [])) for medicine in medicines]
        if benefits_per_medicine:
            axes[1, 1].hist(benefits_per_medicine, bins=15, alpha=0.7, edgecolor='black')
            axes[1, 1].set_title('Benefits per Medicine Distribution')
            axes[1, 1].set_xlabel('Number of Benefits')
            axes[1, 1].set_ylabel('Frequency')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_geographic_distribution(self, medicines: List[Dict[str, Any]], 
                                   save_path: Optional[str] = None) -> None:
        """
        Create geographic distribution visualizations.
        
        Args:
            medicines: List of medicine dictionaries
            save_path: Optional path to save the plot
        """
        # Create a map-like visualization of geographic distribution
        region_counts = {}
        for medicine in medicines:
            region = medicine.get('geographic_origin', 'Unknown')
            region_counts[region] = region_counts.get(region, 0) + 1
        
        if region_counts:
            plt.figure(figsize=(12, 8))
            bars = plt.bar(region_counts.keys(), region_counts.values())
            plt.title('Geographic Distribution of Traditional Medicines', fontsize=16, fontweight='bold')
            plt.xlabel('Geographic Region')
            plt.ylabel('Number of Medicines')
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, alpha=0.3)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{int(height)}', ha='center', va='bottom')
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.show()

    # ============================================================================
    # LEGACY METHODS (for backward compatibility)
    # ============================================================================
    
    def load_database(self):
        """Legacy method for loading database."""
        return self.load_data(self.database_path)
    
    def _validate_database_structure(self):
        """Legacy method for validating database structure."""
        if self.data:
            self.validate_data(self.data)
    
    def add_medicine(self, medicine_entry: Dict[str, Any]) -> bool:
        """Legacy method for adding medicine."""
        # Implementation would go here
        return True
    
    def search_medicines(self, query: str, search_type: str = "name", limit: int = 10) -> List[Dict[str, Any]]:
        """Legacy method for searching medicines."""
        # Implementation would go here
        return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """Legacy method for getting statistics."""
        return self.statistical_analysis(self.data)
    
    def analyze_medicines(self, medicines: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of traditional medicines.
        
        Args:
            medicines: List of medicine dictionaries
            
        Returns:
            Dictionary containing comprehensive analysis results
        """
        return {
            'data_validation': self.validate_data(medicines),
            'chemical_analysis': self.analyze_chemical_structures(medicines),
            'statistical_analysis': self.statistical_analysis(medicines),
            'traditional_analysis': self.analyze_traditional_systems(medicines),
            'geographic_analysis': self.geographic_analysis(medicines),
            'benefit_analysis': self.benefit_analysis(medicines)
        }

    # ============================================================================
    # LLM INTEGRATION METHODS
    # ============================================================================
    
    def smart_search(self, query: str, search_type: str = "all", limit: int = 10) -> List[Dict[str, Any]]:
        """
        Smart search across multiple fields with relevance scoring.
        
        Args:
            query: Search query
            search_type: Search type: all, name, benefit, disease, system, region
            limit: Result limit
            
        Returns:
            List of search results with relevance scores
        """
        query_lower = query.lower()
        results = []
        
        for medicine in self.data:
            score = 0
            matched_fields = []
            
            # Product name search
            if search_type in ["all", "name"] and 'product_name' in medicine:
                if query_lower in medicine['product_name'].lower():
                    score += 10
                    matched_fields.append('product_name')
            
            # Scientific name search
            if search_type in ["all", "name"] and 'scientific_name' in medicine:
                if query_lower in medicine.get('scientific_name', '').lower():
                    score += 8
                    matched_fields.append('scientific_name')
            
            # Benefits search
            if search_type in ["all", "benefit"] and 'benefits' in medicine:
                for benefit in medicine['benefits']:
                    if query_lower in benefit.lower():
                        score += 5
                        matched_fields.append('benefits')
                        break
            
            # Disease search
            if search_type in ["all", "disease"] and 'diseases' in medicine:
                for disease in medicine['diseases']:
                    if query_lower in disease.lower():
                        score += 5
                        matched_fields.append('diseases')
                        break
            
            # Traditional system search
            if search_type in ["all", "system"] and 'traditional_system' in medicine:
                if query_lower in medicine.get('traditional_system', '').lower():
                    score += 3
                    matched_fields.append('traditional_system')
            
            # Geographic origin search
            if search_type in ["all", "region"] and 'geographic_origin' in medicine:
                if query_lower in medicine.get('geographic_origin', '').lower():
                    score += 3
                    matched_fields.append('geographic_origin')
            
            # Chemical composition search
            if search_type in ["all", "chemical"] and 'chemical_composition' in medicine:
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
        
        # Sort by relevance
        results.sort(key=lambda x: x['_relevance_score'], reverse=True)
        return results[:limit]
    
    def llm_query(self, query: str, context_limit: int = 5, include_smiles: bool = False) -> Dict[str, Any]:
        """
        LLM-optimized query interface designed for AI chatbot integration.
        
        Args:
            query: Natural language query
            context_limit: Context entry limit
            include_smiles: Whether to include SMILES notations
            
        Returns:
            LLM-friendly structured response
        """
        # Analyze query type
        query_analysis = self._analyze_llm_query(query)
        
        # Execute smart search
        search_results = self.smart_search(query, limit=context_limit)
        
        # Prepare LLM response
        response = {
            "query": query,
            "query_type": query_analysis["type"],
            "extracted_keywords": query_analysis["keywords"],
            "total_found": len(search_results),
            "context_data": [],
            "database_context": self._get_llm_database_context(),
            "summary": {}
        }
        
        # Format search results for LLM context
        for result in search_results:
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
            
            # Include chemical composition if requested
            if include_smiles and 'chemical_composition' in result:
                context_entry["chemical_composition"] = result['chemical_composition']
            
            response["context_data"].append(context_entry)
        
        # Add summary information
        response["summary"] = {
            "total_medicines_in_database": len(self.data),
            "results_returned": len(search_results),
            "search_coverage": f"{len(search_results)}/{len(self.data)} medicines"
        }
        
        return response
    
    def get_llm_context_for_query(self, query: str, limit: int = 3) -> str:
        """
        Get formatted LLM context string
        
        Args:
            query: User's search query
            limit: Maximum number of results to include
            
        Returns:
            Formatted context string for LLM
        """
        results = self.llm_query(query, context_limit=limit, include_smiles=True)
        
        if not results['context_data']:
            return "No relevant traditional medicine data found for this query."
        
        # Format context for LLM
        context_parts = [
            f"TRADITIONAL MEDICINE DATABASE CONTEXT for query: '{query}'",
            f"Found {results['total_found']} relevant medicines:",
            ""
        ]
        
        for i, medicine in enumerate(results['context_data'], 1):
            context_parts.extend([
                f"{i}. {medicine['product_name']}",
                f"   Scientific Name: {medicine.get('scientific_name', 'Not specified')}",
                f"   Traditional System: {medicine.get('traditional_system', 'Not specified')}",
                f"   Geographic Origin: {medicine.get('geographic_origin', 'Not specified')}",
                f"   Benefits: {', '.join(medicine.get('benefits', []))}",
                f"   Treats: {', '.join(medicine.get('diseases', []))}",
                f"   Relevance Score: {medicine.get('relevance_score', 0)}",
                ""
            ])
            
            # Include chemical composition if available
            if 'chemical_composition' in medicine:
                comp = medicine['chemical_composition']
                if 'ingredients' in comp:
                    context_parts.append("   Chemical Composition:")
                    for ingredient, compounds in comp['ingredients'].items():
                        if isinstance(compounds, dict):
                            compound_names = list(compounds.keys())
                            context_parts.append(f"     - {ingredient}: {', '.join(compound_names[:3])}")
            context_parts.append("")
        
        context_parts.extend([
            f"Database Summary: {results['database_context']['total_medicines']} total medicines",
            f"Database Version: {results['database_context']['version']}",
            ""
        ])
        
        return "\n".join(context_parts)
    
    def _analyze_llm_query(self, query: str) -> Dict[str, Any]:
        """
        Analyze LLM query to determine search strategy.
        
        Args:
            query: Natural language query
            
        Returns:
            Dictionary with analysis results
        """
        query_lower = query.lower()
        analysis = {
            'search_strategy': 'general',
            'keywords': [],
            'medical_focus': False,
            'chemical_focus': False,
            'system_focus': False
        }
        
        # Medical keyword detection
        medical_keywords = ['disease', 'illness', 'condition', 'treatment', 'cure', 'medicine', 'drug']
        if any(keyword in query_lower for keyword in medical_keywords):
            analysis['medical_focus'] = True
            analysis['search_strategy'] = 'medical'
        
        # Chemical keyword detection
        chemical_keywords = ['smiles', 'compound', 'chemical', 'molecule', 'structure', 'formula']
        if any(keyword in query_lower for keyword in chemical_keywords):
            analysis['chemical_focus'] = True
            analysis['search_strategy'] = 'chemical'
        
        # Traditional system detection
        system_keywords = ['ayurveda', 'tcm', 'chinese', 'traditional', 'system']
        if any(keyword in query_lower for keyword in system_keywords):
            analysis['system_focus'] = True
            analysis['search_strategy'] = 'system'
        
        # Extract keywords
        import re
        words = re.findall(r'\b\w+\b', query_lower)
        analysis['keywords'] = [word for word in words if len(word) > 2]
        
        return analysis
    
    def _get_llm_database_context(self) -> Dict[str, Any]:
        """
        Get database context information for LLM
        
        Returns:
            Database metadata
        """
        return {
            "total_medicines": len(self.data),
            "description": "Traditional medicine database with chemical compositions and SMILES notations",
            "version": "1.0.0",
            "capabilities": [
                "Search by medicine name",
                "Search by benefits/effects", 
                "Search by diseases/conditions",
                "Search by traditional medicine system",
                "Chemical composition analysis",
                "SMILES notation lookup"
            ]
        }
