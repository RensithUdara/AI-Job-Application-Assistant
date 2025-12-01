"""
Interview Preparation Tab Module
Displays interview questions and preparation guidance.
"""

import streamlit as st
from typing import Dict

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