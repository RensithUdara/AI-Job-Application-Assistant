"""
Resume Structure Tab Module
Displays resume structure analysis including section completeness and quality scoring.
"""

import streamlit as st
import plotly.express as px
from typing import Dict
from ui.components import get_section_status_icon

def display_structure_tab(resume_data: Dict):
    """Display resume structure analysis."""
    st.header("📋 Resume Structure Analysis")
    
    # Section completeness
    sections_found = resume_data.get('sections_found', {})
    missing_sections = resume_data.get('missing_sections', [])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Section Completeness")
        
        for section, present in sections_found.items():
            status_icon = get_section_status_icon(present)
            section_name = section.replace('_', ' ').title()
            
            if present:
                st.success(f"{status_icon} {section_name}")
            else:
                st.error(f"{status_icon} {section_name}")
    
    with col2:
        # Section completeness pie chart
        present_count = sum(sections_found.values())
        total_count = len(sections_found)
        missing_count = total_count - present_count
        
        fig = px.pie(
            values=[present_count, missing_count],
            names=['Present', 'Missing'],
            title="Resume Completeness",
            color_discrete_map={'Present': '#28a745', 'Missing': '#dc3545'}
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, width='stretch')
    
    # Contact information quality
    st.subheader("Contact Information")
    contact_info = resume_data.get('contact_info', {})
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        email_status = "✅ Valid" if contact_info.get('valid_email') else "❌ Missing/Invalid"
        st.metric("Email", email_status)
    
    with col2:
        phone_status = "✅ Present" if contact_info.get('has_phone') else "❌ Missing"
        st.metric("Phone", phone_status)
    
    with col3:
        linkedin_status = "✅ Present" if contact_info.get('has_linkedin') else "❌ Missing"
        st.metric("LinkedIn", linkedin_status)
    
    # Resume quality score breakdown
    st.subheader("Quality Score Breakdown")
    quality_score = resume_data.get('quality_score', 0)
    
    progress_col, info_col = st.columns([2, 1])
    
    with progress_col:
        st.progress(quality_score / 100)
        
        if quality_score >= 80:
            st.success(f"Excellent resume quality: {quality_score}/100")
        elif quality_score >= 60:
            st.warning(f"Good resume quality: {quality_score}/100")
        else:
            st.error(f"Needs improvement: {quality_score}/100")
    
    with info_col:
        st.info("""
        **Quality factors:**
        - Section completeness
        - Contact information
        - Skills diversity
        - Overall structure
        """)
    
    # Consistency Analysis (New Advanced Feature)
    if 'consistency_analysis' in resume_data:
        st.subheader("📏 Resume Consistency Analysis")
        consistency = resume_data['consistency_analysis']
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Consistency Score", f"{consistency['consistency_score']}/100")
        with col2:
            st.info(consistency['consistency_level'])
        
        if consistency['issues_found']:
            st.warning("**Consistency Issues Found:**")
            for issue in consistency['issues_found']:
                st.write(f"• {issue}")
                
            st.info("**Recommendations:**")
            for rec in consistency['recommendations']:
                st.write(f"• {rec}")