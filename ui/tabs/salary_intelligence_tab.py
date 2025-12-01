"""
Salary Intelligence Tab Module
Displays salary analysis and compensation insights.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from typing import Dict

def display_salary_intelligence_tab(resume_data: Dict, jd_data: Dict, match_data: Dict):
    """Display salary intelligence and compensation analysis."""
    st.header("💰 Salary Intelligence & Compensation Analysis")
    
    # Sample salary estimation
    st.subheader("🎯 Salary Estimation")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Base Salary Range", "$85,000 - $120,000")
    with col2:
        st.metric("5-Year Projection", "$140,000")
    with col3:
        st.metric("Market Position", "Competitive")
    with col4:
        st.metric("Growth Potential", "Strong")
    
    # Compensation breakdown
    st.subheader("📆 Compensation Breakdown")
    
    compensation_data = {
        'Component': ['Base Salary', 'Bonus', 'Stock Options', 'Benefits'],
        'Percentage': [70, 15, 10, 5],
        'Amount Range': [
            "$70,000 - $100,000",
            "$10,500 - $15,000",
            "$7,000 - $10,000",
            "$3,500 - $5,000"
        ]
    }
    
    df_comp = pd.DataFrame(compensation_data)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig_pie = px.pie(df_comp, values='Percentage', names='Component', 
                       title="Compensation Structure")
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.dataframe(df_comp, use_container_width=True)
    
    # Negotiation insights
    st.subheader("🤝 Negotiation Intelligence")
    
    negotiation_tips = [
        "Research market rates for your role and location",
        "Highlight your unique skills and achievements",
        "Consider total compensation, not just base salary",
        "Be prepared to negotiate benefits and perks",
        "Practice your negotiation conversation beforehand"
    ]
    
    for tip in negotiation_tips:
        st.write(f"💡 {tip}")
    
    # Industry comparison
    st.subheader("🏭 Industry Salary Comparison")
    
    industry_comparison = {
        'Industry': ['Technology', 'Finance', 'Healthcare', 'Consulting', 'Retail'],
        'Average Salary': [120000, 115000, 85000, 110000, 65000],
        'Growth Rate': [8.5, 6.2, 7.1, 5.8, 3.2]
    }
    
    df_industry = pd.DataFrame(industry_comparison)
    
    fig_bar = px.bar(df_industry, x='Industry', y='Average Salary',
                    title="Average Salaries by Industry",
                    color='Growth Rate', color_continuous_scale='Viridis')
    st.plotly_chart(fig_bar, use_container_width=True)