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
            
            # Advanced analysis features
            red_flag_analysis = self.detect_job_red_flags(jd_text)
            interview_prediction = self.predict_interview_process(jd_text)
            keyword_ranking = self.rank_keyword_importance(jd_text)
            role_expansion = self.generate_role_expansion_summary(jd_text)
            
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
                'red_flag_analysis': red_flag_analysis,
                'interview_prediction': interview_prediction,
                'keyword_ranking': keyword_ranking,
                'role_expansion': role_expansion,
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
    
    def detect_job_red_flags(self, jd_text: str) -> Dict:
        """Detect potential warning signs in job descriptions."""
        text_lower = jd_text.lower()
        red_flags = []
        risk_score = 0
        
        # High pressure indicators
        pressure_keywords = [
            'high pressure', 'fast paced', 'tight deadline', 'aggressive timeline',
            'work under pressure', 'demanding environment', 'high stress'
        ]
        
        for keyword in pressure_keywords:
            if keyword in text_lower:
                red_flags.append(f'High pressure environment: "{keyword}"')
                risk_score += 15
        
        # Work-life balance concerns
        worklife_keywords = [
            'work weekends', 'overtime required', 'long hours', 'available 24/7',
            'on-call rotation', 'flexible schedule' # can be code for unpredictable hours
        ]
        
        for keyword in worklife_keywords:
            if keyword in text_lower:
                red_flags.append(f'Work-life balance concern: "{keyword}"')
                risk_score += 20
        
        # Compensation red flags
        compensation_flags = [
            'competitive salary', 'salary commensurate', 'based on experience',
            'equity in lieu', 'deferred compensation'
        ]
        
        for flag in compensation_flags:
            if flag in text_lower:
                red_flags.append(f'Vague compensation: "{flag}"')
                risk_score += 10
        
        # Unrealistic requirements
        if '5+ years' in text_lower and ('entry' in text_lower or 'junior' in text_lower):
            red_flags.append('Unrealistic experience requirements for level')
            risk_score += 25
        
        # Excessive requirements
        skill_count = len(self.all_skills.intersection(set(text_lower.split())))
        if skill_count > 15:
            red_flags.append(f'Excessive skill requirements ({skill_count} skills listed)')
            risk_score += 15
        
        # Determine risk level
        if risk_score >= 60:
            risk_level = 'High Risk - Proceed with caution'
        elif risk_score >= 30:
            risk_level = 'Moderate Risk - Ask detailed questions'
        elif risk_score >= 10:
            risk_level = 'Low Risk - Minor concerns'
        else:
            risk_level = 'Low Risk - Good opportunity'
        
        return {
            'red_flags': red_flags,
            'risk_score': min(100, risk_score),
            'risk_level': risk_level,
            'recommendation': self._get_risk_recommendation(risk_score),
            'questions_to_ask': self._generate_clarifying_questions(red_flags)
        }
    
    def _get_risk_recommendation(self, score: int) -> str:
        """Generate recommendation based on risk score."""
        if score >= 60:
            return "High risk job. Research company culture thoroughly before applying."
        elif score >= 30:
            return "Some concerns present. Prepare specific questions for interview."
        else:
            return "Appears to be a reasonable opportunity with standard expectations."
    
    def _generate_clarifying_questions(self, red_flags: List[str]) -> List[str]:
        """Generate questions to ask during interview based on red flags."""
        questions = []
        
        if any('pressure' in flag.lower() for flag in red_flags):
            questions.append('What does a typical workweek look like for this role?')
            questions.append('How does the team handle tight deadlines?')
        
        if any('weekend' in flag.lower() or 'hour' in flag.lower() for flag in red_flags):
            questions.append('What are the expectations for work-life balance?')
            questions.append('How often do team members work outside normal hours?')
        
        if any('salary' in flag.lower() or 'compensation' in flag.lower() for flag in red_flags):
            questions.append('What is the salary range for this position?')
            questions.append('What does the complete compensation package include?')
        
        return questions
    
    def predict_interview_process(self, jd_text: str) -> Dict:
        """Predict interview process based on job description keywords."""
        text_lower = jd_text.lower()
        
        # Technical assessment indicators
        technical_keywords = [
            'coding challenge', 'technical assessment', 'programming test',
            'algorithm', 'data structure', 'system design', 'code review'
        ]
        
        technical_likely = any(keyword in text_lower for keyword in technical_keywords)
        
        # Cultural fit indicators
        culture_keywords = [
            'culture fit', 'team player', 'collaboration', 'values',
            'mission driven', 'fast-paced', 'startup environment'
        ]
        
        culture_focus = sum(1 for keyword in culture_keywords if keyword in text_lower)
        
        # Technical depth indicators
        tech_stack_mentioned = len([skill for skill in self.all_skills if skill in text_lower])
        
        # Predict interview stages
        predicted_stages = ['Initial HR Screening']
        
        if technical_likely or tech_stack_mentioned >= 5:
            predicted_stages.extend(['Technical Phone Screen', 'Coding Challenge'])
        
        if culture_focus >= 3:
            predicted_stages.append('Culture Fit Interview')
        
        predicted_stages.append('Final Interview with Hiring Manager')
        
        # Experience level affects process
        if 'senior' in text_lower or 'lead' in text_lower:
            predicted_stages.append('System Design Interview')
        
        # Estimate timeline
        timeline_days = len(predicted_stages) * 3 + 5  # Rough estimate
        
        return {
            'predicted_stages': predicted_stages,
            'technical_assessment_likely': technical_likely,
            'culture_focus_level': 'High' if culture_focus >= 3 else 'Medium' if culture_focus >= 1 else 'Low',
            'estimated_timeline': f'{timeline_days-5}-{timeline_days+5} days',
            'preparation_tips': self._get_interview_prep_tips(predicted_stages),
            'confidence_level': self._calculate_prediction_confidence(technical_likely, culture_focus, tech_stack_mentioned)
        }
    
    def _get_interview_prep_tips(self, stages: List[str]) -> List[str]:
        """Generate preparation tips based on predicted interview stages."""
        tips = []
        
        if 'Technical Phone Screen' in stages:
            tips.append('Prepare to explain technical concepts clearly over phone')
        
        if 'Coding Challenge' in stages:
            tips.append('Practice coding problems on platforms like LeetCode')
            tips.append('Focus on clean, readable code with good time complexity')
        
        if 'Culture Fit Interview' in stages:
            tips.append('Research company values and prepare behavioral examples')
            tips.append('Prepare questions about team dynamics and company culture')
        
        if 'System Design Interview' in stages:
            tips.append('Study system design fundamentals (scalability, databases, APIs)')
            tips.append('Practice designing systems relevant to the company\'s domain')
        
        return tips
    
    def _calculate_prediction_confidence(self, technical_likely: bool, culture_focus: int, tech_count: int) -> str:
        """Calculate confidence in interview prediction."""
        confidence_score = 50  # Base confidence
        
        if technical_likely:
            confidence_score += 20
        if culture_focus >= 2:
            confidence_score += 15
        if tech_count >= 8:
            confidence_score += 15
        
        if confidence_score >= 80:
            return 'High Confidence'
        elif confidence_score >= 60:
            return 'Medium Confidence'
        else:
            return 'Low Confidence'
    
    def extract_job_trends(self, jd_text: str) -> Dict:
        """Extract job market trends from job description."""
        trending_tech = [
            'python', 'react', 'node.js', 'aws', 'docker', 'kubernetes', 
            'microservices', 'machine learning', 'ai', 'cloud', 'devops',
            'javascript', 'typescript', 'angular', 'vue', 'mongodb', 'postgresql'
        ]
        
        jd_lower = jd_text.lower()
        
        # Find trending technologies mentioned
        mentioned_trends = []
        for tech in trending_tech:
            if tech in jd_lower:
                mentioned_trends.append(tech)
        
        # Determine market demand level
        if len(mentioned_trends) >= 8:
            demand_level = 'Very High'
        elif len(mentioned_trends) >= 5:
            demand_level = 'High'
        elif len(mentioned_trends) >= 2:
            demand_level = 'Medium'
        else:
            demand_level = 'Low'
        
        return {
            'trending_skills': mentioned_trends,
            'market_demand_level': demand_level,
            'trend_analysis': {
                'hot_technologies': mentioned_trends[:5],
                'skill_diversity': len(set(mentioned_trends)),
                'future_proof_rating': min(100, len(mentioned_trends) * 10)
            },
            'recommendations': [
                'Focus on trending technologies for better opportunities',
                'Combine multiple trending skills for competitive advantage',
                'Stay updated with emerging technologies'
            ]
        }
    
    def rank_keyword_importance(self, jd_text: str) -> Dict:
        """Rank keywords by importance and frequency in job description."""
        # Clean and process text
        jd_lower = jd_text.lower()
        
        # Technical skills keywords
        technical_keywords = [
            'python', 'javascript', 'java', 'react', 'angular', 'vue', 'node.js',
            'aws', 'azure', 'docker', 'kubernetes', 'sql', 'mongodb', 'postgresql',
            'html', 'css', 'git', 'agile', 'scrum', 'machine learning', 'ai'
        ]
        
        # Experience keywords
        experience_keywords = [
            'experience', 'years', 'senior', 'junior', 'lead', 'manager', 'architect'
        ]
        
        # Soft skills keywords
        soft_skills = [
            'communication', 'teamwork', 'leadership', 'problem solving', 
            'analytical', 'creative', 'collaborative'
        ]
        
        # Count keyword frequencies
        keyword_counts = {}
        all_keywords = technical_keywords + experience_keywords + soft_skills
        
        for keyword in all_keywords:
            count = jd_lower.count(keyword)
            if count > 0:
                keyword_counts[keyword] = count
        
        # Calculate importance scores
        ranked_skills = {}
        critical_skills = []
        important_skills = []
        nice_to_have_skills = []
        
        for keyword, count in keyword_counts.items():
            # Base importance score
            importance_score = count * 10
            
            # Boost technical skills
            if keyword in technical_keywords:
                importance_score *= 1.5
            
            # Determine priority level
            if importance_score >= 20:
                priority = 'Critical'
                critical_skills.append(keyword)
            elif importance_score >= 10:
                priority = 'Important'
                important_skills.append(keyword)
            else:
                priority = 'Nice-to-have'
                nice_to_have_skills.append(keyword)
            
            ranked_skills[keyword] = {
                'frequency': count,
                'importance_score': int(importance_score),
                'priority': priority
            }
        
        # Get top 5 skills
        top_5_skills = sorted(keyword_counts.keys(), 
                             key=lambda x: ranked_skills[x]['importance_score'], 
                             reverse=True)[:5]
        
        return {
            'ranked_skills': ranked_skills,
            'top_5_skills': top_5_skills,
            'critical_skills': critical_skills,
            'important_skills': important_skills,
            'nice_to_have_skills': nice_to_have_skills,
            'keyword_analysis': {
                'total_keywords_found': len(keyword_counts),
                'technical_keywords_found': len([k for k in keyword_counts if k in technical_keywords]),
                'skill_diversity_score': min(100, len(keyword_counts) * 5)
            }
        }
    
    def generate_role_expansion_summary(self, jd_text: str) -> Dict:
        """Generate AI-powered role expansion and analysis."""
        jd_lower = jd_text.lower()
        
        # Role type classification
        role_indicators = {
            'frontend_developer': ['frontend', 'react', 'angular', 'vue', 'html', 'css', 'javascript'],
            'backend_developer': ['backend', 'api', 'server', 'database', 'python', 'java', 'node'],
            'fullstack_developer': ['fullstack', 'full stack', 'frontend', 'backend'],
            'data_analyst': ['data', 'analytics', 'sql', 'tableau', 'power bi', 'excel'],
            'devops_engineer': ['devops', 'aws', 'docker', 'kubernetes', 'ci/cd', 'deployment'],
            'mobile_developer': ['mobile', 'android', 'ios', 'react native', 'flutter']
        }
        
        # Determine primary role
        role_scores = {}
        for role, keywords in role_indicators.items():
            score = sum(1 for keyword in keywords if keyword in jd_lower)
            if score > 0:
                role_scores[role] = score
        
        primary_role = max(role_scores, key=role_scores.get) if role_scores else 'general_software_engineer'
        
        # Extract key aspects
        key_aspects = []
        if 'team' in jd_lower or 'collaboration' in jd_lower:
            key_aspects.append('team_collaboration')
        if 'leadership' in jd_lower or 'lead' in jd_lower:
            key_aspects.append('leadership')
        if 'mentoring' in jd_lower or 'mentor' in jd_lower:
            key_aspects.append('mentoring')
        if 'architecture' in jd_lower or 'design' in jd_lower:
            key_aspects.append('system_design')
        
        # Technical focus areas
        technical_focus = []
        tech_areas = {
            'Web Development': ['web', 'html', 'css', 'javascript'],
            'Cloud Computing': ['aws', 'azure', 'cloud', 'docker'],
            'Database Management': ['sql', 'database', 'mongodb', 'postgresql'],
            'Mobile Development': ['mobile', 'android', 'ios'],
            'AI/ML': ['machine learning', 'ai', 'data science']
        }
        
        for area, keywords in tech_areas.items():
            if any(keyword in jd_lower for keyword in keywords):
                technical_focus.append(area)
        
        # Work environment
        work_environment = []
        if 'remote' in jd_lower:
            work_environment.append('remote')
        if 'agile' in jd_lower or 'scrum' in jd_lower:
            work_environment.append('agile')
        if 'startup' in jd_lower:
            work_environment.append('startup')
        
        # Career level assessment
        experience_mentions = re.findall(r'(\d+)\+?\s*years?', jd_lower)
        if experience_mentions:
            years = max([int(year) for year in experience_mentions])
            if years >= 7:
                career_level = 'Senior Level'
                growth_potential = 'Leadership Track'
            elif years >= 3:
                career_level = 'Mid Level'
                growth_potential = 'Senior Track'
            else:
                career_level = 'Entry Level'
                growth_potential = 'Mid-Level Track'
        else:
            career_level = 'Not Specified'
            growth_potential = 'Variable'
        
        return {
            'primary_role_type': primary_role,
            'role_explanation': f"This position is primarily a {primary_role.replace('_', ' ')} role based on required skills and responsibilities.",
            'key_aspects': key_aspects,
            'technical_focus': technical_focus,
            'work_environment': work_environment,
            'career_level': career_level,
            'growth_potential': growth_potential,
            'role_complexity_score': min(100, len(key_aspects) * 15 + len(technical_focus) * 10)
        }
    
    def analyze_industry_insights(self, jd_text: str) -> Dict:
        """Analyze industry-specific insights from job description."""
        jd_lower = jd_text.lower()
        
        # Industry detection
        industry_indicators = {
            'fintech': ['fintech', 'financial', 'banking', 'payment', 'trading', 'cryptocurrency', 'blockchain'],
            'healthcare': ['healthcare', 'medical', 'hospital', 'patient', 'clinical', 'pharma', 'biotech'],
            'e_commerce': ['e-commerce', 'ecommerce', 'retail', 'marketplace', 'shopping', 'customer'],
            'gaming': ['gaming', 'game', 'entertainment', 'mobile games', 'console', 'unity', 'unreal'],
            'education': ['education', 'learning', 'student', 'academic', 'school', 'university', 'edtech'],
            'enterprise': ['enterprise', 'b2b', 'saas', 'corporate', 'business', 'crm', 'erp'],
            'media': ['media', 'content', 'streaming', 'video', 'social media', 'publishing'],
            'automotive': ['automotive', 'car', 'vehicle', 'transportation', 'mobility', 'autonomous'],
            'cybersecurity': ['security', 'cybersecurity', 'threat', 'vulnerability', 'compliance', 'privacy']
        }
        
        detected_industries = []
        industry_scores = {}
        
        for industry, keywords in industry_indicators.items():
            score = sum(1 for keyword in keywords if keyword in jd_lower)
            if score > 0:
                industry_scores[industry] = score
                detected_industries.append(industry)
        
        primary_industry = max(industry_scores, key=industry_scores.get) if industry_scores else 'general_tech'
        
        # Industry-specific insights
        industry_insights = {
            'fintech': {
                'growth_outlook': 'High',
                'key_trends': ['Digital payments', 'DeFi', 'RegTech', 'Open banking'],
                'skill_premiums': ['Blockchain', 'Security', 'Compliance'],
                'avg_salary_multiplier': 1.2
            },
            'healthcare': {
                'growth_outlook': 'Very High',
                'key_trends': ['Telemedicine', 'AI diagnostics', 'Health data'],
                'skill_premiums': ['HIPAA compliance', 'Medical data', 'AI/ML'],
                'avg_salary_multiplier': 1.15
            },
            'e_commerce': {
                'growth_outlook': 'High',
                'key_trends': ['Mobile commerce', 'Personalization', 'AR/VR shopping'],
                'skill_premiums': ['Microservices', 'Cloud', 'Analytics'],
                'avg_salary_multiplier': 1.1
            },
            'gaming': {
                'growth_outlook': 'Very High',
                'key_trends': ['Mobile gaming', 'VR/AR', 'Cloud gaming'],
                'skill_premiums': ['Unity', 'Unreal Engine', 'Graphics programming'],
                'avg_salary_multiplier': 1.05
            }
        }
        
        current_insights = industry_insights.get(primary_industry, {
            'growth_outlook': 'Moderate',
            'key_trends': ['Digital transformation', 'Cloud adoption'],
            'skill_premiums': ['Cloud', 'DevOps', 'Security'],
            'avg_salary_multiplier': 1.0
        })
        
        # Company size detection
        company_size_indicators = {
            'startup': ['startup', 'early stage', 'seed', 'series a', 'fast-paced', 'agile environment'],
            'scale_up': ['scale-up', 'growing', 'expanding', 'series b', 'series c'],
            'enterprise': ['enterprise', 'fortune', 'established', 'large company', 'multinational'],
            'mid_size': ['mid-size', 'medium', '100-500', 'growing company']
        }
        
        company_size = 'unknown'
        for size, indicators in company_size_indicators.items():
            if any(indicator in jd_lower for indicator in indicators):
                company_size = size
                break
        
        # Remote work analysis
        remote_indicators = ['remote', 'work from home', 'distributed', 'anywhere', 'flexible location']
        remote_score = sum(1 for indicator in remote_indicators if indicator in jd_lower)
        remote_friendliness = 'High' if remote_score >= 2 else 'Medium' if remote_score == 1 else 'Low'
        
        return {
            'primary_industry': primary_industry,
            'detected_industries': detected_industries,
            'industry_confidence': max(industry_scores.values()) if industry_scores else 0,
            'growth_outlook': current_insights['growth_outlook'],
            'key_trends': current_insights['key_trends'],
            'skill_premiums': current_insights['skill_premiums'],
            'salary_multiplier': current_insights['avg_salary_multiplier'],
            'company_size': company_size,
            'remote_friendliness': remote_friendliness,
            'market_insights': [
                f'This {primary_industry} role shows {current_insights["growth_outlook"].lower()} growth potential',
                f'Industry trends include: {', '.join(current_insights["key_trends"][:2])}',
                f'Skills commanding premium: {', '.join(current_insights["skill_premiums"][:2])}'
            ]
        }
    
    def assess_job_difficulty_advanced(self, jd_text: str) -> Dict:
        """Advanced job difficulty assessment with multiple factors."""
        difficulty_score = 0
        difficulty_factors = []
        
        jd_lower = jd_text.lower()
        
        # Experience requirements
        experience_patterns = re.findall(r'(\d+)\+?\s*(?:years?|yrs?)', jd_lower)
        if experience_patterns:
            max_years = max([int(year) for year in experience_patterns])
            if max_years >= 7:
                difficulty_score += 30
                difficulty_factors.append(f'{max_years}+ years experience required')
            elif max_years >= 5:
                difficulty_score += 20
                difficulty_factors.append(f'{max_years}+ years experience required')
            elif max_years >= 3:
                difficulty_score += 10
                difficulty_factors.append(f'{max_years}+ years experience required')
        
        # Technical skills complexity
        advanced_skills = [
            'machine learning', 'deep learning', 'kubernetes', 'microservices',
            'system design', 'distributed systems', 'blockchain', 'ai',
            'computer vision', 'nlp', 'big data', 'spark', 'kafka'
        ]
        
        advanced_skill_count = sum(1 for skill in advanced_skills if skill in jd_lower)
        difficulty_score += min(25, advanced_skill_count * 5)
        if advanced_skill_count > 3:
            difficulty_factors.append(f'{advanced_skill_count} advanced technical skills required')
        
        # Education requirements
        education_keywords = ['phd', 'masters', 'ms', 'mba', 'bachelor', 'bs', 'degree']
        education_mentions = sum(1 for keyword in education_keywords if keyword in jd_lower)
        if 'phd' in jd_lower:
            difficulty_score += 20
            difficulty_factors.append('PhD preferred or required')
        elif any(keyword in jd_lower for keyword in ['masters', 'ms', 'mba']):
            difficulty_score += 10
            difficulty_factors.append('Advanced degree preferred')
        
        # Competitive indicators
        competitive_terms = [
            'top talent', 'exceptional', 'world-class', 'elite', 'cutting-edge',
            'innovative', 'disruptive', 'game-changing', 'revolutionary'
        ]
        competitive_count = sum(1 for term in competitive_terms if term in jd_lower)
        difficulty_score += min(15, competitive_count * 3)
        if competitive_count >= 3:
            difficulty_factors.append('Highly competitive position language')
        
        # Responsibility level
        leadership_terms = ['lead', 'senior', 'principal', 'architect', 'manager', 'director']
        leadership_mentions = sum(1 for term in leadership_terms if term in jd_lower)
        if leadership_mentions >= 2:
            difficulty_score += 15
            difficulty_factors.append('Leadership responsibilities')
        
        # Multiple technology stacks
        tech_stacks = ['frontend', 'backend', 'mobile', 'devops', 'data', 'ml', 'security']
        stack_count = sum(1 for stack in tech_stacks if stack in jd_lower)
        if stack_count >= 4:
            difficulty_score += 10
            difficulty_factors.append('Multiple technology stack knowledge required')
        
        # Determine difficulty level
        if difficulty_score >= 80:
            difficulty_level = 'Extremely Hard'
            difficulty_description = 'This is an extremely challenging role requiring top-tier expertise'
        elif difficulty_score >= 60:
            difficulty_level = 'Hard'
            difficulty_description = 'This role requires significant experience and advanced skills'
        elif difficulty_score >= 40:
            difficulty_level = 'Moderate'
            difficulty_description = 'This role requires solid experience and technical competency'
        elif difficulty_score >= 20:
            difficulty_level = 'Easy-Moderate'
            difficulty_description = 'This role is accessible to candidates with some experience'
        else:
            difficulty_level = 'Easy'
            difficulty_description = 'This role is suitable for entry-level or junior candidates'
        
        return {
            'difficulty_score': min(100, difficulty_score),
            'difficulty_level': difficulty_level,
            'difficulty_description': difficulty_description,
            'difficulty_factors': difficulty_factors,
            'preparation_timeline': self._get_preparation_timeline(difficulty_score),
            'success_probability': self._calculate_success_probability(difficulty_score),
            'recommendation': self._get_difficulty_recommendation(difficulty_score)
        }
    
    def _get_preparation_timeline(self, difficulty_score: int) -> str:
        """Get recommended preparation timeline based on difficulty."""
        if difficulty_score >= 80:
            return '6-12 months intensive preparation'
        elif difficulty_score >= 60:
            return '3-6 months focused preparation'
        elif difficulty_score >= 40:
            return '1-3 months preparation'
        elif difficulty_score >= 20:
            return '2-4 weeks preparation'
        else:
            return '1-2 weeks preparation'
    
    def _calculate_success_probability(self, difficulty_score: int) -> Dict:
        """Calculate success probability for different candidate levels."""
        base_probabilities = {
            'entry_level': max(5, 80 - difficulty_score),
            'mid_level': max(15, 90 - (difficulty_score * 0.8)),
            'senior_level': max(25, 95 - (difficulty_score * 0.6))
        }
        return base_probabilities
    
    def _get_difficulty_recommendation(self, difficulty_score: int) -> str:
        """Get personalized recommendation based on difficulty."""
        if difficulty_score >= 80:
            return 'Consider building more experience before applying. Focus on skill development and networking.'
        elif difficulty_score >= 60:
            return 'Prepare thoroughly. Consider highlighting transferable skills and relevant projects.'
        elif difficulty_score >= 40:
            return 'Good fit with proper preparation. Tailor your application to match key requirements.'
        else:
            return 'Well-suited for your level. Apply with confidence while highlighting relevant experience.'
    
    def analyze_benefits_package(self, jd_text: str) -> Dict:
        """Analyze benefits and compensation package from job description."""
        benefits_analysis = {
            'salary_mentioned': False,
            'equity_mentioned': False,
            'benefits_score': 0,
            'benefits_found': [],
            'missing_benefits': [],
            'package_competitiveness': 'Unknown'
        }
        
        jd_lower = jd_text.lower()
        
        # Salary detection
        salary_patterns = [
            r'\$\d{2,3}[,k]\d{0,3}',
            r'salary.*\$\d+',
            r'\d{2,3}k',
            r'competitive salary'
        ]
        
        for pattern in salary_patterns:
            if re.search(pattern, jd_lower):
                benefits_analysis['salary_mentioned'] = True
                break
        
        # Equity detection
        equity_terms = ['equity', 'stock options', 'rsu', 'espp', 'ownership']
        benefits_analysis['equity_mentioned'] = any(term in jd_lower for term in equity_terms)
        
        # Standard benefits
        benefit_categories = {
            'health_insurance': ['health insurance', 'medical', 'dental', 'vision'],
            'retirement': ['401k', 'retirement', 'pension', 'matching'],
            'time_off': ['pto', 'vacation', 'paid time off', 'unlimited pto'],
            'flexible_work': ['remote', 'flexible', 'work from home', 'hybrid'],
            'professional_development': ['training', 'learning', 'conference', 'education'],
            'wellness': ['gym', 'fitness', 'wellness', 'mental health'],
            'family': ['parental leave', 'family', 'childcare'],
            'transportation': ['commuter', 'parking', 'transit']
        }
        
        found_benefits = []
        for category, keywords in benefit_categories.items():
            if any(keyword in jd_lower for keyword in keywords):
                found_benefits.append(category)
        
        benefits_analysis['benefits_found'] = found_benefits
        benefits_analysis['benefits_score'] = min(100, len(found_benefits) * 12.5)
        
        # Standard benefits that should be mentioned
        expected_benefits = ['health_insurance', 'retirement', 'time_off']
        benefits_analysis['missing_benefits'] = [b for b in expected_benefits if b not in found_benefits]
        
        # Competitiveness assessment
        total_score = (
            (20 if benefits_analysis['salary_mentioned'] else 0) +
            (15 if benefits_analysis['equity_mentioned'] else 0) +
            (benefits_analysis['benefits_score'] * 0.65)
        )
        
        if total_score >= 85:
            benefits_analysis['package_competitiveness'] = 'Excellent'
        elif total_score >= 70:
            benefits_analysis['package_competitiveness'] = 'Good'
        elif total_score >= 50:
            benefits_analysis['package_competitiveness'] = 'Average'
        else:
            benefits_analysis['package_competitiveness'] = 'Below Average'
        
        return benefits_analysis
    
    def process_job_description(self, jd_text: str) -> Dict:
        """Main method to process job description with all features."""
        # This method should exist to maintain compatibility
        return self.process_jd(jd_text)