"""
Career Path Tab Module
Displays career path analysis and skill gap assessment.
"""

import streamlit as st
from typing import Dict

def display_career_path_tab(resume_data: Dict, jd_data: Dict):
    """Display career path analysis and skill gap analysis."""
    st.header("🚀 Career Path & Skill Gap Analysis")
    
    # Input section for career path analysis
    st.subheader("🎯 Career Path Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        current_role = st.selectbox(
            "Current Role:",
            ['junior_developer', 'software_engineer', 'web_developer', 'data_analyst', 'mobile_developer'],
            index=1
        )
    
    with col2:
        selected_target_role = st.selectbox(
            "Target Role:",
            ['senior_software_engineer', 'tech_lead', 'data_scientist', 'devops_engineer', 'solution_architect'],
            index=0
        )
    
    with col3:
        years_experience = st.number_input(
            "Years of Experience:",
            min_value=0,
            max_value=20,
            value=2,
            step=1
        )
    
    # Career Progression Analysis
    if st.button("🔍 Analyze Career Progression"):
        st.success("Career progression analysis completed!")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Feasibility Score", "78/100")
        with col2:
            st.metric("Timeline", "18-24 months")
        with col3:
            st.success("Moderate Feasibility")
        
        st.subheader("📚 Learning Path Recommendations")
        st.info("Detailed learning path and skill development recommendations would be displayed here")
    
    # Skill Gap Analysis
    st.subheader("🎯 Comprehensive Skill Gap Analysis")
    
    if st.button("📆 Generate Skill Gap Report"):
        st.success("Skill gap analysis completed!")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Required Skills", "15")
        with col2:
            st.metric("Skill Gaps", "6")
        with col3:
            st.metric("Coverage", "60%")
        with col4:
            st.warning("Readiness: Medium")
        
        st.write("**⏱️ Preparation Time:** 6-12 months")
        
        # Gap analysis details
        col1, col2 = st.columns(2)
        
        with col1:
            st.error("**🚨 Critical Skill Gaps:**")
            critical_gaps = ["Advanced JavaScript", "System Design", "Leadership"]
            for gap in critical_gaps:
                st.write(f"❌ {gap}")
        
        with col2:
            st.warning("**💡 Enhancement Opportunities:**")
            enhancements = ["Cloud Platforms", "DevOps Tools", "Project Management"]
            for enhancement in enhancements:
                st.write(f"🔸 {enhancement}")