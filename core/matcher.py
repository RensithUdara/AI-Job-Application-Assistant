from typing import Dict, List, Set, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Matcher:
    def __init__(self):
        """Initialize the matcher for resume-job description comparison."""
        self.vectorizer = TfidfVectorizer(stop_words='english', lowercase=True, max_features=1000)
    
    def match_resume_to_jd(self, resume_data: Dict, jd_data: Dict) -> Dict:
        """Compare resume with job description and provide match analysis."""
        try:
            # Extract skills sets
            resume_skills = resume_data.get('resume_skills', {}).get('all_skills', set())
            jd_skills = jd_data.get('jd_skills', {}).get('all_skills', set())
            
            # Convert to lowercase for comparison
            resume_skills_lower = {skill.lower() for skill in resume_skills}
            jd_skills_lower = {skill.lower() for skill in jd_skills}
            
            # Basic skill matching
            skill_match_result = self._analyze_skill_match(resume_skills_lower, jd_skills_lower)
            
            # Category-wise matching
            category_match = self._analyze_category_match(resume_data, jd_data)
            
            # Text similarity (semantic matching)
            text_similarity = self._calculate_text_similarity(
                resume_data.get('cleaned_text', ''), 
                jd_data.get('cleaned_text', '')
            )
            
            # Priority analysis for missing skills
            priority_analysis = self._analyze_missing_skill_priorities(
                skill_match_result['missing_skills'], jd_data
            )
            
            # Overall match score calculation
            overall_score = self._calculate_overall_score(
                skill_match_result, category_match, text_similarity
            )
            
            return {
                'match_score_overall': overall_score,
                'skill_match': skill_match_result,
                'category_match': category_match,
                'text_similarity': text_similarity,
                'priority_analysis': priority_analysis,
                'matched_skills': list(skill_match_result['matched_skills']),
                'missing_skills': list(skill_match_result['missing_skills']),
                'resume_only_skills': list(skill_match_result['resume_only_skills']),
                'technical_match': category_match.get('technical_match', 0),
                'soft_skill_match': category_match.get('soft_skill_match', 0)
            }
        
        except Exception as e:
            return {
                'error': str(e),
                'match_score_overall': 0,
                'matched_skills': [],
                'missing_skills': [],
                'resume_only_skills': [],
                'technical_match': 0,
                'soft_skill_match': 0
            }
    
    def _analyze_skill_match(self, resume_skills: Set[str], jd_skills: Set[str]) -> Dict:
        """Analyze skill overlap between resume and job description."""
        matched_skills = resume_skills.intersection(jd_skills)
        missing_skills = jd_skills - resume_skills
        resume_only_skills = resume_skills - jd_skills
        
        # Calculate match percentage
        total_jd_skills = len(jd_skills)
        match_percentage = (len(matched_skills) / total_jd_skills * 100) if total_jd_skills > 0 else 0
        
        return {
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'resume_only_skills': resume_only_skills,
            'match_percentage': round(match_percentage, 2),
            'total_jd_skills': total_jd_skills,
            'total_matched': len(matched_skills),
            'total_missing': len(missing_skills)
        }
    
    def _analyze_category_match(self, resume_data: Dict, jd_data: Dict) -> Dict:
        """Analyze match by skill categories."""
        resume_categories = resume_data.get('resume_skills', {}).get('by_category', {})
        jd_categories = jd_data.get('jd_skills', {}).get('by_category', {})
        
        category_matches = {}
        technical_categories = [
            'programming_languages', 'web_technologies', 'mobile_technologies', 
            'databases', 'cloud_platforms', 'tools', 'frameworks', 'concepts'
        ]
        
        technical_total = 0
        technical_matched = 0
        soft_skill_total = 0
        soft_skill_matched = 0
        
        for category in set(list(resume_categories.keys()) + list(jd_categories.keys())):
            resume_skills_in_cat = set(skill.lower() for skill in resume_categories.get(category, []))
            jd_skills_in_cat = set(skill.lower() for skill in jd_categories.get(category, []))
            
            matched = len(resume_skills_in_cat.intersection(jd_skills_in_cat))
            total_jd = len(jd_skills_in_cat)
            
            match_percent = (matched / total_jd * 100) if total_jd > 0 else 0
            
            category_matches[category] = {
                'matched': matched,
                'total_required': total_jd,
                'match_percentage': round(match_percent, 2)
            }
            
            # Aggregate technical vs soft skills
            if category in technical_categories:
                technical_matched += matched
                technical_total += total_jd
            elif category == 'soft_skills':
                soft_skill_matched += matched
                soft_skill_total += total_jd
        
        technical_match = (technical_matched / technical_total * 100) if technical_total > 0 else 0
        soft_skill_match = (soft_skill_matched / soft_skill_total * 100) if soft_skill_total > 0 else 0
        
        return {
            'category_breakdown': category_matches,
            'technical_match': round(technical_match, 2),
            'soft_skill_match': round(soft_skill_match, 2)
        }
    
    def _calculate_text_similarity(self, resume_text: str, jd_text: str) -> Dict:
        """Calculate semantic similarity between resume and job description texts."""
        try:
            if not resume_text or not jd_text:
                return {'cosine_similarity': 0, 'method': 'TF-IDF + Cosine'}
            
            # Prepare texts for vectorization
            texts = [resume_text, jd_text]
            
            # Create TF-IDF vectors
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return {
                'cosine_similarity': round(float(similarity) * 100, 2),
                'method': 'TF-IDF + Cosine Similarity'
            }
        
        except Exception:
            return {'cosine_similarity': 0, 'method': 'Error in calculation'}
    
    def _analyze_missing_skill_priorities(self, missing_skills: Set[str], jd_data: Dict) -> Dict:
        """Analyze priority of missing skills based on job requirements."""
        critical_skills = set(skill.lower() for skill in jd_data.get('critical_skills', []))
        bonus_skills = set(skill.lower() for skill in jd_data.get('bonus_skills', []))
        
        high_priority = []
        medium_priority = []
        low_priority = []
        
        for skill in missing_skills:
            skill_lower = skill.lower()
            if skill_lower in critical_skills:
                high_priority.append(skill)
            elif skill_lower in bonus_skills:
                medium_priority.append(skill)
            else:
                low_priority.append(skill)
        
        return {
            'high_priority': high_priority,
            'medium_priority': medium_priority,
            'low_priority': low_priority,
            'critical_missing_count': len(high_priority)
        }
    
    def _calculate_overall_score(self, skill_match: Dict, category_match: Dict, 
                               text_similarity: Dict) -> int:
        """Calculate overall match score (0-100)."""
        # Weighted scoring
        skill_score = skill_match.get('match_percentage', 0) * 0.5  # 50% weight
        technical_score = category_match.get('technical_match', 0) * 0.3  # 30% weight
        text_score = text_similarity.get('cosine_similarity', 0) * 0.2  # 20% weight
        
        overall_score = skill_score + technical_score + text_score
        
        return min(int(overall_score), 100)