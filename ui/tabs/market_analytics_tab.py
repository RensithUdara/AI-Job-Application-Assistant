"""
Market Analytics Tab Module
Displays real-time market analytics and trends.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from typing import Dict

def display_market_analytics_tab(resume_data: Dict, jd_data: Dict, match_data: Dict):
    """Display real-time market analytics and trends."""
    st.header("🌐 Real-Time Market Analytics & Trends")
    
    # Market demand analysis
    st.subheader("📈 Market Demand Analysis")
    
    # Skills demand trends
    skills_demand = {
        'Skill': ['Python', 'JavaScript', 'AWS', 'React', 'Docker', 'Kubernetes', 'Machine Learning', 'Data Analysis'],
        'Demand Score': [95, 90, 88, 85, 82, 78, 92, 87],
        'Growth Trend': [12, 8, 15, 7, 18, 22, 25, 14],
        'Job Openings': [45000, 38000, 32000, 28000, 25000, 18000, 35000, 31000]
    }
    
    df_skills = pd.DataFrame(skills_demand)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_scatter = px.scatter(df_skills, x='Demand Score', y='Growth Trend', 
                               size='Job Openings', hover_name='Skill',
                               title="Skills Market Analysis",
                               labels={'Growth Trend': 'Growth Rate (%)', 'Demand Score': 'Market Demand'})
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        fig_bar = px.bar(df_skills, x='Skill', y='Job Openings',
                        title="Current Job Openings by Skill",
                        color='Demand Score', color_continuous_scale='Blues')
        fig_bar.update_xaxes(tickangle=45)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Geographic market analysis
    st.subheader("🗺️ Geographic Market Hotspots")
    
    geographic_data = {
        'Location': ['San Francisco', 'New York', 'Seattle', 'Austin', 'Boston', 'Chicago', 'Los Angeles', 'Denver'],
        'Job Opportunities': [8500, 7200, 6800, 4500, 4200, 3800, 5200, 3200],
        'Average Salary': [145000, 125000, 135000, 95000, 115000, 85000, 120000, 90000],
        'Cost of Living Index': [180, 150, 140, 95, 130, 100, 145, 105]
    }
    
    df_geo = pd.DataFrame(geographic_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_bubble = px.scatter(df_geo, x='Average Salary', y='Job Opportunities',
                              size='Cost of Living Index', hover_name='Location',
                              title="Market Opportunities by Location")
        st.plotly_chart(fig_bubble, use_container_width=True)
    
    with col2:
        df_geo['Opportunity Score'] = (df_geo['Job Opportunities'] / df_geo['Cost of Living Index'] * 100).round(1)
        fig_bar_geo = px.bar(df_geo, x='Location', y='Opportunity Score',
                           title="Location Opportunity Score",
                           color='Opportunity Score', color_continuous_scale='Greens')
        fig_bar_geo.update_xaxes(tickangle=45)
        st.plotly_chart(fig_bar_geo, use_container_width=True)
    
    # Remote work trends
    st.subheader("🏠 Remote Work Market Analysis")
    
    remote_stats = {
        'Work Type': ['Fully Remote', 'Hybrid', 'On-site', 'Flexible'],
        'Job Postings %': [35, 40, 20, 5],
        'Salary Premium %': [5, 2, 0, 8]
    }
    
    df_remote = pd.DataFrame(remote_stats)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_pie_remote = px.pie(df_remote, values='Job Postings %', names='Work Type',
                              title="Distribution of Work Arrangements")
        st.plotly_chart(fig_pie_remote, use_container_width=True)
    
    with col2:
        fig_bar_remote = px.bar(df_remote, x='Work Type', y='Salary Premium %',
                              title="Salary Premium by Work Type",
                              color='Salary Premium %', color_continuous_scale='RdYlBu')
        st.plotly_chart(fig_bar_remote, use_container_width=True)