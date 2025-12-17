"""
Summary Tab Module
Displays overall application match summary and key metrics.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict
from ui.components import create_gauge_chart

def display_summary_tab(resume_data: Dict, jd_data: Dict, match_data: Dict):
    """Display summary information."""
    st.header("📊 Application Match Summary")
    
    # Overall match score with gauge
    match_score = match_data.get('match_score_overall', 0)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Create gauge chart
        fig = create_gauge_chart(match_score, "Overall Match Score")
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        # Get detected role from resume's role compatibility analysis
        role_compatibility = resume_data.get('role_compatibility', {})
        detected_role = role_compatibility.get('best_match_role', 'Unknown')
        if detected_role:
            detected_role = detected_role.replace('_', ' ').title()
        else:
            detected_role = 'Unknown'
        
        st.metric("Detected Role", detected_role)
        st.metric("Experience Level", jd_data.get('seniority', 'Not specified'))
    
    with col3:
        st.metric("Resume Quality", f"{resume_data.get('quality_score', 0)}/100")
        st.metric("Skills Match", f"{match_data.get('skill_match', {}).get('match_percentage', 0):.1f}%")
    
    # Interpretation
    if match_score >= 70:
        st.success("🟢 Strong match! Your resume aligns well with the job requirements.")
    elif match_score >= 40:
        st.warning("🟡 Moderate match. There are some areas for improvement.")
    else:
        st.error("🔴 Low match. Significant improvements needed to align with job requirements.")
    
    # Market Analysis Summary
    st.subheader("Market Analysis")
    market_analysis = match_data.get('market_analysis', {})
    market_position = market_analysis.get('market_position', 'Unknown')
    
    if market_position == 'Highly Competitive':
        st.success(f"🌟 Market Position: {market_position}")
    elif market_position == 'Competitive':
        st.info(f"💼 Market Position: {market_position}")
    else:
        st.warning(f"📊 Market Position: {market_position}")
    
    # Show strengths and improvement areas
    col_strengths, col_improvements = st.columns(2)
    
    with col_strengths:
        strengths = market_analysis.get('strengths', [])
        if strengths:
            st.write("**Key Strengths:**")
            for strength in strengths:
                st.write(f"• {strength}")
    
    with col_improvements:
        improvements = market_analysis.get('improvement_areas', [])
        if improvements:
            st.write("**Areas for Improvement:**")
            for improvement in improvements:
                st.write(f"• {improvement}")
    
    # Enhanced statistics
    st.subheader("Detailed Analytics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_jd_skills = len(jd_data.get('all_jd_skills_list', []))
        st.metric("Total JD Skills", total_jd_skills)
    
    with col2:
        matched_skills = len(match_data.get('matched_skills', []))
        st.metric("Matched Skills", matched_skills)
    
    with col3:
        missing_skills = len(match_data.get('missing_skills', []))
        st.metric("Missing Skills", missing_skills)
    
    with col4:
        critical_missing = match_data.get('priority_analysis', {}).get('critical_missing_count', 0)
        st.metric("Critical Gaps", critical_missing)
    
    # Additional metrics row
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        ats_score = resume_data.get('ats_analysis', {}).get('score', 0)
        st.metric("ATS Score", f"{ats_score}/100")
    
    with col6:
        competitiveness = match_data.get('market_analysis', {}).get('competitiveness_score', 0)
        st.metric("Market Competitiveness", f"{competitiveness:.0f}%")
    
    with col7:
        exp_score = match_data.get('experience_alignment', {}).get('experience_score', 0)
        st.metric("Experience Fit", f"{exp_score}/100")
    
    with col8:
        word_count = resume_data.get('word_count', 0)
        st.metric("Resume Word Count", word_count)