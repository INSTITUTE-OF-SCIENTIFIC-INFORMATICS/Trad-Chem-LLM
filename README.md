# 🧪 Trad-Chem LLM

Traditional Chemistry Large Language Model Chatbot

**@author SaltyHeart**

## 📖 Description

Trad-Chem LLM is a specialized AI chatbot designed for traditional chemistry education and research. It provides expert-level assistance in organic chemistry, inorganic chemistry, physical chemistry, analytical chemistry, and biochemistry.

## ✨ Features

- 🎯 Specialized chemistry knowledge base with traditional medicine focus
- 🧪 **Integrated Chemical Database** - Connect your own chemical data repository
- 🌿 **Traditional Plant Medicine** - Comprehensive plant chemical compositions and benefits
- 🧬 **SMILES Notation Support** - Chemical structure representations
- 💬 Interactive chat interface powered by Google Gemini Flash
- ⚙️ Configurable AI model parameters
- 📊 Chat history export and management
- 🎨 Modern Apple Design-inspired UI
- 🔒 Secure API key management
- 📱 Responsive web interface
- 🔍 **Smart Data Integration** - Automatically enhances responses with relevant chemical data

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Trad-Chem-LLM
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   # Copy the template file
   copy env_template.txt .env
   
   # Edit .env file and add your Gemini API key
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```

3.1. **TradChem Database Integration** (Already configured!)
   ```bash
   # The TradChem package is already configured in chemical_data_config.py
   # Repository: https://github.com/INSTITUTE-OF-SCIENTIFIC-INFORMATICS/Trad-Chem.git
   # Package: tradchem
   ```

4. **Run the application**
   ```bash
   # Option 1: Using the launcher script
   python run.py
   
   # Option 2: Direct Streamlit command
   streamlit run app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:8501`

## 📁 Project Structure

```
Trad-Chem-LLM/
├── app.py                        # Main Streamlit application
├── config.py                     # Configuration management
├── chemical_data_config.py       # Chemical database integration config
├── run.py                        # Application launcher
├── requirements.txt              # Python dependencies
├── env_template.txt              # Environment variables template
├── utils/
│   ├── __init__.py              # Package initializer
│   ├── llm_handler.py           # Gemini API interaction handler
│   └── chemical_data_handler.py # Chemical database integration
├── README.md                    # Project documentation
├── .gitignore                   # Git ignore rules
└── LICENSE                      # License file
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# API Configuration
GEMINI_API_KEY=your_gemini_api_key

# App Settings
APP_TITLE=Trad-Chem LLM
APP_VERSION=1.0.0
DEBUG_MODE=False

# Model Configuration
DEFAULT_MODEL=gemini-1.5-flash
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=2000
```

### TradChem Database Integration ✅ **PRE-CONFIGURED**

Your chatbot is already integrated with the [**TradChem Database**](https://github.com/INSTITUTE-OF-SCIENTIFIC-INFORMATICS/Trad-Chem.git) from the Institute of Scientific Informatics!

#### 🧪 **What's Included:**

- **Comprehensive Plant Database**: Traditional medicinal plants with scientific names
- **Chemical Compositions**: SMILES notations and molecular structures
- **Traditional Medicine Systems**: Ayurveda, Traditional Chinese Medicine, etc.
- **Geographic Origins**: Plant sources from around the world
- **Therapeutic Benefits**: Traditional uses and disease treatments
- **Chemical Analysis**: Molecular formulas, weights, and properties

#### 📊 **TradChem Data Structure:**

```python
{
    "plants": {
        "turmeric_extract": {
            "scientific_name": "Curcuma longa",
            "traditional_system": "Ayurveda",
            "geographic_origin": "India",
            "compounds": ["curcumin", "demethoxycurcumin"],
            "benefits": ["Anti-inflammatory", "Antioxidant"],
            "diseases": ["Arthritis", "Digestive disorders"]
        }
    },
    "compounds": {
        "curcumin": {
            "smiles": "COC1=CC(\\C=C\\C(=O)CC(=O)\\C=C\\C2=CC(OC)=C(O)C=C2)=CC(OC)=C1O",
            "molecular_formula": "C21H20O6",
            "molecular_weight": 368.38,
            "source_plants": ["turmeric_extract"]
        }
    }
}
```

#### 🔧 **Auto-Enhancement Features:**

- **Smart Context Injection**: Automatically finds relevant plant/compound data for user queries
- **Traditional System Search**: Filters by Ayurveda, TCM, etc.
- **Geographic Search**: Finds plants by region (India, China, etc.)
- **Disease-Based Search**: Discovers plants traditionally used for specific conditions
- **Chemical Structure Analysis**: SMILES notation validation and molecular properties

### Model Parameters

- **Temperature**: Controls randomness (0.0 = deterministic, 2.0 = very random)
- **Max Tokens**: Maximum length of AI responses
- **Model**: OpenAI model to use (gpt-3.5-turbo, gpt-4, etc.)

## 🎯 Usage Examples

### Chemistry & Traditional Medicine Questions You Can Ask

#### 🌿 **Traditional Medicine Queries:**
- "What are the chemical compounds in turmeric and their SMILES notations?"
- "Show me Ayurvedic plants used for inflammation"
- "What traditional Chinese medicines help with digestive issues?"
- "Which plants from India have anti-inflammatory properties?"
- "What is the molecular structure of curcumin?"

#### 🧪 **Chemistry & SMILES Questions:**
- "Explain the SMILES notation for gingerol"
- "What is the molecular weight of azadirachtin?"
- "Show me the chemical composition of neem extract"
- "Compare the structures of curcumin and demethoxycurcumin"

#### 📚 **General Chemistry Questions:**
- "Explain the mechanism of SN2 reactions"
- "What is the difference between ionic and covalent bonding?"
- "How do you calculate the pH of a buffer solution?"
- "Describe the structure and properties of benzene"

### Features

1. **Chat Interface**: Type your chemistry questions in natural language
2. **History Management**: View, export, and clear chat history
3. **Model Settings**: Adjust AI response parameters in the sidebar
4. **Export Data**: Download chat logs as JSON files

## 🛠️ Development

### Adding New Features

1. **New LLM Providers**: Extend `utils/llm_handler.py`
2. **UI Components**: Modify `app.py` Streamlit components
3. **Configuration**: Update `config.py` for new settings

### Code Structure

- **app.py**: Main Streamlit interface and chat logic
- **config.py**: Configuration management and environment variables
- **utils/llm_handler.py**: LLM API interactions and response generation
- **run.py**: Application launcher with dependency checking

## 📋 Requirements

See `requirements.txt` for detailed dependencies:

- streamlit>=1.28.0
- google-generativeai>=0.3.0
- python-dotenv>=1.0.0
- requests>=2.31.0
- pandas>=2.0.0
- numpy>=1.24.0
- scipy>=1.10.0
- matplotlib>=3.7.0
- seaborn>=0.12.0
- scikit-learn>=1.3.0
- jsonschema>=4.17.0
- pydantic>=2.0.0
- **TradChem Package** (installed from GitHub)

## 🔒 Security

- API keys are stored in environment variables
- .env file is excluded from version control
- No sensitive data is logged or stored persistently

## 🐛 Troubleshooting

### Common Issues

1. **"Module not found" errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **API key not configured**
   - Ensure `.env` file exists with valid `OPENAI_API_KEY`

3. **Port already in use**
   ```bash
   streamlit run app.py --server.port 8502
   ```

4. **Slow responses**
   - Check internet connection
   - Verify OpenAI API status
   - Reduce max_tokens in settings

## 📄 License

This project is licensed under the terms specified in the LICENSE file.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review existing GitHub issues
3. Create a new issue with detailed information

## 🤝 **Acknowledgments**

Special thanks to the [**Institute of Scientific Informatics**](https://github.com/INSTITUTE-OF-SCIENTIFIC-INFORMATICS) for providing the comprehensive [**TradChem Database**](https://github.com/INSTITUTE-OF-SCIENTIFIC-INFORMATICS/Trad-Chem.git) that powers this chatbot's traditional medicine knowledge.

---

**@author SaltyHeart** | Trad-Chem LLM v1.0.0 | **Powered by TradChem Database & Google Gemini Flash**
