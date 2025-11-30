import re
import json
from typing import Dict, List, Set, Optional
from fuzzywuzzy import fuzz
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
            
            return {
                'jd_text': jd_text,
                'cleaned_text': cleaned_text,
                'jd_role': jd_role,
                'jd_skills': jd_skills,
                'required_experience': experience_info['experience_range'],
                'seniority': experience_info['seniority'],
                'critical_skills': skill_categories['critical_skills'],
                'bonus_skills': skill_categories['bonus_skills'],
                'all_jd_skills_list': list(jd_skills['all_skills'])
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