import pandas as pd
from typing import Dict, List, Optional
import random
import re

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
            insights['industry_insights'].append(f'Trending technologies mentioned: {", ".join(matched_trending)}')
        
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
    
    def generate_professional_summary(self, resume_data: Dict, target_role: str = None) -> Dict:
        """Generate professional summary options for resume."""
        skills = resume_data.get('skills_found', [])
        experience_sections = resume_data.get('sections', {}).get('experience', '')
        
        # Extract years of experience (simplified)
        years_exp = 2  # Default for students
        if 'intern' in experience_sections.lower():
            years_exp = 1
        elif 'years' in experience_sections.lower():
            years_exp = 3
        
        # Generate different summary styles
        summaries = {
            'achievement_focused': self._create_achievement_summary(skills, years_exp, target_role),
            'skill_focused': self._create_skill_summary(skills, years_exp, target_role),
            'passion_focused': self._create_passion_summary(skills, years_exp, target_role)
        }
        
        return {
            'summary_options': summaries,
            'recommendation': 'Choose the summary that best matches the job description tone',
            'tips': [
                'Keep it concise (2-3 sentences)',
                'Include your target role',
                'Mention your strongest skills',
                'Add quantifiable achievements if possible'
            ]
        }
    
    def _create_achievement_summary(self, skills: List[str], years: int, role: str) -> str:
        """Create achievement-focused summary."""
        skill_str = ', '.join(skills[:3]) if skills else 'programming'
        
        if years <= 1:
            return f"Computer Science student with hands-on experience in {skill_str}. Successfully completed multiple projects including web applications and mobile apps, demonstrating strong problem-solving abilities and passion for software development."
        else:
            return f"Results-driven software developer with {years}+ years of experience in {skill_str}. Proven track record of delivering high-quality applications and collaborating effectively in team environments. Passionate about creating innovative solutions."
    
    def _create_skill_summary(self, skills: List[str], years: int, role: str) -> str:
        """Create skill-focused summary."""
        skill_str = ', '.join(skills[:4]) if skills else 'Python, JavaScript, React'
        
        return f"Skilled software developer proficient in {skill_str}. Strong foundation in full-stack development with experience in both frontend and backend technologies. Eager to apply technical expertise in a dynamic development environment."
    
    def _create_passion_summary(self, skills: List[str], years: int, role: str) -> str:
        """Create passion-focused summary."""
        return f"Passionate software developer with expertise in modern technologies and a drive for continuous learning. Experienced in building scalable applications and solving complex technical challenges. Seeking opportunities to contribute to innovative projects and grow professionally."
    
    def generate_linkedin_headlines(self, resume_data: Dict, target_role: str = None) -> List[str]:
        """Generate LinkedIn headline options."""
        skills = resume_data.get('skills_found', [])
        top_skills = skills[:3] if len(skills) >= 3 else skills
        
        headlines = []
        
        # Skill-focused headlines
        if top_skills:
            headlines.append(f"{' | '.join(top_skills)} Developer | Problem Solver")
            headlines.append(f"Software Developer | {' • '.join(top_skills)} | Open to Opportunities")
        
        # Role-focused headlines
        if target_role:
            headlines.append(f"Aspiring {target_role} | Building Amazing Applications")
            headlines.append(f"{target_role} | Passionate about Technology & Innovation")
        
        # Generic but effective options
        headlines.extend([
            "Software Developer | Full-Stack Enthusiast | Always Learning",
            "Computer Science Student | Future Software Engineer | Tech Enthusiast",
            "Passionate Developer | Building the Future, One Line of Code at a Time"
        ])
        
        return headlines[:5]  # Return top 5 options
    
    def analyze_resume_weaknesses(self, resume_data: Dict) -> Dict:
        """Comprehensive weakness analysis with improvement suggestions."""
        weaknesses = []
        improvements = []
        
        # Analyze bullet points if available
        bullet_analysis = resume_data.get('bullet_analysis', {})
        if bullet_analysis:
            avg_score = bullet_analysis.get('average_score', 0)
            if avg_score < 6:
                weaknesses.append("Weak bullet points lacking impact and quantification")
                improvements.extend([
                    "Rewrite bullets using STAR method (Situation, Task, Action, Result)",
                    "Add specific numbers and metrics to show impact",
                    "Start each bullet with strong action verbs"
                ])
        
        # Analyze action verbs
        action_verb_analysis = resume_data.get('action_verb_analysis', {})
        if action_verb_analysis:
            ratio = action_verb_analysis.get('verb_strength_ratio', 0)
            if ratio < 1:
                weaknesses.append("Overuse of weak action verbs")
                improvements.append("Replace weak verbs (helped, worked) with strong ones (implemented, achieved)")
        
        # Analyze quantification
        quant_analysis = resume_data.get('quantification_analysis', {})
        if quant_analysis:
            quant_score = quant_analysis.get('quantification_score', 0)
            if quant_score < 5:
                weaknesses.append("Lack of quantified achievements")
                improvements.append("Add numbers, percentages, and timeframes to demonstrate impact")
        
        # Check ATS compatibility
        ats_analysis = resume_data.get('ats_analysis', {})
        if ats_analysis:
            ats_score = ats_analysis.get('ats_score', 100)
            if ats_score < 80:
                weaknesses.append("Poor ATS compatibility")
                improvements.extend([
                    "Use standard section headings",
                    "Avoid complex formatting and tables",
                    "Include more relevant keywords"
                ])
        
        # Check sections
        missing_sections = resume_data.get('missing_sections', [])
        if missing_sections:
            weaknesses.append(f"Missing important sections: {', '.join(missing_sections)}")
            improvements.append("Add missing resume sections for completeness")
        
        # Overall assessment
        priority_level = 'high' if len(weaknesses) >= 4 else 'medium' if len(weaknesses) >= 2 else 'low'
        
        return {
            'weaknesses_found': weaknesses,
            'improvement_suggestions': improvements,
            'priority_level': priority_level,
            'overall_assessment': self._get_weakness_assessment(len(weaknesses))
        }
    
    def _get_weakness_assessment(self, weakness_count: int) -> str:
        """Get overall assessment based on weakness count."""
        if weakness_count >= 5:
            return "Significant improvements needed across multiple areas"
        elif weakness_count >= 3:
            return "Several areas need attention for better impact"
        elif weakness_count >= 1:
            return "Minor improvements can enhance resume effectiveness"
        else:
            return "Resume is well-structured with minimal issues"
    
    def generate_interview_preparation_plan(self, resume_data: Dict, jd_data: Dict, 
                                          match_data: Dict) -> Dict:
        """Generate comprehensive interview preparation plan."""
        skills_found = resume_data.get('skills_found', [])
        missing_skills = match_data.get('missing_skills', [])
        role = jd_data.get('jd_role', 'software_developer')
        
        # Technical preparation based on skills
        technical_prep = {
            'skills_to_review': skills_found[:5],  # Top 5 skills to highlight
            'skills_to_study': missing_skills[:3],  # Top 3 gaps to address
            'coding_topics': self._get_coding_topics(role),
            'system_design_topics': self._get_system_design_topics(role)
        }
        
        # Behavioral preparation
        behavioral_prep = {
            'star_examples_needed': [
                'Tell me about a challenging project you worked on',
                'Describe a time you had to learn a new technology quickly',
                'Give an example of when you collaborated with a team',
                'Tell me about a time you solved a difficult problem'
            ],
            'company_research': [
                'Study company mission, values, and recent news',
                'Understand their products/services and target market',
                'Research the team and company culture',
                'Prepare thoughtful questions about the role'
            ]
        }
        
        # Timeline and priorities
        timeline = {
            '1_week_before': ['Complete company research', 'Prepare STAR examples'],
            '3_days_before': ['Review technical concepts', 'Practice coding problems'],
            '1_day_before': ['Mock interview practice', 'Prepare questions to ask'],
            'day_of': ['Review key points', 'Prepare materials', 'Arrive early']
        }
        
        return {
            'technical_preparation': technical_prep,
            'behavioral_preparation': behavioral_prep,
            'timeline': timeline,
            'confidence_tips': [
                'Practice explaining technical concepts in simple terms',
                'Prepare specific examples from your projects',
                'Focus on problem-solving approach, not just solutions',
                'Show enthusiasm for learning and growth'
            ]
        }
    
    def _get_coding_topics(self, role: str) -> List[str]:
        """Get relevant coding topics based on role."""
        topics_by_role = {
            'web_developer': ['JavaScript fundamentals', 'React/Vue concepts', 'REST API design', 'Database queries'],
            'mobile_developer': ['Mobile UI patterns', 'State management', 'API integration', 'Platform-specific features'],
            'data_analyst': ['SQL queries', 'Data manipulation with Python', 'Statistical concepts', 'Data visualization']
        }
        return topics_by_role.get(role, topics_by_role['web_developer'])
    
    def _get_system_design_topics(self, role: str) -> List[str]:
        """Get system design topics based on role."""
        if 'senior' in role.lower() or 'lead' in role.lower():
            return ['Database design', 'API architecture', 'Scalability concepts', 'Caching strategies']
        else:
            return ['Basic architecture patterns', 'Database relationships', 'API design principles']
    
    def generate_career_roadmap(self, current_skills: List[str], target_role: str, 
                               experience_level: str = 'beginner') -> Dict:
        """Generate detailed career roadmap with timeline."""
        
        # Define skill progression paths for different roles
        role_progressions = {
            'web_developer': {
                'beginner': [
                    {'month': 1, 'skills': ['HTML', 'CSS'], 'projects': ['Static website', 'CSS animations']},
                    {'month': 2, 'skills': ['JavaScript'], 'projects': ['Interactive webpage', 'Calculator app']},
                    {'month': 3, 'skills': ['React'], 'projects': ['Todo app', 'Weather dashboard']},
                    {'month': 4, 'skills': ['Node.js', 'Express'], 'projects': ['REST API', 'Backend server']},
                    {'month': 5, 'skills': ['Database', 'MongoDB'], 'projects': ['Full-stack app', 'User authentication']},
                    {'month': 6, 'skills': ['Deployment', 'AWS'], 'projects': ['Deployed portfolio', 'Production app']}
                ],
                'intermediate': [
                    {'month': 1, 'skills': ['Advanced React', 'Redux'], 'projects': ['E-commerce frontend']},
                    {'month': 2, 'skills': ['TypeScript'], 'projects': ['Typed React application']},
                    {'month': 3, 'skills': ['Testing', 'Jest'], 'projects': ['Test-driven development']},
                    {'month': 4, 'skills': ['GraphQL'], 'projects': ['GraphQL API integration']},
                    {'month': 5, 'skills': ['Docker', 'CI/CD'], 'projects': ['Containerized deployment']},
                    {'month': 6, 'skills': ['System Design'], 'projects': ['Scalable architecture']}
                ]
            },
            'mobile_developer': {
                'beginner': [
                    {'month': 1, 'skills': ['Dart', 'Flutter Basics'], 'projects': ['Hello World app', 'Basic UI']},
                    {'month': 2, 'skills': ['Flutter Widgets'], 'projects': ['Calculator app', 'Todo list']},
                    {'month': 3, 'skills': ['State Management'], 'projects': ['Shopping cart', 'User preferences']},
                    {'month': 4, 'skills': ['API Integration'], 'projects': ['Weather app', 'News reader']},
                    {'month': 5, 'skills': ['Local Storage', 'SQLite'], 'projects': ['Notes app', 'Expense tracker']},
                    {'month': 6, 'skills': ['Firebase', 'Authentication'], 'projects': ['Social app', 'Chat application']}
                ]
            },
            'data_analyst': {
                'beginner': [
                    {'month': 1, 'skills': ['Excel Advanced', 'SQL Basics'], 'projects': ['Sales analysis', 'Data cleaning']},
                    {'month': 2, 'skills': ['Python', 'Pandas'], 'projects': ['Data manipulation', 'CSV analysis']},
                    {'month': 3, 'skills': ['Data Visualization', 'Matplotlib'], 'projects': ['Chart creation', 'Dashboard']},
                    {'month': 4, 'skills': ['Statistics', 'Hypothesis Testing'], 'projects': ['A/B testing', 'Statistical analysis']},
                    {'month': 5, 'skills': ['Tableau', 'Power BI'], 'projects': ['Interactive dashboard', 'Business reports']},
                    {'month': 6, 'skills': ['Machine Learning Basics'], 'projects': ['Predictive model', 'Classification']}
                ]
            }
        }
        
        # Get appropriate progression
        target_progression = role_progressions.get(target_role, role_progressions['web_developer'])
        level_progression = target_progression.get(experience_level, target_progression['beginner'])
        
        # Identify gaps based on current skills
        current_skills_lower = [skill.lower() for skill in current_skills]
        
        roadmap_steps = []
        for step in level_progression:
            step_skills = step['skills']
            missing_skills = [skill for skill in step_skills if skill.lower() not in current_skills_lower]
            
            if missing_skills:  # Only include if there are skills to learn
                roadmap_steps.append({
                    'month': step['month'],
                    'skills_to_learn': missing_skills,
                    'all_skills': step_skills,
                    'projects': step['projects'],
                    'estimated_hours': len(missing_skills) * 20,  # 20 hours per skill
                    'priority': 'High' if step['month'] <= 3 else 'Medium'
                })
        
        # Generate learning resources for each step
        for step in roadmap_steps:
            step['resources'] = self._get_learning_resources_for_skills(step['skills_to_learn'])
        
        return {
            'roadmap_steps': roadmap_steps,
            'total_timeline_months': len(roadmap_steps),
            'estimated_total_hours': sum(step['estimated_hours'] for step in roadmap_steps),
            'next_milestone': roadmap_steps[0] if roadmap_steps else None,
            'career_advice': self._generate_career_advice(target_role, experience_level)
        }
    
    def _get_learning_resources_for_skills(self, skills: List[str]) -> Dict:
        """Get learning resources for specific skills."""
        resources = {
            'courses': [],
            'documentation': [],
            'practice_sites': [],
            'youtube_channels': []
        }
        
        skill_resources = {
            'html': {
                'courses': ['freeCodeCamp HTML/CSS', 'MDN HTML Tutorial'],
                'practice_sites': ['Codecademy', 'W3Schools'],
                'youtube_channels': ['Traversy Media', 'The Net Ninja']
            },
            'css': {
                'courses': ['CSS Grid Garden', 'Flexbox Froggy'],
                'practice_sites': ['CSS Battle', 'Frontend Mentor'],
                'youtube_channels': ['Kevin Powell', 'Layout Land']
            },
            'javascript': {
                'courses': ['JavaScript30', 'Eloquent JavaScript'],
                'practice_sites': ['Codewars', 'HackerRank JavaScript'],
                'youtube_channels': ['Wes Bos', 'Fun Fun Function']
            },
            'react': {
                'courses': ['React Official Tutorial', 'Scrimba React Course'],
                'documentation': ['React.dev', 'React Router Docs'],
                'youtube_channels': ['Codevolution', 'Academind']
            },
            'python': {
                'courses': ['Python.org Tutorial', 'Automate the Boring Stuff'],
                'practice_sites': ['LeetCode Python', 'Codewars Python'],
                'youtube_channels': ['Corey Schafer', 'Real Python']
            }
        }
        
        for skill in skills:
            skill_lower = skill.lower()
            if skill_lower in skill_resources:
                skill_res = skill_resources[skill_lower]
                resources['courses'].extend(skill_res.get('courses', []))
                resources['documentation'].extend(skill_res.get('documentation', []))
                resources['practice_sites'].extend(skill_res.get('practice_sites', []))
                resources['youtube_channels'].extend(skill_res.get('youtube_channels', []))
        
        return resources
    
    def _generate_career_advice(self, target_role: str, experience_level: str) -> List[str]:
        """Generate career advice based on target role and experience level."""
        advice = []
        
        if experience_level == 'beginner':
            advice.extend([
                'Focus on building a strong portfolio with real projects',
                'Contribute to open source projects to gain experience',
                'Join developer communities and attend meetups',
                'Practice coding regularly and build the habit'
            ])
        
        if target_role == 'web_developer':
            advice.extend([
                'Learn both frontend and backend technologies for versatility',
                'Stay updated with modern frameworks and tools',
                'Practice responsive design and accessibility'
            ])
        elif target_role == 'mobile_developer':
            advice.extend([
                'Choose between native (iOS/Android) or cross-platform (Flutter/React Native)',
                'Understand mobile UX principles and design patterns',
                'Learn about app store deployment and optimization'
            ])
        elif target_role == 'data_analyst':
            advice.extend([
                'Develop strong SQL skills as foundation',
                'Learn to tell stories with data visualization',
                'Understand business context for data analysis'
            ])
        
        return advice
    
    def estimate_hiring_probability(self, resume_data: Dict, jd_data: Dict, 
                                  match_data: Dict) -> Dict:
        """Estimate probability of getting hired based on multiple factors."""
        
        # Factor 1: Skills Match (40% weight)
        skills_score = match_data.get('overall_match', 0)
        skills_probability = (skills_score / 100) * 40
        
        # Factor 2: Experience Alignment (25% weight)
        experience_data = match_data.get('experience_analysis', {})
        exp_score = experience_data.get('alignment_score', 50)
        experience_probability = (exp_score / 100) * 25
        
        # Factor 3: Resume Quality (20% weight)
        quality_score = resume_data.get('quality_score', 0)
        quality_probability = (quality_score / 100) * 20
        
        # Factor 4: ATS Compatibility (15% weight)
        ats_data = resume_data.get('ats_analysis', {})
        ats_score = ats_data.get('score', 70)
        ats_probability = (ats_score / 100) * 15
        
        # Calculate total probability
        total_probability = skills_probability + experience_probability + quality_probability + ats_probability
        
        # Adjust based on competition level (estimated)
        competition_adjustment = self._estimate_competition_adjustment(jd_data)
        adjusted_probability = total_probability * competition_adjustment
        
        # Generate specific recommendations
        improvement_areas = []
        if skills_score < 70:
            improvement_areas.append('Skills alignment needs improvement')
        if exp_score < 60:
            improvement_areas.append('Experience relevance could be stronger')
        if quality_score < 80:
            improvement_areas.append('Resume quality should be enhanced')
        if ats_score < 75:
            improvement_areas.append('ATS compatibility needs optimization')
        
        return {
            'hiring_probability': round(adjusted_probability, 1),
            'confidence_level': self._get_probability_confidence_level(adjusted_probability),
            'breakdown': {
                'skills_match': round(skills_probability, 1),
                'experience_alignment': round(experience_probability, 1),
                'resume_quality': round(quality_probability, 1),
                'ats_compatibility': round(ats_probability, 1)
            },
            'improvement_areas': improvement_areas,
            'next_steps': self._generate_hiring_improvement_steps(improvement_areas),
            'competition_factor': round(competition_adjustment, 2)
        }
    
    def _estimate_competition_adjustment(self, jd_data: Dict) -> float:
        """Estimate competition level and adjust probability accordingly."""
        base_adjustment = 1.0
        
        # Check for high-competition indicators
        jd_text = jd_data.get('text', '').lower()
        
        # Popular companies or roles
        if any(company in jd_text for company in ['google', 'facebook', 'amazon', 'microsoft', 'apple']):
            base_adjustment *= 0.7  # High competition
        
        # Remote work (often more competitive)
        if 'remote' in jd_text:
            base_adjustment *= 0.85
        
        # Entry-level positions (high competition)
        if any(level in jd_text for level in ['entry', 'junior', 'graduate', 'intern']):
            base_adjustment *= 0.8
        
        return base_adjustment
    
    def _get_probability_confidence_level(self, probability: float) -> str:
        """Convert probability to confidence level description."""
        if probability >= 80:
            return 'Very Strong Candidate'
        elif probability >= 65:
            return 'Strong Candidate'
        elif probability >= 50:
            return 'Competitive Candidate'
        elif probability >= 35:
            return 'Moderate Chance'
        else:
            return 'Needs Significant Improvement'
    
    def _generate_hiring_improvement_steps(self, improvement_areas: List[str]) -> List[str]:
        """Generate specific steps to improve hiring probability."""
        steps = []
        
        if 'Skills alignment' in str(improvement_areas):
            steps.append('Focus on learning the top 3 missing skills from job requirements')
        
        if 'Experience relevance' in str(improvement_areas):
            steps.append('Reframe existing experience to better match job requirements')
            steps.append('Consider building relevant projects to demonstrate skills')
        
        if 'Resume quality' in str(improvement_areas):
            steps.append('Improve resume formatting and content structure')
            steps.append('Add quantified achievements and stronger action verbs')
        
        if 'ATS compatibility' in str(improvement_areas):
            steps.append('Optimize resume for ATS systems with better keyword usage')
        
        return steps
    
    def estimate_salary_range(self, role: str, location: str, experience: str) -> Dict:
        """Estimate salary range based on role, location, and experience."""
        # Base salary data (simplified for demo)
        base_salaries = {
            'software_engineer': {'entry': 75000, 'mid': 100000, 'senior': 135000},
            'web_developer': {'entry': 65000, 'mid': 85000, 'senior': 110000},
            'mobile_developer': {'entry': 70000, 'mid': 95000, 'senior': 125000},
            'data_analyst': {'entry': 60000, 'mid': 80000, 'senior': 105000}
        }
        
        # Location multipliers
        location_multipliers = {
            'California': 1.4, 'New York': 1.3, 'Texas': 1.1, 
            'Remote': 1.0, 'US': 1.0, 'Europe': 0.8
        }
        
        base_salary = base_salaries.get(role, base_salaries['software_engineer'])[experience]
        multiplier = location_multipliers.get(location, 1.0)
        
        adjusted_salary = int(base_salary * multiplier)
        
        # Calculate range (±15%)
        salary_range = {
            'min': int(adjusted_salary * 0.85),
            'average': adjusted_salary,
            'max': int(adjusted_salary * 1.15)
        }
        
        # Growth projections
        growth_projections = {
            '1_year': int(adjusted_salary * 1.08),
            '3_year': int(adjusted_salary * 1.25),
            '5_year': int(adjusted_salary * 1.45)
        }
        
        return {
            'salary_range': salary_range,
            'growth_projections': growth_projections,
            'market_insights': [
                f'{role.replace("_", " ").title()} roles in {location} show strong demand',
                f'Average salary growth is 8-12% annually for {experience} level',
                'Remote work options can expand salary opportunities'
            ],
            'negotiation_tips': [
                'Highlight specific technical skills and achievements',
                'Research company-specific salary data before negotiations',
                'Consider total compensation including benefits and equity',
                'Time negotiations around performance reviews or job offers'
            ]
        }
    
    def detect_competition_level(self, jd_text: str, jd_data: Dict) -> Dict:
        """Analyze and detect competition level for a job posting."""
        competition_score = 50  # Base score
        factors = []
        
        jd_lower = jd_text.lower()
        
        # High competition indicators
        high_competition_terms = [
            'competitive salary', 'top talent', 'best candidates', 'exceptional',
            'unicorn', 'rockstar', 'ninja', 'guru', 'world-class'
        ]
        
        # Experience requirements
        experience_requirements = jd_data.get('job_requirements', {}).get('total_requirements', 0)
        
        # Check for high competition terms
        competition_terms_found = sum(1 for term in high_competition_terms if term in jd_lower)
        if competition_terms_found > 0:
            competition_score += competition_terms_found * 15
            factors.append(f'Uses competitive language ({competition_terms_found} terms)')
        
        # Analyze requirements complexity
        if experience_requirements > 10:
            competition_score += 20
            factors.append('Extensive requirements list')
        elif experience_requirements > 6:
            competition_score += 10
            factors.append('Moderate requirements list')
        
        # Check for multiple technical skills
        tech_skills = ['python', 'javascript', 'react', 'angular', 'aws', 'docker', 'kubernetes']
        tech_count = sum(1 for skill in tech_skills if skill in jd_lower)
        
        if tech_count >= 6:
            competition_score += 15
            factors.append('Requires multiple advanced technologies')
        elif tech_count >= 3:
            competition_score += 8
            factors.append('Requires several technologies')
        
        # Check for years of experience
        experience_mentions = re.findall(r'(\d+)\+?\s*years?', jd_lower)
        if experience_mentions:
            max_years = max([int(year) for year in experience_mentions])
            if max_years >= 7:
                competition_score += 20
                factors.append(f'Requires {max_years}+ years experience')
            elif max_years >= 5:
                competition_score += 15
                factors.append(f'Requires {max_years}+ years experience')
        
        # Determine competition level
        if competition_score >= 85:
            level = 'Very High'
            description = 'Extremely competitive position requiring top-tier candidates'
            timeline = 'Apply within 2-3 days, prepare extensively'
        elif competition_score >= 70:
            level = 'High'
            description = 'Highly competitive position with many qualified applicants'
            timeline = 'Apply within 1 week, tailor application carefully'
        elif competition_score >= 55:
            level = 'Medium'
            description = 'Moderately competitive position'
            timeline = 'Apply within 2 weeks, customize resume'
        else:
            level = 'Low'
            description = 'Lower competition, good opportunities for qualified candidates'
            timeline = 'Apply within 3-4 weeks'
        
        # Application strategy
        if competition_score >= 70:
            strategy = [
                'Customize resume extensively for exact keyword matching',
                'Write compelling cover letter highlighting unique value',
                'Apply as early as possible',
                'Network with current employees if possible',
                'Prepare for multiple interview rounds'
            ]
        else:
            strategy = [
                'Customize resume to match key requirements',
                'Apply with professional presentation',
                'Highlight relevant experience clearly'
            ]
        
        return {
            'competition_level': level,
            'competition_score': min(100, competition_score),
            'description': description,
            'factors': factors,
            'application_strategy': strategy,
            'timeline_advice': timeline
        }
    
    def generate_multiple_resume_versions(self, resume_data: Dict, target_roles: List[str]) -> Dict:
        """Generate multiple customized resume versions for different roles."""
        versions = {}
        
        # Get base resume skills
        base_skills = resume_data.get('resume_skills', {}).get('all_skills', [])
        
        # Role-specific optimizations
        role_optimizations = {
            'web_developer': {
                'priority_skills': ['HTML', 'CSS', 'JavaScript', 'React', 'Node.js'],
                'keywords': ['frontend', 'backend', 'responsive', 'web development'],
                'summary_focus': 'web application development and user experience'
            },
            'mobile_developer': {
                'priority_skills': ['React Native', 'iOS', 'Android', 'Flutter', 'Swift'],
                'keywords': ['mobile', 'app development', 'cross-platform', 'native'],
                'summary_focus': 'mobile application development and platform optimization'
            },
            'data_analyst': {
                'priority_skills': ['Python', 'SQL', 'Tableau', 'Excel', 'Power BI'],
                'keywords': ['analytics', 'data visualization', 'insights', 'reporting'],
                'summary_focus': 'data analysis and business intelligence'
            },
            'software_engineer': {
                'priority_skills': ['Python', 'Java', 'Git', 'APIs', 'Testing'],
                'keywords': ['software development', 'engineering', 'architecture', 'scalable'],
                'summary_focus': 'software engineering and system architecture'
            }
        }
        
        for role in target_roles:
            optimization = role_optimizations.get(role, role_optimizations['software_engineer'])
            
            # Find matching skills with resume
            matched_priority_skills = [skill for skill in optimization['priority_skills'] 
                                     if any(skill.lower() in base_skill.lower() for base_skill in base_skills)]
            
            # Generate customized summary
            role_name = role.replace('_', ' ').title()
            summary = f"Experienced {role_name} specializing in {optimization['summary_focus']}. "
            summary += f"Proficient in {', '.join(matched_priority_skills[:3])} with strong problem-solving skills."
            
            versions[role] = {
                'summary': summary,
                'prioritized_skills': {
                    'high_priority': matched_priority_skills,
                    'medium_priority': [skill for skill in base_skills if skill not in matched_priority_skills][:5],
                    'keywords_to_add': optimization['keywords']
                },
                'customization_tips': [
                    f'Emphasize {role_name} specific projects and achievements',
                    f'Include {", ".join(optimization["keywords"])} keywords naturally',
                    'Tailor work experience descriptions to match role requirements',
                    'Add relevant certifications or courses for this role'
                ],
                'keyword_optimization': optimization['keywords'][:4]
            }
        
        # Generate overall application strategy
        application_strategy = {
            'primary_focus': 'Customize each resume version for specific role requirements',
            'keyword_strategy': 'Use role-specific terminology and industry buzzwords',
            'experience_emphasis': 'Highlight most relevant projects and achievements first',
            'skill_presentation': 'Order skills by relevance to each specific role'
        }
        
        return {
            'versions': versions,
            'application_strategy': application_strategy,
            'total_versions_generated': len(versions)
        }