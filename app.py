import streamlit as st
import os
from datetime import datetime
import json
from utils.llm_handler import LLMHandler
from utils.contributors_handler import contributors_handler
from config import Config

# @author Anu Gamage
# LinkedIn: https://www.linkedin.com/in/anu-gamage-62192b201/
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

# Initialize LLM handler with TradChem integration
if 'llm_handler' not in st.session_state:
    st.session_state.llm_handler = LLMHandler()

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
    st.markdown("**Developed and maintained by Anu Gamage and Trad-Chem Community [Institute of Scientific Informatics, Sri Lanka]**")
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
        st.info("Please configure your Gemini API key in Streamlit secrets")
    
    st.markdown("---")
    
    # TradChem Database Status
    st.subheader("🌿 TradChem Database")
    tradchem_status = st.session_state.llm_handler.get_tradchem_status()
    
    if tradchem_status['available']:
        st.success("✅ TradChem Connected")
        if tradchem_status['loaded']:
            stats = tradchem_status['stats']
            st.info(f"📊 {stats.get('total_medicines', 0)} medicines")
            st.info(f"🏛️ {len(stats.get('traditional_systems', []))} traditional systems")
        else:
            if st.button("🔄 Load TradChem Database"):
                with st.spinner("Loading TradChem database..."):
                    success = st.session_state.llm_handler.tradchem_handler.load_database()
                    if success:
                        st.rerun()
    else:
        st.warning("⚠️ TradChem Not Available")
        st.info("Using enhanced sample data")
    
    # TradChem integration info
    with st.expander("📖 TradChem Integration"):
        st.markdown("""
        **TradChem Database Integration:**
        
        The chatbot integrates with the comprehensive TradChem database containing:
        - Traditional medicine data from multiple systems
        - Chemical compositions with SMILES notations
        - Benefits and disease treatment information
        - Geographic and cultural context
        
        **Status:**
        """)
        
        if tradchem_status['available']:
            st.success("✅ TradChem database connected")
            stats = tradchem_status['stats']
            if stats:
                st.write(f"**Medicines:** {stats.get('total_medicines', 'N/A')}")
                st.write(f"**Systems:** {', '.join(stats.get('traditional_systems', [])[:3])}")
                st.write(f"**Regions:** {', '.join(stats.get('geographic_regions', [])[:3])}")
        else:
            st.warning("⚠️ TradChem not found")
            st.write("Ensure Trad-Chem directory is present in project root")
    
    # Contributors section
    with st.expander("👥 Contributors & Credits"):
        contributors_data = contributors_handler.get_all_contributors()
        
        # Lead Developer
        lead_dev = contributors_data.get('lead_developer', {})
        if lead_dev:
            st.markdown("### 🚀 Lead Developer")
            st.markdown(f"**{lead_dev.get('name', 'Unknown')}**")
            st.markdown(f"*{lead_dev.get('role', 'Developer')}*")
            if lead_dev.get('linkedin'):
                st.markdown(f"[LinkedIn Profile]({lead_dev['linkedin']})")
            if lead_dev.get('bio'):
                st.write(lead_dev['bio'])
            
            if lead_dev.get('contributions'):
                st.markdown("**Key Contributions:**")
                for contribution in lead_dev['contributions'][:3]:  # Show first 3
                    st.write(f"• {contribution}")
        
        # Core Contributors
        core_contributors = contributors_data.get('core_contributors', [])
        if core_contributors:
            st.markdown("### 🏛️ Core Contributors")
            for contributor in core_contributors:
                st.markdown(f"**{contributor.get('name', 'Unknown')}**")
                st.markdown(f"*{contributor.get('role', 'Contributor')}*")
                if contributor.get('organization'):
                    st.write(f"📍 {contributor['organization']}")
                if contributor.get('bio'):
                    st.write(contributor['bio'])
                
                # Display team members if available
                team_members = contributor.get('team_members', [])
                if team_members:
                    st.markdown("**🌟 Team Members:**")
                    for member in team_members:
                        member_name = member.get('name', 'Unknown')
                        member_role = member.get('role', 'Contributor')
                        if member.get('highlighted', False):
                            # Highlight important team members
                            st.markdown(f"⭐ **{member_name}** - *{member_role}*")
                        else:
                            st.markdown(f"• **{member_name}** - *{member_role}*")
                st.markdown("")
        
        # Acknowledgments
        acknowledgments = contributors_data.get('acknowledgments', [])
        if acknowledgments:
            st.markdown("### 🙏 Special Acknowledgments")
            for ack in acknowledgments:
                st.write(f"**{ack.get('name', 'Unknown')}** - {ack.get('contribution', 'Support')}")
        
        # How to Contribute
        contrib_guide = contributors_data.get('how_to_contribute', {})
        if contrib_guide:
            st.markdown("### 🤝 How to Contribute")
            st.write("We welcome contributions! Ways to get involved:")
            for key, value in contrib_guide.items():
                if key != 'contact':
                    st.write(f"• **{key.replace('_', ' ').title()}**: {value}")
            
            if contrib_guide.get('contact'):
                st.info(f"💬 Contact: {contrib_guide['contact']}")
        
        # Project Info
        project_info = contributors_data.get('project_info', {})
        if project_info:
            st.markdown("### 📄 Project Information")
            st.write(f"**Organization**: {project_info.get('organization', 'N/A')}")
            st.write(f"**License**: {project_info.get('license', 'N/A')}")
            if project_info.get('repository'):
                st.markdown(f"[View on GitHub]({project_info['repository']})")

# Main interface
st.title("🧪 Trad-Chem LLM")
st.markdown("### Traditional Chemistry Large Language Model Assistant")
st.markdown("Ask questions about product name, benefits, diseases, chemical composition and SMILES notations for plant species commonly employed in traditional medicinal practices.")

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
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🧪 Trad-Chem LLM | @author Anu Gamage</p>
    <p>Specialized AI Assistant for Traditional Chemistry</p>
</div>
""", unsafe_allow_html=True)