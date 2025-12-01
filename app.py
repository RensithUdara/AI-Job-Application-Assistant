"""
AI Job Application Assistant - Main Application
Simplified and modular version with organized UI components.
"""

import streamlit as st
import sys
import os

# Add the core directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

# Import UI modules
from ui.components import setup_page_config, apply_custom_css, display_main_header, display_footer
from ui.sidebar import initialize_session_state, display_sidebar
from ui.modals import display_chat_modal, display_interview_modal, display_templates_modal
from ui.input_section import display_input_section, process_analysis_request
from ui.results_display import display_results

def main():
    """Main application function."""
    # Setup page configuration
    setup_page_config()
    
    # Apply custom CSS
    apply_custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Display sidebar and get settings
    sidebar_settings = display_sidebar()
    
    # Display main header
    display_main_header()
    
    # Display modal dialogs if active
    display_chat_modal()
    display_interview_modal()
    display_templates_modal()
    
    # Display input section
    resume_content, jd_text = display_input_section()
    
    # Analysis button
    if st.button("🔍 Analyze Application", type="primary"):
        results = process_analysis_request(resume_content, jd_text)
        if results:
            # Store settings for analysis customization
            st.session_state.sidebar_settings = sidebar_settings
    
    # Display results if analysis is completed
    if st.session_state.analysis_done and st.session_state.results:
        st.markdown("---")
        display_results(st.session_state.results)
    
    # Display footer
    display_footer()

if __name__ == "__main__":
    main()