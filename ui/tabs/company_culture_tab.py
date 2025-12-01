"""
Company Culture Tab Module
Displays company culture analysis and fit assessment.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict

def display_company_culture_tab(resume_data: Dict, jd_data: Dict, match_data: Dict):
    """Display company culture analysis and fit assessment."""
    st.header("🏢 Company Culture & Fit Analysis")
    
    # Culture assessment
    st.subheader("🔍 Company Culture Insights")
    
    # Simulated culture analysis
    culture_indicators = {
        'Culture Aspect': [
            'Innovation Focus',
            'Work-Life Balance',
            'Team Collaboration',
            'Growth Opportunities',
            'Diversity & Inclusion',
            'Remote Flexibility'
        ],
        'Score': [85, 70, 90, 80, 75, 95],
        'Evidence': [
            'Mentions "innovative solutions" and "cutting-edge"',
            'Standard benefits package mentioned',
            'Emphasizes "team player" and "cross-functional"',
            'Career development and learning opportunities',
            'Equal opportunity employer statement',
            'Hybrid/remote work options available'
        ]
    }
    
    df_culture = pd.DataFrame(culture_indicators)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=df_culture['Score'],
            theta=df_culture['Culture Aspect'],
            fill='toself',
            name='Company Culture'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            title="Company Culture Profile"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        st.dataframe(df_culture[['Culture Aspect', 'Score', 'Evidence']], use_container_width=True)
    
    # Values alignment
    st.subheader("🎯 Values Alignment Assessment")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Overall Culture Fit", "87%", "↗ +5%")
    
    with col2:
        st.metric("Mission Alignment", "92%", "↗ +8%")
    
    with col3:
        st.metric("Work Style Match", "78%", "→ 0%")
    
    # Company benefits analysis
    st.subheader("💼 Benefits & Perks Analysis")
    
    benefits_categories = {
        'Category': ['Health & Wellness', 'Financial', 'Time Off', 'Professional Development', 'Work Environment'],
        'Score': [85, 70, 90, 95, 80],
        'Details': [
            'Health insurance, dental, vision, gym membership',
            '401k matching, stock options, bonus structure',
            'Unlimited PTO, sabbatical options, holidays',
            'Conference budget, training courses, certifications',
            'Flexible hours, remote work, modern office'
        ]
    }
    
    df_benefits = pd.DataFrame(benefits_categories)
    
    fig_benefits = px.bar(df_benefits, x='Category', y='Score',
                        title="Benefits Package Analysis",
                        color='Score', color_continuous_scale='Greens',
                        hover_data=['Details'])
    fig_benefits.update_xaxes(tickangle=45)
    st.plotly_chart(fig_benefits, use_container_width=True)
    
    # Employee reviews simulation
    st.subheader("⭐ Employee Sentiment Analysis")
    
    sentiment_data = {
        'Review Source': ['Glassdoor', 'Indeed', 'Blind', 'LinkedIn'],
        'Overall Rating': [4.2, 4.0, 3.8, 4.5],
        'Work-Life Balance': [3.9, 4.1, 3.6, 4.2],
        'Career Growth': [4.0, 3.8, 3.9, 4.3],
        'Compensation': [4.3, 4.2, 4.0, 4.1]
    }
    
    df_sentiment = pd.DataFrame(sentiment_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_ratings = px.bar(df_sentiment, x='Review Source', y='Overall Rating',
                           title="Employee Ratings by Platform",
                           color='Overall Rating', color_continuous_scale='RdYlGn')
        st.plotly_chart(fig_ratings, use_container_width=True)
    
    with col2:
        # Create a heatmap of all ratings
        rating_cols = ['Overall Rating', 'Work-Life Balance', 'Career Growth', 'Compensation']
        fig_heatmap = px.imshow(df_sentiment[rating_cols].T, 
                              x=df_sentiment['Review Source'],
                              y=rating_cols,
                              title="Detailed Ratings Heatmap",
                              color_continuous_scale='RdYlGn')
        st.plotly_chart(fig_heatmap, use_container_width=True)