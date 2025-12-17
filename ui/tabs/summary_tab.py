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
    
    # Overall match score with gauge and key metrics
    match_score = match_data.get('match_score_overall', 0)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Create gauge chart
        fig = create_gauge_chart(match_score, "Overall Match Score")
        st.plotly_chart(fig, use_container_width=True)
    
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
        
        # Job title from JD
        jd_role = jd_data.get('jd_role', 'Unknown').replace('_', ' ').title()
        st.metric("Target Role", jd_role)
    
    with col3:
        st.metric("Resume Quality", f"{resume_data.get('quality_score', 0):.0f}/100")
        st.metric("Skills Match", f"{match_data.get('skill_match', {}).get('match_percentage', 0):.1f}%")
        st.metric("ATS Score", f"{resume_data.get('ats_analysis', {}).get('score', 0):.0f}/100")
    
    st.markdown("---")
    
    # Interpretation with color coding
    if match_score >= 70:
        st.success("🟢 **Strong Match!** Your resume aligns well with the job requirements. You're a competitive candidate.")
    elif match_score >= 50:
        st.warning("🟡 **Moderate Match.** There are some areas for improvement to strengthen your candidacy.")
    else:
        st.error("🔴 **Low Match.** Significant improvements needed to align with job requirements. Focus on the critical gaps below.")
    
    st.markdown("---")
    
    # Key Metrics Overview
    st.subheader("📈 Key Performance Indicators")
    
    metric_cols = st.columns(5)
    
    with metric_cols[0]:
        total_jd_skills = len(jd_data.get('all_jd_skills_list', []))
        st.metric("Total JD Skills", total_jd_skills, delta=None, help="Total skills required by job")
    
    with metric_cols[1]:
        matched_skills = len(match_data.get('matched_skills', []))
        st.metric("Matched Skills", matched_skills, delta=f"+{(matched_skills/total_jd_skills*100):.0f}%", help="Skills you already have")
    
    with metric_cols[2]:
        missing_skills = len(match_data.get('missing_skills', []))
        st.metric("Missing Skills", missing_skills, delta=None, help="Skills to develop")
    
    with metric_cols[3]:
        critical_missing = match_data.get('priority_analysis', {}).get('critical_missing_count', 0)
        st.metric("Critical Gaps", critical_missing, delta=None, help="Must-have missing skills")
    
    with metric_cols[4]:
        competitiveness = match_data.get('market_analysis', {}).get('competitiveness_score', 0)
        st.metric("Competitiveness", f"{competitiveness:.0f}%", help="Market positioning")
    
    st.markdown("---")
    
    # Market Analysis Summary
    st.subheader("🌐 Market Analysis & Position")
    market_analysis = match_data.get('market_analysis', {})
    market_position = market_analysis.get('market_position', 'Unknown')
    
    market_col1, market_col2, market_col3 = st.columns(3)
    
    with market_col1:
        if market_position == 'Highly Competitive':
            st.success(f"🌟 **Market Position:** {market_position}")
        elif market_position == 'Competitive':
            st.info(f"💼 **Market Position:** {market_position}")
        else:
            st.warning(f"📊 **Market Position:** {market_position}")
    
    with market_col2:
        salary_range = market_analysis.get('salary_range', 'Not available')
        st.info(f"💰 **Salary Range:** {salary_range}")
    
    with market_col3:
        demand_level = market_analysis.get('demand_level', 'Medium')
        st.metric("Demand Level", demand_level)
    
    st.markdown("---")
    
    # Show strengths and improvement areas
    st.subheader("💪 Strengths vs 🎯 Improvement Areas")
    col_strengths, col_improvements = st.columns(2)
    
    with col_strengths:
        strengths = market_analysis.get('strengths', [])
        if strengths:
            st.write("### ✨ Key Strengths")
            for i, strength in enumerate(strengths, 1):
                st.write(f"{i}. {strength}")
        else:
            st.info("No specific strengths identified yet")
    
    with col_improvements:
        improvements = market_analysis.get('improvement_areas', [])
        if improvements:
            st.write("### 🚀 Areas for Improvement")
            for i, improvement in enumerate(improvements, 1):
                st.write(f"{i}. {improvement}")
        else:
            st.info("No specific improvements needed")
    
    with col7:
        exp_score = match_data.get('experience_alignment', {}).get('experience_score', 0)
        st.metric("Experience Fit", f"{exp_score}/100")
    
    with col8:
        word_count = resume_data.get('word_count', 0)
        st.metric("Resume Word Count", word_count)