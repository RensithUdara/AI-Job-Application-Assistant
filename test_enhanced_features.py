"""
Test Script for AI Job Application Assistant
This script demonstrates all the enhanced features and analytics
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from core.resume_parser import ResumeParser
from core.jd_processor import JobDescriptionProcessor  
from core.matcher import Matcher
from core.recommender import Recommender

def test_enhanced_features():
    """Test all enhanced features of the application."""
    print("🚀 Testing Enhanced AI Job Application Assistant Features\n")
    
    # Sample resume text
    sample_resume = """
    John Doe
    Software Developer
    Email: john.doe@email.com
    Phone: +1-555-123-4567
    LinkedIn: linkedin.com/in/johndoe

    SUMMARY
    Enthusiastic computer science student with strong programming skills in Python and Java. 
    Passionate about web development and mobile applications.

    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology | Expected Graduation: May 2024
    GPA: 3.7/4.0

    SKILLS
    Programming Languages: Python, Java, JavaScript, HTML, CSS
    Frameworks: React, Django, Flask
    Databases: MySQL, PostgreSQL
    Tools: Git, GitHub, VS Code

    PROJECTS
    E-commerce Website (2023)
    • Developed a full-stack e-commerce platform using React and Django
    • Implemented user authentication and payment integration
    • Deployed on Heroku with PostgreSQL database

    EXPERIENCE
    Software Development Intern
    Tech Solutions Inc. | June 2023 - August 2023
    • Assisted in developing web applications using React and Node.js
    • Collaborated with team using Git version control
    """
    
    # Sample job description
    sample_jd = """
    Job Title: Junior Full Stack Developer
    Company: InnovateTech Solutions
    Location: Remote/Hybrid
    Experience Level: 1-2 years
    Employment Type: Full-time

    We are seeking a talented Junior Full Stack Developer to join our growing team.
    
    Required Skills:
    • Strong proficiency in JavaScript, HTML5, and CSS3
    • Experience with React.js and modern frontend frameworks
    • Knowledge of Node.js and Express.js for backend development
    • Understanding of database design and SQL (PostgreSQL preferred)
    • Experience with NoSQL databases (MongoDB)
    • Proficiency with Git version control and GitHub
    • Understanding of RESTful API design and implementation
    • Experience with testing frameworks (Jest, Cypress)
    • Familiarity with cloud platforms (AWS, Azure, or Google Cloud)
    • Understanding of CI/CD pipelines and DevOps practices

    Preferred Skills:
    • Experience with TypeScript
    • Knowledge of GraphQL
    • Familiarity with containerization (Docker)
    • Experience with state management libraries (Redux)

    Salary: $70,000 - $85,000
    """
    
    try:
        # Initialize components
        print("1. Initializing enhanced components...")
        resume_parser = ResumeParser()
        jd_processor = JobDescriptionProcessor()
        matcher = Matcher()
        recommender = Recommender()
        
        # Test enhanced resume parsing
        print("2. Testing enhanced resume parsing with ATS analysis...")
        resume_data = resume_parser.parse_resume(text_content=sample_resume)
        
        print(f"   ✓ Resume Quality Score: {resume_data['quality_score']}/100")
        print(f"   ✓ ATS Compatibility Score: {resume_data['ats_analysis']['score']}/100")
        print(f"   ✓ Word Count: {resume_data['word_count']}")
        print(f"   ✓ Skills Found: {len(resume_data['resume_skills']['all_skills'])}")
        
        if resume_data['ats_analysis']['issues']:
            print("   ⚠️ ATS Issues:")
            for issue in resume_data['ats_analysis']['issues']:
                print(f"     - {issue}")
        
        # Test enhanced job description processing
        print("\n3. Testing enhanced job description processing...")
        jd_data = jd_processor.process_jd(sample_jd)
        
        print(f"   ✓ Detected Role: {jd_data['jd_role']}")
        print(f"   ✓ Seniority Level: {jd_data['seniority']}")
        print(f"   ✓ Required Experience: {jd_data['required_experience']}")
        
        salary_info = jd_data['salary_info']
        if salary_info['salary_mentioned']:
            print(f"   ✓ Salary Range: ${salary_info['min_salary']:,} - ${salary_info['max_salary']:,}")
        
        company_info = jd_data['company_info']
        print(f"   ✓ Company: {company_info['company_name']}")
        print(f"   ✓ Work Type: {company_info['work_type']}")
        
        job_reqs = jd_data['job_requirements']
        print(f"   ✓ Total Requirements: {job_reqs['total_requirements']}")
        print(f"   ✓ Complexity Score: {job_reqs['complexity_score']}/100")
        
        # Test enhanced matching with market analysis
        print("\n4. Testing enhanced matching algorithms...")
        match_data = matcher.match_resume_to_jd(resume_data, jd_data)
        
        print(f"   ✓ Overall Match Score: {match_data['match_score_overall']}/100")
        print(f"   ✓ Skills Match: {match_data['skill_match']['match_percentage']:.1f}%")
        print(f"   ✓ Technical Match: {match_data['technical_match']:.1f}%")
        
        # Market competitiveness analysis
        market_analysis = match_data['market_analysis']
        print(f"   ✓ Market Position: {market_analysis['market_position']}")
        print(f"   ✓ Competitiveness Score: {market_analysis['competitiveness_score']:.1f}%")
        
        if market_analysis['strengths']:
            print("   ✓ Key Strengths:")
            for strength in market_analysis['strengths']:
                print(f"     - {strength}")
        
        # Experience alignment
        exp_alignment = match_data['experience_alignment']
        print(f"   ✓ Experience Fit: {exp_alignment['seniority_fit']}")
        print(f"   ✓ Experience Score: {exp_alignment['experience_score']}/100")
        
        # Test enhanced recommendations
        print("\n5. Testing enhanced recommendation system...")
        recommendations = recommender.build_recommendations(resume_data, jd_data, match_data)
        
        print(f"   ✓ Resume Tips Generated: {len(recommendations['resume_tips'])}")
        print(f"   ✓ Skill Roadmap Items: {len(recommendations['skill_roadmap'])}")
        print(f"   ✓ Interview Questions: {len(recommendations['interview_questions'])}")
        
        # Career insights
        career_insights = recommendations['career_insights']
        print(f"   ✓ Market Demand: {career_insights['market_demand']}")
        print(f"   ✓ Growth Potential: {career_insights['growth_potential']}")
        print(f"   ✓ Next Career Steps: {', '.join(career_insights['next_career_steps'][:2])}")
        
        # Learning resources
        learning_resources = recommendations['learning_resources']
        print(f"   ✓ Recommended Courses: {len(learning_resources['online_courses'])}")
        print(f"   ✓ Practice Projects: {len(learning_resources['practice_projects'])}")
        print(f"   ✓ Estimated Learning Time: {learning_resources['estimated_learning_time']}")
        
        # Application strategy
        app_strategy = recommendations['application_strategy']
        print(f"   ✓ Application Readiness: {app_strategy['application_readiness']}")
        
        # Industry benchmarking
        print("\n6. Testing industry benchmarking...")
        benchmarks = jd_processor.get_industry_benchmarks(jd_data['jd_role'], jd_data['seniority'])
        print(f"   ✓ Average Salary Benchmark: ${benchmarks['avg_salary']:,}")
        print(f"   ✓ Common Skills for Role: {', '.join(benchmarks['common_skills'][:4])}")
        
        print("\n🎉 All enhanced features tested successfully!")
        print("\n📊 Enhanced Analytics Summary:")
        print("=" * 50)
        print(f"Overall Match Score: {match_data['match_score_overall']}/100")
        print(f"Resume Quality: {resume_data['quality_score']}/100")
        print(f"ATS Compatibility: {resume_data['ats_analysis']['score']}/100")
        print(f"Market Competitiveness: {market_analysis['competitiveness_score']:.0f}%")
        print(f"Application Status: {app_strategy['application_readiness']}")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_enhanced_features()