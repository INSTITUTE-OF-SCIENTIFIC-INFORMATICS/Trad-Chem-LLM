import google.generativeai as genai
import streamlit as st
from config import Config
from .chemical_data_handler import ChemicalDataHandler

# @author SaltyHeart

class LLMHandler:
    """Handler for Large Language Model API interactions using Google Gemini"""
    
    def __init__(self, chemical_repo_url=None, chemical_package_name=None):
        """Initialize the LLM handler with Gemini API configuration"""
        self.model = None
        self.chemical_handler = ChemicalDataHandler(chemical_repo_url, chemical_package_name)
        self.setup_client()
    
    def setup_client(self):
        """Setup Gemini client if API key is available"""
        try:
            if Config.GEMINI_API_KEY:
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.model = genai.GenerativeModel(Config.DEFAULT_MODEL)
                st.success("✅ Gemini API connected successfully")
            else:
                st.warning("⚠️ Gemini API key not configured. Please set your API key in the .env file.")
        except Exception as e:
            st.error(f"❌ Error setting up Gemini API: {str(e)}")
    
    def generate_response(self, user_message, chat_history=None, temperature=None, max_tokens=None):
        """Generate response using Gemini Flash with integrated chemical data"""
        if not self.model:
            return "Please configure your Gemini API key to enable AI responses."
        
        try:
            # Prepare the prompt with system instructions and chat history
            prompt_parts = [Config.SYSTEM_PROMPT, "\n\n"]
            
            # Enhance prompt with relevant chemical data
            chemical_context = self.chemical_handler.enhance_llm_prompt(user_message)
            if chemical_context:
                prompt_parts.append("CHEMICAL DATABASE CONTEXT:\n")
                prompt_parts.append(chemical_context)
                prompt_parts.append("\n")
            
            # Add chat history for context if provided
            if chat_history:
                for message in chat_history[-6:]:  # Last 6 messages for context
                    role = "User" if message["role"] == "user" else "Assistant"
                    prompt_parts.append(f"{role}: {message['content']}\n")
            
            # Add current user message
            prompt_parts.append(f"User: {user_message}\nAssistant: ")
            
            full_prompt = "".join(prompt_parts)
            
            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                temperature=temperature or Config.DEFAULT_TEMPERATURE,
                max_output_tokens=max_tokens or Config.DEFAULT_MAX_TOKENS,
                top_p=0.95,
                top_k=64
            )
            
            # Generate response
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
        return self.model is not None and Config.GEMINI_API_KEY 