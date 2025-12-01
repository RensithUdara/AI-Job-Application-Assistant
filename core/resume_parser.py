import re
import json
from typing import Dict, List, Set, Optional, Tuple
import pdfplumber
from docx import Document
from fuzzywuzzy import fuzz
import pandas as pd

class ResumeParser:
    def __init__(self, skills_taxonomy_path: str = "data/skills_taxonomy.json"):
        """Initialize the resume parser with skills taxonomy."""
        with open(skills_taxonomy_path, 'r', encoding='utf-8') as f:
            self.skills_taxonomy = json.load(f)
        
        # Flatten skills for easier searching
        self.all_skills = set()
        for category, skills in self.skills_taxonomy.items():
            self.all_skills.update([skill.lower() for skill in skills])
        
        # Professional action verbs for analysis
        self.strong_action_verbs = [
            'Achieved', 'Analyzed', 'Architected', 'Automated', 'Built', 'Collaborated',
            'Configured', 'Created', 'Delivered', 'Designed', 'Developed', 'Engineered',
            'Enhanced', 'Established', 'Executed', 'Implemented', 'Improved', 'Increased',
            'Initiated', 'Launched', 'Led', 'Managed', 'Optimized', 'Orchestrated',
            'Planned', 'Reduced', 'Resolved', 'Scaled', 'Streamlined', 'Transformed'
        ]
        
        self.weak_action_verbs = [
            'Did', 'Worked', 'Helped', 'Assisted', 'Participated', 'Involved',
            'Responsible', 'Used', 'Tried', 'Handled', 'Dealt', 'Made'
        ]
        
        # Common section headers
        self.section_keywords = {
            'contact': ['contact', 'personal information', 'contact information'],
            'summary': ['summary', 'objective', 'profile', 'about', 'career objective'],
            'education': ['education', 'academic', 'qualification', 'degree'],
            'experience': ['experience', 'work experience', 'employment', 'work history', 'professional experience'],
            'skills': ['skills', 'technical skills', 'competencies', 'expertise'],
            'projects': ['projects', 'personal projects', 'academic projects', 'portfolio'],
            'certifications': ['certifications', 'certificates', 'awards', 'achievements']
        }
    
    def parse_resume(self, file_content=None, text_content=None) -> Dict:
        """Parse resume from file or text and extract information."""
        try:
            # Extract text from file or use provided text
            if file_content is not None:
                text = self._extract_text_from_file(file_content)
            elif text_content is not None:
                text = text_content
            else:
                raise ValueError("Either file_content or text_content must be provided")
            
            # Clean and normalize text
            cleaned_text = self._clean_text(text)
            
            # Extract information
            sections_found = self._detect_sections(cleaned_text)
            contact_info = self._extract_contact_info(cleaned_text)
            resume_skills = self._extract_skills(cleaned_text)
            quality_score = self._calculate_quality_score(sections_found, contact_info, resume_skills)
            ats_analysis = self.calculate_ats_score(text)
            
            return {
                'raw_text': text,
                'cleaned_text': cleaned_text,
                'sections_found': sections_found,
                'missing_sections': self._get_missing_sections(sections_found),
                'contact_info': contact_info,
                'resume_skills': resume_skills,
                'quality_score': quality_score,
                'ats_analysis': ats_analysis,
                'word_count': len(text.split()),
                'character_count': len(text)
            }
        
        except Exception as e:
            return {
                'error': str(e),
                'sections_found': {},
                'missing_sections': [],
                'contact_info': {},
                'resume_skills': {'by_category': {}, 'all_skills': set()},
                'quality_score': 0
            }
    
    def _extract_text_from_file(self, file_content) -> str:
        """Extract text from PDF or DOCX file."""
        file_type = file_content.type if hasattr(file_content, 'type') else 'text/plain'
        
        if 'pdf' in file_type.lower():
            return self._extract_from_pdf(file_content)
        elif 'word' in file_type.lower() or file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            return self._extract_from_docx(file_content)
        else:
            # Assume it's plain text
            return str(file_content.read(), 'utf-8') if hasattr(file_content, 'read') else str(file_content)
    
    def _extract_from_pdf(self, file_content) -> str:
        """Extract text from PDF file."""
        text = ""
        try:
            with pdfplumber.open(file_content) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
        return text
    
    def _extract_from_docx(self, file_content) -> str:
        """Extract text from DOCX file."""
        try:
            doc = Document(file_content)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Convert to lowercase for processing
        text = text.lower()
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep important ones
        text = re.sub(r'[^\w\s@.\-+()]', ' ', text)
        return text.strip()
    
    def _detect_sections(self, text: str) -> Dict[str, bool]:
        """Detect which sections are present in the resume."""
        sections_found = {}
        
        for section, keywords in self.section_keywords.items():
            found = False
            for keyword in keywords:
                if keyword in text:
                    found = True
                    break
            sections_found[section] = found
        
        return sections_found
    
    def _extract_contact_info(self, text: str) -> Dict:
        """Extract contact information from resume."""
        contact_info = {
            'email': None,
            'phone': None,
            'linkedin': None,
            'valid_email': False,
            'has_phone': False,
            'has_linkedin': False
        }
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info['email'] = emails[0]
            contact_info['valid_email'] = True
        
        # Extract phone
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact_info['phone'] = ''.join(phones[0]) if isinstance(phones[0], tuple) else phones[0]
            contact_info['has_phone'] = True
        
        # Extract LinkedIn
        if 'linkedin' in text or 'linked.in' in text:
            linkedin_pattern = r'linkedin\.com/in/[\w-]+'
            linkedin_matches = re.findall(linkedin_pattern, text)
            if linkedin_matches:
                contact_info['linkedin'] = linkedin_matches[0]
            contact_info['has_linkedin'] = True
        
        return contact_info
    
    def _extract_skills(self, text: str) -> Dict:
        """Extract skills from resume text."""
        resume_skills = {
            'by_category': {},
            'all_skills': set()
        }
        
        for category, skills in self.skills_taxonomy.items():
            found_skills = []
            
            for skill in skills:
                skill_lower = skill.lower()
                # Exact match
                if skill_lower in text:
                    found_skills.append(skill)
                    resume_skills['all_skills'].add(skill_lower)
                else:
                    # Fuzzy match
                    words_in_text = text.split()
                    for word in words_in_text:
                        if len(word) > 2 and fuzz.ratio(skill_lower, word) > 85:
                            found_skills.append(skill)
                            resume_skills['all_skills'].add(skill_lower)
                            break
            
            if found_skills:
                resume_skills['by_category'][category] = found_skills
        
        return resume_skills
    
    def _get_missing_sections(self, sections_found: Dict[str, bool]) -> List[str]:
        """Get list of missing sections."""
        return [section for section, found in sections_found.items() if not found]
    
    def _calculate_quality_score(self, sections_found: Dict[str, bool], 
                                contact_info: Dict, resume_skills: Dict) -> int:
        """Calculate overall resume quality score (0-100)."""
        score = 0
        
        # Section completeness (30 points)
        total_sections = len(sections_found)
        found_sections = sum(sections_found.values())
        if total_sections > 0:
            score += (found_sections / total_sections) * 30
        
        # Contact information (20 points)
        if contact_info.get('valid_email'):
            score += 10
        if contact_info.get('has_phone'):
            score += 5
        if contact_info.get('has_linkedin'):
            score += 5
        
        # Skills diversity and depth (30 points)
        skill_categories = len(resume_skills['by_category'])
        total_skills = len(resume_skills['all_skills'])
        
        if skill_categories > 0:
            score += min(skill_categories * 4, 15)  # Max 15 for categories
        if total_skills > 0:
            score += min(total_skills * 1.5, 15)  # Max 15 for total skills
        
        # Content quality indicators (20 points)
        score += self._assess_content_quality(sections_found)
        
        return min(int(score), 100)
    
    def _assess_content_quality(self, sections_found: Dict[str, bool]) -> int:
        """Assess content quality based on section presence and importance."""
        quality_score = 0
        
        # Critical sections
        if sections_found.get('experience', False):
            quality_score += 8
        if sections_found.get('projects', False):
            quality_score += 6
        if sections_found.get('education', False):
            quality_score += 4
        if sections_found.get('certifications', False):
            quality_score += 2
        
        return quality_score
    
    def calculate_ats_score(self, text: str) -> Dict:
        """Calculate ATS (Applicant Tracking System) compatibility score."""
        ats_score = 100
        issues = []
        
        # Check for ATS-friendly formatting
        if len(re.findall(r'[^\w\s@.\-+()]', text)) > len(text) * 0.1:
            ats_score -= 15
            issues.append("Too many special characters may confuse ATS systems")
        
        # Check for standard section headers
        standard_headers = ['experience', 'education', 'skills', 'summary']
        missing_headers = []
        for header in standard_headers:
            if header not in text.lower():
                missing_headers.append(header)
        
        if missing_headers:
            ats_score -= len(missing_headers) * 5
            issues.append(f"Missing standard sections: {', '.join(missing_headers)}")
        
        # Check text length (too short or too long)
        word_count = len(text.split())
        if word_count < 200:
            ats_score -= 20
            issues.append("Resume appears too short (< 200 words)")
        elif word_count > 1000:
            ats_score -= 10
            issues.append("Resume may be too long for ATS parsing (> 1000 words)")
        
        return {
            'score': max(0, ats_score),
            'issues': issues,
            'word_count': word_count
        }
    
    def analyze_bullet_points(self, text: str) -> Dict:
        """Analyze bullet points quality using advanced NLP techniques."""
        bullets = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                bullet_text = line[1:].strip()
                if len(bullet_text) > 10:  # Meaningful bullet
                    score = self._score_bullet_point(bullet_text)
                    bullets.append({
                        'text': bullet_text,
                        'score': score,
                        'feedback': self._get_bullet_feedback(bullet_text, score),
                        'suggestions': self._get_bullet_suggestions(bullet_text)
                    })
        
        avg_score = sum([b['score'] for b in bullets]) / len(bullets) if bullets else 0
        
        return {
            'bullets': bullets,
            'total_bullets': len(bullets),
            'average_score': round(avg_score, 1),
            'quality_level': self._get_quality_level(avg_score),
            'improvement_tips': self._get_overall_bullet_tips(bullets)
        }
    
    def _score_bullet_point(self, bullet: str) -> int:
        """Score individual bullet point quality (1-10)."""
        score = 4  # Base score
        bullet_lower = bullet.lower()
        
        # Check for strong action verbs (+2)
        has_strong_verb = any(verb.lower() in bullet_lower for verb in self.strong_action_verbs)
        if has_strong_verb:
            score += 2
        
        # Check for weak action verbs (-1)
        has_weak_verb = any(verb.lower() in bullet_lower for verb in self.weak_action_verbs)
        if has_weak_verb:
            score -= 1
        
        # Check for quantification (+2)
        numbers = re.findall(r'\d+', bullet)
        percentages = re.findall(r'\d+%', bullet)
        if numbers or percentages:
            score += 2
        
        # Check for impact words (+1)
        impact_words = ['increased', 'improved', 'reduced', 'enhanced', 'optimized', 'delivered']
        if any(word in bullet_lower for word in impact_words):
            score += 1
        
        # Check for technical skills (+1)
        technical_terms = ['api', 'database', 'framework', 'algorithm', 'system', 'application']
        if any(term in bullet_lower for term in technical_terms):
            score += 1
        
        # Check for result/outcome indicators (+1)
        result_indicators = ['resulting in', 'leading to', 'which resulted', 'achieving', 'delivered']
        if any(indicator in bullet_lower for indicator in result_indicators):
            score += 1
        
        # Penalty for too short (-1)
        if len(bullet.split()) < 6:
            score -= 1
        
        # Penalty for too generic (-1)
        generic_phrases = ['responsible for', 'worked on', 'helped with', 'assisted in']
        if any(phrase in bullet_lower for phrase in generic_phrases):
            score -= 1
        
        return max(1, min(10, score))
    
    def _get_bullet_feedback(self, bullet: str, score: int) -> str:
        """Generate specific improvement feedback for bullet points."""
        if score >= 8:
            return "🌟 Excellent bullet! Strong action verb, quantified results, and clear impact."
        elif score >= 6:
            return "✅ Good bullet. Consider adding specific metrics or stronger action verbs."
        elif score >= 4:
            return "⚠️ Average bullet. Add quantifiable results and use stronger action verbs."
        else:
            return "❌ Weak bullet. Rewrite with action verb, specific details, and measurable impact."
    
    def _get_bullet_suggestions(self, bullet: str) -> List[str]:
        """Generate specific improvement suggestions for bullet points."""
        suggestions = []
        bullet_lower = bullet.lower()
        
        # Check for missing quantification
        if not re.search(r'\d', bullet):
            suggestions.append("Add specific numbers, percentages, or timeframes")
        
        # Check for weak verbs
        if any(verb.lower() in bullet_lower for verb in self.weak_action_verbs):
            suggestions.append("Replace weak action verbs with stronger alternatives")
        
        # Check for missing impact
        impact_words = ['increased', 'improved', 'reduced', 'enhanced', 'optimized']
        if not any(word in bullet_lower for word in impact_words):
            suggestions.append("Include the impact or result of your action")
        
        # Check for vague terms
        vague_terms = ['various', 'multiple', 'several', 'many']
        if any(term in bullet_lower for term in vague_terms):
            suggestions.append("Replace vague terms with specific details")
        
        return suggestions
    
    def _get_quality_level(self, score: float) -> str:
        """Convert numeric score to quality level."""
        if score >= 8:
            return "Excellent"
        elif score >= 6:
            return "Good" 
        elif score >= 4:
            return "Average"
        else:
            return "Needs Improvement"
    
    def _get_overall_bullet_tips(self, bullets: List[Dict]) -> List[str]:
        """Generate overall improvement tips based on all bullets."""
        tips = []
        
        if len(bullets) < 3:
            tips.append("Add more bullet points to better showcase your experience")
        
        avg_score = sum([b['score'] for b in bullets]) / len(bullets) if bullets else 0
        
        if avg_score < 6:
            tips.append("Focus on rewriting bullets with the STAR method (Situation, Task, Action, Result)")
            tips.append("Start each bullet with a strong action verb")
            tips.append("Include specific numbers and metrics wherever possible")
        
        return tips
    
    def analyze_action_verbs(self, text: str) -> Dict:
        """Comprehensive action verb analysis."""
        text_lower = text.lower()
        
        strong_found = []
        weak_found = []
        
        # Find specific instances
        for verb in self.strong_action_verbs:
            if verb.lower() in text_lower:
                strong_found.append(verb)
        
        for verb in self.weak_action_verbs:
            if verb.lower() in text_lower:
                weak_found.append(verb)
        
        # Generate suggestions for improvement
        suggestions = []
        verb_replacements = {
            'helped': ['Assisted', 'Supported', 'Facilitated', 'Collaborated'],
            'worked': ['Developed', 'Created', 'Built', 'Implemented'],
            'did': ['Completed', 'Executed', 'Delivered', 'Achieved'],
            'used': ['Utilized', 'Applied', 'Implemented', 'Leveraged'],
            'responsible': ['Managed', 'Led', 'Oversaw', 'Coordinated']
        }
        
        for weak_verb in weak_found:
            if weak_verb.lower() in verb_replacements:
                suggestions.append({
                    'weak_verb': weak_verb,
                    'alternatives': verb_replacements[weak_verb.lower()]
                })
        
        strength_ratio = len(strong_found) / max(1, len(weak_found))
        
        return {
            'strong_verbs_found': strong_found,
            'weak_verbs_found': weak_found,
            'strong_count': len(strong_found),
            'weak_count': len(weak_found),
            'verb_strength_ratio': round(strength_ratio, 2),
            'verb_recommendations': suggestions,
            'overall_assessment': self._assess_verb_usage(strength_ratio)
        }
    
    def _assess_verb_usage(self, ratio: float) -> str:
        """Assess overall verb usage quality."""
        if ratio >= 2:
            return "Excellent use of strong action verbs"
        elif ratio >= 1:
            return "Good balance of action verbs"
        elif ratio >= 0.5:
            return "Room for improvement in action verb usage"
        else:
            return "Needs significant improvement in action verb usage"
    
    def analyze_quantification(self, text: str) -> Dict:
        """Analyze quantification and metrics usage in resume."""
        # Find different types of metrics
        numbers = re.findall(r'\b\d+\b', text)
        percentages = re.findall(r'\d+%', text)
        monetary = re.findall(r'\$[\d,]+', text)
        timeframes = re.findall(r'\d+\s*(years?|months?|weeks?|days?)', text, re.IGNORECASE)
        sizes = re.findall(r'\d+\s*(users?|customers?|people|members?|employees?)', text, re.IGNORECASE)
        
        # Analyze sentences for quantification opportunities
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 20]
        unquantified_sentences = []
        
        for sentence in sentences:
            if not re.search(r'\d', sentence) and len(sentence.split()) > 5:
                # Check if it's an achievement that could be quantified
                achievement_indicators = ['improved', 'increased', 'reduced', 'managed', 'led', 'created']
                if any(indicator in sentence.lower() for indicator in achievement_indicators):
                    unquantified_sentences.append(sentence)
        
        # Generate specific suggestions
        suggestions = []
        if len(numbers) < 5:
            suggestions.append("Add more specific numbers to quantify your achievements")
        if not percentages:
            suggestions.append("Include percentage improvements where applicable (e.g., 'increased efficiency by 25%')")
        if not timeframes:
            suggestions.append("Mention timeframes for projects and achievements")
        if len(unquantified_sentences) > 3:
            suggestions.append("Several achievements lack quantification - add metrics to show impact")
        
        quantification_score = min(10, len(numbers) + len(percentages) * 2 + len(monetary) + len(timeframes))
        
        return {
            'numbers_count': len(numbers),
            'percentages_count': len(percentages),
            'monetary_count': len(monetary),
            'timeframes_count': len(timeframes),
            'sizes_count': len(sizes),
            'quantification_score': quantification_score,
            'unquantified_opportunities': len(unquantified_sentences),
            'suggestions': suggestions,
            'sample_unquantified': unquantified_sentences[:3]  # Show first 3 examples
        }