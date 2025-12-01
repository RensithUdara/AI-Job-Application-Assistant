"""
Advanced Career Path Analyzer
Provides intelligent career progression insights, skill gap analysis, and personalized roadmaps.
"""

import json
import re
from typing import Dict, List, Tuple
from datetime import datetime, timedelta


class CareerAnalyzer:
    """Advanced career path and skill gap analysis."""
    
    def __init__(self):
        """Initialize with enhanced data sources."""
        # Load market trends and salary data
        try:
            with open('data/market_trends.json', 'r', encoding='utf-8') as f:
                self.market_trends = json.load(f)
            with open('data/salary_data.json', 'r', encoding='utf-8') as f:
                self.salary_data = json.load(f)
            with open('data/skills_taxonomy.json', 'r', encoding='utf-8') as f:
                self.skills_taxonomy = json.load(f)
        except FileNotFoundError:
            self.market_trends = {}
            self.salary_data = {}
            self.skills_taxonomy = {}
    
    def analyze_career_progression(self, current_role: str, target_role: str, 
                                 current_skills: List[str], experience_years: int) -> Dict:
        """Analyze career progression path from current to target role."""
        
        progression_analysis = {
            'feasibility_score': 0,
            'progression_timeline': '',
            'required_skills': [],
            'skill_gaps': [],
            'intermediate_roles': [],
            'learning_path': [],
            'salary_progression': {},
            'market_demand': {},
            'success_factors': []
        }
        
        # Define career progression paths
        career_paths = {
            'junior_developer': {
                'next_roles': ['software_engineer', 'web_developer', 'mobile_developer'],
                'timeline': '1-2 years',
                'key_skills': ['programming fundamentals', 'version control', 'testing']
            },
            'software_engineer': {
                'next_roles': ['senior_software_engineer', 'tech_lead', 'full_stack_developer'],
                'timeline': '2-3 years',
                'key_skills': ['system design', 'leadership', 'architecture']
            },
            'senior_software_engineer': {
                'next_roles': ['staff_engineer', 'engineering_manager', 'solution_architect'],
                'timeline': '3-5 years',
                'key_skills': ['technical leadership', 'mentoring', 'cross-team collaboration']
            },
            'web_developer': {
                'next_roles': ['senior_web_developer', 'full_stack_developer', 'frontend_architect'],
                'timeline': '2-3 years',
                'key_skills': ['advanced frameworks', 'performance optimization', 'user experience']
            },
            'data_analyst': {
                'next_roles': ['senior_data_analyst', 'data_scientist', 'business_intelligence_analyst'],
                'timeline': '2-4 years',
                'key_skills': ['machine learning', 'advanced statistics', 'data engineering']
            }
        }
        
        # Calculate feasibility score
        feasibility_factors = []
        score = 50  # Base score
        
        # Experience factor
        if experience_years >= 3:
            score += 20
            feasibility_factors.append('Sufficient experience for mid-level transition')
        elif experience_years >= 1:
            score += 10
            feasibility_factors.append('Some experience to build upon')
        
        # Current role alignment
        current_path = career_paths.get(current_role, {})
        if target_role in current_path.get('next_roles', []):
            score += 25
            feasibility_factors.append('Direct progression path available')
            progression_analysis['progression_timeline'] = current_path.get('timeline', '2-3 years')
        else:
            # Check if it's a 2-step progression
            for intermediate in current_path.get('next_roles', []):
                intermediate_path = career_paths.get(intermediate, {})
                if target_role in intermediate_path.get('next_roles', []):
                    score += 15
                    progression_analysis['intermediate_roles'].append(intermediate)
                    feasibility_factors.append('2-step progression path identified')
                    progression_analysis['progression_timeline'] = '3-5 years'
                    break
        
        # Skill alignment analysis
        target_skills = self._get_role_required_skills(target_role)
        skill_overlap = set(current_skills).intersection(set(target_skills))
        skill_match_ratio = len(skill_overlap) / len(target_skills) if target_skills else 0
        
        score += int(skill_match_ratio * 20)
        if skill_match_ratio >= 0.7:
            feasibility_factors.append('Strong skill alignment with target role')
        elif skill_match_ratio >= 0.4:
            feasibility_factors.append('Moderate skill alignment - some gaps to fill')
        else:
            feasibility_factors.append('Significant skill development needed')
        
        progression_analysis['feasibility_score'] = min(100, score)
        progression_analysis['success_factors'] = feasibility_factors
        
        # Identify skill gaps
        missing_skills = set(target_skills) - set(current_skills)
        progression_analysis['skill_gaps'] = list(missing_skills)
        progression_analysis['required_skills'] = target_skills
        
        # Generate learning path
        progression_analysis['learning_path'] = self._generate_learning_path(
            missing_skills, target_role, experience_years
        )
        
        # Salary progression analysis
        progression_analysis['salary_progression'] = self._analyze_salary_progression(
            current_role, target_role, experience_years
        )
        
        # Market demand analysis
        progression_analysis['market_demand'] = self._analyze_market_demand(target_role)
        
        return progression_analysis
    
    def _get_role_required_skills(self, role: str) -> List[str]:
        """Get required skills for a specific role."""
        role_skills_mapping = {
            'software_engineer': [
                'programming', 'algorithms', 'data structures', 'version control',
                'testing', 'debugging', 'system design', 'databases'
            ],
            'senior_software_engineer': [
                'advanced programming', 'system architecture', 'technical leadership',
                'code review', 'mentoring', 'project management', 'performance optimization'
            ],
            'web_developer': [
                'html', 'css', 'javascript', 'responsive design', 'frontend frameworks',
                'backend development', 'api integration', 'web security'
            ],
            'data_scientist': [
                'python', 'machine learning', 'statistics', 'data visualization',
                'sql', 'big data', 'deep learning', 'research methodology'
            ],
            'devops_engineer': [
                'ci/cd', 'containerization', 'cloud platforms', 'infrastructure as code',
                'monitoring', 'security', 'automation', 'linux'
            ],
            'mobile_developer': [
                'mobile frameworks', 'native development', 'cross-platform',
                'mobile ui/ux', 'app store deployment', 'mobile security'
            ]
        }
        return role_skills_mapping.get(role, [])
    
    def _generate_learning_path(self, missing_skills: set, target_role: str, experience_years: int) -> List[Dict]:
        """Generate a structured learning path for skill gaps."""
        learning_path = []
        
        # Prioritize skills based on role requirements
        skill_priorities = {
            'high': ['programming', 'system design', 'algorithms', 'leadership'],
            'medium': ['testing', 'databases', 'security', 'cloud'],
            'low': ['soft skills', 'documentation', 'project management']
        }
        
        # Categorize missing skills by priority
        high_priority = [skill for skill in missing_skills 
                        if any(hp in skill.lower() for hp in skill_priorities['high'])]
        medium_priority = [skill for skill in missing_skills 
                          if any(mp in skill.lower() for mp in skill_priorities['medium'])]
        low_priority = [skill for skill in missing_skills 
                       if skill not in high_priority and skill not in medium_priority]
        
        # Create phased learning plan
        phases = [
            {
                'phase': 'Phase 1 (Months 1-3)',
                'focus': 'Foundation Skills',
                'skills': high_priority[:3],
                'resources': ['Online courses', 'Books', 'Practice projects'],
                'timeline': '3 months',
                'success_metrics': ['Complete 2-3 projects', 'Pass certification if available']
            },
            {
                'phase': 'Phase 2 (Months 4-6)',
                'focus': 'Intermediate Skills',
                'skills': medium_priority[:3] + high_priority[3:],
                'resources': ['Advanced courses', 'Open source contributions', 'Mentorship'],
                'timeline': '3 months',
                'success_metrics': ['Contribute to open source', 'Build portfolio project']
            },
            {
                'phase': 'Phase 3 (Months 7-9)',
                'focus': 'Advanced & Specialized Skills',
                'skills': low_priority + medium_priority[3:],
                'resources': ['Conferences', 'Networking', 'Real-world projects'],
                'timeline': '3 months',
                'success_metrics': ['Industry recognition', 'Job applications ready']
            }
        ]
        
        return phases
    
    def _analyze_salary_progression(self, current_role: str, target_role: str, experience_years: int) -> Dict:
        """Analyze salary progression potential."""
        progression = {
            'current_estimated_salary': 0,
            'target_estimated_salary': 0,
            'potential_increase': 0,
            'roi_timeline': '',
            'factors_affecting_salary': []
        }
        
        # Get salary data
        base_salaries = self.salary_data.get('base_salaries', {})
        
        # Determine experience level
        exp_level = 'entry' if experience_years < 2 else 'mid' if experience_years < 5 else 'senior'
        
        # Current role salary
        current_salary_data = base_salaries.get(current_role, {})
        progression['current_estimated_salary'] = current_salary_data.get(exp_level, 70000)
        
        # Target role salary (assuming progression means higher level)
        target_exp_level = 'mid' if exp_level == 'entry' else 'senior'
        target_salary_data = base_salaries.get(target_role, {})
        progression['target_estimated_salary'] = target_salary_data.get(target_exp_level, 90000)
        
        # Calculate increase
        increase = progression['target_estimated_salary'] - progression['current_estimated_salary']
        progression['potential_increase'] = increase
        progression['percentage_increase'] = round((increase / progression['current_estimated_salary']) * 100, 1)
        
        # ROI timeline
        if increase > 0:
            if increase >= 30000:
                progression['roi_timeline'] = 'High ROI - 6-12 months payback period'
            elif increase >= 15000:
                progression['roi_timeline'] = 'Good ROI - 12-18 months payback period'
            else:
                progression['roi_timeline'] = 'Moderate ROI - 18-24 months payback period'
        
        # Factors affecting salary
        progression['factors_affecting_salary'] = [
            'Geographic location and cost of living',
            'Company size and industry sector',
            'Technical skill depth and breadth',
            'Leadership and communication skills',
            'Market demand for the role',
            'Economic conditions and hiring trends'
        ]
        
        return progression
    
    def _analyze_market_demand(self, role: str) -> Dict:
        """Analyze market demand for target role."""
        # Use market trends data
        hot_skills = self.market_trends.get('hot_skills_2024', [])
        job_market = self.market_trends.get('job_market_predictions_2025', {})
        
        demand_analysis = {
            'demand_level': 'Moderate',
            'growth_trend': 'Stable',
            'competition_level': 'Medium',
            'market_factors': [],
            'demand_score': 50
        }
        
        # Role-specific demand analysis
        role_demand_mapping = {
            'software_engineer': {'demand': 'Very High', 'growth': 'Strong', 'competition': 'High'},
            'data_scientist': {'demand': 'High', 'growth': 'Very Strong', 'competition': 'Very High'},
            'devops_engineer': {'demand': 'Very High', 'growth': 'Strong', 'competition': 'Medium'},
            'web_developer': {'demand': 'High', 'growth': 'Moderate', 'competition': 'High'},
            'mobile_developer': {'demand': 'High', 'growth': 'Moderate', 'competition': 'Medium'}
        }
        
        role_info = role_demand_mapping.get(role, {})
        demand_analysis.update(role_info)
        
        # Calculate demand score
        demand_scores = {'Very High': 90, 'High': 75, 'Moderate': 50, 'Low': 25}
        demand_analysis['demand_score'] = demand_scores.get(role_info.get('demand', 'Moderate'), 50)
        
        # Market factors
        if role in ['ai_engineer', 'machine_learning_engineer', 'data_scientist']:
            demand_analysis['market_factors'].append('AI/ML boom driving high demand')
        if role in ['devops_engineer', 'cloud_engineer']:
            demand_analysis['market_factors'].append('Cloud adoption increasing opportunities')
        if role in ['cybersecurity_analyst', 'security_engineer']:
            demand_analysis['market_factors'].append('Rising cybersecurity concerns')
        
        return demand_analysis
    
    def generate_skill_gap_report(self, current_skills: List[str], target_role: str, 
                                industry: str = 'technology') -> Dict:
        """Generate comprehensive skill gap analysis report."""
        
        report = {
            'gap_analysis_summary': {},
            'critical_gaps': [],
            'nice_to_have_gaps': [],
            'skill_development_priority': [],
            'learning_resources': {},
            'timeline_estimate': '',
            'cost_estimate': {},
            'progress_tracking': {}
        }
        
        # Get required skills for target role
        required_skills = self._get_role_required_skills(target_role)
        current_skills_lower = [skill.lower() for skill in current_skills]
        
        # Identify gaps
        all_gaps = []
        critical_gaps = []
        nice_to_have_gaps = []
        
        for required_skill in required_skills:
            if not any(req_skill in curr_skill for curr_skill in current_skills_lower 
                      for req_skill in required_skill.lower().split()):
                all_gaps.append(required_skill)
                
                # Categorize as critical or nice-to-have
                if required_skill in ['programming', 'system design', 'algorithms', 'databases']:
                    critical_gaps.append(required_skill)
                else:
                    nice_to_have_gaps.append(required_skill)
        
        report['critical_gaps'] = critical_gaps
        report['nice_to_have_gaps'] = nice_to_have_gaps
        
        # Gap analysis summary
        total_required = len(required_skills)
        total_gaps = len(all_gaps)
        skill_coverage = ((total_required - total_gaps) / total_required) * 100 if total_required > 0 else 0
        
        report['gap_analysis_summary'] = {
            'total_required_skills': total_required,
            'total_skill_gaps': total_gaps,
            'skill_coverage_percentage': round(skill_coverage, 1),
            'readiness_level': 'High' if skill_coverage >= 80 else 'Medium' if skill_coverage >= 60 else 'Low',
            'estimated_preparation_time': self._estimate_preparation_time(total_gaps, critical_gaps)
        }
        
        # Skill development priority
        report['skill_development_priority'] = self._prioritize_skill_development(
            critical_gaps, nice_to_have_gaps, target_role
        )
        
        # Learning resources
        report['learning_resources'] = self._recommend_learning_resources(all_gaps)
        
        # Timeline and cost estimates
        report['timeline_estimate'] = self._estimate_learning_timeline(all_gaps)
        report['cost_estimate'] = self._estimate_learning_costs(all_gaps)
        
        # Progress tracking framework
        report['progress_tracking'] = self._create_progress_tracking_framework(all_gaps)
        
        return report
    
    def _estimate_preparation_time(self, total_gaps: int, critical_gaps: List[str]) -> str:
        """Estimate time needed to fill skill gaps."""
        if total_gaps <= 2:
            return '1-3 months'
        elif total_gaps <= 4:
            return '3-6 months'
        elif total_gaps <= 6:
            return '6-9 months'
        else:
            return '9-12 months'
    
    def _prioritize_skill_development(self, critical_gaps: List[str], 
                                   nice_to_have_gaps: List[str], target_role: str) -> List[Dict]:
        """Prioritize skills based on importance and learning difficulty."""
        priorities = []
        
        # Priority 1: Critical gaps (must-have)
        for skill in critical_gaps:
            priorities.append({
                'skill': skill,
                'priority': 'High',
                'category': 'Critical',
                'learning_difficulty': self._assess_learning_difficulty(skill),
                'market_demand': self._assess_skill_market_demand(skill),
                'recommended_timeline': self._get_skill_learning_timeline(skill)
            })
        
        # Priority 2: Nice-to-have gaps
        for skill in nice_to_have_gaps:
            priorities.append({
                'skill': skill,
                'priority': 'Medium',
                'category': 'Enhancement',
                'learning_difficulty': self._assess_learning_difficulty(skill),
                'market_demand': self._assess_skill_market_demand(skill),
                'recommended_timeline': self._get_skill_learning_timeline(skill)
            })
        
        return priorities
    
    def _assess_learning_difficulty(self, skill: str) -> str:
        """Assess the learning difficulty of a skill."""
        difficulty_mapping = {
            'algorithms': 'Hard',
            'system design': 'Hard',
            'machine learning': 'Hard',
            'programming': 'Medium',
            'databases': 'Medium',
            'testing': 'Easy',
            'version control': 'Easy',
            'documentation': 'Easy'
        }
        
        for key, difficulty in difficulty_mapping.items():
            if key in skill.lower():
                return difficulty
        return 'Medium'
    
    def _assess_skill_market_demand(self, skill: str) -> str:
        """Assess market demand for a specific skill."""
        # Use market trends data if available
        hot_skills = [s.get('skill', '').lower() for s in self.market_trends.get('hot_skills_2024', [])]
        
        if any(hot_skill in skill.lower() for hot_skill in hot_skills):
            return 'Very High'
        
        high_demand_skills = ['python', 'javascript', 'react', 'aws', 'docker', 'kubernetes']
        if any(hd_skill in skill.lower() for hd_skill in high_demand_skills):
            return 'High'
        
        return 'Medium'
    
    def _get_skill_learning_timeline(self, skill: str) -> str:
        """Get recommended learning timeline for a skill."""
        timeline_mapping = {
            'programming': '2-4 months',
            'algorithms': '3-6 months',
            'system design': '4-8 months',
            'databases': '1-3 months',
            'testing': '2-4 weeks',
            'version control': '1-2 weeks',
            'machine learning': '6-12 months'
        }
        
        for key, timeline in timeline_mapping.items():
            if key in skill.lower():
                return timeline
        return '1-2 months'
    
    def _recommend_learning_resources(self, skills: List[str]) -> Dict:
        """Recommend learning resources for skill gaps."""
        resources = {
            'online_courses': [],
            'books': [],
            'practice_platforms': [],
            'certifications': [],
            'projects': []
        }
        
        # Generic recommendations
        resources['online_courses'] = [
            'Coursera - Role-specific specializations',
            'Udemy - Practical skill courses',
            'Pluralsight - Technology training',
            'edX - University-level courses'
        ]
        
        resources['practice_platforms'] = [
            'LeetCode - Algorithm practice',
            'HackerRank - Programming challenges',
            'Codecademy - Interactive learning',
            'FreeCodeCamp - Full-stack development'
        ]
        
        resources['certifications'] = [
            'AWS Certified Solutions Architect',
            'Google Cloud Professional',
            'Microsoft Azure Fundamentals',
            'CompTIA Security+'
        ]
        
        resources['projects'] = [
            'Build a portfolio website',
            'Create a full-stack application',
            'Contribute to open source projects',
            'Complete coding bootcamp projects'
        ]
        
        return resources
    
    def _estimate_learning_timeline(self, gaps: List[str]) -> str:
        """Estimate overall learning timeline."""
        if len(gaps) <= 2:
            return '2-4 months with dedicated study (10-15 hours/week)'
        elif len(gaps) <= 4:
            return '4-6 months with dedicated study (15-20 hours/week)'
        else:
            return '6-12 months with dedicated study (20+ hours/week)'
    
    def _estimate_learning_costs(self, gaps: List[str]) -> Dict:
        """Estimate costs for learning resources."""
        return {
            'online_courses': f'${200 * len(gaps)}-{400 * len(gaps)}',
            'books_resources': f'${50 * len(gaps)}-{100 * len(gaps)}',
            'certification_exams': '$150-$300 per certification',
            'total_estimated_range': f'${300 * len(gaps)}-{800 * len(gaps)}',
            'cost_saving_tips': [
                'Look for free alternatives (YouTube, free courses)',
                'Use company learning budgets',
                'Join study groups for shared resources',
                'Apply for scholarships or discounts'
            ]
        }
    
    def _create_progress_tracking_framework(self, gaps: List[str]) -> Dict:
        """Create a framework for tracking learning progress."""
        return {
            'milestones': [
                {'week': 2, 'goal': 'Complete foundational learning for 1-2 skills'},
                {'week': 6, 'goal': 'Build first practice project'},
                {'week': 10, 'goal': 'Complete intermediate level for priority skills'},
                {'week': 16, 'goal': 'Portfolio project completed'},
                {'week': 20, 'goal': 'Ready for job applications'}
            ],
            'success_metrics': [
                'Complete weekly learning goals',
                'Build practical projects demonstrating skills',
                'Pass practice assessments/quizzes',
                'Receive positive feedback on code reviews',
                'Successfully complete certification exams'
            ],
            'tracking_tools': [
                'Learning journal or blog',
                'GitHub repository for projects',
                'Skill assessment tools',
                'Peer review and feedback',
                'Regular self-assessment quizzes'
            ]
        }