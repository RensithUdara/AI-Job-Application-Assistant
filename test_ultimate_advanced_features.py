"""
Comprehensive Test Suite for All Advanced AI Features
Tests all enhanced functionality including intelligent scoring, career path analysis, and industry insights.
"""

import unittest
import sys
import os
import json

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.resume_parser import ResumeParser
from core.jd_processor import JobDescriptionProcessor
from core.matcher import Matcher
from core.recommender import Recommender
from core.career_analyzer import CareerAnalyzer


class TestAdvancedAIFeatures(unittest.TestCase):
    """Test suite for all advanced AI features."""

    def setUp(self):
        """Set up test components and sample data."""
        self.resume_parser = ResumeParser()
        self.jd_processor = JobDescriptionProcessor()
        self.matcher = Matcher()
        self.recommender = Recommender()
        self.career_analyzer = CareerAnalyzer()
        
        # Sample resume text for testing
        self.sample_resume = """
        John Doe
        Software Engineer
        Email: john.doe@email.com
        Phone: (555) 123-4567
        
        EXPERIENCE
        Senior Software Engineer at TechCorp (2020-2023)
        • Developed scalable web applications using Python and React
        • Led a team of 5 developers on microservices architecture
        • Improved system performance by 40% through optimization
        • Implemented CI/CD pipelines reducing deployment time by 60%
        
        Software Developer at StartupXYZ (2018-2020)
        • Built RESTful APIs using Django and PostgreSQL
        • Collaborated with product team to deliver features on time
        • Mentored 2 junior developers
        
        EDUCATION
        Bachelor of Science in Computer Science
        University of Technology (2014-2018)
        
        SKILLS
        Python, JavaScript, React, Django, PostgreSQL, AWS, Docker, Kubernetes, Git
        Machine Learning, Data Analysis, System Design, Agile Methodology
        """
        
        # Sample job description for testing
        self.sample_jd = """
        Senior Full Stack Developer - TechInnovate Inc.
        
        We are seeking a Senior Full Stack Developer to join our rapidly growing fintech startup.
        
        Requirements:
        • 5+ years of experience in full-stack development
        • Strong proficiency in Python, JavaScript, and React
        • Experience with cloud platforms (AWS, Azure, or GCP)
        • Knowledge of microservices architecture and containerization
        • Familiarity with financial systems and security best practices
        • Bachelor's degree in Computer Science or related field
        
        Responsibilities:
        • Design and develop scalable web applications
        • Lead technical discussions and mentor junior developers
        • Collaborate with product and design teams
        • Implement security measures and compliance requirements
        • Optimize application performance and user experience
        
        What we offer:
        • Competitive salary $120,000 - $160,000
        • Equity options and comprehensive health benefits
        • Remote work flexibility
        • Professional development opportunities
        • Fast-paced, innovative environment
        """

    def test_intelligent_resume_scoring(self):
        """Test the intelligent resume scoring feature."""
        print("\n=== Testing Intelligent Resume Scoring ===")
        
        # Test basic scoring
        scoring_result = self.resume_parser.calculate_intelligent_resume_score(
            self.sample_resume, 'software_engineer'
        )
        
        # Validate scoring structure
        self.assertIn('overall_score', scoring_result)
        self.assertIn('individual_scores', scoring_result)
        self.assertIn('recommendations', scoring_result)
        self.assertIn('strengths', scoring_result)
        self.assertIn('weaknesses', scoring_result)
        
        # Validate score ranges
        self.assertGreaterEqual(scoring_result['overall_score'], 0)
        self.assertLessEqual(scoring_result['overall_score'], 100)
        
        # Validate individual scores
        individual_scores = scoring_result['individual_scores']
        required_categories = [
            'content_quality', 'ats_compatibility', 'keyword_optimization',
            'formatting_score', 'experience_relevance', 'skill_match'
        ]
        
        for category in required_categories:
            self.assertIn(category, individual_scores)
            self.assertGreaterEqual(individual_scores[category], 0)
            self.assertLessEqual(individual_scores[category], 100)
        
        print(f"✅ Overall Score: {scoring_result['overall_score']}/100")
        print(f"✅ Content Quality: {individual_scores['content_quality']}/100")
        print(f"✅ ATS Compatibility: {individual_scores['ats_compatibility']}/100")
        print(f"✅ Recommendations: {len(scoring_result['recommendations'])} suggestions")

    def test_ats_compatibility_analysis(self):
        """Test the advanced ATS compatibility analysis."""
        print("\n=== Testing ATS Compatibility Analysis ===")
        
        ats_result = self.resume_parser.analyze_ats_compatibility_advanced(self.sample_resume)
        
        # Validate ATS analysis structure
        self.assertIn('overall_ats_score', ats_result)
        self.assertIn('ats_grade', ats_result)
        self.assertIn('compatibility_checks', ats_result)
        self.assertIn('parsing_confidence', ats_result)
        self.assertIn('estimated_parsing_success', ats_result)
        
        # Validate ATS score
        self.assertGreaterEqual(ats_result['overall_ats_score'], 0)
        self.assertLessEqual(ats_result['overall_ats_score'], 100)
        
        # Validate grade system
        valid_grades = ['A+', 'A', 'B', 'C', 'D']
        self.assertIn(ats_result['ats_grade'], valid_grades)
        
        # Validate compatibility checks
        checks = ats_result['compatibility_checks']
        required_checks = [
            'file_format', 'font_usage', 'section_headers', 'contact_info',
            'bullet_points', 'keyword_density', 'length', 'graphics_tables'
        ]
        
        for check in required_checks:
            self.assertIn(check, checks)
            self.assertIn('score', checks[check])
            self.assertIn('status', checks[check])
        
        print(f"✅ ATS Score: {ats_result['overall_ats_score']}/100")
        print(f"✅ ATS Grade: {ats_result['ats_grade']}")
        print(f"✅ Parsing Confidence: {ats_result['parsing_confidence']}")

    def test_industry_insights_analysis(self):
        """Test industry-specific insights analysis."""
        print("\n=== Testing Industry Insights Analysis ===")
        
        industry_insights = self.jd_processor.analyze_industry_insights(self.sample_jd)
        
        # Validate industry analysis structure
        required_fields = [
            'primary_industry', 'detected_industries', 'industry_confidence',
            'growth_outlook', 'key_trends', 'skill_premiums', 'salary_multiplier',
            'company_size', 'remote_friendliness', 'market_insights'
        ]
        
        for field in required_fields:
            self.assertIn(field, industry_insights)
        
        # Validate industry detection
        self.assertIsInstance(industry_insights['primary_industry'], str)
        self.assertIsInstance(industry_insights['detected_industries'], list)
        self.assertGreaterEqual(industry_insights['industry_confidence'], 0)
        
        # Validate salary multiplier
        self.assertGreaterEqual(industry_insights['salary_multiplier'], 0.5)
        self.assertLessEqual(industry_insights['salary_multiplier'], 2.0)
        
        print(f"✅ Primary Industry: {industry_insights['primary_industry']}")
        print(f"✅ Growth Outlook: {industry_insights['growth_outlook']}")
        print(f"✅ Company Size: {industry_insights['company_size']}")
        print(f"✅ Remote Friendliness: {industry_insights['remote_friendliness']}")

    def test_job_difficulty_assessment(self):
        """Test advanced job difficulty assessment."""
        print("\n=== Testing Job Difficulty Assessment ===")
        
        difficulty_result = self.jd_processor.assess_job_difficulty_advanced(self.sample_jd)
        
        # Validate difficulty analysis structure
        required_fields = [
            'difficulty_score', 'difficulty_level', 'difficulty_description',
            'difficulty_factors', 'preparation_timeline', 'success_probability',
            'recommendation'
        ]
        
        for field in required_fields:
            self.assertIn(field, difficulty_result)
        
        # Validate difficulty score
        self.assertGreaterEqual(difficulty_result['difficulty_score'], 0)
        self.assertLessEqual(difficulty_result['difficulty_score'], 100)
        
        # Validate difficulty levels
        valid_levels = ['Easy', 'Easy-Moderate', 'Moderate', 'Hard', 'Extremely Hard']
        self.assertIn(difficulty_result['difficulty_level'], valid_levels)
        
        # Validate success probability structure
        success_prob = difficulty_result['success_probability']
        required_levels = ['entry_level', 'mid_level', 'senior_level']
        for level in required_levels:
            self.assertIn(level, success_prob)
            self.assertGreaterEqual(success_prob[level], 0)
            self.assertLessEqual(success_prob[level], 100)
        
        print(f"✅ Difficulty Score: {difficulty_result['difficulty_score']}/100")
        print(f"✅ Difficulty Level: {difficulty_result['difficulty_level']}")
        print(f"✅ Preparation Timeline: {difficulty_result['preparation_timeline']}")

    def test_benefits_package_analysis(self):
        """Test benefits and compensation package analysis."""
        print("\n=== Testing Benefits Package Analysis ===")
        
        benefits_result = self.jd_processor.analyze_benefits_package(self.sample_jd)
        
        # Validate benefits analysis structure
        required_fields = [
            'salary_mentioned', 'equity_mentioned', 'benefits_score',
            'benefits_found', 'missing_benefits', 'package_competitiveness'
        ]
        
        for field in required_fields:
            self.assertIn(field, benefits_result)
        
        # Validate boolean fields
        self.assertIsInstance(benefits_result['salary_mentioned'], bool)
        self.assertIsInstance(benefits_result['equity_mentioned'], bool)
        
        # Validate benefits score
        self.assertGreaterEqual(benefits_result['benefits_score'], 0)
        self.assertLessEqual(benefits_result['benefits_score'], 100)
        
        # Validate competitiveness rating
        valid_ratings = ['Excellent', 'Good', 'Average', 'Below Average']
        self.assertIn(benefits_result['package_competitiveness'], valid_ratings)
        
        print(f"✅ Salary Mentioned: {benefits_result['salary_mentioned']}")
        print(f"✅ Equity Mentioned: {benefits_result['equity_mentioned']}")
        print(f"✅ Benefits Score: {benefits_result['benefits_score']}/100")
        print(f"✅ Package Competitiveness: {benefits_result['package_competitiveness']}")

    def test_career_progression_analysis(self):
        """Test career progression path analysis."""
        print("\n=== Testing Career Progression Analysis ===")
        
        # Mock current skills from resume
        current_skills = ['python', 'javascript', 'react', 'django', 'aws', 'docker']
        
        progression_result = self.career_analyzer.analyze_career_progression(
            'software_engineer', 'senior_software_engineer', current_skills, 3
        )
        
        # Validate progression analysis structure
        required_fields = [
            'feasibility_score', 'progression_timeline', 'required_skills',
            'skill_gaps', 'intermediate_roles', 'learning_path',
            'salary_progression', 'market_demand', 'success_factors'
        ]
        
        for field in required_fields:
            self.assertIn(field, progression_result)
        
        # Validate feasibility score
        self.assertGreaterEqual(progression_result['feasibility_score'], 0)
        self.assertLessEqual(progression_result['feasibility_score'], 100)
        
        # Validate learning path structure
        learning_path = progression_result['learning_path']
        self.assertIsInstance(learning_path, list)
        
        for phase in learning_path:
            required_phase_fields = ['phase', 'focus', 'skills', 'resources', 'timeline']
            for field in required_phase_fields:
                self.assertIn(field, phase)
        
        print(f"✅ Feasibility Score: {progression_result['feasibility_score']}/100")
        print(f"✅ Timeline: {progression_result['progression_timeline']}")
        print(f"✅ Skill Gaps: {len(progression_result['skill_gaps'])} identified")
        print(f"✅ Learning Phases: {len(learning_path)} phases planned")

    def test_skill_gap_analysis(self):
        """Test comprehensive skill gap analysis."""
        print("\n=== Testing Skill Gap Analysis ===")
        
        current_skills = ['python', 'javascript', 'react']
        
        gap_report = self.career_analyzer.generate_skill_gap_report(
            current_skills, 'senior_software_engineer', 'technology'
        )
        
        # Validate gap report structure
        required_fields = [
            'gap_analysis_summary', 'critical_gaps', 'nice_to_have_gaps',
            'skill_development_priority', 'learning_resources', 'timeline_estimate',
            'cost_estimate', 'progress_tracking'
        ]
        
        for field in required_fields:
            self.assertIn(field, gap_report)
        
        # Validate gap analysis summary
        summary = gap_report['gap_analysis_summary']
        required_summary_fields = [
            'total_required_skills', 'total_skill_gaps', 'skill_coverage_percentage',
            'readiness_level', 'estimated_preparation_time'
        ]
        
        for field in required_summary_fields:
            self.assertIn(field, summary)
        
        # Validate skill coverage percentage
        coverage = summary['skill_coverage_percentage']
        self.assertGreaterEqual(coverage, 0)
        self.assertLessEqual(coverage, 100)
        
        # Validate readiness level
        valid_readiness = ['High', 'Medium', 'Low']
        self.assertIn(summary['readiness_level'], valid_readiness)
        
        print(f"✅ Total Required Skills: {summary['total_required_skills']}")
        print(f"✅ Skill Coverage: {coverage}%")
        print(f"✅ Readiness Level: {summary['readiness_level']}")
        print(f"✅ Critical Gaps: {len(gap_report['critical_gaps'])}")

    def test_market_positioning_analysis(self):
        """Test market positioning and competitiveness analysis."""
        print("\n=== Testing Market Positioning Analysis ===")
        
        # Mock resume data
        mock_resume_data = {
            'resume_skills': {'all_skills': ['python', 'react', 'aws', 'docker', 'kubernetes']},
            'sections': {'experience': True}
        }
        
        positioning_result = self.recommender.analyze_market_positioning(
            mock_resume_data, 'software_engineer', 'California'
        )
        
        # Validate positioning analysis structure
        required_fields = [
            'market_tier', 'competitiveness_score', 'positioning_factors',
            'improvement_areas', 'market_advantages'
        ]
        
        for field in required_fields:
            self.assertIn(field, positioning_result)
        
        # Validate competitiveness score
        score = positioning_result['competitiveness_score']
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
        
        # Validate market tier
        self.assertIsInstance(positioning_result['market_tier'], str)
        
        print(f"✅ Market Tier: {positioning_result['market_tier']}")
        print(f"✅ Competitiveness Score: {score}/100")
        print(f"✅ Market Advantages: {len(positioning_result['market_advantages'])}")
        print(f"✅ Improvement Areas: {len(positioning_result['improvement_areas'])}")

    def test_interview_strategy_generation(self):
        """Test interview preparation strategy generation."""
        print("\n=== Testing Interview Strategy Generation ===")
        
        # Mock data
        mock_resume_data = {
            'resume_skills': {'all_skills': ['python', 'react', 'system design']}
        }
        
        mock_jd_data = {
            'jd_text': self.sample_jd,
            'job_requirements': {'total_requirements': 8}
        }
        
        interview_strategy = self.recommender.generate_interview_strategy(
            mock_resume_data, mock_jd_data, 'software_engineer'
        )
        
        # Validate interview strategy structure
        required_fields = [
            'preparation_timeline', 'focus_areas', 'technical_questions',
            'behavioral_questions', 'company_research', 'mock_interview_topics',
            'confidence_boosters'
        ]
        
        for field in required_fields:
            self.assertIn(field, interview_strategy)
            if field == 'preparation_timeline':
                self.assertIsInstance(interview_strategy[field], str)
            else:
                self.assertIsInstance(interview_strategy[field], list)
        
        print(f"✅ Preparation Timeline: {interview_strategy['preparation_timeline']}")
        print(f"✅ Focus Areas: {len(interview_strategy['focus_areas'])} identified")
        print(f"✅ Research Areas: {len(interview_strategy['company_research'])} topics")
        print(f"✅ Confidence Boosters: {len(interview_strategy['confidence_boosters'])}")

    def test_networking_strategy_generation(self):
        """Test networking strategy generation."""
        print("\n=== Testing Networking Strategy Generation ===")
        
        networking_strategy = self.recommender.generate_networking_strategy(
            'software_engineer', ['TechCorp', 'StartupXYZ'], 'California'
        )
        
        # Validate networking strategy structure
        required_fields = [
            'linkedin_optimization', 'networking_events', 'online_communities',
            'informational_interviews', 'content_strategy', 'timeline'
        ]
        
        for field in required_fields:
            self.assertIn(field, networking_strategy)
        
        # Validate timeline structure
        timeline = networking_strategy['timeline']
        expected_timeline_keys = ['week_1', 'week_2', 'week_3', 'week_4', 'ongoing']
        
        for key in expected_timeline_keys:
            self.assertIn(key, timeline)
        
        print(f"✅ LinkedIn Tips: {len(networking_strategy['linkedin_optimization'])}")
        print(f"✅ Networking Events: {len(networking_strategy['networking_events'])}")
        print(f"✅ Online Communities: {len(networking_strategy['online_communities'])}")
        print(f"✅ Timeline Phases: {len(timeline)} phases")

    def test_enhanced_salary_estimation(self):
        """Test enhanced salary estimation with market data."""
        print("\n=== Testing Enhanced Salary Estimation ===")
        
        salary_result = self.recommender.estimate_salary_range(
            'software_engineer', 'california', 'mid'
        )
        
        # Validate salary estimation structure
        required_fields = [
            'base_salary_range', 'adjusted_salary_range', 'location_factor',
            'experience_factor', 'skill_premiums', 'market_insights',
            'negotiation_tips', 'salary_growth_projection'
        ]
        
        for field in required_fields:
            self.assertIn(field, salary_result)
        
        # Validate salary ranges
        base_range = salary_result['base_salary_range']
        self.assertIn('min', base_range)
        self.assertIn('max', base_range)
        self.assertGreater(base_range['max'], base_range['min'])
        
        print(f"✅ Base Range: ${base_range['min']:,} - ${base_range['max']:,}")
        print(f"✅ Location Factor: {salary_result['location_factor']}")
        print(f"✅ Market Insights: {len(salary_result['market_insights'])} insights")

    def test_integration_workflow(self):
        """Test complete integration workflow with all features."""
        print("\n=== Testing Complete Integration Workflow ===")
        
        # Step 1: Parse resume
        resume_data = self.resume_parser.parse_resume(text_content=self.sample_resume)
        self.assertIsNotNone(resume_data)
        
        # Step 2: Process job description
        jd_data = self.jd_processor.process_jd(self.sample_jd)
        self.assertIsNotNone(jd_data)
        
        # Step 3: Enhanced matching
        match_data = self.matcher.match_resume_to_jd(resume_data, jd_data)
        self.assertIsNotNone(match_data)
        
        # Step 4: Advanced recommendations
        recommendations = self.recommender.build_recommendations(resume_data, jd_data, match_data)
        self.assertIsNotNone(recommendations)
        
        # Step 5: Resume scoring
        resume_text = str(resume_data)
        scoring_result = self.resume_parser.calculate_intelligent_resume_score(resume_text)
        self.assertIn('overall_score', scoring_result)
        
        # Step 6: Career analysis
        career_skills = resume_data.get('resume_skills', {}).get('all_skills', [])
        career_analysis = self.career_analyzer.analyze_career_progression(
            'software_engineer', 'senior_software_engineer', career_skills, 3
        )
        self.assertIn('feasibility_score', career_analysis)
        
        # Step 7: Industry insights
        industry_insights = self.jd_processor.analyze_industry_insights(self.sample_jd)
        self.assertIn('primary_industry', industry_insights)
        
        print("✅ Complete workflow executed successfully!")
        print(f"✅ Match Score: {match_data.get('match_score_overall', 0)}/100")
        print(f"✅ Resume Score: {scoring_result['overall_score']}/100")
        print(f"✅ Career Feasibility: {career_analysis['feasibility_score']}/100")
        print(f"✅ Industry: {industry_insights['primary_industry']}")

    def run_all_tests(self):
        """Run all tests and generate comprehensive report."""
        print("🚀 Starting Comprehensive AI Features Test Suite")
        print("=" * 60)
        
        test_methods = [
            self.test_intelligent_resume_scoring,
            self.test_ats_compatibility_analysis,
            self.test_industry_insights_analysis,
            self.test_job_difficulty_assessment,
            self.test_benefits_package_analysis,
            self.test_career_progression_analysis,
            self.test_skill_gap_analysis,
            self.test_market_positioning_analysis,
            self.test_interview_strategy_generation,
            self.test_networking_strategy_generation,
            self.test_enhanced_salary_estimation,
            self.test_integration_workflow
        ]
        
        passed = 0
        failed = 0
        
        for test_method in test_methods:
            try:
                test_method()
                passed += 1
                print(f"✅ {test_method.__name__} PASSED")
            except Exception as e:
                failed += 1
                print(f"❌ {test_method.__name__} FAILED: {str(e)}")
        
        print("\n" + "=" * 60)
        print("🎯 TEST SUITE SUMMARY")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📊 Success Rate: {(passed / (passed + failed)) * 100:.1f}%")
        
        if failed == 0:
            print("🎉 ALL TESTS PASSED! Advanced AI features are working correctly.")
        else:
            print("⚠️ Some tests failed. Please review the errors above.")


def main():
    """Main function to run comprehensive tests."""
    tester = TestAdvancedAIFeatures()
    tester.setUp()
    tester.run_all_tests()


if __name__ == "__main__":
    main()