# 🧪 Trad-Chem LLM Complete Setup Guide

**@author SaltyHeart**

Your Trad-Chem LLM is now fully integrated with the [TradChem Database](https://github.com/INSTITUTE-OF-SCIENTIFIC-INFORMATICS/Trad-Chem.git) and powered by Google Gemini Flash!

## 🎉 What's Been Accomplished:

✅ **Switched from OpenAI to Google Gemini Flash**
✅ **Integrated TradChem Database** from Institute of Scientific Informatics  
✅ **Enhanced Chemical Data Processing** with SMILES notations
✅ **Traditional Medicine Knowledge Base** with plant compositions
✅ **Smart Context Injection** for relevant data enhancement
✅ **Apple Design-inspired UI** with modern interface

## 🚀 Quick Start (1-2-3 Steps):

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install TradChem Database
```bash
pip install git+https://github.com/INSTITUTE-OF-SCIENTIFIC-INFORMATICS/Trad-Chem.git
```

### 3. Launch the Chatbot
```bash
python run.py
# OR
streamlit run app.py
```

### 4. Access Your Chatbot
Open browser: `http://localhost:8501`

## 🧪 TradChem Database Features:

### 🌿 **Traditional Medicine Data**
- **Plant Database**: Scientific names, traditional systems, geographic origins
- **Chemical Compositions**: SMILES notations, molecular formulas, weights
- **Therapeutic Benefits**: Traditional uses and disease treatments
- **Cultural Systems**: Ayurveda, Traditional Chinese Medicine, etc.

### 🔍 **Smart Search Capabilities**
- **Plant Search**: Find by common/scientific name
- **Compound Search**: Search chemical structures and SMILES
- **Disease Search**: Plants traditionally used for specific conditions
- **System Search**: Filter by traditional medicine systems
- **Geographic Search**: Plants by region/origin

## 💬 Example Questions to Try:

### 🌿 **Traditional Medicine Queries:**
- "What are the chemical compounds in turmeric and their SMILES notations?"
- "Show me Ayurvedic plants used for inflammation"
- "What traditional Chinese medicines help with digestive issues?"
- "Which plants from India have anti-inflammatory properties?"

### 🧪 **Chemical Structure Questions:**
- "What is the molecular structure of curcumin?"
- "Explain the SMILES notation for gingerol"
- "What is the molecular weight of azadirachtin?"
- "Compare the structures of curcumin and demethoxycurcumin"

### 📚 **General Chemistry:**
- "Explain aromatic compounds in traditional medicines"
- "How do plant alkaloids work therapeutically?"
- "What makes essential oils chemically active?"

## 🔧 Configuration Details:

### **API Configuration**
- **LLM Model**: Google Gemini Flash (gemini-1.5-flash)
- **API Key**: Pre-configured (AIzaSyByhZlRTeRKYrF1F42T0LJvth2XshH8PIQ)
- **Temperature**: 0.7 (adjustable in sidebar)
- **Max Tokens**: 2000 (adjustable in sidebar)

### **Chemical Database**
- **Package**: TradChem
- **Repository**: https://github.com/INSTITUTE-OF-SCIENTIFIC-INFORMATICS/Trad-Chem.git
- **Data Format**: Plants, compounds, SMILES, traditional systems
- **Auto-loading**: Configured in `chemical_data_config.py`

## 📁 Project Structure:

```
Trad-Chem-LLM/
├── app.py                        # Main Streamlit app with Gemini integration
├── config.py                     # Gemini API and app configuration
├── chemical_data_config.py       # TradChem database settings
├── run.py                        # Application launcher
├── test_setup.py                 # Setup verification script
├── requirements.txt              # All dependencies including TradChem
├── env_template.txt              # Environment variables template
├── utils/
│   ├── __init__.py              # Package initializer
│   ├── llm_handler.py           # Gemini API integration
│   └── chemical_data_handler.py # TradChem database integration
├── SETUP_GUIDE.md              # This comprehensive guide
├── README.md                    # Project documentation
├── .gitignore                   # Git ignore rules
└── LICENSE                      # License file
```

## 🎯 Key Integration Features:

### **Automatic Data Enhancement**
- User queries are automatically enhanced with relevant TradChem data
- Context injection includes plants, compounds, and traditional uses
- SMILES notations and molecular data provided when relevant

### **Sidebar Features**
- **API Status**: Shows Gemini connection status
- **Chemical Database Status**: Shows TradChem data loading status
- **Model Settings**: Adjustable temperature and max tokens
- **Chat Management**: Clear history, export conversations
- **Data Integration Info**: Current TradChem configuration

### **Smart Response Generation**
- Gemini Flash LLM with chemistry-focused system prompts
- Traditional medicine knowledge integration
- SMILES notation support and validation
- Cultural and geographic context awareness

## 🔍 Testing Your Setup:

### **1. Run Setup Test**
```bash
python test_setup.py
```

Expected output:
```
🧪 Trad-Chem LLM Setup Test
========================================
✅ Streamlit OK
✅ Gemini API OK
✅ Config OK
✅ LLM Handler OK
✅ TradChem Package OK
```

### **2. Verify Database Loading**
1. Launch the application: `python run.py`
2. Check sidebar for "🧪 Chemical Database" status
3. Should show "✅ Chemical Data Loaded" with plant/compound counts

### **3. Test Chemical Queries**
Try asking: "What is the SMILES notation for curcumin?"
Expected: Detailed response with chemical structure and traditional medicine context

## 🐛 Troubleshooting:

### **TradChem Package Issues**
```bash
# Reinstall TradChem if needed
pip uninstall tradchem
pip install git+https://github.com/INSTITUTE-OF-SCIENTIFIC-INFORMATICS/Trad-Chem.git
```

### **Dependencies Issues**
```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

### **API Issues**
- Check sidebar for "🔌 API Status"
- Verify Gemini API key in configuration
- Check internet connectivity

## 🎯 Next Steps:

Your Trad-Chem LLM is now fully operational with:
- **Google Gemini Flash** for intelligent responses
- **TradChem Database** for comprehensive traditional medicine data
- **Smart Chemical Context** for enhanced accuracy
- **SMILES Notation Support** for chemical structures
- **Traditional Medicine Systems** integration

Start chatting about traditional chemistry, plant medicines, chemical structures, and SMILES notations!

---

🧪 **Trad-Chem LLM** | Powered by TradChem Database & Google Gemini Flash | @author SaltyHeart