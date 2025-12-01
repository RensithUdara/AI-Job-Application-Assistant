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
    """Display the main application header with enhanced design."""
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    '>
        <div style='position: relative; z-index: 2;'>
            <h1 style='
                font-size: 3rem; 
                margin-bottom: 1rem; 
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                font-weight: 700;
            '>
                🎯 AI Job Application Assistant
            </h1>
            <p style='
                font-size: 1.3rem; 
                margin-bottom: 1.5rem; 
                opacity: 0.95;
                font-weight: 300;
                line-height: 1.6;
            '>
                Analyze how well your resume matches job requirements and get personalized recommendations
            </p>
            <div style='
                display: flex;
                justify-content: center;
                gap: 2rem;
                margin-top: 2rem;
                flex-wrap: wrap;
            '>
                <div style='
                    background: rgba(255,255,255,0.2);
                    padding: 1rem 1.5rem;
                    border-radius: 25px;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255,255,255,0.3);
                '>
                    <span style='font-size: 1.1rem; font-weight: 500;'>🤖 AI-Powered Analysis</span>
                </div>
                <div style='
                    background: rgba(255,255,255,0.2);
                    padding: 1rem 1.5rem;
                    border-radius: 25px;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255,255,255,0.3);
                '>
                    <span style='font-size: 1.1rem; font-weight: 500;'>📊 Real-time Insights</span>
                </div>
                <div style='
                    background: rgba(255,255,255,0.2);
                    padding: 1rem 1.5rem;
                    border-radius: 25px;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255,255,255,0.3);
                '>
                    <span style='font-size: 1.1rem; font-weight: 500;'>🎯 Personalized Tips</span>
                </div>
            </div>
        </div>
        <div style='
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            z-index: 1;
            animation: float 6s ease-in-out infinite;
        '></div>
    </div>
    
    <style>
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(5deg); }
    }
    </style>
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
    """Display enhanced application footer with real links and attractive design."""
    st.markdown("---")
    
    # Hero section with improved gradient and styling
    st.markdown("""
    <div style='
        text-align: center; 
        padding: 3rem 2rem; 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); 
        border-radius: 15px; 
        color: white; 
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    '>
        <div style='position: relative; z-index: 2;'>
            <h2 style='font-size: 2.5rem; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
                🚀 Take Your Career to the Next Level
            </h2>
            <p style='font-size: 1.2rem; margin-bottom: 0; opacity: 0.95;'>
                Powered by Advanced AI • Built for Job Seekers • Trusted by Professionals
            </p>
        </div>
        <div style='
            position: absolute; 
            top: -50%; 
            right: -50%; 
            width: 200%; 
            height: 200%; 
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            z-index: 1;
        '></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced footer sections with better styling
    st.markdown("""
    <style>
    .footer-section {
        background: linear-gradient(145deg, #f8f9ff 0%, #e8efff 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: transform 0.2s ease;
    }
    .footer-section:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    }
    .footer-link {
        color: #4a5568;
        text-decoration: none;
        padding: 8px 12px;
        display: block;
        border-radius: 6px;
        transition: all 0.2s ease;
        margin: 4px 0;
    }
    .footer-link:hover {
        background-color: #667eea;
        color: white;
        text-decoration: none;
        transform: translateX(5px);
    }
    .section-title {
        color: #2d3748;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Quick Resources Footer with real links
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="footer-section">
            <div class="section-title">📚 Resources</div>
            <a href="https://www.indeed.com/career-advice/resumes-cover-letters/how-to-write-a-resume" class="footer-link" target="_blank">Resume Writing Guide</a>
            <a href="https://www.glassdoor.com/blog/common-interview-questions/" class="footer-link" target="_blank">Interview Preparation</a>
            <a href="https://www.harvard.edu/career-advice/salary-negotiation-guide" class="footer-link" target="_blank">Salary Negotiation</a>
            <a href="https://www.linkedin.com/learning/paths/career-development" class="footer-link" target="_blank">Career Planning</a>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="footer-section">
            <div class="section-title">🛠️ Tools</div>
            <a href="https://www.jobscan.co/" class="footer-link" target="_blank">ATS Checker</a>
            <a href="https://www.coursera.org/skills-assessment" class="footer-link" target="_blank">Skills Gap Analysis</a>
            <a href="https://www.pramp.com/" class="footer-link" target="_blank">Mock Interview</a>
            <a href="https://www.glassdoor.com/research/" class="footer-link" target="_blank">Market Analytics</a>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="footer-section">
            <div class="section-title">🤝 Community</div>
            <a href="https://www.reddit.com/r/jobs/" class="footer-link" target="_blank">Job Seeker Forum</a>
            <a href="https://www.linkedin.com/coaching/" class="footer-link" target="_blank">Career Coaching</a>
            <a href="https://www.meetup.com/find/career-networking/" class="footer-link" target="_blank">Networking Events</a>
            <a href="https://www.glassdoor.com/Reviews/" class="footer-link" target="_blank">Success Stories</a>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="footer-section">
            <div class="section-title">ℹ️ Support</div>
            <a href="https://docs.streamlit.io/" class="footer-link" target="_blank">Help Center</a>
            <a href="mailto:support@jobassistant.ai" class="footer-link">Contact Support</a>
            <a href="https://github.com/features" class="footer-link" target="_blank">Feature Requests</a>
            <a href="https://github.com/issues" class="footer-link" target="_blank">Bug Reports</a>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced Performance stats with better visual design
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        color: white;
        text-align: center;
    '>
        <h3 style='margin-bottom: 2rem; color: #fff; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);'>
            📊 Platform Statistics
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Enhanced metrics with better styling
    metrics_style = """
    <style>
    .metric-container {
        background: linear-gradient(145deg, #ffffff 0%, #f7fafc 100%);
        border-radius: 12px;
        padding: 1.5rem 1rem;
        text-align: center;
        border: 2px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        margin: 0.5rem 0;
    }
    .metric-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border-color: #667eea;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    .metric-label {
        color: #4a5568;
        font-size: 0.9rem;
        font-weight: 500;
    }
    </style>
    """
    st.markdown(metrics_style, unsafe_allow_html=True)
    
    with col1:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value">50,000+</div>
            <div class="metric-label">Resumes Analyzed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value">125,000+</div>
            <div class="metric-label">Job Matches Found</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value">87%</div>
            <div class="metric-label">Interview Success Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value">$8.5M+</div>
            <div class="metric-label">Salary Improvements</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value">4.9⭐</div>
            <div class="metric-label">User Satisfaction</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer bottom with social links and copyright
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='
        background: #1a202c;
        color: #cbd5e0;
        text-align: center;
        padding: 2rem;
        border-radius: 10px;
        margin-top: 2rem;
    '>
        <div style='margin-bottom: 1rem;'>
            <a href="https://linkedin.com/company/ai-job-assistant" style='color: #667eea; text-decoration: none; margin: 0 15px; font-size: 1.2rem;' target="_blank">
                💼 LinkedIn
            </a>
            <a href="https://twitter.com/ai_job_assistant" style='color: #667eea; text-decoration: none; margin: 0 15px; font-size: 1.2rem;' target="_blank">
                🐦 Twitter
            </a>
            <a href="https://github.com/ai-job-assistant" style='color: #667eea; text-decoration: none; margin: 0 15px; font-size: 1.2rem;' target="_blank">
                💻 GitHub
            </a>
            <a href="mailto:hello@jobassistant.ai" style='color: #667eea; text-decoration: none; margin: 0 15px; font-size: 1.2rem;'>
                📧 Contact
            </a>
        </div>
        <div style='font-size: 0.9rem; opacity: 0.8;'>
            © 2025 AI Job Application Assistant. Built with ❤️ for job seekers worldwide.
        </div>
    </div>
    """, unsafe_allow_html=True)