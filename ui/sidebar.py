"""
Sidebar Module
Contains all sidebar functionality including navigation, settings, and quick actions.
"""

import streamlit as st

def initialize_session_state():
    """Initialize session state variables."""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'main'
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'analysis_done' not in st.session_state:
        st.session_state.analysis_done = False
    if 'results' not in st.session_state:
        st.session_state.results = {}

def display_sidebar():
    """Display the enhanced sidebar with quick actions and settings."""
    with st.sidebar:
        st.markdown("### 🏠 Navigation")
        
        # Current page indicator
        current_page = st.session_state.get('current_page', 'main')
        
        # Main page
        if st.button("🏠 Main Dashboard", use_container_width=True, disabled=(current_page == 'main')):
            st.session_state.current_page = 'main'
        
        st.markdown("### 🚀 Quick Actions")
        
        # AI Assistant Chat
        if st.button("💬 AI Career Chat", use_container_width=True, disabled=(current_page == 'ai_chat')):
            st.session_state.current_page = 'ai_chat'
        
        # Resume Templates
        if st.button("📄 Resume Templates", use_container_width=True, disabled=(current_page == 'resume_templates')):
            st.session_state.current_page = 'resume_templates'
        
        # Interview Prep
        if st.button("🎤 Mock Interview", use_container_width=True, disabled=(current_page == 'mock_interview')):
            st.session_state.current_page = 'mock_interview'
        
        st.markdown("---")
        
        # Settings
        st.markdown("### ⚙️ Analysis Settings")
        
        analysis_depth = st.selectbox(
            "Analysis Depth:",
            ["Basic", "Comprehensive", "Expert"],
            index=1,
            help="Choose the level of analysis detail"
        )
        
        include_soft_skills = st.checkbox("Include Soft Skills Analysis", value=True)
        include_culture_fit = st.checkbox("Include Culture Fit Analysis", value=True)
        include_salary_insights = st.checkbox("Include Salary Intelligence", value=True)
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("### 📊 Today's Insights")
        st.metric("Jobs Analyzed Today", "1,247", "↗ +12%")
        st.metric("Average Match Score", "78%", "↗ +3%")
        st.metric("Success Rate", "94%", "→ 0%")
        
        st.markdown("---")
        
        # Tips of the day
        st.markdown("### 💡 Daily Tip")
        from ui.components import display_daily_tip
        display_daily_tip()
    
    return {
        'analysis_depth': analysis_depth,
        'include_soft_skills': include_soft_skills,
        'include_culture_fit': include_culture_fit,
        'include_salary_insights': include_salary_insights
    }