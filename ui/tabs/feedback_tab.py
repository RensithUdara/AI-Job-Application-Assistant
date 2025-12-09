"""
Feedback Tab - User feedback submission and viewing interface.
"""

import streamlit as st
from ui.modals import display_feedback_modal, display_feedback_stats, display_recent_feedback


def display_feedback_tab():
    """Display feedback tab with submission form and statistics."""
    st.markdown("# 💬 User Feedback & Support")
    
    # Back button
    col1, col2, col3 = st.columns([1, 10, 1])
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.show_feedback = False
            st.rerun()
    
    st.markdown("---")
    
    # Create tabs for feedback form and statistics
    tab1, tab2, tab3 = st.tabs([
        "📝 Submit Feedback",
        "📊 Feedback Statistics",
        "💭 Recent Feedback"
    ])
    
    with tab1:
        st.markdown("## Submit Your Feedback")
        st.markdown(
            "Your feedback is invaluable! Help us improve the AI Job Application Assistant "
            "by sharing your experience, reporting bugs, or suggesting features."
        )
        st.markdown("---")
        display_feedback_modal()
    
    with tab2:
        st.markdown("## Feedback Statistics")
        st.markdown(
            "See what other users are saying and the overall satisfaction metrics."
        )
        st.markdown("---")
        display_feedback_stats()
    
    with tab3:
        st.markdown("## Recent Feedback")
        st.markdown(
            "View the latest feedback from our user community."
        )
        st.markdown("---")
        display_recent_feedback(limit=20)
