import streamlit as st
import os
from datetime import datetime
import json
from utils.llm_handler import LLMHandler
from config import Config
from chemical_data_config import CHEMICAL_PACKAGE_NAME, CHEMICAL_REPO_URL

# @author SaltyHeart
# Page configuration for the Trad-Chem LLM chatbot
st.set_page_config(
    page_title="Trad-Chem LLM",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Apple Design style
st.markdown("""
<style>
    .main {
        padding: 1rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }
    
    .stButton > button {
        border-radius: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 8px 16px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Initialize LLM handler with chemical data integration
if 'llm_handler' not in st.session_state:
    st.session_state.llm_handler = LLMHandler(
        chemical_repo_url=CHEMICAL_REPO_URL,
        chemical_package_name=CHEMICAL_PACKAGE_NAME
    )

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Initialize model configuration
if 'model_config' not in st.session_state:
    st.session_state.model_config = {
        'temperature': Config.DEFAULT_TEMPERATURE,
        'max_tokens': Config.DEFAULT_MAX_TOKENS
    }

# Sidebar configuration
with st.sidebar:
    st.title("🧪 Trad-Chem LLM")
    st.markdown(f"**Version:** {Config.APP_VERSION}")
    st.markdown("---")
    
    # Model settings
    st.subheader("⚙️ Model Settings")
    temperature = st.slider(
        "Temperature", 
        0.0, 2.0, 
        st.session_state.model_config['temperature'], 
        0.1,
        help="Controls randomness in responses"
    )
    max_tokens = st.slider(
        "Max Tokens", 
        100, 4000, 
        st.session_state.model_config['max_tokens'], 
        100,
        help="Maximum length of AI response"
    )
    
    # Update configuration
    st.session_state.model_config['temperature'] = temperature
    st.session_state.model_config['max_tokens'] = max_tokens
    
    st.markdown("---")
    
    # Chat management
    st.subheader("💬 Chat Management")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    # Export chat history
    if st.button("💾 Export Chat") and st.session_state.messages:
        chat_export = {
            'timestamp': datetime.now().isoformat(),
            'messages': st.session_state.messages,
            'config': st.session_state.model_config
        }
        st.download_button(
            label="📥 Download Chat Log",
            data=json.dumps(chat_export, ensure_ascii=False, indent=2),
            file_name=f"trad_chem_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    st.markdown("---")
    
    # API Status
    st.subheader("🔌 API Status")
    if st.session_state.llm_handler.is_available():
        st.success("✅ Gemini Connected")
    else:
        st.error("❌ Not Connected")
        st.info("Please configure your Gemini API key in the .env file")
    
    st.markdown("---")
    
    # Chemical Data Status
    st.subheader("🧪 Chemical Database")
    chemical_handler = st.session_state.llm_handler.chemical_handler
    
    if chemical_handler.is_loaded:
        st.success("✅ Chemical Data Loaded")
        plants_count = len(chemical_handler.data_cache.get('plants', {}))
        compounds_count = len(chemical_handler.data_cache.get('compounds', {}))
        st.info(f"📊 {plants_count} plants, {compounds_count} compounds")
    else:
        st.warning("⚠️ Using Sample Data")
        if st.button("🔄 Load Chemical Data"):
            with st.spinner("Loading chemical database..."):
                success = chemical_handler.load_chemical_data()
                if success:
                    st.rerun()
    
    # Data integration info
    with st.expander("📖 Chemical Data Integration"):
        st.markdown("""
        **To integrate your chemical repository:**
        
        1. Edit `chemical_data_config.py`
        2. Set your package name or repository URL
        3. Restart the application
        
        **Current Configuration:**
        """)
        
        if CHEMICAL_PACKAGE_NAME:
            st.code(f"Package: {CHEMICAL_PACKAGE_NAME}")
        elif CHEMICAL_REPO_URL:
            st.code(f"Repository: {CHEMICAL_REPO_URL}")
        else:
            st.code("Using sample data")

# Main interface
st.title("🧪 Trad-Chem LLM")
st.markdown("### Traditional Chemistry Large Language Model Assistant")
st.markdown("Ask questions about organic chemistry, inorganic chemistry, physical chemistry, analytical chemistry, and biochemistry.")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask your chemistry question here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("🧪 Thinking..."):
            # Get chat history for context (last 10 messages)
            recent_history = st.session_state.messages[-10:] if len(st.session_state.messages) > 1 else []
            
            # Generate response using LLM handler
            response = st.session_state.llm_handler.generate_response(
                user_message=prompt,
                chat_history=recent_history[:-1],  # Exclude the current user message
                temperature=st.session_state.model_config['temperature'],
                max_tokens=st.session_state.model_config['max_tokens']
            )
        
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🧪 Trad-Chem LLM | @author SaltyHeart</p>
    <p>Specialized AI Assistant for Traditional Chemistry</p>
</div>
""", unsafe_allow_html=True)