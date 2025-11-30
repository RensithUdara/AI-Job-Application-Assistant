import re
import json
from typing import Dict, List, Set, Optional
try:
    from fuzzywuzzy import fuzz
except ImportError:
    # Fallback for basic string matching
    class MockFuzz:
        @staticmethod
        def ratio(s1, s2):
            return 100 if s1 == s2 else 0
    fuzz = MockFuzz()
from collections import Counter

class JobDescriptionProcessor:
    def __init__(self, skills_taxonomy_path: str = "data/skills_taxonomy.json", 
                 job_templates_path: str = "data/job_templates.json"):
        """Initialize the job description processor."""
        with open(skills_taxonomy_path, 'r', encoding='utf-8') as f:
            self.skills_taxonomy = json.load(f)
        
        with open(job_templates_path, 'r', encoding='utf-8') as f:
            self.job_templates = json.load(f)
        
        # Flatten skills for easier searching
        self.all_skills = set()
        for category, skills in self.skills_taxonomy.items():
            self.all_skills.update([skill.lower() for skill in skills])
    
    def process_jd(self, jd_text: str) -> Dict:
        """Process job description and extract relevant information."""
        try:
            # Clean and normalize text
            cleaned_text = self._clean_text(jd_text)
            
            # Extract skills
            jd_skills = self._extract_skills(cleaned_text)
            
            # Classify job role
            jd_role = self._classify_job_role(cleaned_text)
            
            # Extract experience requirements
            experience_info = self._extract_experience_requirements(cleaned_text)
            
            # Categorize skills as must-have vs nice-to-have
            skill_categories = self._categorize_skills(jd_role, jd_skills)
            
            # Additional analytics
            salary_info = self._extract_salary_info(cleaned_text)
            company_info = self._extract_company_info(jd_text)
            job_requirements = self._analyze_job_requirements(cleaned_text)
            
            return {
                'jd_text': jd_text,
                'cleaned_text': cleaned_text,
                'jd_role': jd_role,
                'jd_skills': jd_skills,
                'required_experience': experience_info['experience_range'],
                'seniority': experience_info['seniority'],
                'critical_skills': skill_categories['critical_skills'],
                'bonus_skills': skill_categories['bonus_skills'],
                'all_jd_skills_list': list(jd_skills['all_skills']),
                'salary_info': salary_info,
                'company_info': company_info,
                'job_requirements': job_requirements,
                'word_count': len(jd_text.split())
            }
        
        except Exception as e:
            return {
                'error': str(e),
                'jd_role': 'unknown',
                'jd_skills': {'by_category': {}, 'all_skills': set()},
                'required_experience': 'Not specified',
                'seniority': 'Not specified',
                'critical_skills': [],
                'bonus_skills': [],
                'all_jd_skills_list': []
            }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize job description text."""
        # Convert to lowercase for processing
        text = text.lower()
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep important ones
        text = re.sub(r'[^\w\s@.\-+():]', ' ', text)
        return text.strip()
    
    def _extract_skills(self, text: str) -> Dict:
        """Extract skills from job description text."""
        jd_skills = {
            'by_category': {},
            'all_skills': set(),
            'skill_frequency': {}
        }
        
        for category, skills in self.skills_taxonomy.items():
            found_skills = []
            
            for skill in skills:
                skill_lower = skill.lower()
                # Count occurrences
                skill_count = 0
                
                # Exact match
                if skill_lower in text:
                    skill_count = text.count(skill_lower)
                    found_skills.append(skill)
                    jd_skills['all_skills'].add(skill_lower)
                    jd_skills['skill_frequency'][skill_lower] = skill_count
                else:
                    # Fuzzy match for compound skills
                    words_in_text = text.split()
                    for i, word in enumerate(words_in_text):
                        if len(word) > 2 and fuzz.ratio(skill_lower, word) > 85:
                            found_skills.append(skill)
                            jd_skills['all_skills'].add(skill_lower)
                            jd_skills['skill_frequency'][skill_lower] = 1
                            break
            
            if found_skills:
                jd_skills['by_category'][category] = found_skills
        
        return jd_skills
    
    def _classify_job_role(self, text: str) -> str:
        """Classify job role based on keywords in job description."""
        role_scores = {}
        
        for role, template in self.job_templates.items():
            score = 0
            for keyword in template['keywords']:
                keyword_lower = keyword.lower()
                if keyword_lower in text:
                    # Count occurrences and give higher weight to more mentions
                    occurrences = text.count(keyword_lower)
                    score += occurrences
            
            role_scores[role] = score
        
        # Return role with highest score
        if role_scores and max(role_scores.values()) > 0:
            return max(role_scores, key=role_scores.get)
        else:
            return 'general'  # Default if no clear match
    
    def _extract_experience_requirements(self, text: str) -> Dict:
        """Extract experience requirements and seniority level."""
        experience_info = {
            'experience_range': 'Not specified',
            'seniority': 'Not specified'
        }
        
        # Experience patterns
        exp_patterns = [
            r'(\d+)[\s\-]*(\d+)?\s*years?\s*(?:of\s*)?experience',
            r'minimum\s*(\d+)\s*years?',
            r'at\s*least\s*(\d+)\s*years?',
            r'(\d+)\+?\s*years?',
            r'(\d+)\s*to\s*(\d+)\s*years?'
        ]
        
        for pattern in exp_patterns:
            matches = re.findall(pattern, text)
            if matches:
                if isinstance(matches[0], tuple) and len(matches[0]) == 2 and matches[0][1]:
                    # Range found (e.g., "2-4 years")
                    experience_info['experience_range'] = f"{matches[0][0]}-{matches[0][1]} years"
                else:
                    # Single number found
                    num = matches[0][0] if isinstance(matches[0], tuple) else matches[0]
                    experience_info['experience_range'] = f"{num}+ years"
                break
        
        # Determine seniority based on keywords and experience
        seniority_keywords = {
            'intern': ['intern', 'internship', 'trainee'],
            'junior': ['junior', 'entry level', 'graduate', '0-2 years', 'fresher'],
            'mid': ['mid level', 'intermediate', '2-5 years', '3-6 years'],
            'senior': ['senior', 'lead', '5+ years', 'experienced'],
            'principal': ['principal', 'architect', 'director', 'head of', 'chief']
        }
        
        for level, keywords in seniority_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    experience_info['seniority'] = level.title()
                    break
            if experience_info['seniority'] != 'Not specified':
                break
        
        # Fallback: infer seniority from experience range
        if experience_info['seniority'] == 'Not specified' and experience_info['experience_range'] != 'Not specified':
            exp_text = experience_info['experience_range']
            if any(x in exp_text for x in ['0', '1']):
                experience_info['seniority'] = 'Junior'
            elif any(x in exp_text for x in ['2', '3', '4']):
                experience_info['seniority'] = 'Mid'
            elif any(x in exp_text for x in ['5', '6', '7', '8', '9']):
                experience_info['seniority'] = 'Senior'
        
        return experience_info
    
    def _categorize_skills(self, jd_role: str, jd_skills: Dict) -> Dict:
        """Categorize skills as critical (must-have) vs bonus (nice-to-have)."""
        skill_categories = {
            'critical_skills': [],
            'bonus_skills': []
        }
        
        if jd_role in self.job_templates:
            template = self.job_templates[jd_role]
            must_have_categories = template.get('must_have', [])
            nice_to_have_categories = template.get('nice_to_have', [])
            
            # Categorize skills based on their category
            for category, skills in jd_skills['by_category'].items():
                if category in must_have_categories:
                    skill_categories['critical_skills'].extend(skills)
                elif category in nice_to_have_categories:
                    skill_categories['bonus_skills'].extend(skills)
                else:
                    # Default: treat as bonus if not specified
                    skill_categories['bonus_skills'].extend(skills)
        else:
            # If role not recognized, treat all as bonus
            for skills in jd_skills['by_category'].values():
                skill_categories['bonus_skills'].extend(skills)
        
        return skill_categories
    
    def _extract_salary_info(self, text: str) -> Dict:
        """Extract salary information from job description."""
        salary_info = {
            'min_salary': None,
            'max_salary': None,
            'currency': 'USD',
            'salary_type': 'annual',
            'salary_mentioned': False
        }
        
        # Salary patterns
        salary_patterns = [
            r'\$([\d,]+)\s*[-–]\s*\$([\d,]+)',  # $70,000 - $85,000
            r'\$([\d,]+)k?\s*[-–]\s*([\d,]+)k',  # $70k - 85k
            r'salary.*\$([\d,]+)',  # salary: $75,000
            r'([\d,]+)\s*[-–]\s*([\d,]+)\s*thousand',  # 70 - 85 thousand
        ]
        
        for pattern in salary_patterns:
            matches = re.findall(pattern, text)
            if matches:
                try:
                    if len(matches[0]) == 2:
                        min_sal = int(matches[0][0].replace(',', ''))
                        max_sal = int(matches[0][1].replace(',', ''))
                        salary_info.update({
                            'min_salary': min_sal,
                            'max_salary': max_sal,
                            'salary_mentioned': True
                        })
                        break
                except (ValueError, IndexError):
                    continue
        
        return salary_info
    
    def _extract_company_info(self, text: str) -> Dict:
        """Extract company information from job description."""
        company_info = {
            'company_name': None,
            'location': None,
            'work_type': None,
            'company_size': None
        }
        
        # Extract company name (usually after "Company:")
        company_match = re.search(r'company:\s*([^\n]+)', text, re.IGNORECASE)
        if company_match:
            company_info['company_name'] = company_match.group(1).strip()
        
        # Extract location
        location_match = re.search(r'location:\s*([^\n]+)', text, re.IGNORECASE)
        if location_match:
            company_info['location'] = location_match.group(1).strip()
        
        # Determine work type
        if any(word in text.lower() for word in ['remote', 'work from home', 'wfh']):
            if any(word in text.lower() for word in ['hybrid', 'flexible']):
                company_info['work_type'] = 'Hybrid'
            else:
                company_info['work_type'] = 'Remote'
        elif any(word in text.lower() for word in ['on-site', 'office', 'onsite']):
            company_info['work_type'] = 'On-site'
        else:
            company_info['work_type'] = 'Not specified'
        
        return company_info
    
    def _analyze_job_requirements(self, text: str) -> Dict:
        """Analyze job requirements complexity and structure."""
        requirements = {
            'total_requirements': 0,
            'hard_requirements': 0,
            'soft_requirements': 0,
            'education_required': False,
            'certification_mentioned': False,
            'complexity_score': 0
        }
        
        # Count bullet points as requirements
        bullet_points = re.findall(r'[•·*-]\s*([^\n]+)', text)
        requirements['total_requirements'] = len(bullet_points)
        
        # Analyze requirement types
        hard_skill_keywords = ['experience', 'proficiency', 'knowledge of', 'understanding of', 'years']
        soft_skill_keywords = ['communication', 'teamwork', 'leadership', 'problem solving']
        
        for point in bullet_points:
            point_lower = point.lower()
            if any(keyword in point_lower for keyword in hard_skill_keywords):
                requirements['hard_requirements'] += 1
            if any(keyword in point_lower for keyword in soft_skill_keywords):
                requirements['soft_requirements'] += 1
        
        # Check for education and certification requirements
        if any(word in text.lower() for word in ['degree', 'bachelor', 'master', 'education']):
            requirements['education_required'] = True
        
        if any(word in text.lower() for word in ['certification', 'certified', 'license']):
            requirements['certification_mentioned'] = True
        
        # Calculate complexity score (0-100)
        complexity = 0
        complexity += min(requirements['total_requirements'] * 2, 40)  # Max 40 for total reqs
        complexity += min(requirements['hard_requirements'] * 3, 30)  # Max 30 for hard reqs
        if requirements['education_required']:
            complexity += 15
        if requirements['certification_mentioned']:
            complexity += 15
        
        requirements['complexity_score'] = min(complexity, 100)
        
        return requirements
    
    def get_industry_benchmarks(self, role: str, seniority: str) -> Dict:
        """Get industry benchmarks for role and seniority level."""
        # Industry benchmark data (simplified - in real app, this would come from API/database)
        benchmarks = {
            'web_developer': {
                'junior': {'avg_salary': 65000, 'common_skills': ['javascript', 'html', 'css', 'react']},
                'mid': {'avg_salary': 85000, 'common_skills': ['javascript', 'react', 'node.js', 'sql']},
                'senior': {'avg_salary': 110000, 'common_skills': ['javascript', 'react', 'node.js', 'aws', 'docker']}
            },
            'mobile_developer': {
                'junior': {'avg_salary': 70000, 'common_skills': ['java', 'kotlin', 'android', 'ios']},
                'mid': {'avg_salary': 90000, 'common_skills': ['flutter', 'react native', 'firebase', 'api']},
                'senior': {'avg_salary': 115000, 'common_skills': ['flutter', 'architecture', 'ci/cd', 'testing']}
            },
            'data_analyst': {
                'junior': {'avg_salary': 60000, 'common_skills': ['sql', 'excel', 'python', 'statistics']},
                'mid': {'avg_salary': 80000, 'common_skills': ['sql', 'python', 'tableau', 'machine learning']},
                'senior': {'avg_salary': 105000, 'common_skills': ['python', 'machine learning', 'aws', 'spark']}
            }
        }
        
        seniority_key = seniority.lower() if seniority != 'Not specified' else 'junior'
        if seniority_key not in ['junior', 'mid', 'senior']:
            seniority_key = 'junior'
        
        return benchmarks.get(role, benchmarks.get('web_developer', {})).get(seniority_key, {
            'avg_salary': 70000,
            'common_skills': ['programming', 'problem solving']
        })