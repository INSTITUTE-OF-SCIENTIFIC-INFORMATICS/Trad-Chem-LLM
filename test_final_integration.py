#!/usr/bin/env python3
"""
Final TradChem-LLM Integration Test
@author SaltyHeart

Test script to verify complete integration of TradChem database with Gemini Flash LLM
"""

import os
import sys

def test_tradchem_integration():
    """Test complete TradChem-LLM integration"""
    print("🧪 TradChem-LLM Integration Test")
    print("=" * 50)
    
    # Test 1: TradChem Handler
    print("\n1️⃣ Testing TradChem Handler...")
    try:
        from utils.tradchem_handler import TradChemHandler
        handler = TradChemHandler()
        print(f"   ✅ TradChem Handler created")
        print(f"   📊 TradChem available: {handler.tradchem_available}")
        
        # Load database
        success = handler.load_database()
        print(f"   📊 Database loaded: {success}")
        
        if success:
            stats = handler.get_database_info()
            print(f"   📊 Total medicines: {stats.get('total_medicines', 0)}")
            print(f"   🏛️ Traditional systems: {len(stats.get('traditional_systems', []))}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test 2: LLM Handler
    print("\n2️⃣ Testing LLM Handler...")
    try:
        from utils.llm_handler import LLMHandler
        llm_handler = LLMHandler()
        print(f"   ✅ LLM Handler created")
        print(f"   🤖 Gemini available: {llm_handler.is_available()}")
        
        # Test TradChem status
        tradchem_status = llm_handler.get_tradchem_status()
        print(f"   🌿 TradChem integrated: {tradchem_status['available']}")
        print(f"   📊 Database loaded: {tradchem_status['loaded']}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test 3: Query Integration
    print("\n3️⃣ Testing Query Integration...")
    try:
        test_queries = [
            "What are the benefits of turmeric?",
            "Traditional medicine for inflammation",
            "Ayurvedic herbs for digestion"
        ]
        
        for query in test_queries:
            print(f"\n   🔍 Testing: {query}")
            try:
                context = handler.query_for_llm(query, context_limit=2)
                print(f"      ✅ Context generated: {len(context)} characters")
                print(f"      📝 Preview: {context[:100]}...")
            except Exception as e:
                print(f"      ❌ Query failed: {str(e)}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test 4: Search Functions
    print("\n4️⃣ Testing Search Functions...")
    try:
        search_tests = [
            ('benefits', 'inflammation'),
            ('disease', 'arthritis'),
            ('system', 'Ayurveda')
        ]
        
        for search_type, query in search_tests:
            try:
                if search_type == 'benefits':
                    results = handler.search_by_benefits(query)
                elif search_type == 'disease':
                    results = handler.search_by_disease(query)
                elif search_type == 'system':
                    results = handler.search_by_system(query)
                
                print(f"   ✅ {search_type.title()} search '{query}': {len(results)} results")
            except Exception as e:
                print(f"   ❌ {search_type.title()} search failed: {str(e)}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test 5: Integration Test
    print("\n5️⃣ Running Integration Test...")
    try:
        integration_results = handler.test_integration()
        print(f"   📊 Integration Results:")
        print(f"      TradChem Available: {integration_results['tradchem_available']}")
        print(f"      Database Loaded: {integration_results['database_loaded']}")
        print(f"      Total Medicines: {integration_results['total_medicines']}")
        print(f"      Traditional Systems: {integration_results['traditional_systems']}")
        
        print(f"   🔍 Query Tests:")
        for test in integration_results['test_queries']:
            status = "✅" if test['success'] else "❌"
            print(f"      {status} {test['query']}: {test.get('context_length', 0)} chars")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎯 INTEGRATION TEST COMPLETE")
    print("\n💡 Next Steps:")
    print("   1. Run: streamlit run app.py")
    print("   2. Test queries like:")
    print("      • 'What are the benefits of turmeric?'")
    print("      • 'Show me Ayurvedic herbs for inflammation'")
    print("      • 'Traditional Chinese medicine for digestion'")

if __name__ == "__main__":
    test_tradchem_integration() 