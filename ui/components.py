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
    
    # Enhanced Footer with attractive design and real links
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .footer-section {
        background: transparent;
        padding: 1rem 0;
        border-radius: 0;
        margin: 0;
        box-shadow: none;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
    }
    .footer-column {
        padding: 1.5rem;
        background: rgba(102, 126, 234, 0.1);
        border-radius: 10px;
        margin: 0.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        transition: transform 0.3s ease;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
        color: #2d3748 !important;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    .footer-column:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    .footer-link {
        color: #4a5568 !important;
        text-decoration: none !important;
        padding: 8px 12px;
        border-radius: 6px;
        display: inline-block;
        margin: 2px 0;
        transition: all 0.3s ease;
        border-left: 3px solid transparent;
        font-weight: 500;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif !important;
        font-size: 14px;
        line-height: 1.5;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    .footer-link:hover {
        background-color: #f8f9ff !important;
        border-left: 3px solid #667eea;
        color: #667eea !important;
        transform: translateX(5px);
    }
    .section-header {
        color: #2d3748 !important;
        font-weight: 700;
        margin-bottom: 1rem;
        font-size: 1.2rem;
        text-shadow: none;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    .section-icon {
        font-size: 1.2rem;
        margin-right: 8px;
        display: inline-block;
        vertical-align: middle;
    }
    /* Dark theme compatibility */
    [data-theme="dark"] .footer-column {
        background: #1a202c !important;
        color: #e2e8f0 !important;
    }
    [data-theme="dark"] .section-header {
        color: #f7fafc !important;
    }
    [data-theme="dark"] .footer-link {
        color: #90cdf4 !important;
    }
    [data-theme="dark"] .footer-link:hover {
        background-color: #2d3748 !important;
        color: #63b3ed !important;
    }
    /* Font fallback for better compatibility */
    .footer-section *, .footer-column *, .footer-link *, .section-header * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Quick Resources Footer with enhanced design
    st.markdown('<div class="footer-section">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="footer-column">
            <h3 class="section-header"><span class="section-icon">📚</span>Resources</h3>
            <a href="https://www.indeed.com/career-advice/resumes-cover-letters" target="_blank" class="footer-link">📝 Resume Writing Guide</a><br>
            <a href="https://www.glassdoor.com/blog/common-interview-questions/" target="_blank" class="footer-link">🎤 Interview Preparation</a><br>
            <a href="https://www.harvard.edu/career-advice/salary-negotiation-tips" target="_blank" class="footer-link">💰 Salary Negotiation</a><br>
            <a href="https://www.linkedin.com/advice/0/how-do-you-create-career-development-plan" target="_blank" class="footer-link">📈 Career Planning</a>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="footer-column">
            <h3 class="section-header"><span class="section-icon">🛠️</span>Tools</h3>
            <a href="https://resumeworded.com/ats-resume-scanner" target="_blank" class="footer-link">🤖 ATS Checker</a><br>
            <a href="https://www.coursera.org/skills-assessment" target="_blank" class="footer-link">📊 Skills Gap Analysis</a><br>
            <a href="https://www.pramp.com/" target="_blank" class="footer-link">🎯 Mock Interview</a><br>
            <a href="https://www.bls.gov/ooh/" target="_blank" class="footer-link">📈 Market Analytics</a>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="footer-column">
            <h3 class="section-header"><span class="section-icon">🤝</span>Community</h3>
            <a href="https://www.reddit.com/r/jobs/" target="_blank" class="footer-link">💬 Job Seeker Forum</a><br>
            <a href="https://www.themusejobs.com/coaching" target="_blank" class="footer-link">👥 Career Coaching</a><br>
            <a href="https://www.meetup.com/find/?keywords=networking" target="_blank" class="footer-link">🌐 Networking Events</a><br>
            <a href="https://www.linkedin.com/pulse/topics/success-stories" target="_blank" class="footer-link">🎉 Success Stories</a>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="footer-column">
            <h3 class="section-header"><span class="section-icon">ℹ️</span>Support</h3>
            <a href="https://docs.streamlit.io/" target="_blank" class="footer-link">❓ Help Center</a><br>
            <a href="mailto:support@jobassistant.ai" class="footer-link">📧 Contact Support</a><br>
            <a href="https://github.com/RensithUdara/Ai-Job-Application-Assistant/issues" target="_blank" class="footer-link">💡 Feature Requests</a><br>
            <a href="https://github.com/RensithUdara/Ai-Job-Application-Assistant/issues/new?template=bug_report.md" target="_blank" class="footer-link">🐛 Bug Reports</a>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Performance stats with enhanced styling
    st.markdown("---")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; color: white; text-align: center; margin: 2rem 0;'>
        <h3 style='margin-bottom: 1.5rem; color: white;'>📊 Platform Statistics</h3>
    </div>
    """, unsafe_allow_html=True)
    
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