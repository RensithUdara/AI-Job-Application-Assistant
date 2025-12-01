"""
Networking Hub Tab Module
Displays networking opportunities and professional connections.
"""

import streamlit as st
import pandas as pd
from typing import Dict

def display_networking_hub_tab(resume_data: Dict, jd_data: Dict, match_data: Dict):
    """Display networking opportunities and professional connections."""
    st.header("🤝 Professional Networking Hub")
    
    # Networking strategy
    st.subheader("🎯 Personalized Networking Strategy")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🌟 LinkedIn Optimization:**")
        linkedin_tips = [
            "Update your headline with target keywords",
            "Write a compelling summary",
            "Add relevant skills and endorsements",
            "Share industry-relevant content",
            "Connect with professionals in your field"
        ]
        for tip in linkedin_tips:
            st.write(f"✅ {tip}")
    
    with col2:
        st.write("**📏 Networking Events:**")
        events = [
            "Local tech meetups",
            "Industry conferences",
            "Professional association meetings",
            "Online webinars and workshops",
            "Career fairs and job expos"
        ]
        for event in events:
            st.write(f"🎪 {event}")
    
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