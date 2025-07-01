# @author SaltyHeart
# Chemical Data Integration Configuration

"""
Configuration for integrating external chemical database repository

To integrate your chemical data repository:

1. Option A - Python Package (Recommended):
   If your chemical data is available as a Python package:
   - Install the package: pip install your-chemical-package
   - Set CHEMICAL_PACKAGE_NAME to the package name
   
2. Option B - Git Repository:
   If your chemical data is in a git repository:
   - Set CHEMICAL_REPO_URL to your repository URL
   - Ensure the repository has proper API access or is public

3. Option C - Local Data:
   Leave both options empty to use sample data structure
"""

# Configuration options
CHEMICAL_PACKAGE_NAME = "tradchem"  # TradChem package from INSTITUTE-OF-SCIENTIFIC-INFORMATICS
CHEMICAL_REPO_URL = "https://github.com/INSTITUTE-OF-SCIENTIFIC-INFORMATICS/Trad-Chem.git"

# Data structure expected in your chemical package/repository:
EXPECTED_DATA_STRUCTURE = {
    "plants": {
        "plant_name": {
            "scientific_name": "Scientific Name",
            "compounds": ["compound1", "compound2"],
            "benefits": ["benefit1", "benefit2"],
            "diseases": ["disease1", "disease2"]
        }
    },
    "compounds": {
        "compound_name": {
            "smiles": "SMILES_notation_here",
            "molecular_formula": "C6H12O6",
            "source_plants": ["plant1", "plant2"]
        }
    }
}

# Instructions for setting up your chemical data:
SETUP_INSTRUCTIONS = """
To integrate your chemical data repository:

1. If your data is a Python package:
   - Update CHEMICAL_PACKAGE_NAME with your package name
   - Ensure your package exports the data in the expected structure

2. If your data is in a Git repository:
   - Update CHEMICAL_REPO_URL with your repository URL
   - Ensure the repository is accessible (public or with proper tokens)

3. Your data should follow the expected structure shown above
   
4. Example package structure:
   your_chemical_package/
   ├── __init__.py
   ├── plants.py      # Contains plant data
   ├── compounds.py   # Contains compound data
   └── data/
       ├── plants.json
       └── compounds.json

5. Example __init__.py:
   from .plants import PLANTS_DATA as plants
   from .compounds import COMPOUNDS_DATA as compounds
""" 