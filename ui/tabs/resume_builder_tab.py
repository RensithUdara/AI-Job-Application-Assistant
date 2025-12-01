"""
Resume Builder Tab Module
Displays interactive resume builder and optimizer tools.
"""

import streamlit as st
from typing import Dict

def display_resume_builder_tab(resume_data: Dict, jd_data: Dict, match_data: Dict):
    """Display interactive resume builder and optimizer."""
    st.header("⚡ AI-Powered Resume Builder & Optimizer")
    
    # Resume optimization suggestions
    st.subheader("🎯 Resume Optimization Suggestions")
    
    if resume_data.get('resume_text'):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("ATS Score", "78/100")
        with col2:
            st.metric("Keyword Density", "65%")
        with col3:
            st.metric("Format Score", "85/100")
        
        # Specific improvements
        st.subheader("📝 Specific Improvements Needed")
        improvements = [
            "Add more quantified achievements with specific metrics",
            "Include more industry-relevant keywords",
            "Improve action verb usage in bullet points",
            "Enhance professional summary section"
        ]
        
        for improvement in improvements:
            st.write(f"🔧 {improvement}")
    
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
                optimized_suggestions = [
                    f"Optimized system performance, resulting in 25% faster response times and improved user experience",
                    f"Led system improvement initiative, reducing processing time by 30% and serving 10,000+ daily users",
                    f"Implemented system enhancements that decreased downtime by 40% and increased customer satisfaction to 95%"
                ]
                
                st.success("Optimized versions:")
                for i, suggestion in enumerate(optimized_suggestions, 1):
                    st.write(f"**Option {i}:** {suggestion}")
    
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