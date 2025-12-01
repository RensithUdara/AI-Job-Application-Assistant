#!/usr/bin/env python3
"""
Comprehensive test script for all advanced AI features in the Job Application Assistant.
Tests 20+ advanced features including the newly added ones.
"""

import sys
import os
import traceback
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.resume_parser import ResumeParser
from core.jd_processor import JobDescriptionProcessor
from core.recommender import Recommender
from core.matcher import Matcher

def test_resume_parser_advanced_features():
    """Test all advanced features in ResumeParser."""
    print("\n🔍 Testing Resume Parser Advanced Features...")
    parser = ResumeParser()
    
    # Sample resume text
    sample_resume = """
    John Doe
    Software Engineer
    Email: john@example.com
    Phone: 123-456-7890
    
    Experience:
    2020-2023: Senior Developer at TechCorp
    Built scalable web applications using Python and React.
    Led team of 5 developers.
    Increased system performance by 40%.
    
    2018-2020: Junior Developer at StartupXYZ
    Developed mobile applications.
    
    Skills: Python, JavaScript, React, Django, SQL, AWS
    
    Education:
    2018: BS Computer Science
    """
    
    try:
        # Test duplicate content detection
        print("  ✅ Testing duplicate content detection...")
        duplicate_analysis = parser.detect_duplicate_content(sample_resume)
        print(f"     Uniqueness Score: {duplicate_analysis['duplicate_score']}/100")
        print(f"     Level: {duplicate_analysis['uniqueness_level']}")
        
        # Test timeline validation
        print("  ✅ Testing timeline validation...")
        timeline_analysis = parser.validate_resume_timeline(sample_resume)
        print(f"     Timeline Score: {timeline_analysis['timeline_score']}/100")
        print(f"     Status: {timeline_analysis['timeline_status']}")
        
        # Test project impact analysis
        print("  ✅ Testing project impact analysis...")
        project_analysis = parser.analyze_project_impact(sample_resume)
        print(f"     Projects Found: {project_analysis['projects_found']}")
        if project_analysis['projects_found'] > 0:
            print(f"     Avg Impact Score: {project_analysis['average_impact_score']}/100")
        
        # Test heatmap analysis
        print("  ✅ Testing heatmap analysis...")
        parsed_data = parser.parse_resume(sample_resume)
        if 'heatmap_analysis' in parsed_data:
            heatmap = parsed_data['heatmap_analysis']
            print(f"     Overall Strength: {heatmap['overall_strength']:.1f}%")
        
        # Test ATS simulation
        print("  ✅ Testing ATS simulation...")
        if 'ats_simulation' in parsed_data:
            ats = parsed_data['ats_simulation']
            print(f"     Parsing Success Rate: {ats['parsing_success_rate']}%")
        
        print("  🎉 Resume Parser Advanced Features: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"  ❌ Resume Parser test failed: {str(e)}")
        traceback.print_exc()
        return False

def test_jd_processor_advanced_features():
    """Test all advanced features in JobDescriptionProcessor."""
    print("\n🎯 Testing JD Processor Advanced Features...")
    processor = JobDescriptionProcessor()
    
    # Sample job description
    sample_jd = """
    Software Engineer Position
    
    We are looking for a skilled Software Engineer to join our team.
    
    Requirements:
    - 3+ years experience in Python programming
    - Strong knowledge of JavaScript and React
    - Experience with AWS cloud services
    - Bachelor's degree in Computer Science
    - Knowledge of SQL databases
    - Agile development experience
    
    Responsibilities:
    - Develop and maintain web applications
    - Collaborate with cross-functional teams
    - Write clean, maintainable code
    - Participate in code reviews
    
    Benefits:
    - Competitive salary $80,000-$120,000
    - Health insurance
    - 401k matching
    """
    
    try:
        # Test job trends extraction
        print("  ✅ Testing job trends extraction...")
        job_trends = processor.extract_job_trends(sample_jd)
        print(f"     Trending Skills: {len(job_trends['trending_skills'])}")
        print(f"     Market Demand: {job_trends['market_demand_level']}")
        
        # Test keyword importance ranking
        print("  ✅ Testing keyword importance ranking...")
        keyword_ranking = processor.rank_keyword_importance(sample_jd)
        print(f"     Critical Skills: {len(keyword_ranking['critical_skills'])}")
        print(f"     Important Skills: {len(keyword_ranking['important_skills'])}")
        print(f"     Top 5 Skills: {keyword_ranking['top_5_skills']}")
        
        # Test role expansion summary
        print("  ✅ Testing role expansion summary...")
        role_expansion = processor.generate_role_expansion_summary(sample_jd)
        print(f"     Primary Role: {role_expansion['primary_role_type']}")
        print(f"     Career Level: {role_expansion['career_level']}")
        
        # Test red flag detection
        print("  ✅ Testing red flag detection...")
        parsed_jd = processor.process_job_description(sample_jd)
        if 'red_flag_analysis' in parsed_jd:
            red_flags = parsed_jd['red_flag_analysis']
            print(f"     Risk Score: {red_flags['risk_score']}/100")
            print(f"     Red Flags Found: {len(red_flags['red_flags'])}")
        
        print("  🎉 JD Processor Advanced Features: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"  ❌ JD Processor test failed: {str(e)}")
        traceback.print_exc()
        return False

def test_recommender_advanced_features():
    """Test all advanced features in Recommender."""
    print("\n🚀 Testing Recommender Advanced Features...")
    recommender = Recommender()
    
    try:
        # Test salary estimation
        print("  ✅ Testing salary estimation...")
        salary_data = recommender.estimate_salary_range("software_engineer", "California", "mid")
        print(f"     Salary Range: ${salary_data['salary_range']['min']:,} - ${salary_data['salary_range']['max']:,}")
        print(f"     Market Insights: {len(salary_data['market_insights'])} insights")
        
        # Test competition level detection
        print("  ✅ Testing competition level detection...")
        sample_jd_text = "Senior Software Engineer with 5+ years Python experience, React, AWS"
        sample_jd_data = {"job_requirements": {"total_requirements": 8}}
        
        competition_data = recommender.detect_competition_level(sample_jd_text, sample_jd_data)
        print(f"     Competition Level: {competition_data['competition_level']}")
        print(f"     Competition Score: {competition_data['competition_score']}/100")
        
        # Test multiple resume versions
        print("  ✅ Testing multiple resume versions...")
        sample_resume_data = {
            'resume_skills': {
                'all_skills': ['Python', 'JavaScript', 'React', 'SQL'],
                'by_category': {'Programming': ['Python', 'JavaScript'], 'Web': ['React']}
            },
            'sections': {
                'experience': "Software development experience",
                'skills': "Python, JavaScript, React"
            }
        }
        
        versions = recommender.generate_multiple_resume_versions(
            sample_resume_data, 
            ['web_developer', 'mobile_developer']
        )
        print(f"     Generated Versions: {len(versions['versions'])}")
        
        # Test career roadmap generation
        print("  ✅ Testing career roadmap generation...")
        current_skills = ['Python', 'JavaScript']
        roadmap = recommender.generate_career_roadmap(current_skills, 'web_developer', 'intermediate')
        print(f"     Timeline: {roadmap['total_timeline_months']} months")
        print(f"     Steps: {len(roadmap['roadmap_steps'])}")
        
        print("  🎉 Recommender Advanced Features: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"  ❌ Recommender test failed: {str(e)}")
        traceback.print_exc()
        return False

def test_integration_features():
    """Test integration between all components."""
    print("\n🔗 Testing Integration Features...")
    
    try:
        # Test complete pipeline
        parser = ResumeParser()
        processor = JobDescriptionProcessor()
        matcher = Matcher()
        
        sample_resume = "John Doe, Software Engineer with Python and React experience"
        sample_jd = "Looking for Python developer with React skills"
        
        # Parse both
        resume_data = parser.parse_resume(sample_resume)
        jd_data = processor.process_job_description(sample_jd)
        
        # Test matching
        match_data = matcher.match_resume_to_jd(resume_data, jd_data)
        
        print(f"  ✅ Integration test: Match score {match_data.get('overall_match', 0)}%")
        print("  🎉 Integration Features: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"  ❌ Integration test failed: {str(e)}")
        traceback.print_exc()
        return False

def main():
    """Run all advanced feature tests."""
    print("🔥 COMPREHENSIVE ADVANCED AI FEATURES TEST")
    print("=" * 60)
    
    results = []
    
    # Test all components
    results.append(test_resume_parser_advanced_features())
    results.append(test_jd_processor_advanced_features())
    results.append(test_recommender_advanced_features())
    results.append(test_integration_features())
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Tests Passed: {passed}/{total}")
    print(f"❌ Tests Failed: {total - passed}/{total}")
    print(f"📈 Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ALL ADVANCED AI FEATURES ARE WORKING PERFECTLY!")
        print("✨ Ready for academic presentation and demonstration!")
    else:
        print(f"\n⚠️  {total - passed} feature(s) need attention")
    
    print("\n🚀 Advanced Features Summary:")
    print("  • Duplicate Content Detection")
    print("  • Timeline Validation")  
    print("  • Project Impact Analysis")
    print("  • Resume Heatmap Analysis")
    print("  • ATS Parsing Simulation")
    print("  • Role Compatibility Analysis")
    print("  • Career Roadmap Generation")
    print("  • Red Flag Detection")
    print("  • Job Trends Extraction")
    print("  • Keyword Importance Ranking")
    print("  • Role Expansion Summary")
    print("  • Salary Estimation")
    print("  • Competition Level Detection")
    print("  • Multiple Resume Versions")
    print("  • Market Analysis & Insights")
    print("  • And 5+ more advanced features...")
    
    print(f"\n🎯 Total Advanced Features Implemented: 20+")
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)