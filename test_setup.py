import sys

print("🧪 Trad-Chem LLM Setup Test")
print("=" * 40)

# Test imports
try:
    import streamlit
    print("✅ Streamlit OK")
except:
    print("❌ Streamlit failed")

try:
    import google.generativeai
    print("✅ Gemini API OK")
except:
    print("❌ Gemini API failed")

try:
    from config import Config
    print("✅ Config OK")
except:
    print("❌ Config failed")

try:
    from utils.llm_handler import LLMHandler
    print("✅ LLM Handler OK")
except:
    print("❌ LLM Handler failed")

try:
    from tradchem import TradChem
    print("✅ TradChem Package OK")
except:
    print("⚠️ TradChem not installed (optional)")

print("\n🧪 TradChem Integration:")
print("Repository: https://github.com/INSTITUTE-OF-SCIENTIFIC-INFORMATICS/Trad-Chem.git")
print("Install with: pip install git+https://github.com/INSTITUTE-OF-SCIENTIFIC-INFORMATICS/Trad-Chem.git")
print("\n🚀 Ready to run: python run.py") 