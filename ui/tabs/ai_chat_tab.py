"""
AI Career Chat Tab
Advanced AI-powered career assistance and guidance.
"""

import streamlit as st
import random
from datetime import datetime

def display_ai_chat_tab():
    """Display the AI Career Chat interface as a full tab."""
    st.markdown("## 🤖 AI Career Assistant")
    st.markdown("Get personalized career advice, resume tips, and interview guidance from our AI assistant.")
    
    # Initialize chat history if not exists
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Chat interface
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.markdown("### 💡 Quick Topics")
        if st.button("📝 Resume Tips", use_container_width=True):
            add_quick_response("resume_tips")
        if st.button("🎯 Interview Prep", use_container_width=True):
            add_quick_response("interview_prep")
        if st.button("💰 Salary Negotiation", use_container_width=True):
            add_quick_response("salary_negotiation")
        if st.button("📈 Career Growth", use_container_width=True):
            add_quick_response("career_growth")
        if st.button("🔍 Job Search", use_container_width=True):
            add_quick_response("job_search")
        
        st.markdown("---")
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
    
    with col1:
        # Display chat history
        chat_container = st.container()
        with chat_container:
            if not st.session_state.chat_history:
                st.info("👋 Hello! I'm your AI Career Assistant. Ask me anything about resumes, interviews, career planning, or job searching!")
            
            for i, message in enumerate(st.session_state.chat_history):
                if message['role'] == 'user':
                    st.markdown(f"""
                    <div style='background: #e8f4f8; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #2196F3;'>
                        <strong>👤 You:</strong><br>{message['content']}
                        <small style='color: #666; font-size: 0.8rem;'><br>{message['timestamp']}</small>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='background: #f0f8e8; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #4CAF50;'>
                        <strong>🤖 AI Assistant:</strong><br>{message['content']}
                        <small style='color: #666; font-size: 0.8rem;'><br>{message['timestamp']}</small>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Chat input
        st.markdown("---")
        user_input = st.text_area(
            "💬 Ask me anything about your career:",
            placeholder="e.g., How can I improve my resume for a software engineer position?",
            height=100,
            key="chat_input"
        )
        
        col_send1, col_send2 = st.columns([1, 4])
        with col_send1:
            if st.button("Send 📤", use_container_width=True):
                if user_input.strip():
                    send_message(user_input.strip())

def add_quick_response(topic):
    """Add a quick response for a specific topic."""
    quick_responses = {
        'resume_tips': "I'd love to help you improve your resume! Here are key tips:\n\n• Use action verbs (managed, developed, improved)\n• Quantify achievements with numbers and percentages\n• Tailor keywords to match job descriptions\n• Keep it to 1-2 pages maximum\n• Use consistent formatting and professional fonts\n• Include relevant skills and certifications\n\nWould you like me to elaborate on any of these points?",
        
        'interview_prep': "Great choice! Interview preparation is crucial. Here's my comprehensive guide:\n\n• Research the company thoroughly (mission, values, recent news)\n• Practice STAR method (Situation, Task, Action, Result) for behavioral questions\n• Prepare 5-10 thoughtful questions to ask them\n• Practice common technical questions for your field\n• Plan your outfit and route in advance\n• Bring multiple copies of your resume\n\nWhat specific type of interview are you preparing for?",
        
        'salary_negotiation': "Salary negotiation is an important skill! Here's my strategy:\n\n• Research market rates (Glassdoor, PayScale, LinkedIn Salary)\n• Consider total compensation (benefits, PTO, stock options)\n• Wait for them to make the first offer\n• Negotiate based on value you bring, not personal needs\n• Be prepared to walk away if it doesn't meet your minimum\n• Practice your negotiation conversation beforehand\n\nWhat's your current situation? New job offer or promotion discussion?",
        
        'career_growth': "Career growth requires strategic planning! Here's how to accelerate it:\n\n• Set clear short-term and long-term goals\n• Identify skill gaps in your target roles\n• Seek feedback regularly from supervisors\n• Build internal and external networks\n• Take on stretch assignments and leadership opportunities\n• Consider additional certifications or education\n• Track and document your achievements\n\nWhat level are you at now, and where do you want to be?",
        
        'job_search': "Job searching can be overwhelming, but I'll help you organize it:\n\n• Define your target roles and companies clearly\n• Optimize your LinkedIn profile and resume\n• Use multiple job boards (LinkedIn, Indeed, company sites)\n• Network actively (reach out to connections, attend events)\n• Apply to 10-15 quality positions per week\n• Track applications in a spreadsheet\n• Follow up on applications after 1-2 weeks\n\nAre you currently employed or looking for your first role?"
    }
    
    if topic in quick_responses:
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.chat_history.append({
            'role': 'ai',
            'content': quick_responses[topic],
            'timestamp': timestamp
        })

def send_message(user_input):
    """Send a message and generate AI response."""
    timestamp = datetime.now().strftime("%H:%M")
    
    # Add user message
    st.session_state.chat_history.append({
        'role': 'user',
        'content': user_input,
        'timestamp': timestamp
    })
    
    # Generate AI response
    ai_response = generate_advanced_ai_response(user_input)
    
    st.session_state.chat_history.append({
        'role': 'ai',
        'content': ai_response,
        'timestamp': timestamp
    })

def generate_advanced_ai_response(user_input: str) -> str:
    """Generate contextual AI response based on user input."""
    input_lower = user_input.lower()
    
    # Resume-related responses
    if any(word in input_lower for word in ['resume', 'cv', 'application']):
        return generate_resume_response(input_lower)
    
    # Interview-related responses
    elif any(word in input_lower for word in ['interview', 'questions', 'preparation']):
        return generate_interview_response(input_lower)
    
    # Salary/compensation responses
    elif any(word in input_lower for word in ['salary', 'pay', 'compensation', 'negotiate']):
        return generate_salary_response(input_lower)
    
    # Skills/learning responses
    elif any(word in input_lower for word in ['skills', 'learn', 'certification', 'course']):
        return generate_skills_response(input_lower)
    
    # Career planning responses
    elif any(word in input_lower for word in ['career', 'promotion', 'growth', 'change']):
        return generate_career_response(input_lower)
    
    # Job search responses
    elif any(word in input_lower for word in ['job', 'search', 'apply', 'linkedin']):
        return generate_job_search_response(input_lower)
    
    # Default helpful response
    else:
        return "I'd be happy to help! I specialize in:\n\n• Resume optimization and formatting\n• Interview preparation and practice\n• Salary negotiation strategies\n• Career planning and growth\n• Job search techniques\n• Skill development guidance\n\nWhat specific area would you like assistance with?"

def generate_resume_response(input_lower):
    """Generate resume-specific responses."""
    if 'format' in input_lower or 'template' in input_lower:
        return "For resume formatting, I recommend:\n\n• Use a clean, ATS-friendly template\n• Stick to standard fonts (Arial, Calibri, Times New Roman)\n• Use consistent spacing and bullet points\n• Keep margins at 0.5-1 inch\n• Save as both PDF and Word formats\n\nWould you like specific template recommendations for your industry?"
    
    elif 'keywords' in input_lower or 'ats' in input_lower:
        return "Great question about ATS optimization! Here's how to beat the bots:\n\n• Mirror job description keywords naturally\n• Use standard section headings (Experience, Education, Skills)\n• Avoid images, tables, and fancy formatting\n• Include both acronyms and full terms (AI and Artificial Intelligence)\n• Use industry-standard job titles\n\nDo you have a specific job description you're targeting?"
    
    else:
        return "For resume improvement, focus on:\n\n• Quantifying achievements with specific numbers\n• Using strong action verbs to start bullet points\n• Tailoring content for each application\n• Including relevant keywords from job postings\n• Highlighting your most relevant experience first\n\nWhat industry or role are you targeting?"

def generate_interview_response(input_lower):
    """Generate interview-specific responses."""
    if 'behavioral' in input_lower:
        return "Behavioral interviews use the STAR method:\n\n• **Situation**: Set the context\n• **Task**: Explain what you needed to do\n• **Action**: Describe what you did\n• **Result**: Share the positive outcome\n\nCommon behavioral questions:\n• Tell me about a challenge you overcame\n• Describe a time you worked in a team\n• How do you handle tight deadlines?\n\nWant to practice with a specific scenario?"
    
    elif 'technical' in input_lower:
        return "For technical interviews, preparation is key:\n\n• Review fundamental concepts in your field\n• Practice coding problems on LeetCode/HackerRank\n• Prepare to explain your past projects in detail\n• Study system design if it's a senior role\n• Practice whiteboarding and talking through solutions\n\nWhat's your technical background?"
    
    else:
        return "Interview success comes from preparation:\n\n• Research the company thoroughly\n• Prepare 5-10 thoughtful questions to ask\n• Practice your elevator pitch\n• Plan your outfit and route\n• Bring multiple copies of your resume\n• Follow up within 24 hours\n\nWhat type of interview are you preparing for?"

def generate_salary_response(input_lower):
    """Generate salary negotiation responses."""
    return "Salary negotiation strategy:\n\n• Research market rates thoroughly (Glassdoor, PayScale, levels.fyi)\n• Let them make the first offer\n• Negotiate total compensation, not just base salary\n• Justify with your value and market data\n• Be prepared to walk away\n• Get everything in writing\n\nAverage negotiation increases salary by 10-20%. What's your situation?"

def generate_skills_response(input_lower):
    """Generate skills development responses."""
    return "For skill development:\n\n• Identify gaps by comparing job requirements to your current skills\n• Choose learning methods that fit your style (courses, books, practice)\n• Focus on skills with highest ROI for your career goals\n• Build a portfolio to demonstrate new skills\n• Get certifications for credibility\n\nRecommended platforms: Coursera, Udemy, LinkedIn Learning, Khan Academy\n\nWhat skills are you looking to develop?"

def generate_career_response(input_lower):
    """Generate career planning responses."""
    return "Career growth requires strategic thinking:\n\n• Set clear 1, 3, and 5-year goals\n• Identify the path between current and target roles\n• Build relationships with mentors and sponsors\n• Seek stretch assignments and leadership opportunities\n• Document your achievements regularly\n• Stay visible to decision-makers\n\nWhat's your current role and where do you want to be?"

def generate_job_search_response(input_lower):
    """Generate job search responses."""
    return "Effective job search strategy:\n\n• Define target roles and companies clearly\n• Optimize LinkedIn profile for discovery\n• Apply to 10-15 quality positions weekly\n• Network actively (70% of jobs are never posted)\n• Customize each application\n• Track everything in a spreadsheet\n• Follow up appropriately\n\nAre you currently employed or transitioning?"