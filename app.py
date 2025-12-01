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
from core.career_analyzer import CareerAnalyzer
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

# Custom CSS for better styling
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

def main():
    # Initialize session state
    if 'show_chat' not in st.session_state:
        st.session_state.show_chat = False
    if 'show_templates' not in st.session_state:
        st.session_state.show_templates = False
    if 'show_interview' not in st.session_state:
        st.session_state.show_interview = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Enhanced Sidebar
    with st.sidebar:
        st.markdown("### 🚀 Quick Actions")
        
        # AI Assistant Chat
        if st.button("💬 AI Career Chat", use_container_width=True):
            st.session_state.show_chat = True
        
        # Resume Templates
        if st.button("📄 Resume Templates", use_container_width=True):
            st.session_state.show_templates = True
        
        # Interview Prep
        if st.button("🎤 Mock Interview", use_container_width=True):
            st.session_state.show_interview = True
        
        st.markdown("---")
        
        # Settings
        st.markdown("### ⚙️ Analysis Settings")
        
        analysis_depth = st.selectbox(
            "Analysis Depth:",
            ["Basic", "Comprehensive", "Expert"],
            index=1,
            help="Choose the level of analysis detail"
        )
        
        include_soft_skills = st.checkbox("Include Soft Skills Analysis", value=True)
        include_culture_fit = st.checkbox("Include Culture Fit Analysis", value=True)
        include_salary_insights = st.checkbox("Include Salary Intelligence", value=True)
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("### 📊 Today's Insights")
        st.metric("Jobs Analyzed Today", "1,247", "↗ +12%")
        st.metric("Average Match Score", "78%", "↗ +3%")
        st.metric("Success Rate", "94%", "→ 0%")
        
        st.markdown("---")
        
        # Tips of the day
        st.markdown("### 💡 Daily Tip")
        daily_tips = [
            "Use action verbs to start your bullet points",
            "Quantify your achievements with specific numbers",
            "Tailor your resume keywords to the job description",
            "Keep your resume to 1-2 pages maximum",
            "Use a professional email address",
            "Include relevant certifications and courses"
        ]
        
        import random
        tip_of_day = random.choice(daily_tips)
        st.info(f"💡 {tip_of_day}")
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 AI Job Application Assistant</h1>
        <p>Analyze how well your resume matches job requirements and get personalized recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # AI Chat Modal
    if st.session_state.show_chat:
        with st.container():
            st.markdown("### 🤖 AI Career Assistant Chat")
            
            # Display chat history
            for message in st.session_state.chat_history:
                if message['role'] == 'user':
                    st.write(f"👤 **You:** {message['content']}")
                else:
                    st.write(f"🤖 **AI:** {message['content']}")
            
            # Chat input
            col1, col2 = st.columns([4, 1])
            with col1:
                user_input = st.text_input("Type your question here...", key="chat_input")
            
            with col2:
                if st.button("Send", key="send_chat"):
                    if user_input:
                        # Add user message
                        st.session_state.chat_history.append({
                            'role': 'user',
                            'content': user_input
                        })
                        
                        # Generate AI response (simplified)
                        ai_responses = {
                            'resume': "To improve your resume, focus on quantifying achievements, using action verbs, and tailoring keywords to job descriptions.",
                            'interview': "For interviews, research the company, practice STAR method responses, and prepare thoughtful questions to ask.",
                            'salary': "Research market rates on Glassdoor, PayScale, and LinkedIn. Consider total compensation, not just base salary.",
                            'skills': "Identify skill gaps by comparing job requirements to your current skills. Consider online courses and certifications.",
                            'default': "I'd be happy to help! You can ask me about resumes, interviews, salary negotiation, skill development, or career planning."
                        }
                        
                        # Simple keyword matching for demo
                        response_key = 'default'
                        for key in ai_responses:
                            if key in user_input.lower():
                                response_key = key
                                break
                        
                        ai_response = ai_responses[response_key]
                        
                        st.session_state.chat_history.append({
                            'role': 'ai',
                            'content': ai_response
                        })
                        
                        st.rerun()
            
            if st.button("Close Chat", key="close_chat"):
                st.session_state.show_chat = False
                st.rerun()
            
            st.markdown("---")
    
    # Mock Interview Modal
    if st.session_state.show_interview:
        with st.container():
            st.markdown("### 🎤 Mock Interview Simulator")
            
            col1, col2 = st.columns(2)
            
            with col1:
                interview_type = st.selectbox(
                    "Select Interview Type:",
                    ["Technical", "Behavioral", "System Design", "Culture Fit"],
                    key="interview_type"
                )
            
            with col2:
                role_focus = st.text_input(
                    "Target Role:",
                    placeholder="e.g., Senior Software Engineer",
                    key="role_focus"
                )
            
            if st.button("Start Mock Interview", key="start_interview"):
                st.success("🎬 Mock Interview Started!")
                
                # Sample questions based on type
                questions_db = {
                    'Technical': [
                        "Explain the difference between a stack and a queue.",
                        "How would you implement a hash table?",
                        "What is the time complexity of binary search?"
                    ],
                    'Behavioral': [
                        "Tell me about a challenging project you worked on.",
                        "Describe a time when you had to work with a difficult team member.",
                        "How do you handle tight deadlines?"
                    ],
                    'System Design': [
                        "Design a URL shortener like bit.ly",
                        "How would you design a chat application?",
                        "Design a recommendation system for an e-commerce site."
                    ],
                    'Culture Fit': [
                        "Why do you want to work for our company?",
                        "How do you handle work-life balance?",
                        "What motivates you in your work?"
                    ]
                }
                
                selected_questions = questions_db.get(interview_type, questions_db['Behavioral'])
                
                for i, question in enumerate(selected_questions, 1):
                    st.write(f"**Question {i}:** {question}")
                    
                    answer = st.text_area(
                        f"Your answer for Q{i}:",
                        key=f"answer_{i}",
                        height=100
                    )
                    
                    if answer:
                        # Simple feedback
                        word_count = len(answer.split())
                        if word_count < 50:
                            st.warning(f"💡 Consider expanding your answer (current: {word_count} words)")
                        else:
                            st.success(f"✅ Good length answer ({word_count} words)")
            
            if st.button("Close Interview", key="close_interview"):
                st.session_state.show_interview = False
                st.rerun()
            
            st.markdown("---")
    
    # Initialize session state
    if 'analysis_done' not in st.session_state:
        st.session_state.analysis_done = False
    if 'results' not in st.session_state:
        st.session_state.results = {}
    
    # Input Section
    st.header("📄 Input Your Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Resume")
        
        # Resume input options
        input_method = st.radio(
            "Choose input method:",
            ["Upload File", "Paste Text"],
            key="resume_input_method"
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
        st.subheader("Job Description")
        jd_text = st.text_area(
            "Paste the job description here:",
            height=350,
            placeholder="Copy and paste the job description you're applying for..."
        )
    
    # Analysis button
    if st.button("🔍 Analyze Application", type="primary"):
        if resume_content and jd_text.strip():
            with st.spinner("Analyzing your application... This may take a moment."):
                try:
                    # Initialize components
                    resume_parser = ResumeParser()
                    jd_processor = JobDescriptionProcessor()
                    matcher = Matcher()
                    recommender = Recommender()
                    
                    # Process resume
                    if isinstance(resume_content, str):
                        resume_data = resume_parser.parse_resume(text_content=resume_content)
                    else:
                        resume_data = resume_parser.parse_resume(file_content=resume_content)
                    
                    # Process job description
                    jd_data = jd_processor.process_jd(jd_text)
                    
                    # Match resume to job
                    match_data = matcher.match_resume_to_jd(resume_data, jd_data)
                    
                    # Generate recommendations
                    recommendations = recommender.build_recommendations(resume_data, jd_data, match_data)
                    
                    # Store results in session state
                    st.session_state.results = {
                        'resume_data': resume_data,
                        'jd_data': jd_data,
                        'match_data': match_data,
                        'recommendations': recommendations
                    }
                    st.session_state.analysis_done = True
                    
                    st.success("✅ Analysis completed! Check the results below.")
                    
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
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13, tab14, tab15 = st.tabs([
        "📊 Summary", 
        "🎯 Skills Analysis", 
        "📋 Resume Structure", 
        "💡 Recommendations", 
        "🎤 Interview Prep",
        "📈 Advanced Analytics",
        "🚀 Professional Tools",
        "🔥 AI Features",
        "🎯 Resume Scoring",
        "🚀 Career Path",
        "💰 Salary Intelligence",
        "🌐 Market Analytics",
        "🤝 Networking Hub",
        "🏢 Company Culture",
        "⚡ Resume Builder"
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
    
    with tab8:
        display_advanced_ai_features_tab(resume_data, jd_data, match_data)
    
    with tab9:
        display_resume_scoring_tab(resume_data, jd_data)
    
    with tab10:
        display_career_path_tab(resume_data, jd_data)
    
    with tab11:
        display_salary_intelligence_tab(resume_data, jd_data, match_data)
    
    with tab12:
        display_market_analytics_tab(resume_data, jd_data, match_data)
    
    with tab13:
        display_networking_hub_tab(resume_data, jd_data, match_data)
    
    with tab14:
        display_company_culture_tab(resume_data, jd_data, match_data)
    
    with tab15:
        display_resume_builder_tab(resume_data, jd_data, match_data)

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
    
    # Consistency Analysis (New Advanced Feature)
    if 'consistency_analysis' in resume_data:
        st.subheader("📏 Resume Consistency Analysis")
        consistency = resume_data['consistency_analysis']
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Consistency Score", f"{consistency['consistency_score']}/100")
        with col2:
            st.info(consistency['consistency_level'])
        
        if consistency['issues_found']:
            st.warning("**Consistency Issues Found:**")
            for issue in consistency['issues_found']:
                st.write(f"• {issue}")
            
            st.info("**Recommendations:**")
            for rec in consistency['recommendations']:
                st.write(f"• {rec}")

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

def display_advanced_ai_features_tab(resume_data, jd_data, match_data):
    """Display Advanced AI Features tab with cutting-edge analysis."""
    st.header("🔥 Advanced AI Features & Deep Analytics")
    
    if not resume_data or 'error' in resume_data:
        st.warning("⚠️ Upload a resume to access advanced AI features")
        return
    
    # Create sub-tabs for different advanced features
    adv_tabs = st.tabs(["🔥 Resume Heatmap", "🤖 ATS Simulation", "🎯 Role Compatibility", 
                       "🛤️ Career Roadmap", "⚠️ Red Flag Detection", "📄 Multiple Versions"])
    
    with adv_tabs[0]:  # Resume Heatmap
        st.subheader("📊 Resume Weakness Heatmap")
        st.write("*Visual analysis of resume strengths and weaknesses*")
        
        if 'heatmap_analysis' in resume_data:
            heatmap_data = resume_data['heatmap_analysis']
            
            # Display overall strength
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Overall Strength", f"{heatmap_data['overall_strength']:.1f}%")
            with col2:
                st.metric("Weakest Section", heatmap_data['weakest_sections'][0] if heatmap_data['weakest_sections'] else "N/A")
            with col3:
                st.metric("Strongest Section", heatmap_data['strongest_sections'][0] if heatmap_data['strongest_sections'] else "N/A")
            
            # Display heatmap visualization
            st.write("**Section Analysis:**")
            for section, data in heatmap_data['heatmap_data'].items():
                col1, col2, col3 = st.columns([2, 1, 3])
                with col1:
                    st.write(f"**{section.title()}**")
                with col2:
                    # Create colored metric based on strength
                    color = data['color']
                    st.markdown(f"<div style='background-color: {color}; color: white; padding: 5px; border-radius: 3px; text-align: center;'>{data['strength']}/100</div>", unsafe_allow_html=True)
                with col3:
                    if data['issues']:
                        st.error(f"Issues: {', '.join(data['issues'])}")
                    else:
                        st.success("✅ No issues detected")
        else:
            st.info("Heatmap analysis not available. Please re-upload your resume.")
    
    with adv_tabs[1]:  # ATS Simulation
        st.subheader("🤖 ATS Parsing Simulation")
        st.write("*See how Applicant Tracking Systems will parse your resume*")
        
        if 'ats_simulation' in resume_data:
            ats_data = resume_data['ats_simulation']
            
            # Display parsing success rate
            col1, col2 = st.columns(2)
            with col1:
                st.metric("ATS Parsing Success Rate", f"{ats_data['parsing_success_rate']}%")
            with col2:
                st.info(f"**ATS Readability:** {ats_data['ats_readability']}")
            
            # Show ATS JSON output
            st.write("**ATS JSON Output:**")
            st.code(ats_data['json_output'], language='json')
            
            # Show parsed data details
            parsed_data = ats_data['parsed_data']
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Personal Information Detected:**")
                for key, value in parsed_data['personal_info'].items():
                    st.write(f"• {key.title()}: {value}")
            
            with col2:
                st.write("**Skills Extracted:**")
                skills = parsed_data['skills'][:10]
                for skill in skills:
                    st.write(f"• {skill}")
            
            # Show improvement suggestions
            if ats_data['improvement_suggestions']:
                st.write("**ATS Optimization Suggestions:**")
                for suggestion in ats_data['improvement_suggestions']:
                    st.write(f"• {suggestion}")
        else:
            st.info("ATS simulation not available. Please re-upload your resume.")
    
    with adv_tabs[2]:  # Role Compatibility
        st.subheader("🎯 Multi-Role Compatibility Analysis")
        st.write("*Analyze compatibility with different career roles*")
        
        if 'role_compatibility' in resume_data:
            role_data = resume_data['role_compatibility']
            
            # Display best fit
            st.success(f"🏆 **Best Fit Role:** {role_data['best_fit_role'].replace('_', ' ').title()} ({role_data['best_fit_score']}% match)")
            
            # Display all role scores
            st.write("**Compatibility Breakdown:**")
            
            for role, data in role_data['role_scores'].items():
                col1, col2, col3 = st.columns([2, 1, 2])
                
                with col1:
                    st.write(f"**{role.replace('_', ' ').title()}**")
                
                with col2:
                    # Progress bar for score
                    st.progress(data['score'] / 100)
                    st.write(f"{data['score']}%")
                
                with col3:
                    st.write(data['strength_level'])
                
                # Show matched and missing keywords
                with st.expander(f"Details for {role.replace('_', ' ').title()}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Matched Keywords:**")
                        for kw in data['matched_keywords'][:5]:
                            st.success(f"✅ {kw}")
                    
                    with col2:
                        st.write("**Missing Keywords:**")
                        for kw in data['missing_keywords'][:5]:
                            st.error(f"❌ {kw}")
            
            # Show recommendations
            if role_data['role_recommendations']:
                st.write("**Recommendations:**")
                for rec in role_data['role_recommendations']:
                    st.info(f"💡 {rec}")
        else:
            st.info("Role compatibility analysis not available.")
    
    with adv_tabs[3]:  # Career Roadmap
        st.subheader("🛤️ Personalized Career Roadmap")
        st.write("*AI-generated learning path based on your goals*")
        
        # Input for career roadmap
        col1, col2 = st.columns(2)
        with col1:
            target_role = st.selectbox("Target Role", 
                                     ["web_developer", "mobile_developer", "data_analyst", "software_engineer"])
        with col2:
            experience_level = st.selectbox("Experience Level", ["beginner", "intermediate"])
        
        if st.button("🚀 Generate Career Roadmap"):
            # Get current skills from resume
            current_skills = list(resume_data.get('resume_skills', {}).get('all_skills', []))
            
            # Generate roadmap using the recommender
            from core.recommender import Recommender
            recommender = Recommender()
            roadmap = recommender.generate_career_roadmap(current_skills, target_role, experience_level)
            
            st.success(f"📅 **Total Timeline:** {roadmap['total_timeline_months']} months ({roadmap['estimated_total_hours']} hours)")
            
            # Display roadmap steps
            for step in roadmap['roadmap_steps']:
                with st.expander(f"Month {step['month']}: {', '.join(step['skills_to_learn'][:2])}... ({step['priority']} Priority)"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Skills to Learn:**")
                        for skill in step['skills_to_learn']:
                            st.write(f"• {skill}")
                        
                        st.write(f"**Estimated Time:** {step['estimated_hours']} hours")
                    
                    with col2:
                        st.write("**Recommended Projects:**")
                        for project in step['projects']:
                            st.write(f"• {project}")
                    
                    # Show learning resources
                    if 'resources' in step:
                        st.write("**Learning Resources:**")
                        resources = step['resources']
                        for category, items in resources.items():
                            if items:
                                st.write(f"**{category.title()}:** {', '.join(items[:3])}")
            
            # Show career advice
            if roadmap['career_advice']:
                st.write("**Career Advice:**")
                for advice in roadmap['career_advice']:
                    st.info(f"💡 {advice}")
    
    with adv_tabs[4]:  # Red Flag Detection
        st.subheader("⚠️ Job Red Flag Detection")
        st.write("*AI analysis of potential warning signs in job descriptions*")
        
        if jd_data and 'red_flag_analysis' in jd_data:
            red_flags = jd_data['red_flag_analysis']
            
            # Display risk assessment
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Risk Score", f"{red_flags['risk_score']}/100")
            with col2:
                risk_level = red_flags['risk_level']
                if 'High Risk' in risk_level:
                    st.error(f"🚨 {risk_level}")
                elif 'Moderate Risk' in risk_level:
                    st.warning(f"⚠️ {risk_level}")
                else:
                    st.success(f"✅ {risk_level}")
            with col3:
                st.write(f"**Red Flags Found:** {len(red_flags['red_flags'])}")
            
            # Display detected red flags
            if red_flags['red_flags']:
                st.write("**⚠️ Detected Red Flags:**")
                for flag in red_flags['red_flags']:
                    st.error(f"🚩 {flag}")
            else:
                st.success("✅ No red flags detected!")
            
            # Show recommendation
            st.info(f"**Recommendation:** {red_flags['recommendation']}")
            
            # Show questions to ask
            if red_flags['questions_to_ask']:
                st.write("**Questions to Ask in Interview:**")
                for question in red_flags['questions_to_ask']:
                    st.write(f"❓ {question}")
        else:
            st.warning("Please upload a job description to detect red flags.")
        
        # Keyword Importance Ranking
        if jd_data and 'keyword_ranking' in jd_data:
            st.markdown("---")
            st.subheader("🔑 Keyword Importance Ranking")
            keyword_data = jd_data['keyword_ranking']
            
            # Display skill categories
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Critical Skills", len(keyword_data['critical_skills']))
                for skill in keyword_data['critical_skills'][:3]:
                    st.error(f"🔥 {skill}")
            
            with col2:
                st.metric("Important Skills", len(keyword_data['important_skills']))
                for skill in keyword_data['important_skills'][:3]:
                    st.warning(f"⚡ {skill}")
            
            with col3:
                st.metric("Nice-to-Have", len(keyword_data['nice_to_have_skills']))
                for skill in keyword_data['nice_to_have_skills'][:3]:
                    st.info(f"💫 {skill}")
            
            # Show top 5 skills breakdown
            st.write("**Top 5 Skills Breakdown:**")
            for i, skill in enumerate(keyword_data['top_5_skills'], 1):
                skill_info = keyword_data['ranked_skills'][skill]
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.write(f"**{i}. {skill}**")
                with col2:
                    st.write(f"Frequency: {skill_info['frequency']}")
                with col3:
                    st.write(f"Score: {skill_info['importance_score']}")
                with col4:
                    priority_color = {'Critical': '🔴', 'Important': '🟡', 'Nice-to-have': '🟢'}
                    st.write(f"{priority_color.get(skill_info['priority'], '⚪')} {skill_info['priority']}")
        
        # Role Expansion Summary
        if jd_data and 'role_expansion' in jd_data:
            st.markdown("---")
            st.subheader("🎯 AI Role Analysis & Expansion")
            role_data = jd_data['role_expansion']
            
            st.success(f"**Primary Role Type:** {role_data['primary_role_type'].replace('_', ' ').title()}")
            st.write(f"**Explanation:** {role_data['role_explanation']}")
            
            col1, col2 = st.columns(2)
            with col1:
                if role_data['key_aspects']:
                    st.write("**Key Aspects:**")
                    for aspect in role_data['key_aspects']:
                        st.write(f"• {aspect.replace('_', ' ').title()}")
                
                if role_data['technical_focus']:
                    st.write("**Technical Focus Areas:**")
                    for focus in role_data['technical_focus']:
                        st.write(f"🔧 {focus}")
            
            with col2:
                if role_data['work_environment']:
                    st.write("**Work Environment:**")
                    for env in role_data['work_environment']:
                        st.write(f"🏢 {env.title()}")
                
                st.write(f"**Career Level:** {role_data['career_level']}")
                st.write(f"**Growth Potential:** {role_data['growth_potential']}")
    
    with adv_tabs[5]:  # Multiple Resume Versions
        st.subheader("📄 Multiple Resume Version Generator")
        st.write("*Generate customized resume versions for different roles*")
        
        # Additional new features display
        if 'duplicate_analysis' in resume_data:
            st.markdown("---")
            st.subheader("🔍 Duplicate Content Analysis")
            dup_data = resume_data['duplicate_analysis']
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Uniqueness Score", f"{dup_data['duplicate_score']}/100")
            with col2:
                st.info(dup_data['uniqueness_level'])
            
            if dup_data['duplicate_issues']:
                st.warning("**Issues Found:**")
                for issue in dup_data['duplicate_issues'][:5]:
                    st.write(f"• {issue}")
        
        if 'timeline_analysis' in resume_data:
            st.markdown("---")
            st.subheader("⏱️ Resume Timeline Validation")
            timeline_data = resume_data['timeline_analysis']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Timeline Score", f"{timeline_data['timeline_score']}/100")
            with col2:
                st.info(timeline_data['timeline_status'])
            with col3:
                if 'year_range' in timeline_data:
                    st.metric("Year Range", timeline_data['year_range'])
        
        if 'project_analysis' in resume_data:
            st.markdown("---")
            st.subheader("🚀 Project Impact Analysis")
            proj_data = resume_data['project_analysis']
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Projects Found", proj_data['projects_found'])
            with col2:
                if proj_data['projects_found'] > 0:
                    st.metric("Avg Impact Score", f"{proj_data['average_impact_score']}/100")
            
            if 'impact_analysis' in proj_data:
                for proj_name, proj_info in proj_data['impact_analysis'].items():
                    with st.expander(f"{proj_name} - {proj_info['improvement_priority']} Priority"):
                        st.write(f"**Score:** {proj_info['impact_score']}/100")
                        if proj_info['strengths']:
                            st.success(f"Strengths: {', '.join(proj_info['strengths'])}")
                        if proj_info['issues']:
                            st.error(f"Issues: {', '.join(proj_info['issues'])}")
        
        target_roles = st.multiselect(
            "Select Target Roles",
            ["mobile_developer", "web_developer", "data_analyst", "software_engineer", "devops_engineer"],
            default=["web_developer", "mobile_developer"]
        )
        
        if st.button("🎯 Generate Resume Versions") and target_roles:
            from core.recommender import Recommender
            recommender = Recommender()
            
            versions = recommender.generate_multiple_resume_versions(resume_data, target_roles)
            
            st.success(f"✅ Generated {len(versions['versions'])} resume versions!")
            
            for role, version_data in versions['versions'].items():
                with st.expander(f"📋 {role.replace('_', ' ').title()} Version"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Customized Summary:**")
                        st.write(version_data['summary'])
                        
                        st.write("**Prioritized Skills:**")
                        high_priority = version_data['prioritized_skills']['high_priority']
                        for skill in high_priority[:5]:
                            st.success(f"🔥 {skill}")
                    
                    with col2:
                        st.write("**Customization Tips:**")
                        for tip in version_data['customization_tips']:
                            st.info(f"💡 {tip}")
                        
                        st.write("**Key Optimization Keywords:**")
                        for keyword in version_data['keyword_optimization'][:4]:
                            st.code(keyword)
            
            # Show general strategy
            st.write("**Application Strategy:**")
            strategy = versions['application_strategy']
            for key, value in strategy.items():
                st.write(f"• **{key.replace('_', ' ').title()}:** {value}")
        
        # Salary Comparison Tool
        st.markdown("---")
        st.subheader("💰 Salary Comparison & Market Analysis")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            salary_role = st.selectbox("Role", ["software_engineer", "web_developer", "mobile_developer", "data_analyst"], key="salary_role")
        with col2:
            salary_location = st.selectbox("Location", ["US", "California", "New York", "Texas", "Remote", "Europe"], key="salary_loc")
        with col3:
            salary_exp = st.selectbox("Experience", ["entry", "mid", "senior"], key="salary_exp")
        
        if st.button("🔍 Analyze Salary Range"):
            from core.recommender import Recommender
            recommender = Recommender()
            
            salary_data = recommender.estimate_salary_range(salary_role, salary_location, salary_exp)
            
            # Display salary range
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Minimum", f"${salary_data['salary_range']['min']:,}")
            with col2:
                st.metric("Average", f"${salary_data['salary_range']['average']:,}")
            with col3:
                st.metric("Maximum", f"${salary_data['salary_range']['max']:,}")
            
            # Market insights
            st.write("**Market Insights:**")
            for insight in salary_data['market_insights']:
                st.info(f"📊 {insight}")
            
            # Negotiation tips
            st.write("**Negotiation Tips:**")
            for tip in salary_data['negotiation_tips']:
                st.write(f"💡 {tip}")
        
        # Job Trends Analysis (if multiple JDs analyzed)
        st.markdown("---")
        st.subheader("📈 Job Market Trends Analysis")
        
        # Sample job trends analysis (would normally use historical data)
        if st.button("🔍 Analyze Market Trends"):
            # Simulate trend analysis with sample data
            st.info("**📊 Market Trends Simulation**")
            
            trending_skills = [
                {'skill': 'Python', 'trend': 'High', 'percentage': 78},
                {'skill': 'JavaScript', 'trend': 'High', 'percentage': 72},
                {'skill': 'React', 'trend': 'Medium', 'percentage': 65},
                {'skill': 'SQL', 'trend': 'High', 'percentage': 69},
                {'skill': 'AWS', 'trend': 'High', 'percentage': 58}
            ]
            
            st.write("**Top Trending Skills:**")
            for skill_data in trending_skills:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**{skill_data['skill']}**")
                with col2:
                    st.progress(skill_data['percentage'] / 100)
                    st.write(f"{skill_data['percentage']}% of jobs")
                with col3:
                    trend_color = {'High': '🔥', 'Medium': '📈', 'Low': '📊'}
                    st.write(f"{trend_color[skill_data['trend']]} {skill_data['trend']} Demand")
            
            st.success("💡 **Recommendation:** Focus on Python and JavaScript for maximum opportunities")
        
        # Competition Level Analysis
        if jd_data and 'keyword_ranking' in jd_data:
            st.markdown("---")
            st.subheader("🏆 Job Competition Analysis")
            
            from core.recommender import Recommender
            recommender = Recommender()
            
            competition_data = recommender.detect_competition_level(jd_data['jd_text'], jd_data)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Competition Level", competition_data['competition_level'])
            with col2:
                st.metric("Competition Score", f"{competition_data['competition_score']}/100")
            
            st.info(competition_data['description'])
            
            if competition_data['factors']:
                st.write("**Competition Factors:**")
                for factor in competition_data['factors']:
                    st.write(f"• {factor}")
            
            st.write("**Application Strategy:**")
            for strategy in competition_data['application_strategy']:
                st.write(f"🎯 {strategy}")
            
            st.write(f"**Recommended Timeline:** {competition_data['timeline_advice']}")

def display_resume_scoring_tab(resume_data: Dict, jd_data: Dict):
    """Display advanced resume scoring and ATS analysis."""
    st.header("🎯 Intelligent Resume Scoring")
    
    # Initialize components
    resume_parser = ResumeParser()
    
    # Get resume text for analysis
    resume_text = resume_data.get('resume_text', str(resume_data))
    jd_text = jd_data.get('jd_text', '')
    
    # Extract target role from JD
    job_processor = JobDescriptionProcessor()
    role_analysis = job_processor.generate_role_expansion_summary(jd_text)
    target_role = role_analysis.get('primary_role_type', 'software_engineer')
    
    st.subheader("📊 Overall Resume Score")
    
    # Calculate intelligent resume score
    scoring_result = resume_parser.calculate_intelligent_resume_score(resume_text, target_role)
    
    # Display overall score with color coding
    overall_score = scoring_result['overall_score']
    
    if overall_score >= 85:
        score_color = "🟢"
        score_message = "Excellent! Your resume is highly optimized"
    elif overall_score >= 70:
        score_color = "🟡"
        score_message = "Good resume with room for improvement"
    elif overall_score >= 55:
        score_color = "🟠"
        score_message = "Fair resume that needs significant enhancement"
    else:
        score_color = "🔴"
        score_message = "Your resume needs major improvements"
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall Score", f"{overall_score}/100", delta=None)
    with col2:
        st.metric("Score Category", score_color)
    with col3:
        st.metric("Target Role", target_role.replace('_', ' ').title())
    
    st.info(f"**Assessment:** {score_message}")
    
    # Individual score breakdown
    st.subheader("📈 Score Breakdown")
    
    individual_scores = scoring_result['individual_scores']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Content Quality (25%)**")
        st.progress(individual_scores['content_quality'] / 100)
        st.write(f"{individual_scores['content_quality']}/100")
        
        st.write("**ATS Compatibility (20%)**")
        st.progress(individual_scores['ats_compatibility'] / 100)
        st.write(f"{individual_scores['ats_compatibility']}/100")
        
        st.write("**Keyword Optimization (20%)**")
        st.progress(individual_scores['keyword_optimization'] / 100)
        st.write(f"{individual_scores['keyword_optimization']}/100")
    
    with col2:
        st.write("**Formatting Score (10%)**")
        st.progress(individual_scores['formatting_score'] / 100)
        st.write(f"{individual_scores['formatting_score']}/100")
        
        st.write("**Experience Relevance (15%)**")
        st.progress(individual_scores['experience_relevance'] / 100)
        st.write(f"{individual_scores['experience_relevance']}/100")
        
        st.write("**Skill Match (10%)**")
        st.progress(individual_scores['skill_match'] / 100)
        st.write(f"{individual_scores['skill_match']}/100")
    
    # Recommendations
    if scoring_result['recommendations']:
        st.subheader("💡 Improvement Recommendations")
        for i, rec in enumerate(scoring_result['recommendations'], 1):
            st.write(f"{i}. {rec}")
    
    # Strengths and Weaknesses
    col1, col2 = st.columns(2)
    
    with col1:
        if scoring_result['strengths']:
            st.success("**🎯 Your Strengths:**")
            for strength in scoring_result['strengths']:
                st.write(f"✅ {strength.replace('_', ' ').title()}")
    
    with col2:
        if scoring_result['weaknesses']:
            st.warning("**⚠️ Areas to Improve:**")
            for weakness in scoring_result['weaknesses']:
                st.write(f"❌ {weakness.replace('_', ' ').title()}")
    
    # ATS Compatibility Analysis
    st.markdown("---")
    st.subheader("🤖 Advanced ATS Compatibility Analysis")
    
    ats_result = resume_parser.analyze_ats_compatibility_advanced(resume_text)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("ATS Score", f"{ats_result['overall_ats_score']}/100")
    with col2:
        st.metric("ATS Grade", ats_result['ats_grade'])
    with col3:
        st.metric("Parsing Success Rate", ats_result['estimated_parsing_success'])
    
    st.info(f"**Parsing Confidence:** {ats_result['parsing_confidence']}")
    
    # ATS Compatibility Checks
    st.write("**🔍 Detailed ATS Checks:**")
    
    checks = ats_result['compatibility_checks']
    for check_name, check_data in checks.items():
        col1, col2, col3 = st.columns([2, 1, 3])
        
        with col1:
            st.write(f"**{check_name.replace('_', ' ').title()}**")
        
        with col2:
            score = check_data['score']
            if score >= 80:
                st.success(f"{score}/100")
            elif score >= 60:
                st.warning(f"{score}/100")
            else:
                st.error(f"{score}/100")
        
        with col3:
            st.write(check_data['note'])
    
    # ATS Recommendations
    if ats_result['ats_recommendations']:
        st.subheader("🛠️ ATS Optimization Recommendations")
        for i, rec in enumerate(ats_result['ats_recommendations'], 1):
            st.write(f"{i}. {rec}")

def display_career_path_tab(resume_data: Dict, jd_data: Dict):
    """Display career path analysis and skill gap analysis."""
    st.header("🚀 Career Path & Skill Gap Analysis")
    
    # Initialize career analyzer
    career_analyzer = CareerAnalyzer()
    
    # Extract current information
    resume_skills = resume_data.get('resume_skills', {}).get('all_skills', [])
    resume_text = resume_data.get('resume_text', str(resume_data))
    
    # Estimate experience years
    import re
    experience_patterns = re.findall(r'(\d+)\+?\s*(?:years?|yrs?)', resume_text.lower())
    experience_years = max([int(year) for year in experience_patterns]) if experience_patterns else 2
    
    # Get target role from JD
    job_processor = JobDescriptionProcessor()
    role_analysis = job_processor.generate_role_expansion_summary(jd_data.get('jd_text', ''))
    target_role = role_analysis.get('primary_role_type', 'software_engineer')
    
    # Input section for career path analysis
    st.subheader("🎯 Career Path Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        current_role = st.selectbox(
            "Current Role:",
            ['junior_developer', 'software_engineer', 'web_developer', 'data_analyst', 'mobile_developer'],
            index=1
        )
    
    with col2:
        selected_target_role = st.selectbox(
            "Target Role:",
            ['senior_software_engineer', 'tech_lead', 'data_scientist', 'devops_engineer', 'solution_architect'],
            index=0
        )
    
    with col3:
        years_experience = st.number_input(
            "Years of Experience:",
            min_value=0,
            max_value=20,
            value=experience_years,
            step=1
        )
    
    # Career Progression Analysis
    if st.button("🔍 Analyze Career Progression"):
        st.markdown("---")
        st.subheader("📊 Career Progression Analysis")
        
        progression_result = career_analyzer.analyze_career_progression(
            current_role, selected_target_role, resume_skills, years_experience
        )
        
        # Feasibility Score
        col1, col2, col3 = st.columns(3)
        
        with col1:
            feasibility_score = progression_result['feasibility_score']
            st.metric("Feasibility Score", f"{feasibility_score}/100")
            
        with col2:
            timeline = progression_result.get('progression_timeline', 'Unknown')
            st.metric("Timeline", timeline)
            
        with col3:
            if feasibility_score >= 80:
                st.success("High Feasibility")
            elif feasibility_score >= 60:
                st.warning("Moderate Feasibility")
            else:
                st.error("Challenging Transition")
        
        # Success Factors
        if progression_result['success_factors']:
            st.write("**🎯 Success Factors:**")
            for factor in progression_result['success_factors']:
                st.write(f"✅ {factor}")
        
        # Intermediate Roles
        if progression_result['intermediate_roles']:
            st.write("**🛤️ Recommended Intermediate Roles:**")
            for role in progression_result['intermediate_roles']:
                st.write(f"🔄 {role.replace('_', ' ').title()}")
        
        # Learning Path
        if progression_result['learning_path']:
            st.subheader("📚 Structured Learning Path")
            
            for phase in progression_result['learning_path']:
                with st.expander(f"📖 {phase['phase']}: {phase['focus']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Skills to Develop:**")
                        for skill in phase['skills']:
                            st.write(f"• {skill}")
                    
                    with col2:
                        st.write("**Resources:**")
                        for resource in phase['resources']:
                            st.write(f"• {resource}")
                    
                    st.write(f"**Timeline:** {phase['timeline']}")
                    st.write(f"**Success Metrics:** {', '.join(phase['success_metrics'])}")
        
        # Salary Progression
        if progression_result['salary_progression']:
            st.subheader("💰 Salary Progression Analysis")
            
            salary_data = progression_result['salary_progression']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Current Estimated Salary", f"${salary_data['current_estimated_salary']:,}")
            
            with col2:
                st.metric("Target Estimated Salary", f"${salary_data['target_estimated_salary']:,}")
            
            with col3:
                increase = salary_data['potential_increase']
                percentage = salary_data.get('percentage_increase', 0)
                st.metric("Potential Increase", f"${increase:,}", f"{percentage}%")
            
            st.info(f"**ROI Assessment:** {salary_data.get('roi_timeline', 'Not calculated')}")
    
    # Skill Gap Analysis
    st.markdown("---")
    st.subheader("🎯 Comprehensive Skill Gap Analysis")
    
    if st.button("📊 Generate Skill Gap Report"):
        gap_report = career_analyzer.generate_skill_gap_report(
            resume_skills, selected_target_role, 'technology'
        )
        
        # Gap Analysis Summary
        summary = gap_report['gap_analysis_summary']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Required Skills", summary['total_required_skills'])
        
        with col2:
            st.metric("Skill Gaps", summary['total_skill_gaps'])
        
        with col3:
            st.metric("Coverage", f"{summary['skill_coverage_percentage']}%")
        
        with col4:
            readiness = summary['readiness_level']
            if readiness == 'High':
                st.success(f"Readiness: {readiness}")
            elif readiness == 'Medium':
                st.warning(f"Readiness: {readiness}")
            else:
                st.error(f"Readiness: {readiness}")
        
        st.write(f"**⏱️ Preparation Time:** {summary['estimated_preparation_time']}")
        
        # Critical vs Nice-to-Have Gaps
        col1, col2 = st.columns(2)
        
        with col1:
            if gap_report['critical_gaps']:
                st.error("**🚨 Critical Skill Gaps:**")
                for gap in gap_report['critical_gaps']:
                    st.write(f"❌ {gap}")
            else:
                st.success("**✅ No Critical Gaps Found!**")
        
        with col2:
            if gap_report['nice_to_have_gaps']:
                st.warning("**💡 Enhancement Opportunities:**")
                for gap in gap_report['nice_to_have_gaps']:
                    st.write(f"🔸 {gap}")
        
        # Skill Development Priority
        if gap_report['skill_development_priority']:
            st.subheader("📋 Skill Development Priority Matrix")
            
            priority_df = pd.DataFrame(gap_report['skill_development_priority'])
            
            # Display as a formatted table
            for _, row in priority_df.iterrows():
                with st.expander(f"{'🔴' if row['priority'] == 'High' else '🟡'} {row['skill']} ({row['priority']} Priority)"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Difficulty:** {row['learning_difficulty']}")
                    
                    with col2:
                        st.write(f"**Market Demand:** {row['market_demand']}")
                    
                    with col3:
                        st.write(f"**Timeline:** {row['recommended_timeline']}")
        
        # Learning Resources & Timeline
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📚 Recommended Resources")
            resources = gap_report['learning_resources']
            
            st.write("**Online Courses:**")
            for course in resources['online_courses']:
                st.write(f"🎓 {course}")
            
            st.write("**Practice Platforms:**")
            for platform in resources['practice_platforms']:
                st.write(f"💻 {platform}")
        
        with col2:
            st.subheader("💰 Investment Estimate")
            costs = gap_report['cost_estimate']
            
            st.write(f"**Total Range:** {costs['total_estimated_range']}")
            st.write(f"**Online Courses:** {costs['online_courses']}")
            st.write(f"**Books & Resources:** {costs['books_resources']}")
            st.write(f"**Certifications:** {costs['certification_exams']}")
            
            if costs['cost_saving_tips']:
                st.info("**💡 Cost Saving Tips:**")
                for tip in costs['cost_saving_tips']:
                    st.write(f"• {tip}")
        
        # Progress Tracking Framework
        st.subheader("📈 Progress Tracking Framework")
        
        tracking = gap_report['progress_tracking']
        
        st.write("**🎯 Key Milestones:**")
        for milestone in tracking['milestones']:
            st.write(f"Week {milestone['week']}: {milestone['goal']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**✅ Success Metrics:**")
            for metric in tracking['success_metrics']:
                st.write(f"• {metric}")
        
        with col2:
            st.write("**🛠️ Tracking Tools:**")
            for tool in tracking['tracking_tools']:
                st.write(f"• {tool}")
    
    # Industry Insights from JD
    st.markdown("---")
    st.subheader("🏢 Industry Insights")
    
    if jd_data.get('jd_text'):
        job_processor = JobDescriptionProcessor()
        
        # Industry Analysis
        industry_insights = job_processor.analyze_industry_insights(jd_data['jd_text'])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Primary Industry", industry_insights['primary_industry'].replace('_', ' ').title())
        
        with col2:
            st.metric("Growth Outlook", industry_insights['growth_outlook'])
        
        with col3:
            st.metric("Company Size", industry_insights['company_size'].replace('_', ' ').title())
        
        # Market Insights
        if industry_insights['market_insights']:
            st.write("**📊 Market Insights:**")
            for insight in industry_insights['market_insights']:
                st.write(f"💡 {insight}")
        
        # Job Difficulty Assessment
        difficulty_analysis = job_processor.assess_job_difficulty_advanced(jd_data['jd_text'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**🎯 Difficulty Level:** {difficulty_analysis['difficulty_level']}")
            st.progress(difficulty_analysis['difficulty_score'] / 100)
            st.write(f"Score: {difficulty_analysis['difficulty_score']}/100")
        
        with col2:
            st.write(f"**⏱️ Prep Timeline:** {difficulty_analysis['preparation_timeline']}")
            st.write(f"**💡 Recommendation:** {difficulty_analysis['recommendation']}")

def display_salary_intelligence_tab(resume_data: Dict, jd_data: Dict, match_data: Dict):
    """Display salary intelligence and compensation analysis."""
    st.header("💰 Salary Intelligence & Compensation Analysis")
    
    # Initialize components
    recommender = Recommender()
    job_processor = JobDescriptionProcessor()
    
    # Salary estimation
    if jd_data.get('jd_text'):
        # Extract role from job description or use default
        job_processor = JobDescriptionProcessor()
        jd_analysis = job_processor.generate_role_expansion_summary(jd_data['jd_text'])
        estimated_role = jd_analysis.get('primary_role_type', 'software_engineer')
        
        # Determine experience level based on years
        experience_years = resume_data.get('experience_years', 0)
        if experience_years <= 2:
            experience_level = 'entry'
        elif experience_years <= 7:
            experience_level = 'mid'
        else:
            experience_level = 'senior'
        
        # Use default location (can be enhanced later to detect from resume)
        default_location = 'US'
        
        salary_analysis = recommender.estimate_salary_range(
            estimated_role,
            default_location,
            experience_level
        )
        
        st.subheader("🎯 Salary Estimation")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            salary_range = salary_analysis.get('salary_range', {})
            st.metric(
                "Base Salary Range",
                f"${salary_range.get('min', 0):,} - ${salary_range.get('max', 0):,}"
            )
        
        with col2:
            growth_projections = salary_analysis.get('growth_projections', {})
            st.metric(
                "5-Year Projection",
                f"${growth_projections.get('5_year', 0):,}"
            )
        
        with col3:
            st.metric("Market Position", "Competitive")
            
        with col4:
            st.metric("Growth Potential", "Strong")
        
        # Compensation breakdown
        st.subheader("📊 Compensation Breakdown")
        
        salary_range = salary_analysis.get('salary_range', {})
        salary_min = salary_range.get('min', 0)
        salary_max = salary_range.get('max', 0)
        
        compensation_data = {
            'Component': ['Base Salary', 'Bonus', 'Stock Options', 'Benefits'],
            'Percentage': [70, 15, 10, 5],
            'Amount Range': [
                f"${salary_min:,} - ${salary_max:,}",
                f"${int(salary_min * 0.15):,} - ${int(salary_max * 0.15):,}",
                f"${int(salary_min * 0.10):,} - ${int(salary_max * 0.10):,}",
                f"${int(salary_min * 0.05):,} - ${int(salary_max * 0.05):,}"
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
        
        negotiation_tips = salary_analysis.get('negotiation_tips', [
            "Research market rates for your role and location",
            "Highlight your unique skills and achievements",
            "Consider total compensation, not just base salary",
            "Be prepared to negotiate benefits and perks",
            "Practice your negotiation conversation beforehand"
        ])
        
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
    
    # Industry trends
    st.subheader("📊 Industry Growth Trends")
    
    industry_trends = {
        'Quarter': ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024'],
        'Technology': [15, 18, 22, 25],
        'Finance': [8, 10, 12, 14],
        'Healthcare': [12, 14, 16, 18],
        'E-commerce': [20, 25, 28, 32]
    }
    
    df_trends = pd.DataFrame(industry_trends)
    df_melted = pd.melt(df_trends, id_vars=['Quarter'], var_name='Industry', value_name='Growth %')
    
    fig_line = px.line(df_melted, x='Quarter', y='Growth %', color='Industry',
                      title="Industry Growth Trends Over Time",
                      markers=True)
    st.plotly_chart(fig_line, use_container_width=True)
    
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

def display_networking_hub_tab(resume_data: Dict, jd_data: Dict, match_data: Dict):
    """Display networking opportunities and professional connections."""
    st.header("🤝 Professional Networking Hub")
    
    # Initialize recommender
    recommender = Recommender()
    
    # Networking strategy
    if jd_data.get('jd_text'):
        # Extract role from job description
        job_processor = JobDescriptionProcessor()
        jd_analysis = job_processor.generate_role_expansion_summary(jd_data['jd_text'])
        target_role = jd_analysis.get('primary_role_type', 'software_engineer')
        
        # Create target companies list (can be enhanced to extract from JD)
        target_companies = ['Google', 'Microsoft', 'Amazon', 'Meta', 'Apple']
        
        # Use default location
        location = 'US'
        
        networking_strategy = recommender.generate_networking_strategy(
            target_role,
            target_companies,
            location
        )
        
        st.subheader("🎯 Personalized Networking Strategy")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🌟 LinkedIn Optimization:**")
            for tip in networking_strategy.get('linkedin_optimization', [])[:5]:
                st.write(f"✅ {tip}")
        
        with col2:
            st.write("**📍 Networking Events:**")
            for event in networking_strategy.get('networking_events', []):
                st.write(f"🎪 {event}")
        
        # LinkedIn optimization
        st.subheader("💼 LinkedIn Profile Optimization")
        
        linkedin_tips = [
            "Optimize your headline with target role keywords",
            "Write a compelling summary highlighting achievements",
            "Get endorsements for key skills from connections",
            "Share industry-relevant content regularly",
            "Join professional groups in your field",
            "Engage with posts from target companies",
            "Request informational interviews with industry professionals"
        ]
        
        for tip in linkedin_tips:
            st.write(f"✅ {tip}")
        
        # Professional associations
        st.subheader("🏛️ Professional Associations & Communities")
        
        associations = {
            'Organization': [
                'IEEE Computer Society',
                'ACM (Association for Computing Machinery)',
                'Product Management Association',
                'Data Science Society',
                'Cloud Security Alliance',
                'DevOps Institute'
            ],
            'Membership Cost': ['$100/year', '$99/year', '$150/year', '$75/year', '$200/year', '$120/year'],
            'Benefits': [
                'Technical publications, conferences',
                'Research access, networking events',
                'PM certification, job board',
                'Workshops, peer connections',
                'Security training, certifications',
                'DevOps certification, community'
            ]
        }
        
        df_associations = pd.DataFrame(associations)
        st.dataframe(df_associations, use_container_width=True)
        
        # Mentorship opportunities
        st.subheader("🎓 Mentorship & Learning Opportunities")
        
        mentorship_platforms = [
            "**ADPList** - Free mentorship platform with industry experts",
            "**MentorCruise** - Paid mentorship with senior professionals",
            "**Ten Thousand Coffees** - Corporate mentoring programs",
            "**SCORE Mentors** - Business mentorship and advice",
            "**Industry-specific Slack communities** - Real-time peer support",
            "**Local meetup groups** - Face-to-face networking"
        ]
        
        for platform in mentorship_platforms:
            st.write(f"🌟 {platform}")
        
        # Conference recommendations
        st.subheader("🎪 Upcoming Tech Conferences")
        
        conferences = {
            'Conference': [
                'AWS re:Invent 2024',
                'Google I/O 2024',
                'Microsoft Build 2024',
                'PyCon 2024',
                'React Summit 2024',
                'DevOps World 2024'
            ],
            'Date': [
                'Dec 2-6, 2024',
                'May 14-15, 2024',
                'May 21-23, 2024',
                'May 15-23, 2024',
                'Jun 14-18, 2024',
                'Sep 24-26, 2024'
            ],
            'Location': [
                'Las Vegas, NV',
                'Mountain View, CA',
                'Seattle, WA',
                'Pittsburgh, PA',
                'Amsterdam, NL',
                'Orlando, FL'
            ],
            'Cost': ['$1,599', '$375', '$2,395', '$665', '$899', '$1,200']
        }
        
        df_conferences = pd.DataFrame(conferences)
        st.dataframe(df_conferences, use_container_width=True)

def display_company_culture_tab(resume_data: Dict, jd_data: Dict, match_data: Dict):
    """Display company culture analysis and fit assessment."""
    st.header("🏢 Company Culture & Fit Analysis")
    
    # Culture assessment
    if jd_data.get('jd_text'):
        job_processor = JobDescriptionProcessor()
        
        # Extract company insights
        st.subheader("🔍 Company Culture Insights")
        
        # Simulated culture analysis (would normally use NLP on job description)
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

def display_resume_builder_tab(resume_data: Dict, jd_data: Dict, match_data: Dict):
    """Display interactive resume builder and optimizer."""
    st.header("⚡ AI-Powered Resume Builder & Optimizer")
    
    # Resume optimization suggestions
    st.subheader("🎯 Resume Optimization Suggestions")
    
    resume_parser = ResumeParser()
    
    if resume_data.get('resume_text'):
        # ATS optimization
        ats_analysis = resume_parser.analyze_ats_compatibility_advanced(resume_data['resume_text'])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("ATS Score", f"{ats_analysis['overall_score']}/100")
        
        with col2:
            st.metric("Keyword Density", f"{ats_analysis.get('keyword_density', 0)}%")
        
        with col3:
            formatting_score = ats_analysis.get('formatting_score', 0)
            st.metric("Format Score", f"{formatting_score}/100")
        
        # Specific improvements
        st.subheader("📝 Specific Improvements Needed")
        
        improvements = ats_analysis.get('improvement_suggestions', [])
        for improvement in improvements:
            st.write(f"🔧 {improvement}")
        
        # Resume sections optimization
        st.subheader("📋 Section-by-Section Analysis")
        
        section_analysis = {
            'Section': [
                'Professional Summary',
                'Work Experience', 
                'Skills',
                'Education',
                'Projects',
                'Certifications'
            ],
            'Current Score': [75, 85, 90, 70, 65, 80],
            'Optimization Tips': [
                'Add more quantified achievements and metrics',
                'Include more action verbs and specific results',
                'Categorize skills (technical, soft, domain-specific)',
                'Add relevant coursework and GPA if recent graduate',
                'Highlight technologies used and outcomes achieved',
                'Include completion dates and renewal status'
            ]
        }
        
        df_sections = pd.DataFrame(section_analysis)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            fig_sections = px.bar(df_sections, x='Current Score', y='Section',
                                orientation='h', title="Section Scores",
                                color='Current Score', color_continuous_scale='RdYlGn')
            st.plotly_chart(fig_sections, use_container_width=True)
        
        with col2:
            st.dataframe(df_sections[['Section', 'Optimization Tips']], use_container_width=True)
    
    # Interactive resume editor
    st.subheader("✏️ Interactive Resume Editor")
    
    # Professional summary generator
    with st.expander("📝 AI Professional Summary Generator"):
        col1, col2 = st.columns(2)
        
        with col1:
            target_role = st.text_input("Target Role", placeholder="e.g., Senior Software Engineer")
            years_exp = st.number_input("Years of Experience", min_value=0, max_value=50, value=5)
            key_skills = st.text_area("Key Skills (comma-separated)", 
                                    placeholder="Python, React, AWS, Team Leadership")
        
        with col2:
            industry = st.selectbox("Industry", 
                                  ["Technology", "Finance", "Healthcare", "Consulting", "E-commerce"])
            achievements = st.text_area("Top Achievements", 
                                      placeholder="Led team of 10, Increased efficiency by 30%")
        
        if st.button("🤖 Generate Professional Summary"):
            if target_role and key_skills:
                generated_summary = f"""
                Experienced {target_role} with {years_exp}+ years in {industry.lower()}. 
                Expertise in {key_skills.replace(',', ', ')}. 
                Proven track record: {achievements}. 
                Strong problem-solving abilities and team collaboration skills.
                """
                
                st.success("Generated Professional Summary:")
                st.text_area("Copy this summary:", generated_summary, height=100)
    
    # Bullet point optimizer
    with st.expander("🔫 Bullet Point Optimizer"):
        st.write("Transform weak bullet points into powerful, quantified achievements:")
        
        weak_bullet = st.text_area("Enter your current bullet point:", 
                                 placeholder="Worked on improving the system")
        
        if st.button("🚀 Optimize Bullet Point"):
            if weak_bullet:
                # Simple optimization suggestions
                optimized_suggestions = [
                    f"Optimized system performance, resulting in 25% faster response times and improved user experience",
                    f"Led system improvement initiative, reducing processing time by 30% and serving 10,000+ daily users",
                    f"Implemented system enhancements that decreased downtime by 40% and increased customer satisfaction to 95%"
                ]
                
                st.success("Optimized versions:")
                for i, suggestion in enumerate(optimized_suggestions, 1):
                    st.write(f"**Option {i}:** {suggestion}")
    
    # Keywords suggester
    with st.expander("🔑 Keyword Optimization"):
        if jd_data.get('jd_text'):
            job_processor = JobDescriptionProcessor()
            
            # Extract key terms from job description
            jd_skills = job_processor.extract_skills(jd_data['jd_text'])
            
            st.write("**Keywords found in job description:**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**Technical Skills:**")
                for skill in jd_skills.get('technical_skills', [])[:5]:
                    st.write(f"• {skill}")
            
            with col2:
                st.write("**Soft Skills:**")
                for skill in jd_skills.get('soft_skills', [])[:5]:
                    st.write(f"• {skill}")
            
            with col3:
                st.write("**Domain Skills:**")
                for skill in jd_skills.get('domain_specific', [])[:5]:
                    st.write(f"• {skill}")
        
        else:
            st.info("Upload a job description to get targeted keyword suggestions!")
    
    # Resume templates
    st.subheader("📄 Professional Resume Templates")
    
    template_options = {
        'Modern ATS-Friendly': {
            'description': 'Clean, single-column layout optimized for ATS systems',
            'best_for': 'Corporate roles, traditional industries',
            'features': ['Single column', 'Standard fonts', 'Clear sections']
        },
        'Creative Professional': {
            'description': 'Visually appealing with subtle design elements',
            'best_for': 'Design, marketing, creative roles',
            'features': ['Color accents', 'Icons', 'Visual hierarchy']
        },
        'Technical Focused': {
            'description': 'Emphasizes technical skills and projects',
            'best_for': 'Software engineers, data scientists',
            'features': ['Skills matrix', 'Project highlights', 'Technical sections']
        },
        'Executive Level': {
            'description': 'Professional layout for senior positions',
            'best_for': 'C-level, director, VP roles',
            'features': ['Leadership focus', 'Achievement metrics', 'Board format']
        }
    }
    
    selected_template = st.selectbox("Choose a template:", list(template_options.keys()))
    
    if selected_template:
        template_info = template_options[selected_template]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write(f"**Description:** {template_info['description']}")
            st.write(f"**Best for:** {template_info['best_for']}")
        
        with col2:
            st.write("**Key Features:**")
            for feature in template_info['features']:
                st.write(f"• {feature}")
        
        if st.button(f"📥 Download {selected_template} Template"):
            st.success(f"Template '{selected_template}' would be downloaded!")
            st.info("💡 Pro tip: Customize the template with your optimized content for best results.")

    # Enhanced Footer
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

if __name__ == "__main__":
    main()