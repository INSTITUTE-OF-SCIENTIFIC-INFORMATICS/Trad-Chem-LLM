# 🧪 Trad-Chem LLM - Traditional Chemistry & Medicine AI Assistant

**@author Anu Gamage**  
**LinkedIn:** [https://www.linkedin.com/in/anu-gamage-62192b201/](https://www.linkedin.com/in/anu-gamage-62192b201/)

A specialized AI chatbot powered by Google Gemini Flash and integrated with the comprehensive TradChem database for traditional medicine and chemical knowledge.

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 Features

- **🤖 AI-Powered Chat**: Google Gemini Flash integration for intelligent responses
- **🧪 Chemical Database**: Access to comprehensive traditional medicine data
- **🌿 Traditional Medicine**: Ayurvedic, Traditional Chinese Medicine, and more
- **⚗️ SMILES Notation**: Chemical structure support and molecular data
- **🍎 Apple Design UI**: Clean, modern interface optimized for all devices
- **☁️ Cloud Ready**: Optimized for Streamlit Community Cloud deployment

## 🚀 Quick Deploy to Streamlit Cloud

### Option 1: One-Click Deploy
[![Deploy to Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

1. **Fork this repository** to your GitHub account
2. **Go to [Streamlit Cloud](https://share.streamlit.io)**
3. **Connect your GitHub** account
4. **Create new app** and select your forked repository
5. **Set main file path**: `app.py`
6. **Add your API key** in app settings secrets:
   ```toml
   GEMINI_API_KEY = "your_actual_gemini_api_key"
   ```
7. **Deploy** and your app will be live!

### Option 2: Manual Setup

1. **Clone repository**:
   ```bash
   git clone https://github.com/your-username/Trad-Chem-LLM.git
   cd Trad-Chem-LLM
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure secrets** (copy and edit):
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   # Edit secrets.toml with your actual API key
   ```

4. **Run locally**:
   ```bash
   streamlit run app.py
   ```

## 🔑 API Key Setup

### Get Google Gemini API Key:
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create new API key
3. Copy the key

### For Streamlit Cloud:
1. Go to your app settings
2. Navigate to "Secrets"
3. Add your key:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key_here"
   ```

### For Local Development:
1. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`
2. Add your API key to the file

## 🧪 TradChem Database

The app includes a comprehensive traditional medicine database with:

- **4+ Traditional Medicines**: Kameshwari Rasayana, Ginseng, Turmeric, Ashwagandha
- **Multiple Systems**: Ayurveda, Traditional Chinese Medicine
- **Chemical Data**: Complete SMILES notations and molecular structures
- **Geographic Origins**: India, North America, South Asia
- **17+ Benefits**: Anti-inflammatory, immune support, energy enhancement
- **17+ Disease Treatments**: Arthritis, fatigue, stress disorders

## 🎮 Usage Examples

Try these queries:

### 🌿 Traditional Medicine:
- "What are the chemical compounds in turmeric?"
- "Show me Ayurvedic plants for inflammation"
- "Which Chinese medicines help digestion?"

### 🧪 Chemistry:
- "Explain the SMILES notation for curcumin"
- "What is the molecular structure of gingerol?"
- "Compare curcumin and demethoxycurcumin"

### 📚 General:
- "How do plant alkaloids work?"
- "Explain aromatic compounds in traditional medicines"

## 📁 Project Structure

```
Trad-Chem-LLM/
├── app.py                          # 🎯 Main Streamlit application
├── config.py                       # ⚙️ Configuration management
├── requirements.txt                # 📦 Dependencies for deployment
├── .streamlit/
│   ├── config.toml                # 🛠️ Streamlit configuration
│   └── secrets.toml.example       # 🔑 API key template
├── utils/
│   ├── llm_handler.py             # 🤖 Gemini AI integration
│   └── chemical_data_handler.py   # 🧪 TradChem database
├── Trad-Chem/
│   └── tradchem/
│       └── data/
│           └── tradchem_database.json  # 📊 Medicine database
└── README.md                      # 📖 This documentation
```

## 🔧 Configuration

### Streamlit Cloud Environment Variables:
- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### Optional Customization:
- Modify `config.py` for different model settings
- Update `.streamlit/config.toml` for UI customization
- Edit system prompts in `config.py` for specialized behavior

## 🛠️ Development

### Local Development:
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
streamlit run app.py --server.port=8501

# Access at http://localhost:8501
```

### Adding New Features:
1. **Database Updates**: Modify `Trad-Chem/tradchem/data/tradchem_database.json`
2. **UI Changes**: Edit `app.py` Streamlit components
3. **AI Behavior**: Update system prompts in `config.py`
4. **New Handlers**: Add utilities in `utils/` directory

## 📊 Database Schema

Each medicine entry contains:
```json
{
  "product_name": "Medicine Name",
  "english_name": "English Translation",
  "traditional_system": "Ayurveda/TCM/etc",
  "geographic_origin": "Region",
  "benefits": ["benefit1", "benefit2"],
  "diseases": ["disease1", "disease2"],
  "chemical_composition": {
    "ingredients": {
      "PlantName": {
        "compound1": "SMILES_notation",
        "compound2": "SMILES_notation"
      }
    }
  }
}
```

## 🔒 Security & Privacy

- **API Keys**: Securely managed through Streamlit secrets
- **No Data Storage**: Conversations are not stored permanently
- **Privacy First**: No user tracking or data collection
- **Open Source**: Fully transparent codebase

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **TradChem Database**: [Institute of Scientific Informatics](https://github.com/INSTITUTE-OF-SCIENTIFIC-INFORMATICS/Trad-Chem)
- **Google Gemini**: Powered by Google's advanced AI
- **Streamlit**: For the amazing web framework
- **Traditional Medicine**: Honoring ancient wisdom with modern technology

## 🔗 Links

- **Live Demo**: [Deploy your own](https://share.streamlit.io)
- **TradChem Database**: [Original Repository](https://github.com/INSTITUTE-OF-SCIENTIFIC-INFORMATICS/Trad-Chem)
- **Streamlit Cloud**: [Deployment Platform](https://streamlit.io/cloud)
- **Google Gemini**: [AI Model](https://ai.google.dev)

---

🧪 **Built with ❤️ for Traditional Medicine & Modern Chemistry** | @author Anu Gamage 