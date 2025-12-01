"""
UI Components Module
Contains reusable UI components and helper functions for the Streamlit interface.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List
import random

def format_skills_list(skills):
    """Format skills list for display."""
    if not skills:
        return "None found"
    formatted_skills = [skill.replace('_', ' ').title() for skill in skills]
    return ' • '.join(formatted_skills)

def get_section_status_icon(present):
    """Get status icon for resume sections."""
    return "✅" if present else "❌"

def get_priority_color(priority):
    """Get priority color icon."""
    priority_icons = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
    return priority_icons.get(priority.lower(), '🟡')

def setup_page_config():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="AI Job Application Assistant",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def apply_custom_css():
    """Apply custom CSS styling."""
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }

    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
        color: #212529;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #e9ecef;
    }

    .metric-card strong {
        color: #495057;
        font-weight: 600;
    }

    .metric-card small {
        color: #6c757d;
    }

    .priority-high {
        border-left-color: #dc3545;
        background-color: #fff5f5;
    }

    .priority-high strong {
        color: #c53030;
    }

    .priority-medium {
        border-left-color: #ffc107;
        background-color: #fffbeb;
    }

    .priority-medium strong {
        color: #d69e2e;
    }

    .priority-low {
        border-left-color: #28a745;
        background-color: #f0fff4;
    }

    .priority-low strong {
        color: #38a169;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }

    /* Ensure text visibility in all themes */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: inherit !important;
    }
    </style>
    """, unsafe_allow_html=True)

def display_main_header():
    """Display the main application header."""
    st.markdown("""
    <div class="main-header">
        <h1>🎯 AI Job Application Assistant</h1>
        <p>Analyze how well your resume matches job requirements and get personalized recommendations</p>
    </div>
    """, unsafe_allow_html=True)

def display_daily_tip():
    """Display daily tip in sidebar."""
    daily_tips = [
        "Use action verbs to start your bullet points",
        "Quantify your achievements with specific numbers",
        "Tailor your resume keywords to the job description",
        "Keep your resume to 1-2 pages maximum",
        "Use a professional email address",
        "Include relevant certifications and courses"
    ]
    
    tip_of_day = random.choice(daily_tips)
    st.info(f"💡 {tip_of_day}")

def create_gauge_chart(value, title="Gauge Chart", reference=70):
    """Create a gauge chart using Plotly."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        delta={'reference': reference},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 40], 'color': "lightgray"},
                {'range': [40, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(height=300)
    return fig

def display_priority_card(action: Dict):
    """Display a priority action card."""
    priority = action.get('priority', 'medium')
    priority_icon = get_priority_color(priority)
    
    st.markdown(f"""
    <div class="metric-card priority-{priority}">
        <strong>{priority_icon} {action.get('action', 'Action')}</strong><br>
        <small>Priority: {priority.title()} | Timeframe: {action.get('timeframe', 'TBD')}</small>
    </div>
    """, unsafe_allow_html=True)

def display_footer():
    """Display enhanced application footer."""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white; margin-top: 2rem;'>
        <h3>🚀 Take Your Career to the Next Level</h3>
        <p>Powered by Advanced AI • Built for Job Seekers • Trusted by Professionals</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Resources Footer
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### 📚 Resources")
        st.markdown("""
        - [Resume Writing Guide](/)
        - [Interview Preparation](/)
        - [Salary Negotiation](/)
        - [Career Planning](/)
        """)
    
    with col2:
        st.markdown("### 🛠️ Tools")
        st.markdown("""
        - [ATS Checker](/)
        - [Skills Gap Analysis](/)
        - [Mock Interview](/)
        - [Market Analytics](/)
        """)
    
    with col3:
        st.markdown("### 🤝 Community")
        st.markdown("""
        - [Job Seeker Forum](/)
        - [Career Coaching](/)
        - [Networking Events](/)
        - [Success Stories](/)
        """)
    
    with col4:
        st.markdown("### ℹ️ Support")
        st.markdown("""
        - [Help Center](/)
        - [Contact Support](/)
        - [Feature Requests](/)
        - [Bug Reports](/)
        """)
    
    # Performance stats
    st.markdown("---")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Resumes Analyzed", "50,000+")
    with col2:
        st.metric("Job Matches Found", "125,000+")
    with col3:
        st.metric("Interview Success Rate", "87%")
    with col4:
        st.metric("Salary Improvements", "$8.5M+")
    with col5:
        st.metric("User Satisfaction", "4.9⭐")