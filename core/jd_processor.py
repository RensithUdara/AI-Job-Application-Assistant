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
        
        # Seniority level indicators
        self.seniority_keywords = {
            'intern': ['intern', 'internship', 'student', 'entry-level', 'graduate'],
            'junior': ['junior', 'associate', 'entry-level', '0-2 years', 'new grad'],
            'mid': ['mid-level', '2-5 years', '3-7 years', 'experienced', 'professional'],
            'senior': ['senior', '5+ years', '7+ years', 'lead', 'principal', 'expert'],
            'lead': ['lead', 'manager', 'director', 'head', 'chief', '10+ years']
        }
    
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
    
    def classify_seniority_level(self, jd_text: str) -> Dict:
        """Advanced seniority level classification with confidence scoring."""
        text_lower = jd_text.lower()
        seniority_scores = {}
        
        # Score each seniority level based on keyword presence
        for level, keywords in self.seniority_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            seniority_scores[level] = score
        
        # Extract years of experience mentioned
        experience_years = self._extract_years_experience(text_lower)
        
        # Determine primary seniority level
        if seniority_scores:
            primary_level = max(seniority_scores, key=seniority_scores.get)
            confidence = seniority_scores[primary_level] / max(1, sum(seniority_scores.values()))
        else:
            primary_level = 'mid'  # Default
            confidence = 0.5
        
        # Adjust based on experience years
        if experience_years:
            if min(experience_years) == 0:
                primary_level = 'junior'
            elif max(experience_years) >= 7:
                primary_level = 'senior'
            elif max(experience_years) >= 3:
                primary_level = 'mid'
        
        return {
            'primary_level': primary_level,
            'confidence_score': round(confidence, 2),
            'seniority_scores': seniority_scores,
            'experience_years_mentioned': experience_years,
            'level_description': self._get_seniority_description(primary_level)
        }
    
    def _extract_years_experience(self, text: str) -> List[int]:
        """Extract years of experience mentioned in job description."""
        # Pattern to match years of experience
        patterns = [
            r'(\d+)[\-\+]*\s*years?\s*(?:of\s*)?experience',
            r'(\d+)[\-\+]*\s*yrs?\s*(?:of\s*)?experience',
            r'(\d+)[\-\+]*\s*years?\s*in',
            r'minimum\s*(\d+)\s*years?',
            r'at least\s*(\d+)\s*years?'
        ]
        
        years = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            years.extend([int(match) for match in matches])
        
        return sorted(list(set(years)))
    
    def _get_seniority_description(self, level: str) -> str:
        """Get description for seniority level."""
        descriptions = {
            'intern': 'Internship or student position with learning focus',
            'junior': 'Entry-level position requiring 0-2 years experience',
            'mid': 'Mid-level position requiring 3-5 years experience',
            'senior': 'Senior position requiring 5+ years experience and leadership skills',
            'lead': 'Leadership position requiring 7+ years and team management experience'
        }
        return descriptions.get(level, 'Professional position')
    
    def estimate_job_difficulty(self, jd_text: str, skills_required: List[str]) -> Dict:
        """Estimate job difficulty based on multiple factors."""
        text_lower = jd_text.lower()
        difficulty_score = 0
        factors = {}
        
        # Factor 1: Number of required skills (0-25 points)
        skill_count = len(skills_required)
        skill_difficulty = min(25, skill_count * 2)
        difficulty_score += skill_difficulty
        factors['skills_complexity'] = skill_difficulty
        
        # Factor 2: Advanced technology requirements (0-20 points)
        advanced_tech = ['machine learning', 'ai', 'blockchain', 'kubernetes', 'microservices', 'devops']
        advanced_count = sum(1 for tech in advanced_tech if tech in text_lower)
        tech_difficulty = min(20, advanced_count * 5)
        difficulty_score += tech_difficulty
        factors['technology_complexity'] = tech_difficulty
        
        # Factor 3: Leadership/management requirements (0-15 points)
        leadership_keywords = ['lead', 'manage', 'mentor', 'architect', 'design', 'strategy']
        leadership_count = sum(1 for keyword in leadership_keywords if keyword in text_lower)
        leadership_difficulty = min(15, leadership_count * 3)
        difficulty_score += leadership_difficulty
        factors['leadership_requirements'] = leadership_difficulty
        
        # Factor 4: Education/certification requirements (0-15 points)
        education_keywords = ['degree', 'certification', 'phd', 'masters', 'bachelor']
        education_count = sum(1 for keyword in education_keywords if keyword in text_lower)
        education_difficulty = min(15, education_count * 5)
        difficulty_score += education_difficulty
        factors['education_requirements'] = education_difficulty
        
        # Factor 5: Multi-domain expertise (0-10 points)
        domains = ['frontend', 'backend', 'database', 'mobile', 'cloud', 'security']
        domain_count = sum(1 for domain in domains if domain in text_lower)
        domain_difficulty = min(10, domain_count * 2)
        difficulty_score += domain_difficulty
        factors['domain_breadth'] = domain_difficulty
        
        # Factor 6: Experience level (0-15 points) 
        years_mentioned = self._extract_years_experience(text_lower)
        if years_mentioned:
            max_years = max(years_mentioned)
            experience_difficulty = min(15, max_years * 2)
        else:
            experience_difficulty = 5  # Default moderate
        difficulty_score += experience_difficulty
        factors['experience_level'] = experience_difficulty
        
        # Normalize to 0-100 scale
        normalized_score = min(100, difficulty_score)
        
        return {
            'difficulty_score': normalized_score,
            'difficulty_level': self._get_difficulty_level(normalized_score),
            'breakdown': factors,
            'recommendations': self._get_difficulty_recommendations(normalized_score)
        }
    
    def _get_difficulty_level(self, score: int) -> str:
        """Convert difficulty score to level description."""
        if score >= 80:
            return "Very High - Expert level position"
        elif score >= 65:
            return "High - Advanced professional role"
        elif score >= 45:
            return "Moderate - Mid-level professional role"
        elif score >= 25:
            return "Low-Moderate - Junior to mid-level role"
        else:
            return "Low - Entry-level or simple role"
    
    def _get_difficulty_recommendations(self, score: int) -> List[str]:
        """Generate recommendations based on difficulty score."""
        recommendations = []
        
        if score >= 80:
            recommendations.extend([
                "This is a very challenging role requiring extensive experience",
                "Consider applying only if you meet 80%+ of requirements",
                "Focus on highlighting leadership and advanced technical skills"
            ])
        elif score >= 65:
            recommendations.extend([
                "This role requires strong technical expertise",
                "Ensure you have most of the listed technical skills",
                "Prepare for technical interviews and coding challenges"
            ])
        elif score >= 45:
            recommendations.extend([
                "Moderate difficulty role suitable for mid-level professionals",
                "Focus on demonstrating relevant project experience",
                "Good opportunity for career growth"
            ])
        else:
            recommendations.extend([
                "Entry to mid-level role, good for career development",
                "Focus on willingness to learn and adapt",
                "Highlight relevant coursework and projects"
            ])
        
        return recommendations
    
    def analyze_must_have_vs_nice_to_have(self, jd_text: str, skills_found: List[str]) -> Dict:
        """Advanced skill categorization using NLP patterns."""
        text_lower = jd_text.lower()
        
        # Patterns that indicate must-have requirements
        must_have_patterns = [
            r'required?[:\s]*([^.]*)',
            r'must have[:\s]*([^.]*)', 
            r'essential[:\s]*([^.]*)',
            r'minimum requirements?[:\s]*([^.]*)',
            r'qualifications?[:\s]*([^.]*)'
        ]
        
        # Patterns that indicate nice-to-have requirements
        nice_to_have_patterns = [
            r'preferred?[:\s]*([^.]*)',
            r'nice to have[:\s]*([^.]*)',
            r'bonus[:\s]*([^.]*)',
            r'additional[:\s]*([^.]*)',
            r'plus[:\s]*([^.]*)',
            r'would be great[:\s]*([^.]*)'
        ]
        
        must_have_skills = []
        nice_to_have_skills = []
        
        # Extract must-have skills
        for pattern in must_have_patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                text_section = match.group(1)
                section_skills = [skill for skill in skills_found if skill.lower() in text_section]
                must_have_skills.extend(section_skills)
        
        # Extract nice-to-have skills
        for pattern in nice_to_have_patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                text_section = match.group(1)
                section_skills = [skill for skill in skills_found if skill.lower() in text_section]
                nice_to_have_skills.extend(section_skills)
        
        # Remove duplicates and classify remaining skills
        must_have_skills = list(set(must_have_skills))
        nice_to_have_skills = list(set(nice_to_have_skills))
        
        # Skills not explicitly categorized - use position in text as heuristic
        unclassified_skills = [skill for skill in skills_found 
                              if skill not in must_have_skills and skill not in nice_to_have_skills]
        
        # Heuristic: skills mentioned early are more likely to be must-have
        text_parts = text_lower.split()
        early_text = ' '.join(text_parts[:len(text_parts)//2])  # First half
        
        for skill in unclassified_skills:
            if skill.lower() in early_text:
                must_have_skills.append(skill)
            else:
                nice_to_have_skills.append(skill)
        
        return {
            'must_have_skills': list(set(must_have_skills)),
            'nice_to_have_skills': list(set(nice_to_have_skills)),
            'must_have_count': len(set(must_have_skills)),
            'nice_to_have_count': len(set(nice_to_have_skills)),
            'classification_confidence': self._calculate_classification_confidence(
                must_have_skills, nice_to_have_skills, skills_found
            )
        }
    
    def _calculate_classification_confidence(self, must_have: List[str], 
                                          nice_to_have: List[str], all_skills: List[str]) -> float:
        """Calculate confidence in skill classification."""
        classified_count = len(set(must_have + nice_to_have))
        total_count = len(all_skills)
        
        if total_count == 0:
            return 0.0
        
        return round(classified_count / total_count, 2)