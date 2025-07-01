import os
import streamlit as st

# @author SaltyHeart
# Configuration optimized for Streamlit Community Cloud deployment

class Config:
    """Configuration class for Trad-Chem LLM chatbot - Streamlit Cloud optimized"""
    
    # API Configuration - uses Streamlit secrets management
    @staticmethod
    def get_gemini_api_key():
        """Get Gemini API key from Streamlit secrets or environment"""
        try:
            # Try Streamlit secrets first (for cloud deployment)
            return st.secrets["GEMINI_API_KEY"]
        except:
            # Fallback to environment variable (for local development)
            return os.getenv('GEMINI_API_KEY', 'AIzaSyBoYS2l7AydcTx1AahU9VP7uSmbtMVgAxE')
    
    # Application Settings
    APP_TITLE = 'Trad-Chem LLM'
    APP_VERSION = '1.0.0'
    DEBUG_MODE = False
    
    # Model Configuration
    DEFAULT_MODEL = 'gemini-1.5-flash'
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_MAX_TOKENS = 2000
    
    # Chemistry-specific prompts
    SYSTEM_PROMPT = """You are Trad-Chem LLM, a specialized AI assistant for traditional chemistry and medicinal plants.
    You have extensive knowledge in:
    - Organic chemistry, inorganic chemistry, physical chemistry, analytical chemistry, and biochemistry
    - Traditional medicinal plants and their chemical compositions
    - SMILES notations and molecular structures
    - Plant-based therapeutic compounds and their benefits
    - Chemical analysis of natural products
    
    When responding to questions, utilize the integrated chemical database to provide accurate information about 
    plant species, their chemical compositions, therapeutic benefits, and associated diseases they treat.
    Always prioritize safety and best practices in chemical procedures and traditional medicine usage.""" 