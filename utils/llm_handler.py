import google.generativeai as genai
import streamlit as st
from config import Config
from .clean_tradchem_handler import CleanTradChemHandler as TradChemHandler

# @author Anu Gamage
# LinkedIn: https://www.linkedin.com/in/anu-gamage-62192b201/

class LLMHandler:
    """Handler for Large Language Model API interactions using Google Gemini Flash with TradChem integration"""
    
    def __init__(self, chemical_repo_url=None, chemical_package_name=None):
        """Initialize the LLM handler with Gemini API and TradChem integration"""
        self.model = None
        self.tradchem_handler = TradChemHandler()
        
        # Ensure TradChem database is loaded
        if not self.tradchem_handler.is_loaded:
            st.info("🔄 Loading TradChem database for LLM integration...")
            load_success = self.tradchem_handler.load_database()
            if load_success:
                st.success("✅ TradChem database loaded for LLM integration")
            else:
                st.warning("⚠️ TradChem database loading failed, using sample data")
        
        self.setup_client()
    
    def setup_client(self):
        """Setup Gemini client if API key is available"""
        try:
            api_key = Config.get_gemini_api_key()
            if api_key:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel(Config.DEFAULT_MODEL)
                st.success("✅ Gemini Flash API connected successfully")
            else:
                st.warning("⚠️ Gemini API key not configured. Please set GEMINI_API_KEY in Streamlit secrets.")
        except Exception as e:
            st.error(f"❌ Error setting up Gemini API: {str(e)}")
    
    def generate_response(self, user_message, chat_history=None, temperature=None, max_tokens=None):
        """Generate response using Gemini Flash with integrated TradChem data"""
        if not self.model:
            return "Please configure your Gemini API key to enable AI responses."
        
        try:
            # Get traditional medicine context from TradChem
            tradchem_context = self.tradchem_handler.query_for_llm(user_message, context_limit=5)
            
            # Check if specific TradChem data was found
            has_specific_data = (tradchem_context and 
                               len(tradchem_context) > 200 and 
                               "TRADITIONAL MEDICINE DATABASE CONTEXT" in tradchem_context and
                               "No specific traditional medicine data found" not in tradchem_context)
            
            if has_specific_data:
                # Extract medicine names from context for display
                lines = tradchem_context.split('\n')
                medicine_lines = [line for line in lines if line.strip() and 
                                line[0].isdigit() and '.' in line[:5]]
                if medicine_lines:
                    medicine_names = [line.split('.', 1)[1].strip() for line in medicine_lines[:3]]
                    st.success(f"✅ Found TradChem data: {', '.join(medicine_names)}")
                else:
                    st.success(f"✅ Found relevant TradChem data ({len(tradchem_context)} characters)")
            else:
                # Check if it's a suggestions response
                if "TRY THESE QUERIES INSTEAD" in tradchem_context:
                    st.info("💡 Showing available TradChem data and suggested queries")
                else:
                    st.warning("⚠️ No specific TradChem data found for this query, using general knowledge")
            
            # Prepare the enhanced prompt
            prompt_parts = []
            
            # Add system prompt
            prompt_parts.append(Config.SYSTEM_PROMPT)
            prompt_parts.append("\n\n")
            
            # Add TradChem context if available
            if tradchem_context and len(tradchem_context) > 100:
                prompt_parts.append("TRADITIONAL MEDICINE DATABASE CONTEXT:")
                prompt_parts.append(tradchem_context)
                prompt_parts.append("\n")
                
                if has_specific_data:
                    prompt_parts.append("Instructions: Use the traditional medicine data above to provide accurate, evidence-based responses. ")
                    prompt_parts.append("Include specific plant names, scientific names, benefits, and traditional usage when relevant. ")
                    prompt_parts.append("If chemical compounds or SMILES notations are mentioned, explain them clearly.\n\n")
                else:
                    prompt_parts.append("Instructions: The above shows available data in the TradChem database. ")
                    prompt_parts.append("If the user's query is not covered by available data, suggest they try the recommended queries ")
                    prompt_parts.append("or explain that the database is expanding and their topic may be added in future updates.\n\n")
            
            # Add chat history for context if provided
            if chat_history:
                prompt_parts.append("CHAT HISTORY:\n")
                for message in chat_history[-6:]:  # Last 6 messages for context
                    role = "User" if message["role"] == "user" else "Assistant"
                    prompt_parts.append(f"{role}: {message['content']}\n")
                prompt_parts.append("\n")
            
            # Add current user message
            prompt_parts.append(f"Current User Question: {user_message}")
            prompt_parts.append("\n\nAssistant Response:")
            
            full_prompt = "".join(prompt_parts)
            
            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                temperature=temperature or Config.DEFAULT_TEMPERATURE,
                max_output_tokens=max_tokens or Config.DEFAULT_MAX_TOKENS,
                top_p=0.95,
                top_k=64
            )
            
            # Generate response using Gemini Flash
            response = self.model.generate_content(
                full_prompt,
                generation_config=generation_config
            )
            
            return response.text
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            return "Sorry, I encountered an error while processing your request. Please try again."
    
    def is_available(self):
        """Check if Gemini service is available"""
        return self.model is not None and Config.get_gemini_api_key()
    
    def get_tradchem_status(self):
        """Get TradChem integration status"""
        return {
            'available': self.tradchem_handler.tradchem_available,
            'loaded': self.tradchem_handler.is_loaded,
            'stats': self.tradchem_handler.get_database_info()
        }
    
    def test_tradchem_integration(self):
        """Test TradChem integration"""
        return self.tradchem_handler.test_integration()
    
    def search_traditional_medicine(self, query: str, search_type: str = 'general'):
        """Search traditional medicine database"""
        if search_type == 'benefits':
            return self.tradchem_handler.search_by_benefits(query)
        elif search_type == 'disease':
            return self.tradchem_handler.search_by_disease(query)
        elif search_type == 'system':
            return self.tradchem_handler.search_by_system(query)
        else:
            # General search using LLM query
            context = self.tradchem_handler.query_for_llm(query, context_limit=10)
            return context 