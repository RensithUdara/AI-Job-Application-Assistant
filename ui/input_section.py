"""
Input Section Module
Contains the resume and job description input functionality.
"""

import streamlit as st

def display_input_section():
    """Display the input section for resume and job description."""
    st.header("📄 Input Your Information")
    
    col1, col2 = st.columns(2)
    
    resume_content = None
    jd_text = None
    
    with col1:
        st.subheader("Resume")
        
        # Resume input options
        input_method = st.radio(
            "Choose input method:",
            ["Upload File", "Paste Text"],
            key="resume_input_method"
        )
        
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
    
    return resume_content, jd_text

def process_analysis_request(resume_content, jd_text):
    """Process the analysis request and return results."""
    if not resume_content or not jd_text.strip():
        st.warning("⚠️ Please provide both resume and job description.")
        return None
    
    with st.spinner("Analyzing your application... This may take a moment."):
        try:
            # Import core components
            from core.resume_parser import ResumeParser
            from core.jd_processor import JobDescriptionProcessor
            from core.matcher import Matcher
            from core.recommender import Recommender
            
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
            results = {
                'resume_data': resume_data,
                'jd_data': jd_data,
                'match_data': match_data,
                'recommendations': recommendations
            }
            
            st.session_state.results = results
            st.session_state.analysis_done = True
            
            st.success("✅ Analysis completed! Check the results below.")
            return results
            
        except Exception as e:
            st.error(f"❌ Error during analysis: {str(e)}")
            return None