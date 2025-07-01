# 🧪 Trad-Chem LLM - Traditional Chemistry Large Language Model

**@author Anu Gamage**

A sophisticated AI chatbot powered by Google Gemini Flash and integrated with the comprehensive TradChem traditional medicine database.

## 🎯 Project Overview

**Trad-Chem LLM** is an advanced AI assistant specialized in traditional chemistry and medicinal plants. It combines the power of Google's Gemini Flash API with real traditional medicine data to provide accurate, evidence-based responses about:

- **Traditional Medicinal Plants** and their chemical compositions
- **SMILES Notations** and molecular structures
- **Plant-based Therapeutic Compounds** and their benefits
- **Chemical Analysis** of natural products
- **Traditional Medicine Systems** (Ayurveda, TCM, etc.)

## ✨ Key Features

### 🤖 AI-Powered Chat Interface
- **Google Gemini Flash Integration** for intelligent responses
- **Apple Design-inspired UI** with modern gradients and styling
- **Real-time Chemistry Assistance** with contextual awareness
- **Smart Context Injection** from TradChem database

### 🌿 TradChem Database Integration
- **Real Traditional Medicine Data** with chemical compositions
- **SMILES Chemical Formulas** for molecular analysis
- **Multi-field Search** by plants, compounds, diseases, benefits
- **Geographic and Cultural Context** for traditional medicines
- **Clean Database Access** bypassing encoding issues

### ⚙️ Advanced Configuration
- **Customizable Model Parameters** (temperature, max tokens)
- **Chat History Management** with export functionality
- **API Status Monitoring** for Gemini and TradChem
- **Comprehensive Error Handling** with fallback options

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API key
- TradChem database (included)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/your-repo/Trad-Chem-LLM.git
cd Trad-Chem-LLM
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure API key:**
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

4. **Run the application:**
```bash
streamlit run app.py
```

5. **Access the application:**
Open your browser and go to `http://localhost:8501`

## 🗄️ TradChem Database

### Integration Status: ✅ **FULLY OPERATIONAL**

The application now uses a **clean TradChem handler** that:
- ✅ Directly accesses the JSON database
- ✅ Bypasses Python module import issues
- ✅ Provides real traditional medicine data
- ✅ Supports SMILES chemical formulas
- ✅ Includes comprehensive plant information

### Sample Database Content:
- **Kameshwari Rasayanaya** - Ayurvedic vitality enhancement
  - Cannabis compounds with SMILES notations
  - Bee honey glucose and fructose
  - Ghee fatty acids
- **Traditional Medicine Systems** - Multiple cultural approaches
- **Chemical Compositions** - Detailed molecular data

## 🔧 Technical Architecture

### Core Components

1. **app.py** - Main Streamlit application with UI
2. **config.py** - Configuration management with Gemini API settings
3. **utils/llm_handler.py** - Google Gemini Flash API integration
4. **utils/clean_tradchem_handler.py** - Clean TradChem database access
5. **utils/chemical_data_handler.py** - Legacy handler with enhanced sample data

### API Integration

- **Google Gemini Flash** (`gemini-1.5-flash`)
  - Temperature control: 0.0 - 2.0
  - Token limits: 100 - 4000
  - Smart context injection from TradChem

### Database Structure

```json
{
  "product_name": "Traditional Medicine Name",
  "benefits": ["Benefit 1", "Benefit 2"],
  "diseases": ["Disease 1", "Disease 2"],
  "chemical_composition": {
    "ingredients": {
      "Ingredient Name": {
        "compound_name": "SMILES_notation"
      }
    }
  }
}
```

## 🧪 Usage Examples

### Basic Chemistry Questions
- "What are the chemical compounds in turmeric?"
- "Explain the SMILES notation for curcumin"
- "What are the benefits of cannabis in traditional medicine?"

### Traditional Medicine Queries
- "Show me Ayurvedic medicines for inflammation"
- "What plants help with digestive disorders?"
- "Explain the traditional use of bee honey compounds"

### Advanced Analysis
- "Compare the molecular structures of different gingerol compounds"
- "What are the geographic origins of anti-inflammatory plants?"
- "Analyze the chemical composition of Kameshwari Rasayanaya"

## 📊 Features & Capabilities

### Chat Interface
- 💬 **Interactive Chat** with memory and context
- 📁 **Export Chat History** in JSON format
- 🗑️ **Clear Chat** functionality
- 🎛️ **Model Configuration** controls

### TradChem Integration
- 🔍 **Smart Search** across multiple fields
- 📈 **Relevance Scoring** for search results
- 🧬 **Chemical Formula Display** with SMILES
- 🌍 **Geographic and Cultural Context**

### Technical Features
- 🔌 **API Status Monitoring**
- ⚡ **Real-time Error Handling**
- 🎨 **Apple Design UI**
- 📱 **Responsive Layout**

## 🛠️ Configuration

### Environment Variables
```env
GEMINI_API_KEY=your_gemini_api_key
APP_TITLE=Trad-Chem LLM
APP_VERSION=1.0.0
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=2000
```

### Model Parameters
- **Temperature**: Controls response creativity (0.0 = focused, 2.0 = creative)
- **Max Tokens**: Maximum response length (100-4000)
- **Context Limit**: Number of TradChem results to include (3-10)

## 🧪 Testing

### Integration Tests
```bash
# Test TradChem integration
python test_clean_integration.py

# Test application setup
python test_setup.py

# Final integration verification
python test_final_integration.py
```

### Expected Results
- ✅ Clean TradChem handler creates successfully
- ✅ Database loads without null bytes issues
- ✅ LLM integration functions properly
- ✅ Real traditional medicine data accessible

## 📁 Project Structure

```
Trad-Chem-LLM/
├── app.py                          # Main Streamlit application
├── config.py                       # Configuration settings
├── requirements.txt                 # Python dependencies
├── utils/
│   ├── llm_handler.py              # Gemini API integration
│   ├── clean_tradchem_handler.py   # Clean TradChem access
│   └── chemical_data_handler.py    # Legacy enhanced handler
├── Trad-Chem/                      # TradChem database
│   └── tradchem/
│       └── data/
│           └── tradchem_database.json
└── tests/                          # Test files
    ├── test_clean_integration.py   # Integration tests
    └── test_setup.py               # Setup verification
```

## 🤝 Contributing

We welcome contributions to expand the traditional medicine database and improve the LLM integration!

### How to Contribute
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Areas
- 🌿 **Traditional Medicine Data** - Add new plants and compounds
- 🧬 **Chemical Analysis** - Improve SMILES notation accuracy
- 🎨 **UI/UX Improvements** - Enhance user interface
- 🔧 **API Integration** - Add new LLM providers

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **TradChem Database** - Comprehensive traditional medicine data
- **Google Gemini Flash** - Advanced language model capabilities
- **Streamlit Community** - Excellent web app framework
- **Traditional Medicine Practitioners** - Invaluable knowledge preservation
- **Open Source Community** - Collaborative development support

## 📞 Support & Contact

- **Issues**: Report bugs via [GitHub Issues](https://github.com/your-repo/issues)
- **Documentation**: Full API documentation available
- **Community**: Join our discussions for feature requests

---

**@author Anu Gamage** | Trad-Chem LLM v1.0.0 | **Powered by TradChem Database & Google Gemini Flash**

*Specialized AI Assistant for Traditional Chemistry and Medicinal Plants*
