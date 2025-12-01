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
            
            # Advanced analysis features
            heatmap_analysis = self.generate_resume_weakness_heatmap(text)
            consistency_analysis = self.check_resume_consistency(text)
            role_compatibility = self.calculate_role_compatibility_scores(text)
            ats_simulation = self.simulate_ats_parsing(text)
            
            return {
                'raw_text': text,
                'cleaned_text': cleaned_text,
                'sections_found': sections_found,
                'missing_sections': self._get_missing_sections(sections_found),
                'contact_info': contact_info,
                'resume_skills': resume_skills,
                'quality_score': quality_score,
                'ats_analysis': ats_analysis,
                'heatmap_analysis': heatmap_analysis,
                'consistency_analysis': consistency_analysis,
                'role_compatibility': role_compatibility,
                'ats_simulation': ats_simulation,
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
    
    def generate_resume_weakness_heatmap(self, text: str) -> Dict:
        """Generate visual heatmap of resume strengths and weaknesses."""
        sections = self._parse_sections(text)
        heatmap_data = {}
        
        # Analyze each section for strength (0-100)
        for section_name, content in sections.items():
            if not content:
                heatmap_data[section_name] = {'strength': 0, 'color': '#ff4444', 'issues': ['Missing section']}
                continue
            
            strength_score = 50  # Base score
            issues = []
            
            # Word count analysis
            word_count = len(content.split())
            if word_count < 20:
                strength_score -= 20
                issues.append('Too brief')
            elif word_count > 200:
                strength_score -= 10
                issues.append('Too verbose')
            else:
                strength_score += 10
            
            # Keyword density
            if section_name == 'skills':
                skill_count = len([skill for skill in self.all_skills if skill in content.lower()])
                if skill_count >= 8:
                    strength_score += 20
                elif skill_count >= 4:
                    strength_score += 10
                else:
                    issues.append('Few skills detected')
            
            # Action verb presence for experience/projects
            if section_name in ['experience', 'projects']:
                strong_verbs = sum(1 for verb in self.strong_action_verbs if verb.lower() in content.lower())
                if strong_verbs >= 3:
                    strength_score += 15
                elif strong_verbs >= 1:
                    strength_score += 5
                else:
                    strength_score -= 10
                    issues.append('Lacks strong action verbs')
            
            # Quantification check
            if re.search(r'\d', content):
                strength_score += 10
            else:
                issues.append('Missing quantifiable metrics')
            
            # Determine color based on strength
            strength_score = max(0, min(100, strength_score))
            if strength_score >= 80:
                color = '#22c55e'  # Green
            elif strength_score >= 60:
                color = '#eab308'  # Yellow
            elif strength_score >= 40:
                color = '#f97316'  # Orange
            else:
                color = '#ef4444'  # Red
            
            heatmap_data[section_name] = {
                'strength': strength_score,
                'color': color,
                'issues': issues
            }
        
        return {
            'heatmap_data': heatmap_data,
            'overall_strength': sum(data['strength'] for data in heatmap_data.values()) / len(heatmap_data),
            'weakest_sections': sorted(heatmap_data.keys(), key=lambda k: heatmap_data[k]['strength'])[:3],
            'strongest_sections': sorted(heatmap_data.keys(), key=lambda k: heatmap_data[k]['strength'], reverse=True)[:3]
        }
    
    def check_resume_consistency(self, text: str) -> Dict:
        """Check for consistency issues in resume formatting and content."""
        issues = []
        consistency_score = 100
        
        # Check date formats
        date_patterns = [
            r'\d{4}\s*-\s*\d{4}',  # 2019 - 2021
            r'\d{2}\s*-\s*\d{2}',  # 19 - 21
            r'\w+\s+\d{4}',        # January 2019
            r'\d{1,2}/\d{4}'       # 01/2019
        ]
        
        date_formats_found = []
        for pattern in date_patterns:
            if re.search(pattern, text):
                date_formats_found.append(pattern)
        
        if len(date_formats_found) > 1:
            issues.append('Mixed date formats detected')
            consistency_score -= 15
        
        # Check bullet point consistency
        bullet_patterns = [r'^\s*•', r'^\s*-', r'^\s*\*']
        bullet_types_found = []
        for pattern in bullet_patterns:
            if re.search(pattern, text, re.MULTILINE):
                bullet_types_found.append(pattern)
        
        if len(bullet_types_found) > 1:
            issues.append('Inconsistent bullet point styles')
            consistency_score -= 10
        
        # Check for mixed tenses
        past_tense_words = ['worked', 'developed', 'created', 'built', 'managed']
        present_tense_words = ['work', 'develop', 'create', 'build', 'manage']
        
        past_count = sum(1 for word in past_tense_words if word in text.lower())
        present_count = sum(1 for word in present_tense_words if word in text.lower())
        
        if past_count > 0 and present_count > 0 and abs(past_count - present_count) < 2:
            issues.append('Mixed verb tenses (past/present)')
            consistency_score -= 12
        
        # Check capitalization consistency
        section_headers = re.findall(r'^([A-Z][A-Z\s]+)$', text, re.MULTILINE)
        if section_headers:
            all_caps = all(header.isupper() for header in section_headers)
            title_case = all(header.istitle() for header in section_headers)
            
            if not (all_caps or title_case):
                issues.append('Inconsistent section header capitalization')
                consistency_score -= 8
        
        return {
            'consistency_score': max(0, consistency_score),
            'issues_found': issues,
            'consistency_level': self._get_consistency_level(consistency_score),
            'recommendations': self._get_consistency_recommendations(issues)
        }
    
    def _get_consistency_level(self, score: int) -> str:
        """Convert consistency score to level."""
        if score >= 90:
            return "Excellent - Highly consistent"
        elif score >= 75:
            return "Good - Minor inconsistencies"
        elif score >= 60:
            return "Fair - Some consistency issues"
        else:
            return "Poor - Major consistency problems"
    
    def _get_consistency_recommendations(self, issues: List[str]) -> List[str]:
        """Generate recommendations based on consistency issues."""
        recommendations = []
        
        if 'Mixed date formats' in str(issues):
            recommendations.append("Standardize all dates to same format (e.g., 'Jan 2019 - Dec 2021')")
        
        if 'Inconsistent bullet' in str(issues):
            recommendations.append("Use consistent bullet points throughout (• or - but not both)")
        
        if 'Mixed verb tenses' in str(issues):
            recommendations.append("Use past tense for previous roles, present tense for current role")
        
        if 'capitalization' in str(issues):
            recommendations.append("Standardize section headers (all CAPS or Title Case)")
        
        return recommendations
    
    def calculate_role_compatibility_scores(self, text: str, target_roles: List[str] = None) -> Dict:
        """Calculate compatibility scores for different roles."""
        if not target_roles:
            target_roles = ['mobile_developer', 'web_developer', 'data_analyst', 'software_engineer']
        
        role_keywords = {
            'mobile_developer': ['flutter', 'android', 'ios', 'kotlin', 'swift', 'react native', 'mobile', 'app store'],
            'web_developer': ['javascript', 'react', 'html', 'css', 'node.js', 'angular', 'vue', 'web', 'frontend', 'backend'],
            'data_analyst': ['sql', 'python', 'excel', 'tableau', 'statistics', 'data', 'analytics', 'visualization'],
            'software_engineer': ['programming', 'algorithms', 'data structures', 'system design', 'api', 'database'],
            'devops_engineer': ['docker', 'kubernetes', 'aws', 'ci/cd', 'jenkins', 'terraform', 'cloud'],
            'full_stack_developer': ['frontend', 'backend', 'database', 'api', 'full stack', 'end-to-end']
        }
        
        text_lower = text.lower()
        role_scores = {}
        
        for role in target_roles:
            if role not in role_keywords:
                continue
            
            keywords = role_keywords[role]
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            
            # Calculate base score
            base_score = (matches / len(keywords)) * 100
            
            # Bonus for multiple mentions of same keyword
            keyword_frequency = sum(text_lower.count(keyword) for keyword in keywords)
            frequency_bonus = min(20, keyword_frequency * 2)
            
            # Experience relevance bonus
            experience_bonus = 0
            if 'experience' in text_lower and any(keyword in text_lower for keyword in keywords[:3]):
                experience_bonus = 15
            
            final_score = min(100, base_score + frequency_bonus + experience_bonus)
            
            role_scores[role] = {
                'score': round(final_score, 1),
                'matched_keywords': [kw for kw in keywords if kw in text_lower],
                'missing_keywords': [kw for kw in keywords if kw not in text_lower][:5],  # Top 5 missing
                'strength_level': self._get_role_strength_level(final_score)
            }
        
        # Find best fit
        best_role = max(role_scores.keys(), key=lambda k: role_scores[k]['score'])
        
        return {
            'role_scores': role_scores,
            'best_fit_role': best_role,
            'best_fit_score': role_scores[best_role]['score'],
            'role_recommendations': self._get_role_recommendations(role_scores)
        }
    
    def _get_role_strength_level(self, score: float) -> str:
        """Convert role compatibility score to strength level."""
        if score >= 80:
            return "Excellent Match"
        elif score >= 60:
            return "Good Match"
        elif score >= 40:
            return "Fair Match"
        elif score >= 20:
            return "Weak Match"
        else:
            return "Poor Match"
    
    def _get_role_recommendations(self, role_scores: Dict) -> List[str]:
        """Generate role-based recommendations."""
        recommendations = []
        
        # Find top 2 roles
        sorted_roles = sorted(role_scores.items(), key=lambda x: x[1]['score'], reverse=True)
        
        if len(sorted_roles) >= 2:
            best_role, best_data = sorted_roles[0]
            second_role, second_data = sorted_roles[1]
            
            if best_data['score'] >= 70:
                recommendations.append(f"Strong candidate for {best_role.replace('_', ' ').title()} roles")
            elif best_data['score'] >= 50:
                recommendations.append(f"Consider targeting {best_role.replace('_', ' ').title()} positions with skill enhancement")
            
            # Gap analysis
            if best_data['score'] < 60:
                missing = best_data['missing_keywords'][:3]
                recommendations.append(f"Focus on learning: {', '.join(missing)} to improve {best_role.replace('_', ' ')} compatibility")
        
        return recommendations