"""
Skills Analysis Tab Module
Displays detailed skills analysis including matched, missing, and additional skills.
"""

import streamlit as st
import plotly.express as px
from typing import Dict
from ui.components import format_skills_list

def display_skills_tab(match_data: Dict, jd_data: Dict, resume_data: Dict):
    """Display skills analysis."""
    st.header("🎯 Skills Analysis")
    
    # Skills comparison chart
    col1, col2 = st.columns(2)
    
    with col1:
        # Matched vs Missing skills
        matched_count = len(match_data.get('matched_skills', []))
        missing_count = len(match_data.get('missing_skills', []))
        
        fig = px.bar(
            x=['Matched Skills', 'Missing Skills'],
            y=[matched_count, missing_count],
            title="Skills Overview",
            color=['Matched Skills', 'Missing Skills'],
            color_discrete_map={
                'Matched Skills': '#28a745',
                'Missing Skills': '#dc3545'
            }
        )
        fig.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        # Category-wise match
        category_match = match_data.get('category_match', {}).get('category_breakdown', {})
        
        if category_match:
            categories = list(category_match.keys())
            percentages = [category_match[cat].get('match_percentage', 0) for cat in categories]
            
            fig = px.bar(
                x=categories,
                y=percentages,
                title="Match by Category",
                color=percentages,
                color_continuous_scale=['red', 'yellow', 'green']
            )
            fig.update_layout(height=300, xaxis={'tickangle': 45})
            st.plotly_chart(fig, width='stretch')
    
    # Detailed skills breakdown
    st.subheader("Detailed Skills Breakdown")
    
    tab1, tab2, tab3 = st.tabs(["✅ Matched Skills", "❌ Missing Skills", "➕ Additional Skills"])
    
    with tab1:
        matched_skills = match_data.get('matched_skills', [])
        if matched_skills:
            st.success(f"You have {len(matched_skills)} skills that match the job requirements:")
            skills_text = format_skills_list(matched_skills)
            st.write(skills_text)
        else:
            st.info("No exact skill matches found.")
    
    with tab2:
        missing_skills = match_data.get('missing_skills', [])
        priority_analysis = match_data.get('priority_analysis', {})
        
        if missing_skills:
            st.error(f"You are missing {len(missing_skills)} skills from the job requirements:")
            
            # High priority missing skills
            high_priority = priority_analysis.get('high_priority', [])
            if high_priority:
                st.markdown("**🔴 High Priority (Critical):**")
                st.write(format_skills_list(high_priority))
            
            # Medium priority missing skills
            medium_priority = priority_analysis.get('medium_priority', [])
            if medium_priority:
                st.markdown("**🟡 Medium Priority:**")
                st.write(format_skills_list(medium_priority))
            
            # Low priority missing skills
            low_priority = priority_analysis.get('low_priority', [])
            if low_priority:
                st.markdown("**🟢 Low Priority:**")
                st.write(format_skills_list(low_priority))
        else:
            st.success("Great! You have all the required skills.")
    
    with tab3:
        resume_only_skills = match_data.get('resume_only_skills', [])
        if resume_only_skills:
            st.info(f"You have {len(resume_only_skills)} additional skills not mentioned in the job description:")
            st.write(format_skills_list(resume_only_skills))
        else:
            st.info("No additional skills beyond job requirements found.")