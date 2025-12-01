"""
Results Display Module
Contains all result display functionality including tabs and visualizations.
"""

import streamlit as st
from typing import Dict

# Import individual tab modules
from ui.tabs import (
    summary_tab, skills_tab, structure_tab, recommendations_tab, interview_tab,
    advanced_analytics_tab, professional_tools_tab, ai_features_tab, 
    resume_scoring_tab, career_path_tab, salary_intelligence_tab,
    market_analytics_tab, networking_hub_tab, company_culture_tab,
    resume_builder_tab
)

def display_results(results: Dict):
    """Display analysis results in organized tabs."""
    if not results:
        return
    
    resume_data = results['resume_data']
    jd_data = results['jd_data']
    match_data = results['match_data']
    recommendations = results['recommendations']
    
    # Create tabs
    tabs = st.tabs([
        "📊 Summary", 
        "🎯 Skills Analysis", 
        "📋 Resume Structure", 
        "💡 Recommendations", 
        "🎤 Interview Prep",
        "📈 Advanced Analytics",
        "🚀 Professional Tools",
        "🔥 AI Features",
        "🎯 Resume Scoring",
        "🚀 Career Path",
        "💰 Salary Intelligence",
        "🌐 Market Analytics",
        "🤝 Networking Hub",
        "🏢 Company Culture",
        "⚡ Resume Builder"
    ])
    
    with tabs[0]:
        summary_tab.display_summary_tab(resume_data, jd_data, match_data)
    
    with tabs[1]:
        skills_tab.display_skills_tab(match_data, jd_data, resume_data)
    
    with tabs[2]:
        structure_tab.display_structure_tab(resume_data)
    
    with tabs[3]:
        recommendations_tab.display_recommendations_tab(recommendations)
    
    with tabs[4]:
        interview_tab.display_interview_tab(recommendations)
    
    with tabs[5]:
        advanced_analytics_tab.display_advanced_analytics_tab(resume_data, jd_data, match_data, recommendations)
    
    with tabs[6]:
        professional_tools_tab.display_professional_tools_tab(resume_data, jd_data, match_data, recommendations)
    
    with tabs[7]:
        ai_features_tab.display_advanced_ai_features_tab(resume_data, jd_data, match_data)
    
    with tabs[8]:
        resume_scoring_tab.display_resume_scoring_tab(resume_data, jd_data)
    
    with tabs[9]:
        career_path_tab.display_career_path_tab(resume_data, jd_data)
    
    with tabs[10]:
        salary_intelligence_tab.display_salary_intelligence_tab(resume_data, jd_data, match_data)
    
    with tabs[11]:
        market_analytics_tab.display_market_analytics_tab(resume_data, jd_data, match_data)
    
    with tabs[12]:
        networking_hub_tab.display_networking_hub_tab(resume_data, jd_data, match_data)
    
    with tabs[13]:
        company_culture_tab.display_company_culture_tab(resume_data, jd_data, match_data)
    
    with tabs[14]:
        resume_builder_tab.display_resume_builder_tab(resume_data, jd_data, match_data)