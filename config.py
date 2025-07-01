import os
from dotenv import load_dotenv

# @author SaltyHeart
# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for Trad-Chem LLM chatbot"""
    
    # API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyBoYS2l7AydcTx1AahU9VP7uSmbtMVgAxE')
    
    # Application Settings
    APP_TITLE = os.getenv('APP_TITLE', 'Trad-Chem LLM')
    APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
    
    # Model Configuration
    DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'gemini-1.5-flash')
    DEFAULT_TEMPERATURE = float(os.getenv('DEFAULT_TEMPERATURE', '0.7'))
    DEFAULT_MAX_TOKENS = int(os.getenv('DEFAULT_MAX_TOKENS', '2000'))
    
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