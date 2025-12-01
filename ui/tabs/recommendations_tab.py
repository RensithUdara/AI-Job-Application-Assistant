"""
Recommendations Tab Module
Displays personalized recommendations and improvement suggestions.
"""

import streamlit as st
import plotly.express as px
from typing import Dict
from ui.components import get_priority_color, display_priority_card

def display_recommendations_tab(recommendations: Dict):
    """Display recommendations."""
    st.header("💡 Personalized Recommendations")
    
    # Priority actions
    st.subheader("🎯 Priority Actions")
    priority_actions = recommendations.get('priority_actions', [])
    
    if priority_actions:
        for action in priority_actions:
            display_priority_card(action)
    
    # Resume improvement tips
    st.subheader("📝 Resume Improvement Tips")
    resume_tips = recommendations.get('resume_tips', [])
    
    if resume_tips:
        for tip in resume_tips:
            priority_icon = get_priority_color(tip.get('priority', 'medium'))
            
            with st.expander(f"{priority_icon} {tip.get('title', 'Tip')}"):
                st.write(tip.get('description', 'No description available.'))
                st.caption(f"Category: {tip.get('category', 'General')} | Priority: {tip.get('priority', 'Medium')}")
    else:
        st.info("Your resume structure looks good! No specific improvements needed.")
    
    # Skill development roadmap
    st.subheader("🛣️ Skill Development Roadmap")
    skill_roadmap = recommendations.get('skill_roadmap', [])
    
    if skill_roadmap:
        # Create priority counts for visualization
        priority_counts = {}
        for item in skill_roadmap:
            priority = item.get('priority', 'medium')
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        if priority_counts:
            # Create priority distribution chart
            fig = px.pie(
                values=list(priority_counts.values()),
                names=list(priority_counts.keys()),
                title="Learning Priority Distribution",
                color_discrete_map={
                    'high': '#dc3545',
                    'medium': '#ffc107',
                    'low': '#28a745'
                }
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, width='stretch')
        
        # Display roadmap details
        for item in skill_roadmap:
            priority_icon = get_priority_color(item.get('priority', 'medium'))
            
            st.markdown(f"""
            <div class="metric-card">
                <strong>{priority_icon} {item.get('timeframe', 'TBD')}: {item.get('skill', 'Skill')}</strong><br>
                {item.get('action', 'No action specified.')}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Continue building projects with your current skills to strengthen your portfolio.")