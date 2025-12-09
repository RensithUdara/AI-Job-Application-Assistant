"""
Modal Dialogs Module
Contains modal dialog functionality for chat, interviews, templates, and feedback.
"""

import streamlit as st
from core.feedback_tracker import get_feedback_tracker

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


def display_feedback_modal():
    """Display feedback modal with star rating and text input."""
    st.markdown("### 💬 We'd Love Your Feedback!")
    st.markdown("Help us improve the AI Job Application Assistant by sharing your experience.")
    
    # Initialize session state for rating
    if 'feedback_rating' not in st.session_state:
        st.session_state.feedback_rating = 0
    
    # Rating section with interactive stars
    st.markdown("#### Rate Your Experience")
    
    # Create 5 columns for stars
    cols = st.columns(5)
    
    for i in range(5):
        with cols[i]:
            if st.button(
                "⭐",
                key=f"feedback_star_{i+1}",
                help=["Poor", "Fair", "Good", "Very Good", "Excellent"][i],
                use_container_width=True
            ):
                st.session_state.feedback_rating = i + 1
    
    # Display selected rating
    if st.session_state.feedback_rating > 0:
        rating_labels = {
            1: "😞 Poor",
            2: "😕 Fair",
            3: "😐 Good",
            4: "😊 Very Good",
            5: "😍 Excellent"
        }
        st.markdown(
            f"**Your Rating: {st.session_state.feedback_rating} Stars** - "
            f"{rating_labels[st.session_state.feedback_rating]}"
        )
    else:
        st.info("👆 Click the stars to rate your experience (1-5)")
    
    st.markdown("---")
    
    # Feedback type selection
    st.markdown("#### What type of feedback?")
    feedback_type = st.selectbox(
        "Select feedback category:",
        [
            "General Feedback",
            "Bug Report",
            "Feature Request",
            "Improvement Suggestion",
            "Other"
        ],
        label_visibility="collapsed",
        key="feedback_type_select"
    )
    
    # Map display names to database values
    type_mapping = {
        "General Feedback": "general",
        "Bug Report": "bug",
        "Feature Request": "feature_request",
        "Improvement Suggestion": "improvement",
        "Other": "other"
    }
    feedback_type_value = type_mapping[feedback_type]
    
    st.markdown("---")
    
    # Feature mention (optional)
    st.markdown("#### Which feature(s) are you referring to? (Optional)")
    features = [
        "Resume Parser",
        "Job Matcher",
        "AI Chat",
        "Interview Prep",
        "Resume Templates",
        "Salary Intelligence",
        "Career Path Analyzer",
        "UI/UX",
        "Performance",
        "Database/Metrics",
        "Other"
    ]
    feature_mentioned = st.multiselect(
        "Select features (optional):",
        features,
        label_visibility="collapsed",
        key="feedback_features"
    )
    
    st.markdown("---")
    
    # Feedback text
    st.markdown("#### Your Feedback")
    feedback_text = st.text_area(
        "Please share your thoughts (minimum 10 characters):",
        height=120,
        placeholder="Tell us what you think... What did you like? What could be improved?",
        label_visibility="collapsed",
        max_chars=2000,
        key="feedback_text_area"
    )
    
    st.markdown("---")
    
    # Submit button
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        submit_btn = st.button(
            "📤 Submit Feedback",
            use_container_width=True,
            type="primary",
            key="submit_feedback_btn"
        )
    
    with col2:
        clear_btn = st.button(
            "🔄 Clear",
            use_container_width=True,
            key="clear_feedback_btn"
        )
    
    # Handle submission
    if submit_btn:
        # Validation
        if st.session_state.feedback_rating == 0:
            st.error("❌ Please select a star rating (1-5)")
            return False
        
        if not feedback_text or len(feedback_text.strip()) < 10:
            st.error("❌ Please enter at least 10 characters of feedback")
            return False
        
        # Record feedback
        tracker = get_feedback_tracker()
        feature_str = ", ".join(feature_mentioned) if feature_mentioned else None
        
        success = tracker.record_feedback(
            user_id="default",
            rating=st.session_state.feedback_rating,
            feedback_text=feedback_text,
            feedback_type=feedback_type_value,
            feature_mentioned=feature_str
        )
        
        if success:
            st.success("✅ Thank you for your feedback! We appreciate your input.")
            st.balloons()
            # Reset form
            st.session_state.feedback_rating = 0
            return True
        else:
            st.error("❌ Failed to submit feedback. Please try again.")
            return False
    
    # Clear form
    if clear_btn:
        st.session_state.feedback_rating = 0
        st.rerun()
    
    return False


def display_feedback_stats():
    """Display feedback statistics in a readable format."""
    tracker = get_feedback_tracker()
    summary = tracker.get_feedback_summary()
    
    if summary['total_feedbacks'] == 0:
        st.info("📊 No feedback collected yet. Be the first to share your thoughts!")
        return
    
    st.markdown("### 📊 Feedback Statistics")
    
    # Main stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Feedback", summary['total_feedbacks'])
    
    with col2:
        st.metric(
            "Average Rating",
            f"{summary['avg_rating']:.1f} ⭐",
            help="Average star rating across all feedback"
        )
    
    with col3:
        st.metric("Best Rating", f"{summary['max_rating']} ⭐")
    
    with col4:
        st.metric("Lowest Rating", f"{summary['min_rating']} ⭐")
    
    st.markdown("---")
    
    # Rating distribution
    st.markdown("#### Rating Distribution")
    distribution = tracker.get_rating_distribution()
    
    # Create bar chart data
    ratings = list(range(1, 6))
    counts = [distribution[r] for r in ratings]
    
    max_count = max(counts) if counts else 1
    for rating, count in zip(ratings, counts):
        percentage = (count / max_count * 100) if max_count > 0 else 0
        bar = "█" * int(percentage / 5)
        st.write(f"{rating} ⭐ {bar} {count} feedback(s)")
    
    st.markdown("---")
    
    # Feedback type distribution
    if summary['feedback_type_distribution']:
        st.markdown("#### Feedback Type Distribution")
        type_dist = summary['feedback_type_distribution']
        
        type_labels = {
            'general': '💬 General',
            'bug': '🐛 Bug Report',
            'feature_request': '🚀 Feature Request',
            'improvement': '✨ Improvement',
            'other': '📝 Other'
        }
        
        for ftype, count in sorted(type_dist.items(), key=lambda x: x[1], reverse=True):
            label = type_labels.get(ftype, ftype)
            st.write(f"{label}: {count}")
    
    st.markdown("---")
    
    # Top mentioned features
    if summary['top_features']:
        st.markdown("#### Most Mentioned Features")
        for feature in summary['top_features'][:5]:
            star_rating = "⭐" * int(feature['avg_rating'])
            st.write(
                f"**{feature['feature']}** - "
                f"{star_rating} ({feature['avg_rating']}/5 avg, {feature['count']} mentions)"
            )


def display_recent_feedback(limit: int = 5):
    """Display recent feedback entries."""
    tracker = get_feedback_tracker()
    recent = tracker.get_recent_feedback(limit=limit)
    
    if not recent:
        st.info("📭 No feedback yet. Your feedback will appear here!")
        return
    
    st.markdown("### 📝 Recent Feedback")
    
    for feedback in recent:
        with st.expander(
            f"{'⭐' * feedback['rating']} {feedback['type'].replace('_', ' ').title()} - {feedback['created_at'][:10]}"
        ):
            st.write(f"**Rating:** {feedback['rating']} ⭐")
            st.write(f"**Type:** {feedback['type'].replace('_', ' ').title()}")
            if feedback['feature']:
                st.write(f"**Features:** {feedback['feature']}")
            st.markdown("---")
            st.write(feedback['text'])