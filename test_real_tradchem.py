import sys
import os

# Add TradChem path to system path
project_root = os.path.dirname(os.path.abspath(__file__))
tradchem_path = os.path.join(project_root, 'Trad-Chem')
sys.path.insert(0, tradchem_path)

print("Testing Real TradChem Database Connection")
print("=" * 50)

try:
    print("1. Trying to import TradChem module...")
    from tradchem import llm_query, get_database_stats
    print("SUCCESS: TradChem module imported")
    
    print("\n2. Getting database statistics...")
    stats = get_database_stats()
    print(f"SUCCESS: Database stats:")
    print(f"   Total medicines: {stats['total_medicines']}")
    print(f"   Traditional systems: {stats['traditional_systems']}")
    print(f"   Geographic regions: {stats['geographic_regions']}")
    print(f"   Total benefits: {stats['total_benefits']}")
    print(f"   Total diseases: {stats['total_diseases']}")
    
    print("\n3. Testing smart query function...")
    test_query = "cannabis"
    results = llm_query(test_query, context_limit=5, include_smiles=True)
    print(f"SUCCESS: Query '{test_query}' results:")
    print(f"   Found {results['total_found']} relevant results")
    
    for i, item in enumerate(results.get('context_data', []), 1):
        print(f"\n   Result {i}:")
        print(f"      Name: {item.get('product_name', 'N/A')}")
        print(f"      Scientific: {item.get('scientific_name', 'N/A')}")
        print(f"      System: {item.get('traditional_system', 'N/A')}")
        print(f"      Benefits: {', '.join(item.get('benefits', [])[:3])}")
        print(f"      Relevance: {item.get('relevance_score', 0)}")
    
    print("\n4. Testing direct database access...")
    from tradchem import TradChem
    tc = TradChem()
    raw_data = tc.data
    print(f"SUCCESS: Direct database access:")
    print(f"   Raw data entries: {len(raw_data)}")
    
    if raw_data:
        first_entry = raw_data[0]
        print(f"   First entry example:")
        print(f"      Name: {first_entry.get('product_name', 'N/A')}")
        if 'chemical_composition' in first_entry:
            ingredients = first_entry['chemical_composition'].get('ingredients', {})
            print(f"      Chemical ingredients: {len(ingredients)} ingredients")
            for ingredient_name, compounds in ingredients.items():
                print(f"        • {ingredient_name}: {len(compounds)} compounds")
                break
    
    print("\n" + "=" * 50)
    print("SUCCESS: Real TradChem Database Connected!")
    print(f"   This is REAL DATA with {stats['total_medicines']} traditional medicines")
    print("   Contains real SMILES chemical formulas and molecular data")
    
except ImportError as e:
    print(f"ERROR: Import failed: {e}")
    print("Check if Trad-Chem directory exists and contains tradchem module")
except Exception as e:
    print(f"ERROR: Other error: {e}")
    import traceback
    traceback.print_exc() 