"""
Advanced Analytics Tab Module
Displays advanced analytics, market intelligence, and career insights.
"""

import streamlit as st
import plotly.express as px
from typing import Dict

def display_advanced_analytics_tab(resume_data: Dict, jd_data: Dict, match_data: Dict, recommendations: Dict):
    """Display advanced analytics and insights."""
    st.header("📈 Advanced Analytics & Market Intelligence")
    
    # Career Insights
    career_insights = recommendations.get('career_insights', {})
    if career_insights:
        st.subheader("🚀 Career Growth Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Market Demand", career_insights.get('market_demand', 'Unknown'))
        with col2:
            st.metric("Growth Potential", career_insights.get('growth_potential', 'Unknown'))
        with col3:
            next_steps = career_insights.get('next_career_steps', [])
            if next_steps:
                st.metric("Next Career Step", next_steps[0])
        
        # Industry insights
        industry_insights = career_insights.get('industry_insights', [])
        if industry_insights:
            st.subheader("📆 Industry Insights")
            for insight in industry_insights:
                st.info(insight)
        
        # Trending skills
        trending_skills = career_insights.get('skill_trends', [])
        if trending_skills:
            st.subheader("📈 Trending Technologies")
            st.write(f"This role mentions these trending technologies: **{', '.join(trending_skills)}**")
    
    # Learning Resources
    st.subheader("📚 Personalized Learning Path")
    learning_resources = recommendations.get('learning_resources', {})
    
    if learning_resources:
        # Learning timeline
        estimated_time = learning_resources.get('estimated_learning_time', 'Not calculated')
        st.info(f"⏱️ **Estimated Learning Time:** {estimated_time}")
        
        # Course recommendations
        courses = learning_resources.get('online_courses', [])
        if courses:
            st.write("**📖 Recommended Courses:**")
            for course in courses:
                st.write(f"• **{course.get('skill')}**: {course.get('course')} ({course.get('platform')}) - {course.get('estimated_time')}")
        
        # Practice projects
        projects = learning_resources.get('practice_projects', [])
        if projects:
            st.write("**🔧 Practice Projects:**")
            for project in projects:
                st.write(f"• {project}")
        
        # Certifications
        certifications = learning_resources.get('certifications', [])
        if certifications:
            st.write("**🏆 Relevant Certifications:**")
            for cert in certifications:
                st.write(f"• {cert.get('certification')} (for {cert.get('skill')})")
    
    # Application Strategy
    st.subheader("🎯 Strategic Application Advice")
    app_strategy = recommendations.get('application_strategy', {})
    
    if app_strategy:
        readiness = app_strategy.get('application_readiness', 'Unknown')
        
        if readiness == 'Ready to Apply':
            st.success(f"✅ **Status:** {readiness}")
        elif readiness == 'Nearly Ready':
            st.warning(f"⚠️ **Status:** {readiness}")
        else:
            st.error(f"❌ **Status:** {readiness}")
        
        # Recommended approach
        approach = app_strategy.get('recommended_approach', [])
        if approach:
            st.write("**📋 Recommended Approach:**")
            for item in approach:
                st.write(f"• {item}")
        
        # Timeline suggestions
        timeline = app_strategy.get('timeline_suggestions', [])
        if timeline:
            st.write("**⏰ Timeline Suggestions:**")
            for item in timeline:
                st.write(f"• {item}")
        
        # Application tips
        tips = app_strategy.get('application_tips', [])
        if tips:
            with st.expander("💡 Application Tips"):
                for tip in tips:
                    st.write(f"• {tip}")
    
    # ATS Analysis
    st.subheader("🤖 ATS Compatibility Analysis")
    ats_analysis = resume_data.get('ats_analysis', {})
    
    if ats_analysis:
        ats_score = ats_analysis.get('score', 0)
        
        # ATS Score visualization
        from ui.components import create_gauge_chart
        fig = create_gauge_chart(ats_score, "ATS Compatibility Score")
        fig.update_layout(height=250)
        st.plotly_chart(fig, width='stretch')
        
        # ATS Issues
        issues = ats_analysis.get('issues', [])
        if issues:
            st.write("**⚠️ ATS Optimization Suggestions:**")
            for issue in issues:
                st.write(f"• {issue}")
        else:
            st.success("✅ Your resume appears to be ATS-friendly!")
    
    # Detailed Statistics
    st.subheader("📆 Detailed Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Resume Statistics:**")
        st.write(f"• Word Count: {resume_data.get('word_count', 0)}")
        st.write(f"• Character Count: {resume_data.get('character_count', 0)}")
        st.write(f"• Quality Score: {resume_data.get('quality_score', 0)}/100")
        
        # Skills by category chart
        resume_skills_by_cat = resume_data.get('resume_skills', {}).get('by_category', {})
        if resume_skills_by_cat:
            categories = list(resume_skills_by_cat.keys())
            counts = [len(skills) for skills in resume_skills_by_cat.values()]
            
            fig = px.pie(
                values=counts,
                names=categories,
                title="Your Skills by Category"
            )
            st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.write("**Job Description Analysis:**")
        st.write(f"• Word Count: {jd_data.get('word_count', 0)}")
        
        job_reqs = jd_data.get('job_requirements', {})
        if job_reqs:
            st.write(f"• Total Requirements: {job_reqs.get('total_requirements', 0)}")
            st.write(f"• Hard Requirements: {job_reqs.get('hard_requirements', 0)}")
            st.write(f"• Soft Requirements: {job_reqs.get('soft_requirements', 0)}")
            st.write(f"• Complexity Score: {job_reqs.get('complexity_score', 0)}/100")
        
        # Salary analysis if available
        salary_info = jd_data.get('salary_info', {})
        if salary_info.get('salary_mentioned'):
            min_sal = salary_info.get('min_salary', 0)
            max_sal = salary_info.get('max_salary', 0)
            st.write(f"• Salary Range: ${min_sal:,} - ${max_sal:,}")