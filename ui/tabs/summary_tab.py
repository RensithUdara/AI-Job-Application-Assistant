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
    
    st.markdown("---")
    
    # Detailed Analytics
    st.subheader("📊 Detailed Analytics")
    
    analytics_col1, analytics_col2 = st.columns(2)
    
    with analytics_col1:
        st.write("#### Skill Gap Analysis")
        ats_score = resume_data.get('ats_analysis', {}).get('score', 0)
        quality_score = resume_data.get('quality_score', 0)
        
        # Create mini metrics
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            st.metric("Resume Quality", f"{quality_score:.0f}/100", help="Overall resume format & content quality")
        with col_a2:
            st.metric("ATS Compatibility", f"{ats_score:.0f}/100", help="Optimization for Applicant Tracking Systems")
    
    with analytics_col2:
        st.write("#### Experience Analysis")
        exp_requirement = jd_data.get('experience_range', 'Not specified')
        seniority = jd_data.get('seniority', 'Not specified')
        
        col_a3, col_a4 = st.columns(2)
        with col_a3:
            st.metric("Required Experience", exp_requirement)
        with col_a4:
            st.metric("Seniority Level", seniority)
    
    st.markdown("---")
    
    # Quick Action Items
    st.subheader("⚡ Quick Action Items")
    
    priority_analysis = match_data.get('priority_analysis', {})
    priority_skills = priority_analysis.get('critical_missing', [])
    
    if priority_skills:
        st.write("**🎯 Focus on these critical skills:**")
        for i, skill in enumerate(priority_skills[:5], 1):  # Top 5 critical skills
            st.write(f"{i}. **{skill}** - Priority: HIGH")
    else:
        st.success("✅ No critical skill gaps identified!")
    
    st.markdown("---")
    
    # Match Score Breakdown (Visual)
    st.subheader("📉 Match Score Breakdown")
    
    skill_match = match_data.get('skill_match', {}).get('match_percentage', 0)
    experience_match = match_data.get('experience_match', 0)
    education_match = match_data.get('education_match', 0)
    salary_match = match_data.get('salary_match', 0)
    
    breakdown_col1, breakdown_col2 = st.columns(2)
    
    with breakdown_col1:
        breakdown_data = {
            'Skill Match': skill_match,
            'Experience Match': experience_match,
            'Education Match': education_match,
            'Salary Alignment': salary_match,
        }
        
        for category, value in breakdown_data.items():
            progress_value = min(100, max(0, value))
            st.write(f"**{category}**: {progress_value:.0f}%")
            st.progress(progress_value / 100)
    
    with breakdown_col2:
        st.write("**Match Score Interpretation:**")
        st.write("""
        - **80-100%**: Excellent fit - Strong candidate
        - **60-79%**: Good fit - Competitive candidate  
        - **40-59%**: Moderate fit - Has potential with gaps
        - **Below 40%**: Low fit - Significant improvements needed
        """)
    
    st.markdown("---")
    
    # Recommendation Summary
    st.subheader("💡 Application Strategy Recommendation")
    
    if match_score >= 75:
        recommendation = "🟢 **Apply Now!** You're a strong match for this role. Customize your cover letter to highlight the matched skills."
        icon = "✅"
    elif match_score >= 50:
        recommendation = "🟡 **Apply with Strategy.** Address the skill gaps in your cover letter and resume. Show willingness to learn missing skills."
        icon = "⏳"
    else:
        recommendation = "🔴 **Consider Alternatives.** Focus on building the critical skills first, then apply in 3-6 months."
        icon = "⚠️"
    
    st.info(f"{icon} {recommendation}")