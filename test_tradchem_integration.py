#!/usr/bin/env python3
"""
TradChem Integration Test Script
@author SaltyHeart

This script tests the TradChem database integration with the chatbot.
"""

import sys
import traceback

print("🧪 TradChem Integration Test")
print("=" * 50)

def test_1_tradchem_package():
    """Test 1: Check if TradChem package is installed"""
    print("\n1️⃣ Testing TradChem Package Installation...")
    
    try:
        import tradchem
        print("   ✅ TradChem package imported successfully")
        
        # Try to create instance
        tc = tradchem.TradChem()
        print("   ✅ TradChem instance created")
        
        return True
    except ImportError:
        print("   ❌ TradChem package NOT installed")
        print("   💡 Solution: pip install git+https://github.com/INSTITUTE-OF-SCIENTIFIC-INFORMATICS/Trad-Chem.git")
        return False
    except Exception as e:
        print(f"   ❌ TradChem error: {e}")
        return False

def test_2_chemical_data_handler():
    """Test 2: Check Chemical Data Handler"""
    print("\n2️⃣ Testing Chemical Data Handler...")
    
    try:
        from utils.chemical_data_handler import ChemicalDataHandler
        print("   ✅ Chemical Data Handler imported")
        
        # Test configuration
        from chemical_data_config import CHEMICAL_PACKAGE_NAME, CHEMICAL_REPO_URL
        print(f"   📦 Package configured: {CHEMICAL_PACKAGE_NAME}")
        print(f"   🔗 Repository configured: {CHEMICAL_REPO_URL}")
        
        # Create handler instance
        handler = ChemicalDataHandler(CHEMICAL_REPO_URL, CHEMICAL_PACKAGE_NAME)
        print("   ✅ Handler instance created")
        
        return True, handler
    except Exception as e:
        print(f"   ❌ Handler error: {e}")
        print(f"   Details: {traceback.format_exc()}")
        return False, None

def test_3_data_loading(handler):
    """Test 3: Check Data Loading"""
    print("\n3️⃣ Testing Data Loading...")
    
    if not handler:
        print("   ❌ No handler available")
        return False
    
    try:
        # Test data loading
        success = handler.load_chemical_data()
        
        if success:
            print("   ✅ Data loading successful")
            
            # Check data contents
            plants = handler.data_cache.get('plants', {})
            compounds = handler.data_cache.get('compounds', {})
            
            print(f"   📊 Plants loaded: {len(plants)}")
            print(f"   🧪 Compounds loaded: {len(compounds)}")
            
            # Show sample data
            if plants:
                sample_plant = list(plants.keys())[0]
                print(f"   🌿 Sample plant: {sample_plant}")
                
            if compounds:
                sample_compound = list(compounds.keys())[0]
                print(f"   ⚗️ Sample compound: {sample_compound}")
            
            return True
        else:
            print("   ❌ Data loading failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Loading error: {e}")
        print(f"   Details: {traceback.format_exc()}")
        return False

def test_4_search_functionality(handler):
    """Test 4: Check Search Functions"""
    print("\n4️⃣ Testing Search Functionality...")
    
    if not handler:
        print("   ❌ No handler available")
        return False
    
    try:
        # Test plant search
        turmeric_results = handler.search_plants("turmeric")
        print(f"   🔍 Turmeric search: {len(turmeric_results)} results")
        
        # Test compound search
        curcumin_results = handler.search_compounds("curcumin")
        print(f"   🔍 Curcumin search: {len(curcumin_results)} results")
        
        # Test disease search
        inflammation_results = handler.search_by_disease("inflammation")
        print(f"   🔍 Inflammation search: {len(inflammation_results)} results")
        
        return True
    except Exception as e:
        print(f"   ❌ Search error: {e}")
        return False

def test_5_llm_integration():
    """Test 5: Check LLM Integration"""
    print("\n5️⃣ Testing LLM Integration...")
    
    try:
        from utils.llm_handler import LLMHandler
        from chemical_data_config import CHEMICAL_PACKAGE_NAME, CHEMICAL_REPO_URL
        
        # Create LLM handler with chemical data
        llm_handler = LLMHandler(CHEMICAL_REPO_URL, CHEMICAL_PACKAGE_NAME)
        print("   ✅ LLM Handler with chemical data created")
        
        # Test enhancement
        test_query = "What is turmeric?"
        enhanced_prompt = llm_handler.chemical_handler.enhance_llm_prompt(test_query)
        
        if enhanced_prompt:
            print("   ✅ Query enhancement working")
            print(f"   📝 Enhanced context length: {len(enhanced_prompt)} characters")
        else:
            print("   ⚠️ No enhancement for test query")
        
        return True
    except Exception as e:
        print(f"   ❌ LLM integration error: {e}")
        print(f"   Details: {traceback.format_exc()}")
        return False

def test_6_full_pipeline():
    """Test 6: Full Integration Pipeline"""
    print("\n6️⃣ Testing Full Pipeline...")
    
    try:
        from utils.llm_handler import LLMHandler
        from chemical_data_config import CHEMICAL_PACKAGE_NAME, CHEMICAL_REPO_URL
        
        # Create full pipeline
        llm_handler = LLMHandler(CHEMICAL_REPO_URL, CHEMICAL_PACKAGE_NAME)
        
        # Test if Gemini is available
        if llm_handler.is_available():
            print("   ✅ Gemini API available")
        else:
            print("   ⚠️ Gemini API not available")
        
        # Test chemical data is loaded
        if llm_handler.chemical_handler.is_loaded:
            print("   ✅ Chemical data loaded in LLM handler")
        else:
            print("   ⚠️ Chemical data not loaded in LLM handler")
        
        return True
    except Exception as e:
        print(f"   ❌ Full pipeline error: {e}")
        return False

def main():
    """Run all tests"""
    print("🔬 Testing TradChem Database Integration...")
    
    # Run tests
    test1_result = test_1_tradchem_package()
    test2_result, handler = test_2_chemical_data_handler()
    test3_result = test_3_data_loading(handler) if handler else False
    test4_result = test_4_search_functionality(handler) if handler else False
    test5_result = test_5_llm_integration()
    test6_result = test_6_full_pipeline()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 INTEGRATION TEST SUMMARY:")
    print(f"   1️⃣ TradChem Package: {'✅' if test1_result else '❌'}")
    print(f"   2️⃣ Data Handler: {'✅' if test2_result else '❌'}")
    print(f"   3️⃣ Data Loading: {'✅' if test3_result else '❌'}")
    print(f"   4️⃣ Search Functions: {'✅' if test4_result else '❌'}")
    print(f"   5️⃣ LLM Integration: {'✅' if test5_result else '❌'}")
    print(f"   6️⃣ Full Pipeline: {'✅' if test6_result else '❌'}")
    
    all_passed = all([test1_result, test2_result, test3_result, test4_result, test5_result, test6_result])
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED! TradChem is properly integrated!")
        print("\n💬 Test these queries in your chatbot:")
        print("   • 'What are the chemical compounds in turmeric?'")
        print("   • 'Show me the SMILES notation for curcumin'")
        print("   • 'What Ayurvedic plants help with inflammation?'")
    else:
        print("\n⚠️ SOME TESTS FAILED. Integration needs fixing.")
        if not test1_result:
            print("\n🔧 REQUIRED FIXES:")
            print("   pip install git+https://github.com/INSTITUTE-OF-SCIENTIFIC-INFORMATICS/Trad-Chem.git")

if __name__ == "__main__":
    main()