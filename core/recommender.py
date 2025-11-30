import pandas as pd
from typing import Dict, List, Optional
import random

class Recommender:
    def __init__(self, interview_questions_path: str = "data/interview_questions.csv"):
        """Initialize the recommender with interview questions data."""
        try:
            self.interview_questions = pd.read_csv(interview_questions_path)
        except Exception as e:
            # Create empty dataframe if file doesn't exist
            self.interview_questions = pd.DataFrame(columns=['role', 'skill', 'question', 'type'])
    
    def build_recommendations(self, resume_data: Dict, jd_data: Dict, 
                            match_data: Dict) -> Dict:
        """Build comprehensive recommendations for resume and interview preparation."""
        try:
            # Resume structure recommendations
            resume_tips = self._generate_resume_tips(resume_data, jd_data)
            
            # Skill development roadmap
            skill_roadmap = self._generate_skill_roadmap(match_data, jd_data)
            
            # Interview questions
            interview_questions = self._generate_interview_questions(jd_data, match_data)
            
            # Priority action items
            priority_actions = self._generate_priority_actions(resume_data, match_data)
            
            # Career advancement insights
            career_insights = self._generate_career_insights(jd_data, match_data)
            
            # Personalized learning resources
            learning_resources = self._generate_learning_resources(match_data, jd_data)
            
            # Application strategy
            application_strategy = self._generate_application_strategy(resume_data, jd_data, match_data)
            
            return {
                'resume_tips': resume_tips,
                'skill_roadmap': skill_roadmap,
                'interview_questions': interview_questions,
                'priority_actions': priority_actions,
                'career_insights': career_insights,
                'learning_resources': learning_resources,
                'application_strategy': application_strategy
            }
        
        except Exception as e:
            return {
                'error': str(e),
                'resume_tips': [],
                'skill_roadmap': [],
                'interview_questions': [],
                'priority_actions': [],
                'career_insights': {},
                'learning_resources': {},
                'application_strategy': {}
            }
    
    def _generate_resume_tips(self, resume_data: Dict, jd_data: Dict) -> List[Dict]:
        """Generate resume improvement tips."""
        tips = []
        
        # Check missing sections
        missing_sections = resume_data.get('missing_sections', [])
        
        section_tips = {
            'contact': {
                'title': 'Add Contact Information',
                'description': 'Include a complete contact section with email, phone, and LinkedIn profile.',
                'priority': 'high',
                'category': 'structure'
            },
            'skills': {
                'title': 'Add a Dedicated Skills Section',
                'description': 'Create a separate Skills section listing your technical competencies prominently.',
                'priority': 'high',
                'category': 'structure'
            },
            'projects': {
                'title': 'Include Projects Section',
                'description': 'Add 2-3 relevant projects that showcase your practical experience and skills.',
                'priority': 'high',
                'category': 'content'
            },
            'experience': {
                'title': 'Add Work Experience',
                'description': 'Include any internships, part-time jobs, or volunteer work relevant to the role.',
                'priority': 'medium',
                'category': 'content'
            },
            'certifications': {
                'title': 'Include Certifications',
                'description': 'Add any relevant certifications or online courses you\'ve completed.',
                'priority': 'low',
                'category': 'content'
            }
        }
        
        for section in missing_sections:
            if section in section_tips:
                tips.append(section_tips[section])
        
        # Check contact info quality
        contact_info = resume_data.get('contact_info', {})
        if not contact_info.get('valid_email'):
            tips.append({
                'title': 'Fix Email Address',
                'description': 'Ensure you have a valid, professional email address in your contact information.',
                'priority': 'high',
                'category': 'contact'
            })
        
        if not contact_info.get('has_linkedin'):
            tips.append({
                'title': 'Add LinkedIn Profile',
                'description': 'Include your LinkedIn profile URL to provide more context about your background.',
                'priority': 'medium',
                'category': 'contact'
            })
        
        # Skill-specific recommendations
        missing_skills = set(jd_data.get('all_jd_skills_list', []))
        resume_skills = resume_data.get('resume_skills', {}).get('all_skills', set())
        critical_missing = missing_skills - resume_skills
        
        if critical_missing:
            skills_sample = list(critical_missing)[:5]  # Show top 5
            tips.append({
                'title': 'Add Missing Key Skills',
                'description': f'Include these job-relevant skills in your Skills section: {", ".join(skills_sample)}',
                'priority': 'high',
                'category': 'skills'
            })
        
        return tips
    
    def _generate_skill_roadmap(self, match_data: Dict, jd_data: Dict) -> List[Dict]:
        """Generate a skill development roadmap."""
        roadmap = []
        
        # Get missing skills by priority
        priority_analysis = match_data.get('priority_analysis', {})
        high_priority = priority_analysis.get('high_priority', [])
        medium_priority = priority_analysis.get('medium_priority', [])
        
        # Skill learning suggestions
        skill_suggestions = {
            'python': 'Complete Python basics course and build a small project',
            'java': 'Learn Java fundamentals and object-oriented programming',
            'javascript': 'Master JavaScript ES6+ features and async programming',
            'react': 'Build a portfolio website using React framework',
            'node.js': 'Create a REST API using Node.js and Express',
            'sql': 'Practice SQL queries and database design concepts',
            'git': 'Learn version control basics: commit, push, pull, branching',
            'docker': 'Containerize a simple application using Docker',
            'aws': 'Get familiar with AWS core services (EC2, S3, Lambda)',
            'flutter': 'Build a mobile app using Flutter and Dart',
            'firebase': 'Integrate Firebase for authentication and database',
            'rest api': 'Learn to design and consume RESTful APIs',
            'mongodb': 'Practice NoSQL database operations and design',
            'kubernetes': 'Learn container orchestration basics',
            'machine learning': 'Complete an ML course and implement algorithms'
        }
        
        # High priority skills (Month 1-2)
        for i, skill in enumerate(high_priority[:3], 1):
            skill_lower = skill.lower()
            suggestion = skill_suggestions.get(skill_lower, f'Learn {skill} through online courses and practice projects')
            
            roadmap.append({
                'timeframe': f'Month {i}',
                'skill': skill,
                'action': suggestion,
                'priority': 'high',
                'category': 'critical'
            })
        
        # Medium priority skills (Month 3-4)
        for i, skill in enumerate(medium_priority[:2], len(high_priority[:3]) + 1):
            skill_lower = skill.lower()
            suggestion = skill_suggestions.get(skill_lower, f'Gain familiarity with {skill}')
            
            roadmap.append({
                'timeframe': f'Month {i}',
                'skill': skill,
                'action': suggestion,
                'priority': 'medium',
                'category': 'enhancement'
            })
        
        # Add general recommendations
        if not roadmap:
            roadmap.append({
                'timeframe': 'Month 1',
                'skill': 'Resume Projects',
                'action': 'Build 2-3 projects showcasing your current skills',
                'priority': 'high',
                'category': 'portfolio'
            })
        
        return roadmap
    
    def _generate_interview_questions(self, jd_data: Dict, match_data: Dict) -> List[Dict]:
        """Generate relevant interview questions."""
        questions = []
        
        # Get job role and matched/missing skills
        jd_role = jd_data.get('jd_role', 'general')
        matched_skills = set(skill.lower() for skill in match_data.get('matched_skills', []))
        missing_skills = set(skill.lower() for skill in match_data.get('missing_skills', []))
        
        # Role-specific questions
        role_questions = self.interview_questions[
            self.interview_questions['role'] == jd_role
        ]
        
        # General questions
        general_questions = self.interview_questions[
            self.interview_questions['role'] == 'general'
        ]
        
        # Add role-specific questions
        for _, question in role_questions.head(5).iterrows():
            questions.append({
                'question': question['question'],
                'type': question['type'],
                'skill': question['skill'],
                'category': 'role_specific',
                'difficulty': 'medium'
            })
        
        # Add questions for matched skills
        for skill in list(matched_skills)[:3]:
            skill_questions = self.interview_questions[
                self.interview_questions['skill'].str.lower().str.contains(skill, na=False)
            ]
            if not skill_questions.empty:
                q = skill_questions.iloc[0]
                questions.append({
                    'question': q['question'],
                    'type': q['type'],
                    'skill': skill,
                    'category': 'strength',
                    'difficulty': 'medium'
                })
        
        # Add behavioral questions
        behavioral_questions = general_questions[
            general_questions['type'] == 'behavioral'
        ].sample(n=min(5, len(general_questions)))
        
        for _, question in behavioral_questions.iterrows():
            questions.append({
                'question': question['question'],
                'type': 'behavioral',
                'skill': question['skill'],
                'category': 'behavioral',
                'difficulty': 'medium'
            })
        
        # Add questions about missing skills (prepare for gaps)
        for skill in list(missing_skills)[:2]:
            questions.append({
                'question': f'How would you approach learning {skill} if hired for this role?',
                'type': 'behavioral',
                'skill': skill,
                'category': 'gap_handling',
                'difficulty': 'medium'
            })
        
        return questions[:15]  # Limit to 15 questions
    
    def _generate_priority_actions(self, resume_data: Dict, match_data: Dict) -> List[Dict]:
        """Generate prioritized action items."""
        actions = []
        
        # High priority actions
        quality_score = resume_data.get('quality_score', 0)
        if quality_score < 60:
            actions.append({
                'action': 'Improve overall resume structure and content',
                'priority': 'high',
                'timeframe': 'This week',
                'category': 'resume'
            })
        
        critical_missing = match_data.get('priority_analysis', {}).get('critical_missing_count', 0)
        if critical_missing > 0:
            actions.append({
                'action': f'Learn {critical_missing} critical missing skills',
                'priority': 'high',
                'timeframe': '1-2 months',
                'category': 'skills'
            })
        
        # Medium priority actions
        match_score = match_data.get('match_score_overall', 0)
        if match_score < 70:
            actions.append({
                'action': 'Build projects demonstrating job-relevant skills',
                'priority': 'medium',
                'timeframe': '2-4 weeks',
                'category': 'portfolio'
            })
        
        # Always include interview prep
        actions.append({
            'action': 'Practice interview questions and prepare STAR method stories',
            'priority': 'medium',
            'timeframe': 'Before interviews',
            'category': 'interview'
        })
        
        return actions
    
    def _generate_career_insights(self, jd_data: Dict, match_data: Dict) -> Dict:
        """Generate career advancement insights and market analysis."""
        insights = {
            'market_demand': 'Moderate',
            'growth_potential': 'Good',
            'skill_trends': [],
            'next_career_steps': [],
            'industry_insights': []
        }
        
        # Analyze role demand based on skills
        role = jd_data.get('jd_role', 'general')
        skills = jd_data.get('all_jd_skills_list', [])
        
        # High-demand skill indicators
        high_demand_skills = ['python', 'javascript', 'react', 'aws', 'docker', 'kubernetes', 'machine learning']
        trending_skills = ['ai', 'blockchain', 'flutter', 'typescript', 'graphql', 'terraform']
        
        matched_high_demand = [s for s in skills if s.lower() in high_demand_skills]
        matched_trending = [s for s in skills if s.lower() in trending_skills]
        
        if len(matched_high_demand) >= 3:
            insights['market_demand'] = 'High'
            insights['industry_insights'].append('This role involves high-demand skills with strong market potential')
        
        if matched_trending:
            insights['skill_trends'] = matched_trending
            insights['industry_insights'].append(f'Trending technologies mentioned: {', '.join(matched_trending)}')
        
        # Career progression suggestions
        role_progressions = {
            'web_developer': ['Senior Developer', 'Full Stack Architect', 'Tech Lead'],
            'mobile_developer': ['Senior Mobile Developer', 'Mobile Architect', 'Platform Lead'],
            'data_analyst': ['Senior Analyst', 'Data Scientist', 'Analytics Manager'],
            'software_engineer': ['Senior Engineer', 'Staff Engineer', 'Engineering Manager']
        }
        
        insights['next_career_steps'] = role_progressions.get(role, ['Senior Role', 'Team Lead', 'Specialist'])
        
        # Growth potential based on match score
        match_score = match_data.get('match_score_overall', 0)
        if match_score >= 75:
            insights['growth_potential'] = 'Excellent'
        elif match_score >= 50:
            insights['growth_potential'] = 'Good'
        else:
            insights['growth_potential'] = 'Needs Development'
        
        return insights
    
    def _generate_learning_resources(self, match_data: Dict, jd_data: Dict) -> Dict:
        """Generate personalized learning resource recommendations."""
        resources = {
            'online_courses': [],
            'practice_projects': [],
            'certifications': [],
            'books_articles': [],
            'estimated_learning_time': ''
        }
        
        missing_skills = match_data.get('missing_skills', [])
        priority_analysis = match_data.get('priority_analysis', {})
        high_priority_skills = priority_analysis.get('high_priority', [])
        
        # Course recommendations based on missing skills
        course_mapping = {
            'python': {'course': 'Python for Beginners', 'platform': 'Codecademy', 'time': '4-6 weeks'},
            'javascript': {'course': 'JavaScript Fundamentals', 'platform': 'freeCodeCamp', 'time': '3-4 weeks'},
            'react': {'course': 'React - The Complete Guide', 'platform': 'Udemy', 'time': '6-8 weeks'},
            'node.js': {'course': 'Node.js Development', 'platform': 'Coursera', 'time': '4-5 weeks'},
            'aws': {'course': 'AWS Cloud Practitioner', 'platform': 'AWS Training', 'time': '2-3 weeks'},
            'docker': {'course': 'Docker Mastery', 'platform': 'Udemy', 'time': '3-4 weeks'},
            'sql': {'course': 'SQL for Data Science', 'platform': 'Coursera', 'time': '3-4 weeks'}
        }
        
        # Add courses for high-priority missing skills
        total_weeks = 0
        for skill in high_priority_skills[:4]:  # Top 4 skills
            skill_lower = skill.lower()
            if skill_lower in course_mapping:
                course_info = course_mapping[skill_lower]
                resources['online_courses'].append({
                    'skill': skill,
                    'course': course_info['course'],
                    'platform': course_info['platform'],
                    'estimated_time': course_info['time']
                })
                # Extract weeks for time calculation
                weeks = int(course_info['time'].split('-')[0])
                total_weeks += weeks
        
        resources['estimated_learning_time'] = f'{total_weeks}-{total_weeks + len(high_priority_skills)} weeks'
        
        # Project recommendations
        project_mapping = {
            'web_developer': [
                'Build a personal portfolio website',
                'Create a full-stack e-commerce app',
                'Develop a REST API with authentication'
            ],
            'mobile_developer': [
                'Build a mobile app with local storage',
                'Create an app with API integration',
                'Develop a cross-platform Flutter app'
            ],
            'data_analyst': [
                'Analyze a public dataset',
                'Create interactive dashboards',
                'Build a machine learning model'
            ]
        }
        
        role = jd_data.get('jd_role', 'web_developer')
        resources['practice_projects'] = project_mapping.get(role, project_mapping['web_developer'])
        
        # Certification recommendations
        cert_mapping = {
            'aws': 'AWS Cloud Practitioner',
            'google cloud': 'Google Cloud Associate',
            'azure': 'Microsoft Azure Fundamentals',
            'docker': 'Docker Certified Associate',
            'kubernetes': 'Certified Kubernetes Administrator'
        }
        
        for skill in high_priority_skills:
            skill_lower = skill.lower()
            if skill_lower in cert_mapping:
                resources['certifications'].append({
                    'skill': skill,
                    'certification': cert_mapping[skill_lower]
                })
        
        return resources
    
    def _generate_application_strategy(self, resume_data: Dict, jd_data: Dict, 
                                     match_data: Dict) -> Dict:
        """Generate strategic advice for job application approach."""
        strategy = {
            'application_readiness': 'Not Ready',
            'recommended_approach': [],
            'timeline_suggestions': [],
            'networking_advice': [],
            'application_tips': []
        }
        
        match_score = match_data.get('match_score_overall', 0)
        competitiveness = match_data.get('market_analysis', {}).get('competitiveness_score', 0)
        
        # Determine readiness
        if match_score >= 70 and competitiveness >= 60:
            strategy['application_readiness'] = 'Ready to Apply'
            strategy['recommended_approach'].append('Apply directly with confidence')
            strategy['timeline_suggestions'].append('Apply within the next 1-2 weeks')
        elif match_score >= 50:
            strategy['application_readiness'] = 'Nearly Ready'
            strategy['recommended_approach'].append('Apply but continue skill development')
            strategy['timeline_suggestions'].append('Apply now while learning missing skills')
        else:
            strategy['application_readiness'] = 'Needs Preparation'
            strategy['recommended_approach'].append('Focus on skill development first')
            strategy['timeline_suggestions'].append('Prepare for 1-2 months before applying')
        
        # Networking advice
        company_info = jd_data.get('company_info', {})
        if company_info.get('company_name'):
            strategy['networking_advice'].extend([
                f"Research {company_info['company_name']} employees on LinkedIn",
                'Attend industry meetups and conferences',
                'Join relevant professional communities'
            ])
        
        # Application tips based on analysis
        ats_score = resume_data.get('ats_analysis', {}).get('score', 0)
        if ats_score < 70:
            strategy['application_tips'].append('Optimize resume for ATS systems before applying')
        
        missing_critical = len(match_data.get('priority_analysis', {}).get('high_priority', []))
        if missing_critical > 3:
            strategy['application_tips'].append('Consider applying for junior positions to gain experience')
        
        strategy['application_tips'].extend([
            'Tailor your resume for each application',
            'Write a compelling cover letter highlighting relevant projects',
            'Prepare portfolio showcasing your best work'
        ])
        
        return strategy