import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List
import sys
import os

# Add the core directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from core.resume_parser import ResumeParser
from core.jd_processor import JobDescriptionProcessor
from core.matcher import Matcher
from core.recommender import Recommender
# Import utility functions
def format_skills_list(skills):
    if not skills:
        return "None found"
    formatted_skills = [skill.replace('_', ' ').title() for skill in skills]
    return ' • '.join(formatted_skills)

def get_section_status_icon(present):
    return "✅" if present else "❌"

def get_priority_color(priority):
    priority_icons = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
    return priority_icons.get(priority.lower(), '🟡')

# Page configuration
st.set_page_config(
    page_title="AI Job Application Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global Styles */
.stApp {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* Main Header with Advanced Gradient */
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    padding: 2.5rem;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 100%);
    pointer-events: none;
}

.main-header h1 {
    font-weight: 700;
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.main-header p {
    font-weight: 300;
    font-size: 1.1rem;
    opacity: 0.9;
}

/* Enhanced Metric Cards */
.metric-card {
    background: linear-gradient(145deg, #ffffff 0%, #f8f9fb 100%);
    padding: 1.5rem;
    border-radius: 15px;
    border-left: 5px solid #667eea;
    margin: 1rem 0;
    color: #2d3748;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    border: 1px solid rgba(255,255,255,0.8);
    transition: all 0.3s ease;
    position: relative;
    backdrop-filter: blur(10px);
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 35px rgba(0,0,0,0.12);
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #667eea, transparent);
    border-radius: 15px 15px 0 0;
}

.metric-card strong {
    color: #1a202c;
    font-weight: 600;
    font-size: 1.1rem;
}

.metric-card small {
    color: #718096;
    font-weight: 400;
}

/* Priority Cards with Glassmorphism */
.priority-high {
    border-left-color: #e53e3e;
    background: linear-gradient(145deg, #fed7d7 0%, #feb2b2 100%);
    box-shadow: 0 8px 32px rgba(229, 62, 62, 0.2);
}

.priority-high strong {
    color: #c53030;
    text-shadow: 1px 1px 2px rgba(197, 48, 48, 0.1);
}

.priority-medium {
    border-left-color: #d69e2e;
    background: linear-gradient(145deg, #fefcbf 0%, #faf089 100%);
    box-shadow: 0 8px 32px rgba(214, 158, 46, 0.2);
}

.priority-medium strong {
    color: #b7791f;
    text-shadow: 1px 1px 2px rgba(183, 121, 31, 0.1);
}

.priority-low {
    border-left-color: #38a169;
    background: linear-gradient(145deg, #c6f6d5 0%, #9ae6b4 100%);
    box-shadow: 0 8px 32px rgba(56, 161, 105, 0.2);
}

.priority-low strong {
    color: #276749;
    text-shadow: 1px 1px 2px rgba(39, 103, 73, 0.1);
}

/* Enhanced Tab Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    padding: 8px;
    margin-bottom: 2rem;
}

.stTabs [data-baseweb="tab"] {
    height: 55px;
    padding: 12px 24px;
    border-radius: 8px;
    transition: all 0.3s ease;
    font-weight: 500;
    background: transparent;
}

.stTabs [data-baseweb="tab"]:hover {
    background: rgba(102, 126, 234, 0.1);
    transform: translateY(-1px);
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

/* Professional Input Sections */
.upload-section {
    background: rgba(255, 255, 255, 0.9);
    padding: 2rem;
    border-radius: 15px;
    margin: 1rem 0;
    box-shadow: 0 5px 20px rgba(0,0,0,0.05);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Custom Buttons */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 2rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    background: linear-gradient(135deg, #5a6fd8 0%, #6a42a0 100%);
}

.stButton > button:active {
    transform: translateY(0);
}

/* Enhanced Metrics */
.metric-container {
    background: linear-gradient(145deg, #ffffff 0%, #f7fafc 100%);
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border: 1px solid rgba(255, 255, 255, 0.8);
    transition: transform 0.2s ease;
}

.metric-container:hover {
    transform: scale(1.02);
}

/* Success/Warning/Error Messages */
.stAlert {
    border-radius: 10px;
    border: none;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

/* Progress Bars */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    border-radius: 10px;
}

/* Expanders */
.streamlit-expanderHeader {
    background: rgba(102, 126, 234, 0.05);
    border-radius: 10px;
    border: 1px solid rgba(102, 126, 234, 0.1);
}

/* Text Areas and Inputs */
.stTextArea > div > div > textarea,
.stTextInput > div > div > input {
    border-radius: 10px;
    border: 2px solid #e2e8f0;
    transition: border-color 0.3s ease;
}

.stTextArea > div > div > textarea:focus,
.stTextInput > div > div > input:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* File Uploader */
.uploadedFile {
    background: linear-gradient(145deg, #f7fafc 0%, #edf2f7 100%);
    border-radius: 10px;
    border: 2px dashed #cbd5e0;
}

/* Sidebar Styling */
.css-1d391kg {
    background: linear-gradient(180deg, #f7fafc 0%, #edf2f7 100%);
}

/* Animation Classes */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in-up {
    animation: fadeInUp 0.6s ease-out;
}

@keyframes pulse {
    0% {
        box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7);
    }
    70% {
        box-shadow: 0 0 0 10px rgba(102, 126, 234, 0);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(102, 126, 234, 0);
    }
}

.pulse {
    animation: pulse 2s infinite;
}

/* Dark Mode Support */
@media (prefers-color-scheme: dark) {
    .metric-card {
        background: linear-gradient(145deg, #2d3748 0%, #4a5568 100%);
        color: #e2e8f0;
        border-color: #4a5568;
    }
    
    .main-header {
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
}

/* Responsive Design */
@media (max-width: 768px) {
    .main-header {
        padding: 1.5rem;
    }
    
    .main-header h1 {
        font-size: 2rem;
    }
    
    .metric-card {
        padding: 1rem;
        margin: 0.5rem 0;
    }
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #5a6fd8, #6a42a0);
}

/* Ensure text visibility in all themes */
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
    color: inherit !important;
    font-family: 'Inter', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

def main():
    # Enhanced Header with Animation
    st.markdown("""
    <div class="main-header fade-in-up">
        <h1>🎯 AI Job Application Assistant</h1>
        <p>Transform your career with intelligent analysis, professional insights, and personalized recommendations</p>
        <div style="margin-top: 1rem; opacity: 0.8; font-size: 0.9rem;">
            ✨ Professional • 🚀 Intelligent • 📊 Comprehensive • 🎯 Results-Driven
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'analysis_done' not in st.session_state:
        st.session_state.analysis_done = False
    if 'results' not in st.session_state:
        st.session_state.results = {}
    
    # Enhanced Input Section
    st.markdown("""
    <div class="fade-in-up" style="margin-top: 2rem;">
        <h2 style="color: #2d3748; font-weight: 600; margin-bottom: 1.5rem; text-align: center;">
            📄 Input Your Information
        </h2>
        <p style="text-align: center; color: #718096; margin-bottom: 2rem; font-size: 1.1rem;">
            Upload your resume and job description to get started with professional analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="upload-section">
            <h3 style="color: #2d3748; margin-bottom: 1rem; display: flex; align-items: center;">
                📄 Your Resume
                <span style="margin-left: 0.5rem; font-size: 0.7rem; background: #667eea; color: white; padding: 0.2rem 0.5rem; border-radius: 20px;">REQUIRED</span>
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Resume input options with enhanced styling
        input_method = st.radio(
            "Choose input method:",
            ["Upload File", "Paste Text"],
            key="resume_input_method",
            help="Upload a PDF/DOCX file or paste your resume text directly"
        )
        
        resume_content = None
        
        if input_method == "Upload File":
            uploaded_file = st.file_uploader(
                "Upload your resume",
                type=['pdf', 'docx', 'txt'],
                help="Supported formats: PDF, DOCX, TXT"
            )
            if uploaded_file is not None:
                resume_content = uploaded_file
                st.success(f"✅ File uploaded: {uploaded_file.name}")
        else:
            resume_text = st.text_area(
                "Paste your resume text here:",
                height=300,
                placeholder="Copy and paste your resume content here..."
            )
            if resume_text.strip():
                resume_content = resume_text
    
    with col2:
        st.markdown("""
        <div class="upload-section">
            <h3 style="color: #2d3748; margin-bottom: 1rem; display: flex; align-items: center;">
                🎯 Job Description
                <span style="margin-left: 0.5rem; font-size: 0.7rem; background: #667eea; color: white; padding: 0.2rem 0.5rem; border-radius: 20px;">REQUIRED</span>
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        jd_text = st.text_area(
            "Paste the complete job description:",
            height=350,
            placeholder="📋 Copy and paste the complete job description here...\n\nInclude:\n• Job title and responsibilities\n• Required skills and qualifications\n• Experience requirements\n• Company information\n• Salary range (if mentioned)",
            help="The more detailed the job description, the better our analysis will be!"
        )
    
    # Professional Analysis Button
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
    </div>
    """, unsafe_allow_html=True)
    
    analyze_col1, analyze_col2, analyze_col3 = st.columns([1, 2, 1])
    with analyze_col2:
        if st.button("🚀 Start Professional Analysis", type="primary", use_container_width=True):
            if resume_content and jd_text.strip():
                # Enhanced loading with progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    with st.spinner('🔍 Performing comprehensive analysis...'):
                        status_text.text('Initializing AI processors...')
                        progress_bar.progress(20)
                        
                        # Initialize components
                        resume_parser = ResumeParser()
                        jd_processor = JobDescriptionProcessor()
                        matcher = Matcher()
                        recommender = Recommender()
                        
                        status_text.text('Analyzing resume content...')
                        progress_bar.progress(40)
                        
                        # Process resume
                        if isinstance(resume_content, str):
                            resume_data = resume_parser.parse_resume(text_content=resume_content)
                        else:
                            resume_data = resume_parser.parse_resume(file_content=resume_content)
                        
                        status_text.text('Processing job description...')
                        progress_bar.progress(60)
                        
                        # Process job description
                        jd_data = jd_processor.process_jd(jd_text)
                        
                        status_text.text('Performing intelligent matching...')
                        progress_bar.progress(80)
                        
                        # Match resume to job
                        match_data = matcher.match_resume_to_jd(resume_data, jd_data)
                        
                        status_text.text('Generating personalized recommendations...')
                        progress_bar.progress(90)
                        
                        # Generate recommendations
                        recommendations = recommender.build_recommendations(resume_data, jd_data, match_data)
                        
                        status_text.text('Finalizing analysis...')
                        progress_bar.progress(100)
                        
                        # Store results in session state
                        st.session_state.results = {
                            'resume_data': resume_data,
                            'jd_data': jd_data,
                            'match_data': match_data,
                            'recommendations': recommendations
                        }
                        st.session_state.analysis_done = True
                        
                        # Clear progress indicators
                        progress_bar.empty()
                        status_text.empty()
                        
                        # Success message with animation
                        st.markdown("""
                        <div class="fade-in-up" style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); border-radius: 10px; margin: 1rem 0; border-left: 4px solid #28a745;">
                            <h3 style="color: #155724; margin: 0;">✅ Analysis Completed Successfully!</h3>
                            <p style="color: #155724; margin: 0.5rem 0 0 0;">Professional insights and recommendations are ready below</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")
        else:
            st.warning("⚠️ Please provide both resume and job description.")
    
    # Results Section
    if st.session_state.analysis_done and st.session_state.results:
        st.markdown("---")
        display_results(st.session_state.results)

def display_results(results: Dict):
    """Display analysis results in tabs."""
    resume_data = results['resume_data']
    jd_data = results['jd_data']
    match_data = results['match_data']
    recommendations = results['recommendations']
    
    # Enhanced Results Header
    st.markdown("""
    <div class="fade-in-up" style="text-align: center; margin: 3rem 0 2rem 0;">
        <h2 style="color: #2d3748; font-weight: 600; margin-bottom: 0.5rem;">
            📊 Professional Analysis Results
        </h2>
        <p style="color: #718096; font-size: 1.1rem;">
            Comprehensive insights and personalized recommendations for your career success
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create enhanced tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Executive Summary", 
        "🎯 Skills Intelligence", 
        "📋 Resume Analysis", 
        "💡 Smart Recommendations", 
        "🎤 Interview Mastery",
        "📈 Market Analytics",
        "🚀 Professional Tools"
    ])
    
    with tab1:
        display_summary_tab(resume_data, jd_data, match_data)
    
    with tab2:
        display_skills_tab(match_data, jd_data, resume_data)
    
    with tab3:
        display_structure_tab(resume_data)
    
    with tab4:
        display_recommendations_tab(recommendations)
    
    with tab5:
        display_interview_tab(recommendations)
    
    with tab6:
        display_advanced_analytics_tab(resume_data, jd_data, match_data, recommendations)
    
    with tab7:
        display_professional_tools_tab(resume_data, jd_data, match_data, recommendations)

def display_summary_tab(resume_data: Dict, jd_data: Dict, match_data: Dict):
    """Display summary information."""
    st.header("📊 Application Match Summary")
    
    # Overall match score with gauge
    match_score = match_data.get('match_score_overall', 0)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=match_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Overall Match Score"},
            delta={'reference': 70},
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
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.metric("Detected Role", jd_data.get('jd_role', 'Unknown').replace('_', ' ').title())
        st.metric("Experience Level", jd_data.get('seniority', 'Not specified'))
    
    with col3:
        st.metric("Resume Quality", f"{resume_data.get('quality_score', 0)}/100")
        st.metric("Skills Match", f"{match_data.get('skill_match', {}).get('match_percentage', 0):.1f}%")
    
    # Interpretation
    if match_score >= 70:
        st.success("🟢 Strong match! Your resume aligns well with the job requirements.")
    elif match_score >= 40:
        st.warning("🟡 Moderate match. There are some areas for improvement.")
    else:
        st.error("🔴 Low match. Significant improvements needed to align with job requirements.")
    
    # Market Analysis Summary
    st.subheader("Market Analysis")
    market_analysis = match_data.get('market_analysis', {})
    market_position = market_analysis.get('market_position', 'Unknown')
    
    if market_position == 'Highly Competitive':
        st.success(f"🌟 Market Position: {market_position}")
    elif market_position == 'Competitive':
        st.info(f"💼 Market Position: {market_position}")
    else:
        st.warning(f"📊 Market Position: {market_position}")
    
    # Show strengths and improvement areas
    col_strengths, col_improvements = st.columns(2)
    
    with col_strengths:
        strengths = market_analysis.get('strengths', [])
        if strengths:
            st.write("**Key Strengths:**")
            for strength in strengths:
                st.write(f"• {strength}")
    
    with col_improvements:
        improvements = market_analysis.get('improvement_areas', [])
        if improvements:
            st.write("**Areas for Improvement:**")
            for improvement in improvements:
                st.write(f"• {improvement}")
    
    # Enhanced statistics
    st.subheader("Detailed Analytics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_jd_skills = len(jd_data.get('all_jd_skills_list', []))
        st.metric("Total JD Skills", total_jd_skills)
    
    with col2:
        matched_skills = len(match_data.get('matched_skills', []))
        st.metric("Matched Skills", matched_skills)
    
    with col3:
        missing_skills = len(match_data.get('missing_skills', []))
        st.metric("Missing Skills", missing_skills)
    
    with col4:
        critical_missing = match_data.get('priority_analysis', {}).get('critical_missing_count', 0)
        st.metric("Critical Gaps", critical_missing)
    
    # Additional metrics row
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        ats_score = resume_data.get('ats_analysis', {}).get('score', 0)
        st.metric("ATS Score", f"{ats_score}/100")
    
    with col6:
        competitiveness = match_data.get('market_analysis', {}).get('competitiveness_score', 0)
        st.metric("Market Competitiveness", f"{competitiveness:.0f}%")
    
    with col7:
        exp_score = match_data.get('experience_alignment', {}).get('experience_score', 0)
        st.metric("Experience Fit", f"{exp_score}/100")
    
    with col8:
        word_count = resume_data.get('word_count', 0)
        st.metric("Resume Word Count", word_count)

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

def display_structure_tab(resume_data: Dict):
    """Display resume structure analysis."""
    st.header("📋 Resume Structure Analysis")
    
    # Section completeness
    sections_found = resume_data.get('sections_found', {})
    missing_sections = resume_data.get('missing_sections', [])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Section Completeness")
        
        for section, present in sections_found.items():
            status_icon = get_section_status_icon(present)
            section_name = section.replace('_', ' ').title()
            
            if present:
                st.success(f"{status_icon} {section_name}")
            else:
                st.error(f"{status_icon} {section_name}")
    
    with col2:
        # Section completeness pie chart
        present_count = sum(sections_found.values())
        total_count = len(sections_found)
        missing_count = total_count - present_count
        
        fig = px.pie(
            values=[present_count, missing_count],
            names=['Present', 'Missing'],
            title="Resume Completeness",
            color_discrete_map={'Present': '#28a745', 'Missing': '#dc3545'}
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, width='stretch')
    
    # Contact information quality
    st.subheader("Contact Information")
    contact_info = resume_data.get('contact_info', {})
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        email_status = "✅ Valid" if contact_info.get('valid_email') else "❌ Missing/Invalid"
        st.metric("Email", email_status)
    
    with col2:
        phone_status = "✅ Present" if contact_info.get('has_phone') else "❌ Missing"
        st.metric("Phone", phone_status)
    
    with col3:
        linkedin_status = "✅ Present" if contact_info.get('has_linkedin') else "❌ Missing"
        st.metric("LinkedIn", linkedin_status)
    
    # Resume quality score breakdown
    st.subheader("Quality Score Breakdown")
    quality_score = resume_data.get('quality_score', 0)
    
    progress_col, info_col = st.columns([2, 1])
    
    with progress_col:
        st.progress(quality_score / 100)
        
        if quality_score >= 80:
            st.success(f"Excellent resume quality: {quality_score}/100")
        elif quality_score >= 60:
            st.warning(f"Good resume quality: {quality_score}/100")
        else:
            st.error(f"Needs improvement: {quality_score}/100")
    
    with info_col:
        st.info("""
        **Quality factors:**
        - Section completeness
        - Contact information
        - Skills diversity
        - Overall structure
        """)

def display_recommendations_tab(recommendations: Dict):
    """Display recommendations."""
    st.header("💡 Personalized Recommendations")
    
    # Priority actions
    st.subheader("🎯 Priority Actions")
    priority_actions = recommendations.get('priority_actions', [])
    
    if priority_actions:
        for action in priority_actions:
            priority = action.get('priority', 'medium')
            priority_icon = get_priority_color(priority)
            
            st.markdown(f"""
            <div class="metric-card priority-{priority}">
                <strong>{priority_icon} {action.get('action', 'Action')}</strong><br>
                <small>Priority: {priority.title()} | Timeframe: {action.get('timeframe', 'TBD')}</small>
            </div>
            """, unsafe_allow_html=True)
    
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

def display_interview_tab(recommendations: Dict):
    """Display interview preparation."""
    st.header("🎤 Interview Preparation")
    
    interview_questions = recommendations.get('interview_questions', [])
    
    if not interview_questions:
        st.info("No specific interview questions available. Focus on general preparation.")
        return
    
    # Group questions by category
    questions_by_category = {}
    for q in interview_questions:
        category = q.get('category', 'general')
        if category not in questions_by_category:
            questions_by_category[category] = []
        questions_by_category[category].append(q)
    
    # Display questions by category
    for category, questions in questions_by_category.items():
        category_name = category.replace('_', ' ').title()
        
        with st.expander(f"📝 {category_name} Questions ({len(questions)})"):
            for i, question in enumerate(questions, 1):
                question_type = question.get('type', 'general')
                skill = question.get('skill', '')
                
                st.markdown(f"**Q{i}:** {question.get('question', 'Question not available')}")
                
                if skill and skill != 'soft_skill':
                    st.caption(f"Focus area: {skill} | Type: {question_type}")
                
                st.markdown("---")
    
    # Interview preparation checklist
    st.subheader("✅ Interview Preparation Checklist")
    
    checklist_items = [
        "Review your resume and be ready to discuss each section",
        "Prepare STAR method examples for behavioral questions",
        "Research the company and role thoroughly",
        "Practice coding problems if applicable",
        "Prepare questions to ask the interviewer",
        "Test your technical setup for video interviews",
        "Review the job description and match your experience",
        "Prepare a brief self-introduction (elevator pitch)"
    ]
    
    for item in checklist_items:
        st.checkbox(item, key=f"checklist_{item[:20]}")
    
    # Study focus recommendations
    st.subheader("📚 Study Focus Areas")
    
    # Get skills that need attention
    technical_questions = [q for q in interview_questions if q.get('type') == 'technical']
    focus_skills = list(set([q.get('skill', '') for q in technical_questions if q.get('skill')]))
    
    if focus_skills:
        st.info("Based on the job requirements and your background, focus your study time on:")
        
        for skill in focus_skills[:5]:  # Top 5 skills
            st.markdown(f"• **{skill.replace('_', ' ').title()}**")
    
    st.success("💡 **Pro Tip:** Practice explaining technical concepts in simple terms, as you may need to communicate with non-technical team members!")

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
            st.subheader("📊 Industry Insights")
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
            st.write("**🛠️ Practice Projects:**")
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
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=ats_score,
            title={'text': "ATS Compatibility Score"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "green" if ats_score > 70 else "orange" if ats_score > 50 else "red"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "lightgreen"}
                ]
            }
        ))
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
    st.subheader("📊 Detailed Statistics")
    
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

def display_professional_tools_tab(resume_data: Dict, jd_data: Dict, match_data: Dict, recommendations: Dict):
    """Display professional tools and advanced features."""
    st.header("🚀 Professional Tools & AI Analysis")
    
    # Initialize parsers for advanced analysis
    resume_parser = ResumeParser()
    jd_processor = JobDescriptionProcessor()
    recommender = Recommender()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Resume Quality Analysis")
        
        # Bullet point analysis
        text_content = resume_data.get('text', '')
        if text_content:
            bullet_analysis = resume_parser.analyze_bullet_points(text_content)
            
            # Display bullet scores
            st.markdown("**Bullet Point Quality:**")
            avg_score = bullet_analysis.get('average_score', 0)
            st.metric("Average Score", f"{avg_score}/10", f"{bullet_analysis.get('quality_level', 'Unknown')}")
            
            # Show individual bullet scores
            bullets = bullet_analysis.get('bullets', [])
            if bullets:
                with st.expander(f"📋 Bullet Analysis ({len(bullets)} bullets found)"):
                    for i, bullet in enumerate(bullets[:5], 1):  # Show top 5
                        score = bullet.get('score', 0)
                        feedback = bullet.get('feedback', '')
                        
                        # Color coding based on score
                        if score >= 8:
                            st.success(f"**Bullet {i}** (Score: {score}/10)")
                        elif score >= 6:
                            st.info(f"**Bullet {i}** (Score: {score}/10)")
                        else:
                            st.warning(f"**Bullet {i}** (Score: {score}/10)")
                        
                        st.caption(bullet.get('text', '')[:100] + "...")
                        st.write(feedback)
                        
                        suggestions = bullet.get('suggestions', [])
                        if suggestions:
                            for suggestion in suggestions:
                                st.caption(f"💡 {suggestion}")
                        st.markdown("---")
            
            # Action verb analysis
            st.markdown("**Action Verb Analysis:**")
            verb_analysis = resume_parser.analyze_action_verbs(text_content)
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Strong Verbs", verb_analysis.get('strong_count', 0))
            with col_b:
                st.metric("Weak Verbs", verb_analysis.get('weak_count', 0))
            
            # Show verb improvement suggestions
            verb_recommendations = verb_analysis.get('verb_recommendations', [])
            if verb_recommendations:
                with st.expander("🔄 Verb Improvement Suggestions"):
                    for rec in verb_recommendations[:3]:
                        weak_verb = rec.get('weak_verb', '')
                        alternatives = rec.get('alternatives', [])
                        st.write(f"**Replace '{weak_verb}'** with: {', '.join(alternatives)}")
        
        # Quantification analysis
        st.subheader("📊 Quantification Analysis")
        if text_content:
            quant_analysis = resume_parser.analyze_quantification(text_content)
            
            col_q1, col_q2 = st.columns(2)
            with col_q1:
                st.metric("Numbers Found", quant_analysis.get('numbers_count', 0))
                st.metric("Percentages", quant_analysis.get('percentages_count', 0))
            
            with col_q2:
                st.metric("Timeframes", quant_analysis.get('timeframes_count', 0))
                score = quant_analysis.get('quantification_score', 0)
                st.metric("Quantification Score", f"{score}/10")
            
            # Show unquantified opportunities
            unquantified = quant_analysis.get('sample_unquantified', [])
            if unquantified:
                with st.expander("⚠️ Opportunities to Add Numbers"):
                    for sentence in unquantified:
                        st.caption(f"• {sentence.strip()}")
                    st.info("💡 Add specific numbers, percentages, or timeframes to these statements")
    
    with col2:
        st.subheader("🎯 Job Analysis & Intelligence")
        
        # Role seniority analysis
        jd_text = jd_data.get('text', '')
        if jd_text:
            seniority_analysis = jd_processor.classify_seniority_level(jd_text)
            
            st.markdown("**Role Seniority Classification:**")
            primary_level = seniority_analysis.get('primary_level', 'Unknown')
            confidence = seniority_analysis.get('confidence_score', 0)
            
            st.metric("Seniority Level", primary_level.title(), f"{confidence*100:.0f}% confidence")
            st.caption(seniority_analysis.get('level_description', ''))
            
            years_mentioned = seniority_analysis.get('experience_years_mentioned', [])
            if years_mentioned:
                st.write(f"**Experience Required:** {min(years_mentioned)}-{max(years_mentioned)} years")
        
        # Job difficulty analysis
        if jd_text:
            skills_required = jd_data.get('skills_found', [])
            difficulty_analysis = jd_processor.estimate_job_difficulty(jd_text, skills_required)
            
            st.markdown("**Job Difficulty Assessment:**")
            difficulty_score = difficulty_analysis.get('difficulty_score', 0)
            difficulty_level = difficulty_analysis.get('difficulty_level', 'Unknown')
            
            # Create a gauge-like progress bar
            progress_color = "🔴" if difficulty_score >= 80 else "🟡" if difficulty_score >= 50 else "🟢"
            st.metric("Difficulty Score", f"{difficulty_score}/100", difficulty_level)
            st.progress(difficulty_score / 100)
            
            # Show difficulty breakdown
            breakdown = difficulty_analysis.get('breakdown', {})
            with st.expander("📊 Difficulty Breakdown"):
                for factor, score in breakdown.items():
                    factor_name = factor.replace('_', ' ').title()
                    st.write(f"• **{factor_name}:** {score} points")
        
        # Must-have vs Nice-to-have analysis
        if jd_text and skills_required:
            skill_categorization = jd_processor.analyze_must_have_vs_nice_to_have(jd_text, skills_required)
            
            st.markdown("**Skill Priority Analysis:**")
            
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                must_have_count = skill_categorization.get('must_have_count', 0)
                st.metric("Must-Have Skills", must_have_count)
            
            with col_m2:
                nice_to_have_count = skill_categorization.get('nice_to_have_count', 0)
                st.metric("Nice-to-Have Skills", nice_to_have_count)
            
            confidence = skill_categorization.get('classification_confidence', 0)
            st.caption(f"Classification Confidence: {confidence*100:.0f}%")
    
    # Professional Tools Section
    st.markdown("---")
    st.subheader("🔧 Professional Enhancement Tools")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📝 Professional Summary Generator**")
        if st.button("Generate Summary Options"):
            summary_generator = recommender.generate_professional_summary(resume_data)
            summaries = summary_generator.get('summary_options', {})
            
            for style, summary in summaries.items():
                st.markdown(f"**{style.replace('_', ' ').title()}:**")
                st.text_area(f"summary_{style}", summary, height=100, key=f"summary_{style}")
    
    with col2:
        st.markdown("**💼 LinkedIn Headlines**")
        if st.button("Generate LinkedIn Headlines"):
            headlines = recommender.generate_linkedin_headlines(resume_data)
            
            st.markdown("**Choose your favorite:**")
            for i, headline in enumerate(headlines, 1):
                st.write(f"{i}. {headline}")
    
    with col3:
        st.markdown("**🎯 Interview Prep Plan**")
        if st.button("Generate Interview Plan"):
            prep_plan = recommender.generate_interview_preparation_plan(resume_data, jd_data, match_data)
            
            with st.expander("📚 Technical Preparation"):
                tech_prep = prep_plan.get('technical_preparation', {})
                st.write("**Skills to Review:**", ', '.join(tech_prep.get('skills_to_review', [])))
                st.write("**Skills to Study:**", ', '.join(tech_prep.get('skills_to_study', [])))
                
                coding_topics = tech_prep.get('coding_topics', [])
                if coding_topics:
                    st.write("**Coding Topics:**")
                    for topic in coding_topics:
                        st.write(f"• {topic}")
    
    # Resume Weakness Analysis
    st.markdown("---")
    st.subheader("⚠️ Comprehensive Weakness Analysis")
    
    weakness_analysis = recommender.analyze_resume_weaknesses(resume_data)
    weaknesses = weakness_analysis.get('weaknesses_found', [])
    improvements = weakness_analysis.get('improvement_suggestions', [])
    
    if weaknesses:
        priority_level = weakness_analysis.get('priority_level', 'medium')
        
        if priority_level == 'high':
            st.error(f"🚨 **High Priority Issues Found** ({len(weaknesses)} issues)")
        elif priority_level == 'medium':
            st.warning(f"⚠️ **Medium Priority Issues** ({len(weaknesses)} issues)")
        else:
            st.info(f"ℹ️ **Minor Issues** ({len(weaknesses)} issues)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Issues Found:**")
            for weakness in weaknesses:
                st.write(f"• {weakness}")
        
        with col2:
            st.markdown("**Improvement Actions:**")
            for improvement in improvements:
                st.write(f"💡 {improvement}")
        
        st.caption(weakness_analysis.get('overall_assessment', ''))
    else:
        st.success("🎉 **Excellent!** No major weaknesses detected in your resume.")

if __name__ == "__main__":
    main()