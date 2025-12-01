"""
Resume Templates Tab
Professional resume templates and builder interface.
"""

import streamlit as st

def display_resume_templates_tab():
    """Display the Resume Templates interface as a full tab."""
    st.markdown("## 📄 Professional Resume Templates")
    st.markdown("Choose from our collection of ATS-friendly, professional resume templates designed for different industries and experience levels.")
    
    # Template categories
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 ATS-Friendly", 
        "🎨 Creative Professional", 
        "💻 Technical Focused", 
        "👔 Executive Level"
    ])
    
    with tab1:
        display_ats_templates()
    
    with tab2:
        display_creative_templates()
    
    with tab3:
        display_technical_templates()
    
    with tab4:
        display_executive_templates()

def display_ats_templates():
    """Display ATS-friendly resume templates."""
    st.markdown("### 🎯 ATS-Friendly Templates")
    st.info("These templates are optimized to pass Applicant Tracking Systems (ATS) used by most companies.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='border: 2px solid #667eea; border-radius: 10px; padding: 1rem; margin: 0.5rem 0; background: white;'>
            <h4 style='color: #667eea; margin: 0;'>📋 Classic Professional</h4>
            <p style='margin: 0.5rem 0; color: #666;'>Clean, traditional layout perfect for corporate roles</p>
            <ul style='color: #666; font-size: 0.9rem;'>
                <li>Simple, clean design</li>
                <li>Standard sections layout</li>
                <li>ATS-optimized formatting</li>
                <li>Works for any industry</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Use Template", key="classic_prof"):
            generate_template("classic_professional")
    
    with col2:
        st.markdown("""
        <div style='border: 2px solid #667eea; border-radius: 10px; padding: 1rem; margin: 0.5rem 0; background: white;'>
            <h4 style='color: #667eea; margin: 0;'>📊 Modern Minimalist</h4>
            <p style='margin: 0.5rem 0; color: #666;'>Contemporary design with subtle accents</p>
            <ul style='color: #666; font-size: 0.9rem;'>
                <li>Modern, clean lines</li>
                <li>Subtle color accents</li>
                <li>Excellent readability</li>
                <li>Perfect for tech roles</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Use Template", key="modern_min"):
            generate_template("modern_minimalist")
    
    with col3:
        st.markdown("""
        <div style='border: 2px solid #667eea; border-radius: 10px; padding: 1rem; margin: 0.5rem 0; background: white;'>
            <h4 style='color: #667eea; margin: 0;'>🎯 Skills-Focused</h4>
            <p style='margin: 0.5rem 0; color: #666;'>Highlights skills and achievements prominently</p>
            <ul style='color: #666; font-size: 0.9rem;'>
                <li>Skills section prominent</li>
                <li>Achievement-focused</li>
                <li>Great for career changers</li>
                <li>Quantified results emphasis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Use Template", key="skills_focused"):
            generate_template("skills_focused")

def display_creative_templates():
    """Display creative professional templates."""
    st.markdown("### 🎨 Creative Professional Templates")
    st.info("Eye-catching designs for creative industries while maintaining professionalism.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='border: 2px solid #e91e63; border-radius: 10px; padding: 1rem; margin: 0.5rem 0; background: white;'>
            <h4 style='color: #e91e63; margin: 0;'>🎨 Designer Portfolio</h4>
            <p style='margin: 0.5rem 0; color: #666;'>Perfect for designers and creative professionals</p>
            <ul style='color: #666; font-size: 0.9rem;'>
                <li>Portfolio section included</li>
                <li>Visual hierarchy emphasis</li>
                <li>Color-coordinated design</li>
                <li>Project showcase ready</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Use Template", key="designer_port"):
            generate_template("designer_portfolio")
    
    with col2:
        st.markdown("""
        <div style='border: 2px solid #e91e63; border-radius: 10px; padding: 1rem; margin: 0.5rem 0; background: white;'>
            <h4 style='color: #e91e63; margin: 0;'>📱 Digital Marketing</h4>
            <p style='margin: 0.5rem 0; color: #666;'>Tailored for marketing and social media roles</p>
            <ul style='color: #666; font-size: 0.9rem;'>
                <li>Campaign results focus</li>
                <li>Metrics-driven layout</li>
                <li>Social media integration</li>
                <li>Brand-aware design</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Use Template", key="digital_marketing"):
            generate_template("digital_marketing")
    
    with col3:
        st.markdown("""
        <div style='border: 2px solid #e91e63; border-radius: 10px; padding: 1rem; margin: 0.5rem 0; background: white;'>
            <h4 style='color: #e91e63; margin: 0;'>🎭 Media & Arts</h4>
            <p style='margin: 0.5rem 0; color: #666;'>Ideal for media, arts, and entertainment</p>
            <ul style='color: #666; font-size: 0.9rem;'>
                <li>Creative project emphasis</li>
                <li>Awards and recognition</li>
                <li>Artistic achievement focus</li>
                <li>Industry-specific sections</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Use Template", key="media_arts"):
            generate_template("media_arts")

def display_technical_templates():
    """Display technical-focused templates."""
    st.markdown("### 💻 Technical Focused Templates")
    st.info("Specialized templates for software engineers, developers, and technical roles.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='border: 2px solid #00bcd4; border-radius: 10px; padding: 1rem; margin: 0.5rem 0; background: white;'>
            <h4 style='color: #00bcd4; margin: 0;'>⚡ Software Engineer</h4>
            <p style='margin: 0.5rem 0; color: #666;'>Optimized for software development roles</p>
            <ul style='color: #666; font-size: 0.9rem;'>
                <li>Technical skills prominent</li>
                <li>Project showcase section</li>
                <li>GitHub integration ready</li>
                <li>Programming languages focus</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Use Template", key="software_eng"):
            generate_template("software_engineer")
    
    with col2:
        st.markdown("""
        <div style='border: 2px solid #00bcd4; border-radius: 10px; padding: 1rem; margin: 0.5rem 0; background: white;'>
            <h4 style='color: #00bcd4; margin: 0;'>📊 Data Scientist</h4>
            <p style='margin: 0.5rem 0; color: #666;'>Perfect for data science and analytics roles</p>
            <ul style='color: #666; font-size: 0.9rem;'>
                <li>Research experience focus</li>
                <li>Publications section</li>
                <li>Statistical tools emphasis</li>
                <li>Data visualization projects</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Use Template", key="data_scientist"):
            generate_template("data_scientist")
    
    with col3:
        st.markdown("""
        <div style='border: 2px solid #00bcd4; border-radius: 10px; padding: 1rem; margin: 0.5rem 0; background: white;'>
            <h4 style='color: #00bcd4; margin: 0;'>🔒 Cybersecurity</h4>
            <p style='margin: 0.5rem 0; color: #666;'>Specialized for security and IT roles</p>
            <ul style='color: #666; font-size: 0.9rem;'>
                <li>Security certifications</li>
                <li>Incident response experience</li>
                <li>Compliance knowledge</li>
                <li>Technical expertise focus</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Use Template", key="cybersecurity"):
            generate_template("cybersecurity")

def display_executive_templates():
    """Display executive-level templates."""
    st.markdown("### 👔 Executive Level Templates")
    st.info("Professional templates for C-level executives, VPs, and senior management positions.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='border: 2px solid #795548; border-radius: 10px; padding: 1rem; margin: 0.5rem 0; background: white;'>
            <h4 style='color: #795548; margin: 0;'>🏢 C-Level Executive</h4>
            <p style='margin: 0.5rem 0; color: #666;'>For CEO, CTO, CFO, and other C-suite roles</p>
            <ul style='color: #666; font-size: 0.9rem;'>
                <li>Leadership achievements</li>
                <li>Strategic initiatives focus</li>
                <li>Board experience</li>
                <li>P&L responsibility</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Use Template", key="c_level"):
            generate_template("c_level_executive")
    
    with col2:
        st.markdown("""
        <div style='border: 2px solid #795548; border-radius: 10px; padding: 1rem; margin: 0.5rem 0; background: white;'>
            <h4 style='color: #795548; margin: 0;'>📈 VP/Director</h4>
            <p style='margin: 0.5rem 0; color: #666;'>For Vice Presidents and Director positions</p>
            <ul style='color: #666; font-size: 0.9rem;'>
                <li>Team leadership focus</li>
                <li>Department growth</li>
                <li>Strategic planning</li>
                <li>Cross-functional collaboration</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Use Template", key="vp_director"):
            generate_template("vp_director")
    
    with col3:
        st.markdown("""
        <div style='border: 2px solid #795548; border-radius: 10px; padding: 1rem; margin: 0.5rem 0; background: white;'>
            <h4 style='color: #795548; margin: 0;'>🎯 Senior Manager</h4>
            <p style='margin: 0.5rem 0; color: #666;'>For senior management transitioning to executive roles</p>
            <ul style='color: #666; font-size: 0.9rem;'>
                <li>Management experience</li>
                <li>Process improvement</li>
                <li>Budget management</li>
                <li>Performance optimization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Use Template", key="senior_mgr"):
            generate_template("senior_manager")

def generate_template(template_type):
    """Generate and display the selected resume template."""
    st.success(f"✅ {template_type.replace('_', ' ').title()} template selected!")
    
    templates = {
        'classic_professional': get_classic_professional_template(),
        'modern_minimalist': get_modern_minimalist_template(),
        'skills_focused': get_skills_focused_template(),
        'designer_portfolio': get_designer_portfolio_template(),
        'digital_marketing': get_digital_marketing_template(),
        'media_arts': get_media_arts_template(),
        'software_engineer': get_software_engineer_template(),
        'data_scientist': get_data_scientist_template(),
        'cybersecurity': get_cybersecurity_template(),
        'c_level_executive': get_c_level_executive_template(),
        'vp_director': get_vp_director_template(),
        'senior_manager': get_senior_manager_template()
    }
    
    template_content = templates.get(template_type, get_classic_professional_template())
    
    st.markdown("### 📝 Template Preview & Editor")
    st.info("💡 **Tip:** Copy this template to your preferred document editor (Word, Google Docs) and customize with your information.")
    
    # Editable template
    edited_template = st.text_area(
        "Edit your resume template:",
        value=template_content,
        height=400,
        help="Customize this template with your personal information, experience, and skills."
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.download_button(
            label="📥 Download as Text",
            data=edited_template,
            file_name=f"resume_{template_type}.txt",
            mime="text/plain"
        ):
            st.success("Resume template downloaded!")
    
    with col2:
        if st.button("📋 Copy to Clipboard"):
            st.code(edited_template, language="text")
            st.info("Template displayed above - you can copy it manually.")

def get_classic_professional_template():
    """Classic professional resume template."""
    return """[YOUR NAME]
[Your Phone Number] | [Your Email] | [City, State] | [LinkedIn Profile] | [Portfolio/Website]

PROFESSIONAL SUMMARY
Accomplished [Your Title] with [X] years of experience in [Industry/Field]. Proven track record of [Key Achievement]. Strong expertise in [Key Skills]. Seeking to leverage expertise in [Relevant Area] to drive results at [Target Company Type].

CORE COMPETENCIES
• [Skill 1] • [Skill 2] • [Skill 3] • [Skill 4]
• [Skill 5] • [Skill 6] • [Skill 7] • [Skill 8]

PROFESSIONAL EXPERIENCE

[Job Title] | [Company Name] | [City, State] | [Start Date] – [End Date]
• [Achievement with quantified results - increased/decreased/improved X by Y%]
• [Responsibility that demonstrates key skill]
• [Project or initiative you led with specific outcome]
• [Process improvement or cost savings achieved]

[Job Title] | [Company Name] | [City, State] | [Start Date] – [End Date]
• [Achievement with quantified results]
• [Responsibility that demonstrates leadership]
• [Technology or system implementation]
• [Team management or collaboration experience]

EDUCATION
[Degree Type] in [Field of Study] | [University Name] | [Graduation Year]
• Relevant Coursework: [Course 1], [Course 2], [Course 3]
• [Academic Achievement or Honor]

CERTIFICATIONS & TRAINING
• [Certification Name] - [Issuing Organization] ([Year])
• [Professional Development Course] ([Year])

TECHNICAL SKILLS
Languages: [Programming Languages or Spoken Languages]
Software: [Relevant Software/Tools]
Platforms: [Systems/Platforms you work with]

AWARDS & ACHIEVEMENTS
• [Award/Recognition] - [Organization] ([Year])
• [Achievement or milestone reached]"""

def get_software_engineer_template():
    """Software engineer specialized template."""
    return """[YOUR NAME]
Software Engineer
[Phone] | [Email] | [City, State] | [GitHub] | [LinkedIn] | [Portfolio]

TECHNICAL SUMMARY
Experienced Software Engineer with [X] years developing scalable applications using [Primary Technologies]. Proven expertise in [Specialization] with a strong foundation in [Core Technologies]. Passionate about writing clean, efficient code and solving complex technical challenges.

TECHNICAL SKILLS
Languages: Python, JavaScript, Java, TypeScript, SQL, HTML/CSS
Frameworks: React, Node.js, Django, Flask, Express.js, Spring Boot
Databases: PostgreSQL, MongoDB, MySQL, Redis
Cloud/DevOps: AWS, Docker, Kubernetes, Jenkins, GitLab CI/CD
Tools: Git, VS Code, IntelliJ, Postman, Jira

PROFESSIONAL EXPERIENCE

Senior Software Engineer | [Company Name] | [Location] | [Dates]
• Developed and maintained [type of application] serving [number] users daily
• Improved application performance by [X%] through [specific optimization]
• Led migration from [old technology] to [new technology], reducing [metric] by [X%]
• Collaborated with cross-functional teams to deliver [number] features in [timeframe]
• Mentored [number] junior developers and conducted code reviews

Software Engineer | [Company Name] | [Location] | [Dates]
• Built RESTful APIs using [technology] handling [number] requests per day
• Implemented [feature/system] that increased [metric] by [X%]
• Worked with product team to define technical requirements for [project type]
• Participated in agile development process with [sprint length] sprints

PROJECTS

[Project Name] | [Technologies Used] | [Year]
• [Brief description and your role]
• [Key technical achievement or challenge solved]
• [Link to demo/code if available]

[Project Name] | [Technologies Used] | [Year]
• [Brief description and your role]
• [Technical implementation details]
• [Results or impact achieved]

EDUCATION
[Degree] in [Field] | [University] | [Year]
• Relevant Coursework: Data Structures, Algorithms, Database Systems, Software Engineering

CERTIFICATIONS
• [AWS/Cloud Certification] ([Year])
• [Other relevant certifications]"""

def get_data_scientist_template():
    """Data scientist specialized template.""" 
    return """[YOUR NAME]
Data Scientist
[Phone] | [Email] | [City, State] | [GitHub] | [LinkedIn] | [Kaggle Profile]

PROFESSIONAL SUMMARY
Results-driven Data Scientist with [X] years of experience transforming complex data into actionable business insights. Expertise in machine learning, statistical analysis, and data visualization. Proven track record of building models that drive [business impact] and improve [relevant metrics].

TECHNICAL SKILLS
Programming: Python, R, SQL, Scala, Java
ML/AI: Scikit-learn, TensorFlow, PyTorch, Keras, XGBoost
Data Tools: Pandas, NumPy, Matplotlib, Seaborn, Plotly, Tableau, PowerBI
Databases: PostgreSQL, MySQL, MongoDB, Cassandra, Snowflake
Cloud: AWS (SageMaker, S3, EC2), Google Cloud Platform, Azure
Big Data: Spark, Hadoop, Kafka, Airflow

PROFESSIONAL EXPERIENCE

Senior Data Scientist | [Company Name] | [Location] | [Dates]
• Built predictive models that improved [business metric] by [X%], generating $[amount] in additional revenue
• Developed recommendation system serving [number] users with [accuracy]% accuracy
• Led data science initiatives for [business area], collaborating with [teams]
• Implemented A/B testing framework that increased experiment velocity by [X%]
• Mentored team of [number] junior data scientists and analysts

Data Scientist | [Company Name] | [Location] | [Dates]
• Created machine learning pipeline for [use case] with [metric] improvement
• Performed statistical analysis on [data type] to identify [insights]
• Built interactive dashboards using [tools] for [stakeholder group]
• Optimized existing models, reducing prediction error by [X%]

PROJECTS & RESEARCH

[Project Name] | [Technologies] | [Year]
• [Description of project and your contribution]
• [Machine learning techniques used]
• [Business impact or technical achievement]

[Research Project] | [Publication/Conference] | [Year]
• [Research focus and methodology]
• [Key findings or contributions]

EDUCATION
[Degree] in [Field] | [University] | [Year]
• Thesis: [Title and brief description]
• Relevant Coursework: Machine Learning, Statistics, Linear Algebra, Data Mining

PUBLICATIONS & ACHIEVEMENTS
• [Paper Title] - [Conference/Journal] ([Year])
• [Kaggle Competition] - [Ranking/Achievement] ([Year])
• [Patent or other achievement]"""

# Additional template functions would continue here for other template types...

def get_modern_minimalist_template():
    """Modern minimalist template."""
    return """[YOUR NAME]
[Professional Title]

Contact: [Phone] • [Email] • [City, State] • [LinkedIn] • [Website]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROFILE
Dynamic [profession] with [X] years of experience in [industry]. Specialized in [key expertise] with a proven ability to [key strength]. Committed to delivering [value proposition] through [approach/methodology].

EXPERIENCE

[TITLE] • [COMPANY] • [DATES]
○ [Key achievement with metrics]
○ [Responsibility showcasing leadership]  
○ [Process or efficiency improvement]
○ [Technology or system implementation]

[TITLE] • [COMPANY] • [DATES]
○ [Quantified business impact]
○ [Cross-functional collaboration example]
○ [Innovation or creative solution]
○ [Team leadership or mentoring]

EXPERTISE
Technical: [Skill] • [Skill] • [Skill] • [Skill] • [Skill]
Business: [Skill] • [Skill] • [Skill] • [Skill] • [Skill]

EDUCATION
[Degree] • [University] • [Year]
[Relevant certification or additional education]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

def get_skills_focused_template():
    """Skills-focused template."""
    return """[YOUR NAME]
[Your Title] • [Phone] • [Email] • [LinkedIn]

CORE COMPETENCIES & ACHIEVEMENTS
▪ [Primary Skill Area]: [Specific achievement with numbers/percentages]
▪ [Secondary Skill Area]: [Quantified result or improvement made]  
▪ [Third Skill Area]: [Leadership or innovation example]
▪ [Fourth Skill Area]: [Process improvement or cost savings]

KEY TECHNICAL SKILLS
[Category 1]: [Skill], [Skill], [Skill], [Skill]
[Category 2]: [Skill], [Skill], [Skill], [Skill]  
[Category 3]: [Skill], [Skill], [Skill], [Skill]

PROFESSIONAL HIGHLIGHTS

[Job Title] - [Company] ([Years])
✓ [Major achievement with specific metrics]
✓ [Leadership responsibility and outcome]
✓ [Technical implementation or innovation]

[Job Title] - [Company] ([Years])  
✓ [Process improvement with quantified results]
✓ [Collaboration or cross-functional achievement]
✓ [Problem-solving example with impact]

[Job Title] - [Company] ([Years])
✓ [Growth or expansion contribution]
✓ [Quality improvement or efficiency gain]
✓ [Training or knowledge transfer activity]

EDUCATION & CREDENTIALS
[Degree] in [Field] - [University] ([Year])
[Certification] - [Organization] ([Year])
[Additional Training] - [Provider] ([Year])

PROJECT SHOWCASE
• [Project Name]: [Brief description and your role] → [Outcome achieved]
• [Project Name]: [Technology used and challenge solved] → [Business impact]
• [Project Name]: [Team size and timeline] → [Results delivered]"""

# Placeholder templates for other types
def get_designer_portfolio_template():
    return get_classic_professional_template().replace("PROFESSIONAL SUMMARY", "CREATIVE PORTFOLIO SUMMARY")

def get_digital_marketing_template():
    return get_classic_professional_template().replace("CORE COMPETENCIES", "MARKETING EXPERTISE")

def get_media_arts_template():
    return get_classic_professional_template().replace("PROFESSIONAL EXPERIENCE", "CREATIVE EXPERIENCE")

def get_cybersecurity_template():
    return get_classic_professional_template().replace("TECHNICAL SKILLS", "SECURITY EXPERTISE")

def get_c_level_executive_template():
    return get_classic_professional_template().replace("PROFESSIONAL SUMMARY", "EXECUTIVE LEADERSHIP PROFILE")

def get_vp_director_template():
    return get_classic_professional_template().replace("CORE COMPETENCIES", "LEADERSHIP COMPETENCIES")

def get_senior_manager_template():
    return get_classic_professional_template().replace("PROFESSIONAL EXPERIENCE", "MANAGEMENT EXPERIENCE")