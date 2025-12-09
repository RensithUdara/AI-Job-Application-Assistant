"""
Mock Interview Tab
Interactive mock interview simulator and preparation tool.
"""

import streamlit as st
import random
from datetime import datetime

def display_mock_interview_tab():
    """Display the Mock Interview interface as a full tab."""
    st.markdown("## 🎤 Mock Interview Simulator")
    st.markdown("Practice interviews with AI-powered questions and get real-time feedback to improve your performance.")
    
    # Initialize session state
    if 'interview_session' not in st.session_state:
        st.session_state.interview_session = None
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'interview_responses' not in st.session_state:
        st.session_state.interview_responses = []
    
    # Main interface
    tab1, tab2, tab3 = st.tabs(["🎯 Start Interview", "📊 Practice Questions", "📈 Performance Analytics"])
    
    # Check if interview is in progress
    if st.session_state.interview_session and st.session_state.interview_session['current_question'] < len(st.session_state.interview_session['questions']):
        display_active_interview()
    else:
        with tab1:
            display_interview_setup()
        
        with tab2:
            display_practice_questions()
        
        with tab3:
            display_performance_analytics()

def display_interview_setup():
    """Display interview setup and configuration."""
    st.markdown("### 🎯 Interview Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Interview Settings")
        
        interview_type = st.selectbox(
            "Select Interview Type:",
            ["Behavioral", "Technical", "System Design", "Culture Fit", "Case Study", "Leadership"],
            help="Choose the type of interview you want to practice"
        )
        
        experience_level = st.selectbox(
            "Experience Level:",
            ["Entry Level (0-2 years)", "Mid Level (3-5 years)", "Senior Level (6-10 years)", "Executive (10+ years)"],
            index=1
        )
        
        industry = st.selectbox(
            "Industry Focus:",
            ["Technology", "Finance", "Healthcare", "Marketing", "Sales", "Consulting", "Education", "General"],
            help="Select your target industry for tailored questions"
        )
        
        role_focus = st.text_input(
            "Target Role:",
            placeholder="e.g., Senior Software Engineer, Product Manager, Data Scientist",
            help="Specify the role you're interviewing for"
        )
    
    with col2:
        st.markdown("#### Interview Duration")
        
        question_count = st.slider(
            "Number of Questions:",
            min_value=3,
            max_value=15,
            value=7,
            help="Choose how many questions you want to practice"
        )
        
        time_per_question = st.slider(
            "Time per Question (minutes):",
            min_value=1,
            max_value=10,
            value=3,
            help="Set time limit for each response"
        )
        
        difficulty = st.select_slider(
            "Question Difficulty:",
            options=["Easy", "Medium", "Hard", "Expert"],
            value="Medium"
        )
        
        include_followups = st.checkbox(
            "Include Follow-up Questions", 
            value=True,
            help="Add follow-up questions based on your responses"
        )
    
    st.markdown("---")
    
    # Start interview button
    if st.button("🎬 Start Mock Interview", type="primary", use_container_width=True):
        start_interview_session(interview_type, experience_level, industry, role_focus, question_count, time_per_question, difficulty, include_followups)

def start_interview_session(interview_type, experience_level, industry, role_focus, question_count, time_per_question, difficulty, include_followups):
    """Start a new interview session."""
    st.session_state.interview_session = {
        'type': interview_type,
        'level': experience_level,
        'industry': industry,
        'role': role_focus,
        'question_count': question_count,
        'time_limit': time_per_question,
        'difficulty': difficulty,
        'include_followups': include_followups,
        'questions': generate_interview_questions(interview_type, experience_level, industry, difficulty, question_count),
        'start_time': datetime.now(),
        'current_question': 0,
        'responses': []
    }
    
    st.success("🎬 Interview session started! Good luck!")

def generate_interview_questions(interview_type, experience_level, industry, difficulty, count):
    """Generate interview questions based on parameters."""
    questions_db = {
        'Behavioral': {
            'Easy': [
                "Tell me about yourself and your background.",
                "Why are you interested in this role?",
                "What are your greatest strengths?",
                "Describe a typical day at your current job.",
                "What motivates you in your work?"
            ],
            'Medium': [
                "Tell me about a time when you had to work with a difficult team member.",
                "Describe a situation where you had to meet a tight deadline.",
                "Give an example of when you had to learn something new quickly.",
                "Tell me about a time you failed and how you handled it.",
                "Describe a situation where you had to convince someone to see your point of view."
            ],
            'Hard': [
                "Tell me about a time when you had to make a difficult decision with incomplete information.",
                "Describe a situation where you had to challenge your manager or senior leadership.",
                "Give an example of when you had to deal with a major setback or crisis.",
                "Tell me about a time when you had to lead a team through a significant change.",
                "Describe a situation where you identified and solved a complex problem."
            ],
            'Expert': [
                "Tell me about a time when you had to balance competing priorities from multiple stakeholders.",
                "Describe how you would handle a situation where your team is underperforming consistently.",
                "Give an example of when you had to make an unpopular decision that was right for the business.",
                "Tell me about a time when you had to rebuild trust after a significant failure.",
                "Describe how you've driven innovation or transformation in your organization."
            ]
        },
        'Technical': {
            'Easy': [
                "What programming languages are you most comfortable with and why?",
                "Explain the difference between a stack and a queue.",
                "What is the difference between SQL and NoSQL databases?",
                "How do you ensure your code is maintainable?",
                "What is version control and why is it important?"
            ],
            'Medium': [
                "How would you optimize a slow database query?",
                "Explain the concept of object-oriented programming.",
                "What are the benefits and drawbacks of microservices architecture?",
                "How do you handle errors and exceptions in your code?",
                "Describe the software development lifecycle you follow."
            ],
            'Hard': [
                "Design a system to handle 1 million concurrent users.",
                "How would you implement a cache that automatically evicts least recently used items?",
                "Explain the CAP theorem and its implications for distributed systems.",
                "How do you ensure data consistency in a distributed system?",
                "Design an algorithm to detect cycles in a directed graph."
            ],
            'Expert': [
                "How would you architect a global content delivery network?",
                "Design a real-time collaborative editing system like Google Docs.",
                "How would you implement distributed consensus in a network of nodes?",
                "Design a system for real-time fraud detection at scale.",
                "How would you build a recommendation system for millions of users?"
            ]
        },
        'System Design': {
            'Medium': [
                "Design a URL shortener like bit.ly.",
                "How would you design a chat application like WhatsApp?",
                "Design a social media feed like Twitter.",
                "How would you design a file storage system like Dropbox?",
                "Design a ride-sharing service like Uber."
            ],
            'Hard': [
                "Design a global video streaming service like Netflix.",
                "How would you design a search engine like Google?",
                "Design a distributed cache system like Redis Cluster.",
                "How would you design a payment processing system?",
                "Design a real-time multiplayer game backend."
            ]
        },
        'Culture Fit': [
            "What type of work environment do you thrive in?",
            "How do you handle work-life balance?",
            "What are you looking for in your next role?",
            "How do you stay updated with industry trends?",
            "What questions do you have about our company culture?"
        ],
        'Case Study': [
            "Our user engagement has dropped 20% in the last quarter. How would you investigate and address this?",
            "A key competitor just launched a similar product. What's our response strategy?",
            "We need to reduce costs by 15% without affecting quality. What would you recommend?",
            "How would you launch a new product in a saturated market?",
            "Our team productivity has been declining. How would you diagnose and fix this?"
        ],
        'Leadership': [
            "Describe your leadership style and give an example of it in action.",
            "How do you motivate team members who are struggling with performance?",
            "Tell me about a time when you had to deliver bad news to your team.",
            "How do you handle conflicts between team members?",
            "Describe how you've built and maintained high-performing teams."
        ]
    }
    
    # Get questions based on type and difficulty
    if interview_type in questions_db and difficulty in questions_db[interview_type]:
        available_questions = questions_db[interview_type][difficulty]
    elif interview_type in questions_db:
        # If specific difficulty not available, get all questions for that type
        available_questions = []
        for diff_level in questions_db[interview_type].values():
            if isinstance(diff_level, list):
                available_questions.extend(diff_level)
            else:
                available_questions.extend(diff_level)
    else:
        available_questions = questions_db['Behavioral']['Medium']  # Default fallback
    
    # Select random questions
    selected_questions = random.sample(available_questions, min(count, len(available_questions)))
    
    return selected_questions

def display_active_interview():
    """Display the active interview interface."""
    session = st.session_state.interview_session
    if not session:
        return
    
    st.markdown("### 🎤 Mock Interview in Progress")
    
    # Progress indicator
    progress = session['current_question'] / len(session['questions'])
    st.progress(progress)
    st.write(f"Question {session['current_question'] + 1} of {len(session['questions'])}")
    
    # Current question
    if session['current_question'] < len(session['questions']):
        current_q = session['questions'][session['current_question']]
        
        st.markdown(f"""
        <div style='background: #1a472a; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #4CAF50; margin: 1rem 0;'>
            <h4 style='color: #4CAF50; margin: 0; font-size: 1.1rem;'>🎤 Interview Question:</h4>
            <p style='font-size: 1.15rem; margin: 0.8rem 0 0 0; color: #ffffff; font-weight: 500;'>{current_q}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Response input
        response = st.text_area(
            "Your Response:",
            height=150,
            placeholder="Take your time to think through your response. Use the STAR method (Situation, Task, Action, Result) for behavioral questions.",
            key=f"response_{session['current_question']}"
        )
        
        # Timer (simulated)
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("Submit Response & Next Question", type="primary", use_container_width=True):
                if response.strip():
                    # Save response
                    session['responses'].append({
                        'question': current_q,
                        'response': response,
                        'timestamp': datetime.now(),
                        'word_count': len(response.split()),
                        'feedback': generate_response_feedback(response, session['type'])
                    })
                    
                    # Move to next question
                    session['current_question'] += 1
                    st.session_state.interview_session = session
                else:
                    st.warning("Please provide a response before moving to the next question.")
    
    else:
        # Interview completed
        st.success("🎉 Interview Completed!")
        display_interview_results(session)

def generate_response_feedback(response, interview_type):
    """Generate feedback for user's response."""
    word_count = len(response.split())
    
    feedback = {
        'word_count': word_count,
        'suggestions': [],
        'strengths': [],
        'score': 0
    }
    
    # Basic length assessment
    if word_count < 30:
        feedback['suggestions'].append("Consider providing more detail in your response")
        feedback['score'] += 2
    elif word_count > 200:
        feedback['suggestions'].append("Try to be more concise while maintaining key details")
        feedback['score'] += 3
    else:
        feedback['strengths'].append("Good response length")
        feedback['score'] += 4
    
    # Content analysis (simplified)
    response_lower = response.lower()
    
    if interview_type == 'Behavioral':
        if any(word in response_lower for word in ['situation', 'task', 'action', 'result']):
            feedback['strengths'].append("Good use of STAR method structure")
            feedback['score'] += 2
        else:
            feedback['suggestions'].append("Consider using the STAR method (Situation, Task, Action, Result)")
        
        if any(word in response_lower for word in ['achieved', 'improved', 'increased', 'reduced', '%', 'million', 'thousand']):
            feedback['strengths'].append("Included quantified results")
            feedback['score'] += 2
        else:
            feedback['suggestions'].append("Try to include specific, quantified results")
    
    elif interview_type == 'Technical':
        if any(word in response_lower for word in ['because', 'since', 'due to', 'reason']):
            feedback['strengths'].append("Good explanation of reasoning")
            feedback['score'] += 2
        
        if len([word for word in response_lower.split() if word in ['algorithm', 'performance', 'scalability', 'efficiency']]) > 0:
            feedback['strengths'].append("Technical depth demonstrated")
            feedback['score'] += 2
    
    # Overall score (out of 10)
    feedback['score'] = min(10, max(1, feedback['score']))
    
    return feedback

def display_interview_results(session):
    """Display comprehensive interview results and analysis."""
    st.markdown("### 📊 Interview Performance Summary")
    
    # Overall metrics with better contrast
    col1, col2, col3, col4 = st.columns(4)
    
    avg_score = sum([r['feedback']['score'] for r in session['responses']]) / len(session['responses'])
    total_words = sum([r['word_count'] for r in session['responses']])
    duration = datetime.now() - session['start_time']
    questions_answered = len(session['responses'])
    
    with col1:
        st.markdown(f"""
        <div style='background: #1a2a1a; padding: 1.2rem; border-radius: 8px; text-align: center; border: 1px solid #4CAF50;'>
            <p style='color: #4CAF50; font-size: 0.9rem; margin: 0; font-weight: bold;'>Overall Score</p>
            <p style='color: #ffffff; font-size: 1.8rem; font-weight: bold; margin: 0.5rem 0;'>{avg_score:.1f}/10</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: #1a2a1a; padding: 1.2rem; border-radius: 8px; text-align: center; border: 1px solid #2196F3;'>
            <p style='color: #2196F3; font-size: 0.9rem; margin: 0; font-weight: bold;'>Total Words</p>
            <p style='color: #ffffff; font-size: 1.8rem; font-weight: bold; margin: 0.5rem 0;'>{total_words:,}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='background: #1a2a1a; padding: 1.2rem; border-radius: 8px; text-align: center; border: 1px solid #FF9800;'>
            <p style='color: #FF9800; font-size: 0.9rem; margin: 0; font-weight: bold;'>Duration</p>
            <p style='color: #ffffff; font-size: 1.8rem; font-weight: bold; margin: 0.5rem 0;'>{duration.total_seconds()/60:.0f} min</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style='background: #1a2a1a; padding: 1.2rem; border-radius: 8px; text-align: center; border: 1px solid #9C27B0;'>
            <p style='color: #9C27B0; font-size: 0.9rem; margin: 0; font-weight: bold;'>Questions Answered</p>
            <p style='color: #ffffff; font-size: 1.8rem; font-weight: bold; margin: 0.5rem 0;'>{questions_answered}/{len(session['questions'])}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed feedback for each question
    st.markdown("### 📋 Question-by-Question Feedback")
    
    for i, response_data in enumerate(session['responses'], 1):
        with st.expander(f"Question {i}: Score {response_data['feedback']['score']}/10"):
            st.markdown(f"<p style='color: #ffffff; font-weight: bold;'>📌 Question:</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #e0e0e0; background: #1a1a1a; padding: 1rem; border-radius: 5px; margin: 0.5rem 0;'>{response_data['question']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #ffffff; font-weight: bold;'>💬 Your Response:</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #e0e0e0; background: #1a1a1a; padding: 1rem; border-radius: 5px; margin: 0.5rem 0;'>{response_data['response']}</p>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if response_data['feedback']['strengths']:
                    st.markdown("<div style='background: #1e3a2f; padding: 1rem; border-radius: 5px; border-left: 3px solid #4CAF50;'>", unsafe_allow_html=True)
                    st.markdown("<p style='color: #4CAF50; font-weight: bold; margin: 0;'>✅ Strengths:</p>", unsafe_allow_html=True)
                    for strength in response_data['feedback']['strengths']:
                        st.markdown(f"<p style='color: #e0e0e0; margin: 0.3rem 0;'>• {strength}</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                if response_data['feedback']['suggestions']:
                    st.markdown("<div style='background: #2a3a1a; padding: 1rem; border-radius: 5px; border-left: 3px solid #FFC107;'>", unsafe_allow_html=True)
                    st.markdown("<p style='color: #FFC107; font-weight: bold; margin: 0;'>💡 Suggestions:</p>", unsafe_allow_html=True)
                    for suggestion in response_data['feedback']['suggestions']:
                        st.markdown(f"<p style='color: #e0e0e0; margin: 0.3rem 0;'>• {suggestion}</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
    
    # Action items
    st.markdown("### 🎯 Recommended Next Steps")
    
    avg_score = sum([r['feedback']['score'] for r in session['responses']]) / len(session['responses'])
    
    if avg_score >= 8:
        st.markdown("<div style='background: #1e3a2f; padding: 1.2rem; border-radius: 8px; border-left: 3px solid #4CAF50;'>\n<p style='color: #4CAF50; font-weight: bold; margin: 0;'>✅ Excellent performance! You're well-prepared for interviews.</p>\n<p style='color: #e0e0e0; margin: 0.5rem 0 0 0;'>• Continue practicing with harder questions</p>\n<p style='color: #e0e0e0; margin: 0.2rem 0;'>• Focus on specific technical areas for your target role</p>\n<p style='color: #e0e0e0; margin: 0.2rem 0;'>• Practice negotiation and closing techniques</p>\n</div>", unsafe_allow_html=True)
    elif avg_score >= 6:
        st.markdown("<div style='background: #2a3a1a; padding: 1.2rem; border-radius: 8px; border-left: 3px solid #FFC107;'>\n<p style='color: #FFC107; font-weight: bold; margin: 0;'>ℹ️ Good performance with room for improvement.</p>\n<p style='color: #e0e0e0; margin: 0.5rem 0 0 0;'>• Practice more STAR method responses</p>\n<p style='color: #e0e0e0; margin: 0.2rem 0;'>• Quantify your achievements with specific metrics</p>\n<p style='color: #e0e0e0; margin: 0.2rem 0;'>• Research common questions for your industry</p>\n</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='background: #3a1a1a; padding: 1.2rem; border-radius: 8px; border-left: 3px solid #F44336;'>\n<p style='color: #F44336; font-weight: bold; margin: 0;'>⚠️ More practice needed to improve confidence.</p>\n<p style='color: #e0e0e0; margin: 0.5rem 0 0 0;'>• Focus on storytelling and structure</p>\n<p style='color: #e0e0e0; margin: 0.2rem 0;'>• Prepare 5-10 solid examples from your experience</p>\n<p style='color: #e0e0e0; margin: 0.2rem 0;'>• Practice basic questions until they become natural</p>\n</div>", unsafe_allow_html=True)
    
    # Reset button
    if st.button("🔄 Start New Interview", use_container_width=True):
        st.session_state.interview_session = None
        st.session_state.current_question = 0
        st.session_state.interview_responses = []

def display_practice_questions():
    """Display practice questions by category."""
    st.markdown("### 📚 Practice Questions Library")
    st.info("Browse and practice individual questions by category. Perfect for targeted preparation!")
    
    category = st.selectbox(
        "Select Question Category:",
        ["Behavioral", "Technical", "System Design", "Culture Fit", "Leadership", "Case Study"]
    )
    
    difficulty = st.select_slider(
        "Difficulty Level:",
        options=["Easy", "Medium", "Hard", "Expert"],
        value="Medium"
    )
    
    # Generate questions for the category
    questions = generate_interview_questions(category, "Mid Level", "Technology", difficulty, 10)
    
    st.markdown(f"### {category} Questions - {difficulty} Level")
    
    for i, question in enumerate(questions, 1):
        with st.expander(f"Question {i}"):
            st.write(f"**{question}**")
            
            # Practice response area
            practice_response = st.text_area(
                "Practice your response:",
                height=100,
                key=f"practice_{category}_{i}",
                placeholder="Type your practice response here..."
            )
            
            if practice_response:
                # Simple feedback
                word_count = len(practice_response.split())
                
                if word_count < 30:
                    st.warning(f"Consider expanding your response (current: {word_count} words)")
                elif word_count > 200:
                    st.info(f"Try to be more concise (current: {word_count} words)")
                else:
                    st.success(f"Good response length ({word_count} words)")
                
                # Give tips based on question type
                if category == "Behavioral":
                    st.info("💡 **Tip:** Use the STAR method - Situation, Task, Action, Result")
                elif category == "Technical":
                    st.info("💡 **Tip:** Explain your thought process and consider edge cases")
                elif category == "System Design":
                    st.info("💡 **Tip:** Start with requirements, then discuss architecture and tradeoffs")

def display_performance_analytics():
    """Display performance analytics and improvement tracking."""
    st.markdown("### 📈 Performance Analytics")
    
    # Check if user has completed any interviews
    if 'interview_history' not in st.session_state:
        st.session_state.interview_history = []
    
    if not st.session_state.interview_history:
        st.info("Complete some mock interviews to see your performance analytics here!")
        
        # Sample analytics view
        st.markdown("#### 📊 Sample Analytics (Demo)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Sample performance chart
            import plotly.graph_objects as go
            
            fig = go.Figure(data=go.Scatter(
                x=[1, 2, 3, 4, 5],
                y=[6.2, 7.1, 7.8, 8.3, 8.7],
                mode='lines+markers',
                name='Interview Score',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            ))
            
            fig.update_layout(
                title="Performance Improvement Over Time",
                xaxis_title="Interview Session",
                yaxis_title="Average Score (out of 10)",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Sample strengths/weaknesses
            st.markdown("#### 💪 Strengths")
            st.success("✅ Good technical explanations")
            st.success("✅ Strong quantified examples")
            st.success("✅ Confident communication")
            
            st.markdown("#### 🎯 Areas for Improvement")
            st.info("💡 Practice more system design")
            st.info("💡 Improve behavioral storytelling")
            st.info("💡 Work on conciseness")
    
    else:
        # Show actual analytics when available
        st.success("Analytics will be populated as you complete interviews!")
    
    # Tips for improvement
    st.markdown("---")
    st.markdown("### 💡 General Interview Tips")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Before the Interview:**
        - Research the company thoroughly
        - Review your resume and be ready to discuss anything on it
        - Prepare 5-10 questions to ask them
        - Practice your elevator pitch
        - Plan your outfit and route
        """)
    
    with col2:
        st.markdown("""
        **During the Interview:**
        - Listen carefully to each question
        - Take a moment to think before responding
        - Use specific examples with quantified results
        - Ask clarifying questions when needed
        - Show enthusiasm and cultural fit
        """)
    
    st.markdown("""
    **After the Interview:**
    - Send a thank you email within 24 hours
    - Reflect on what went well and what to improve
    - Follow up appropriately on timing
    - Continue practicing for future opportunities
    """)