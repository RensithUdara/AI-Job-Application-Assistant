"""
Modal Dialogs Module
Contains modal dialog functionality for chat, interviews, and templates.
"""

import streamlit as st

def display_chat_modal():
    """Display AI Career Assistant Chat modal."""
    if not st.session_state.show_chat:
        return
    
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
                    ai_response = generate_ai_response(user_input)
                    
                    st.session_state.chat_history.append({
                        'role': 'ai',
                        'content': ai_response
                    })
                    
                    st.rerun()
        
        if st.button("Close Chat", key="close_chat"):
            st.session_state.show_chat = False
            st.rerun()
        
        st.markdown("---")

def generate_ai_response(user_input: str) -> str:
    """Generate AI response based on user input."""
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
    
    return ai_responses[response_key]

def display_interview_modal():
    """Display Mock Interview Simulator modal."""
    if not st.session_state.show_interview:
        return
        
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

def display_templates_modal():
    """Display Resume Templates modal (placeholder)."""
    if not st.session_state.show_templates:
        return
        
    with st.container():
        st.markdown("### 📄 Resume Templates")
        st.info("Resume template gallery will be displayed here.")
        
        template_categories = [
            "Modern ATS-Friendly Templates",
            "Creative Professional Templates", 
            "Technical Focused Templates",
            "Executive Level Templates"
        ]
        
        for category in template_categories:
            with st.expander(category):
                st.write(f"Templates in {category} category")
        
        if st.button("Close Templates", key="close_templates"):
            st.session_state.show_templates = False
            st.rerun()
        
        st.markdown("---")