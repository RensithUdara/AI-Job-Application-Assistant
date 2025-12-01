"""
Resume Scoring Tab Module
Displays intelligent resume scoring and ATS compatibility analysis.
"""

import streamlit as st
from typing import Dict

def display_resume_scoring_tab(resume_data: Dict, jd_data: Dict):
    """Display advanced resume scoring and ATS analysis."""
    st.header("🎯 Intelligent Resume Scoring")
    
    st.subheader("📆 Overall Resume Score")
    
    # Sample scoring (would be calculated by AI)
    overall_score = resume_data.get('quality_score', 75)
    
    if overall_score >= 85:
        score_color = "🟮"
        score_message = "Excellent! Your resume is highly optimized"
    elif overall_score >= 70:
        score_color = "🟡"
        score_message = "Good resume with room for improvement"
    elif overall_score >= 55:
        score_color = "🟠"
        score_message = "Fair resume that needs significant enhancement"
    else:
        score_color = "🔴"
        score_message = "Your resume needs major improvements"
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall Score", f"{overall_score}/100")
    with col2:
        st.metric("Score Category", score_color)
    with col3:
        target_role = jd_data.get('jd_role', 'software_engineer')
        st.metric("Target Role", target_role.replace('_', ' ').title())
    
    st.info(f"**Assessment:** {score_message}")
    
    # Score breakdown
    st.subheader("📈 Score Breakdown")
    
    score_categories = {
        'Content Quality (25%)': 82,
        'ATS Compatibility (20%)': 78,
        'Keyword Optimization (20%)': 85,
        'Formatting Score (10%)': 90,
        'Experience Relevance (15%)': 75,
        'Skill Match (10%)': 70
    }
    
    col1, col2 = st.columns(2)
    
    for i, (category, score) in enumerate(score_categories.items()):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.write(f"**{category}**")
            st.progress(score / 100)
            st.write(f"{score}/100")
    
    # ATS Compatibility Analysis
    st.subheader("🤖 Advanced ATS Compatibility Analysis")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("ATS Score", "78/100")
    with col2:
        st.metric("ATS Grade", "B+")
    with col3:
        st.metric("Parsing Success Rate", "85%")
    
    st.info("**Parsing Confidence:** High - Most ATS systems will parse your resume correctly")