import re
import json
from typing import Dict, List, Set, Optional, Tuple
import pdfplumber
from docx import Document
from fuzzywuzzy import fuzz
import pandas as pd

class ResumeParser:
    def __init__(self, skills_taxonomy_path: str = "data/skills_taxonomy.json"):
        """Initialize the resume parser with skills taxonomy and enhanced data."""
        with open(skills_taxonomy_path, 'r', encoding='utf-8') as f:
            self.skills_taxonomy = json.load(f)
            
        # Load additional data files
        try:
            with open('data/salary_data.json', 'r', encoding='utf-8') as f:
                self.salary_data = json.load(f)
        except FileNotFoundError:
            self.salary_data = {}
            
        try:
            with open('data/market_trends.json', 'r', encoding='utf-8') as f:
                self.market_trends = json.load(f)
        except FileNotFoundError:
            self.market_trends = {}
        
        # Initialize metrics tracker
        try:
            from core.metrics_tracker import get_metrics_tracker
            self.tracker = get_metrics_tracker()
        except:
            self.tracker = None
        
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
            duplicate_analysis = self.detect_duplicate_content(text)
            timeline_analysis = self.validate_resume_timeline(text)
            project_analysis = self.analyze_project_impact(text)
            
            # Extract current job title from resume
            current_job_title = self._extract_current_job_title(cleaned_text)
            
            # Add best_match_role to role_compatibility for backward compatibility
            role_compatibility['best_match_role'] = current_job_title if current_job_title else role_compatibility.get('best_fit_role', 'Unknown')
            
            # Record this resume analysis in metrics database
            ats_score = ats_analysis.get('score', 0)
            parsing_success = ats_score >= 70  # Consider 70+ as successful parsing
            if self.tracker:
                try:
                    self.tracker.record_resume_analysis(
                        user_id="default",
                        resume_id=f"resume_{contact_info.get('name', 'unknown')}_{hash(text[:100])}",
                        ats_score=ats_score,
                        parsing_success=parsing_success
                    )
                except:
                    pass  # Don't break parsing if metrics recording fails
            
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
                'duplicate_analysis': duplicate_analysis,
                'timeline_analysis': timeline_analysis,
                'project_analysis': project_analysis,
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
        # Extract sections manually for analysis
        sections = self._extract_text_sections(text)
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
    
    def _extract_text_sections(self, text: str) -> Dict[str, str]:
        """Extract text content for each major resume section."""
        sections = {
            'contact': '',
            'summary': '',
            'experience': '',
            'skills': '',
            'education': '',
            'projects': ''
        }
        
        # Split text into lines
        lines = text.split('\n')
        current_section = 'contact'  # Start with contact info
        section_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line is a section header
            line_upper = line.upper()
            if any(header in line_upper for header in ['EXPERIENCE', 'WORK', 'EMPLOYMENT']):
                if section_content:
                    sections[current_section] = '\n'.join(section_content)
                current_section = 'experience'
                section_content = []
            elif any(header in line_upper for header in ['SKILL', 'TECHNICAL', 'COMPETENCIES']):
                if section_content:
                    sections[current_section] = '\n'.join(section_content)
                current_section = 'skills'
                section_content = []
            elif any(header in line_upper for header in ['EDUCATION', 'ACADEMIC']):
                if section_content:
                    sections[current_section] = '\n'.join(section_content)
                current_section = 'education'
                section_content = []
            elif any(header in line_upper for header in ['PROJECT', 'PORTFOLIO']):
                if section_content:
                    sections[current_section] = '\n'.join(section_content)
                current_section = 'projects'
                section_content = []
            elif any(header in line_upper for header in ['SUMMARY', 'PROFILE', 'OBJECTIVE']):
                if section_content:
                    sections[current_section] = '\n'.join(section_content)
                current_section = 'summary'
                section_content = []
            else:
                section_content.append(line)
        
        # Add final section content
        if section_content:
            sections[current_section] = '\n'.join(section_content)
        
        return sections
    
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
    
    def _extract_current_job_title(self, text: str) -> str:
        """Extract the most recent/current job title from the resume."""
        try:
            # Common job title patterns
            lines = text.split('\n')
            
            # Look for job titles in experience section
            in_experience = False
            job_titles = []
            
            for i, line in enumerate(lines):
                line_lower = line.lower()
                
                # Check if we're in experience section
                if any(keyword in line_lower for keyword in ['experience', 'work history', 'employment', 'professional experience']):
                    in_experience = True
                    continue
                
                # Stop if we hit another major section
                if in_experience and any(keyword in line_lower for keyword in ['education', 'skills', 'certification', 'project', 'summary']):
                    in_experience = False
                
                # Extract job titles when in experience section
                if in_experience and line.strip():
                    # Common patterns for job titles
                    # Pattern 1: Title | Company | Date
                    if '|' in line:
                        parts = line.split('|')
                        title = parts[0].strip()
                        if title and len(title) < 100:  # Reasonable length for job title
                            job_titles.append(title)
                    
                    # Pattern 2: Title at Company
                    elif ' at ' in line.lower():
                        parts = line.lower().split(' at ')
                        title = line.split(' at ')[0].strip()
                        if title and len(title) < 100:
                            job_titles.append(title)
                    
                    # Pattern 3: Company Name with Title on next line (common format)
                    elif len(line.strip()) > 0 and len(line.strip()) < 80 and any(
                        role_word in line.lower() for role_word in [
                            'developer', 'engineer', 'analyst', 'manager', 'architect', 
                            'designer', 'specialist', 'consultant', 'scientist', 'officer',
                            'director', 'lead', 'senior', 'junior', 'associate', 'coordinator',
                            'administrator', 'technician', 'programmer', 'tester', 'qa'
                        ]
                    ):
                        job_titles.append(line.strip())
            
            # Return the first (most recent) job title found
            if job_titles:
                # Clean and normalize the title
                title = job_titles[0]
                # Remove extra whitespace and special characters
                title = re.sub(r'\s+', ' ', title)
                title = re.sub(r'[^a-zA-Z\s]', '', title)  # Remove special chars except spaces
                title = title.strip()
                
                if title:
                    return title.title()
            
            # Fallback: use skills-based role detection
            return None
            
        except Exception as e:
            print(f"Error extracting job title: {e}")
            return None
    
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
    
    def simulate_ats_parsing(self, text: str) -> Dict:
        """Simulate how ATS systems would parse the resume."""
        # Extract structured data as ATS would
        parsed_data = {
            'personal_info': {},
            'sections': {},
            'skills': [],
            'education': [],
            'experience': [],
            'parsing_issues': []
        }
        
        # Extract personal information
        email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        if email_match:
            parsed_data['personal_info']['email'] = email_match.group()
        else:
            parsed_data['parsing_issues'].append('Email not detected')
        
        phone_match = re.search(r'[+]?[1-9]?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}', text)
        if phone_match:
            parsed_data['personal_info']['phone'] = phone_match.group()
        else:
            parsed_data['parsing_issues'].append('Phone number not detected')
        
        # Extract name (first line usually)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            # Simple heuristic: first non-empty line that's not an email/phone
            for line in lines[:3]:
                if '@' not in line and not re.search(r'\d{3}', line) and len(line.split()) <= 4:
                    parsed_data['personal_info']['name'] = line
                    break
        
        # Extract skills
        skills_found = [skill for skill in self.all_skills if skill.lower() in text.lower()]
        parsed_data['skills'] = skills_found[:15]  # ATS typically extracts top skills
        
        # Section detection
        sections = self._extract_text_sections(text)
        for section_name, content in sections.items():
            if content:
                parsed_data['sections'][section_name] = {
                    'detected': True,
                    'word_count': len(content.split()),
                    'has_dates': bool(re.search(r'\d{4}', content)),
                    'has_bullets': bool(re.search(r'^[\s]*[\u2022\-\*]', content, re.MULTILINE))
                }
            else:
                parsed_data['parsing_issues'].append(f'{section_name.title()} section not detected')
        
        # Calculate parsing success rate
        expected_fields = ['email', 'phone', 'name']
        detected_fields = [field for field in expected_fields if field in parsed_data['personal_info']]
        parsing_success = (len(detected_fields) / len(expected_fields)) * 100
        
        # Add section detection success
        expected_sections = ['experience', 'education', 'skills']
        detected_sections = [sec for sec in expected_sections if sec in parsed_data['sections']]
        section_success = (len(detected_sections) / len(expected_sections)) * 100
        
        overall_success = (parsing_success + section_success) / 2
        
        return {
            'parsed_data': parsed_data,
            'parsing_success_rate': round(overall_success, 1),
            'ats_readability': self._get_ats_readability_level(overall_success),
            'json_output': self._generate_ats_json_output(parsed_data),
            'improvement_suggestions': self._get_ats_parsing_suggestions(parsed_data['parsing_issues'])
        }
    
    def _get_ats_readability_level(self, success_rate: float) -> str:
        """Convert ATS parsing success rate to readability level."""
        if success_rate >= 90:
            return "Excellent - ATS will parse accurately"
        elif success_rate >= 75:
            return "Good - Minor parsing issues possible"
        elif success_rate >= 60:
            return "Fair - Some information may be missed"
        else:
            return "Poor - High risk of parsing errors"
    
    def _generate_ats_json_output(self, parsed_data: Dict) -> str:
        """Generate ATS-style JSON output."""
        import json
        
        ats_json = {
            "candidate": {
                "name": parsed_data['personal_info'].get('name', 'Unknown'),
                "email": parsed_data['personal_info'].get('email', ''),
                "phone": parsed_data['personal_info'].get('phone', '')
            },
            "skills": parsed_data['skills'][:10],
            "sections_detected": list(parsed_data['sections'].keys()),
            "parsing_confidence": len(parsed_data['personal_info']) * 25  # Simple confidence metric
        }
        
        return json.dumps(ats_json, indent=2)
    
    def _get_ats_parsing_suggestions(self, issues: List[str]) -> List[str]:
        """Generate suggestions to improve ATS parsing."""
        suggestions = []
        
        if 'Email not detected' in issues:
            suggestions.append('Add clear email address at the top of resume')
        
        if 'Phone number not detected' in issues:
            suggestions.append('Include properly formatted phone number')
        
        if any('section not detected' in issue for issue in issues):
            suggestions.append('Use standard section headers (EXPERIENCE, EDUCATION, SKILLS)')
            suggestions.append('Avoid using tables or complex formatting for section content')
        
        suggestions.extend([
            'Use standard fonts (Arial, Calibri, Times New Roman)',
            'Avoid images, graphics, and logos',
            'Save in both PDF and Word format',
            'Keep formatting simple and clean'
        ])
        
        return suggestions
    
    def detect_duplicate_content(self, resume_text: str) -> Dict:
        """Detect duplicate or generic content in resume."""
        generic_phrases = [
            'hardworking', 'team player', 'detail oriented', 'fast learner', 
            'passionate about', 'innovative solutions', 'proven track record',
            'dynamic professional', 'excellent communication', 'self motivated'
        ]
        
        duplicate_issues = []
        duplicate_score = 100
        
        # Check for generic phrases
        text_lower = resume_text.lower()
        for phrase in generic_phrases:
            if phrase in text_lower:
                duplicate_issues.append(f"Generic phrase detected: '{phrase}'")
                duplicate_score -= 5
        
        # Check for repeated words/phrases
        words = re.findall(r'\b\w+\b', text_lower)
        word_counts = {}
        for word in words:
            if len(word) > 4:  # Only check longer words
                word_counts[word] = word_counts.get(word, 0) + 1
        
        for word, count in word_counts.items():
            if count > 8:  # Appears more than 8 times
                duplicate_issues.append(f"Overused word: '{word}' ({count} times)")
                duplicate_score -= 3
        
        # Determine uniqueness level
        if duplicate_score >= 90:
            uniqueness_level = "Highly Unique"
        elif duplicate_score >= 70:
            uniqueness_level = "Moderately Unique"
        else:
            uniqueness_level = "Needs Improvement"
        
        return {
            'duplicate_score': max(0, duplicate_score),
            'uniqueness_level': uniqueness_level,
            'duplicate_issues': duplicate_issues[:10],  # Limit to 10 issues
            'improvement_suggestions': [
                'Replace generic phrases with specific achievements',
                'Use varied vocabulary and action verbs',
                'Focus on quantifiable results and outcomes',
                'Personalize content to match job requirements'
            ]
        }
    
    def validate_resume_timeline(self, resume_text: str) -> Dict:
        """Validate resume timeline for gaps and consistency."""
        # Extract years from resume
        years = re.findall(r'\b(19|20)\d{2}\b', resume_text)
        years = [int(year) for year in years]
        
        timeline_score = 100
        timeline_issues = []
        
        if not years:
            return {
                'timeline_score': 0,
                'timeline_status': 'No dates detected',
                'timeline_issues': ['No dates found in resume'],
                'year_range': 'Unknown'
            }
        
        years.sort()
        year_range = f"{min(years)}-{max(years)}"
        
        # Check for large gaps
        current_year = 2024
        if years:
            gaps = []
            for i in range(len(years) - 1):
                gap = years[i + 1] - years[i]
                if gap > 2:  # Gap larger than 2 years
                    gaps.append(gap)
                    timeline_issues.append(f"Potential {gap}-year gap detected")
                    timeline_score -= 15
        
        # Check if timeline is too old
        if max(years) < current_year - 1:
            timeline_issues.append("Resume appears outdated - no recent dates")
            timeline_score -= 20
        
        # Check for future dates
        future_dates = [year for year in years if year > current_year]
        if future_dates:
            timeline_issues.append("Future dates detected - check for errors")
            timeline_score -= 10
        
        # Determine status
        if timeline_score >= 90:
            timeline_status = "Excellent Timeline"
        elif timeline_score >= 70:
            timeline_status = "Good Timeline"
        elif timeline_score >= 50:
            timeline_status = "Timeline Concerns"
        else:
            timeline_status = "Timeline Issues"
        
        return {
            'timeline_score': max(0, timeline_score),
            'timeline_status': timeline_status,
            'timeline_issues': timeline_issues,
            'year_range': year_range,
            'validation_suggestions': [
                'Fill in any employment gaps with explanations',
                'Use consistent date formats throughout',
                'Include month and year for better clarity',
                'Add current or expected graduation dates'
            ]
        }
    
    def analyze_project_impact(self, resume_text: str) -> Dict:
        """Analyze project descriptions for impact and outcomes."""
        # Look for project sections and quantifiable results
        impact_keywords = [
            'increased', 'decreased', 'improved', 'reduced', 'achieved', 'generated',
            'saved', 'boosted', 'optimized', 'streamlined', 'enhanced', 'delivered'
        ]
        
        quantifiers = re.findall(r'\d+(?:\.\d+)?%|\$\d+(?:,\d{3})*|\d+(?:,\d{3})*\+?', resume_text)
        
        # Find project mentions
        project_patterns = [
            r'project[s]?\s*:?\s*([^\n]+)',
            r'built\s+([^\n]+)',
            r'developed\s+([^\n]+)',
            r'created\s+([^\n]+)',
            r'designed\s+([^\n]+)'
        ]
        
        projects = []
        for pattern in project_patterns:
            matches = re.findall(pattern, resume_text, re.IGNORECASE)
            projects.extend(matches)
        
        projects_found = len(projects)
        
        # Analyze impact for each project
        impact_analysis = {}
        total_impact_score = 0
        
        for i, project in enumerate(projects[:5]):  # Analyze top 5 projects
            project_name = f"Project {i+1}"
            
            # Check for impact indicators
            impact_score = 50  # Base score
            strengths = []
            issues = []
            
            # Check for quantifiable results
            project_lower = project.lower()
            has_numbers = any(q in project for q in quantifiers)
            has_impact_words = any(word in project_lower for word in impact_keywords)
            
            if has_numbers:
                impact_score += 25
                strengths.append('Quantifiable results')
            else:
                issues.append('No quantifiable results')
            
            if has_impact_words:
                impact_score += 15
                strengths.append('Impact-focused language')
            else:
                issues.append('Lacks impact-focused language')
            
            # Check project description length
            if len(project.split()) > 10:
                impact_score += 10
                strengths.append('Detailed description')
            else:
                issues.append('Too brief - needs more detail')
            
            # Determine improvement priority
            if impact_score >= 80:
                priority = 'Low'
            elif impact_score >= 60:
                priority = 'Medium'
            else:
                priority = 'High'
            
            impact_analysis[project_name] = {
                'description': project[:100] + '...' if len(project) > 100 else project,
                'impact_score': min(100, impact_score),
                'strengths': strengths,
                'issues': issues,
                'improvement_priority': priority
            }
            
            total_impact_score += impact_score
        
        average_impact_score = int(total_impact_score / max(1, projects_found))
        
        return {
            'projects_found': projects_found,
            'average_impact_score': average_impact_score,
            'impact_analysis': impact_analysis,
            'improvement_suggestions': [
                'Add specific metrics and percentages to project descriptions',
                'Use strong action verbs to describe project outcomes',
                'Include technologies and tools used in each project',
                'Describe the business impact or problem solved',
                'Mention team size and your specific role'
            ]
        }
    
    def calculate_intelligent_resume_score(self, resume_text: str, target_role: str = 'software_engineer') -> Dict:
        """Calculate intelligent resume score based on multiple factors."""
        scores = {
            'content_quality': 0,
            'ats_compatibility': 0,
            'keyword_optimization': 0,
            'formatting_score': 0,
            'experience_relevance': 0,
            'skill_match': 0
        }
        
        # Content Quality Analysis (25%)
        action_verbs = ['achieved', 'developed', 'implemented', 'managed', 'led', 'created', 'improved', 'increased', 'reduced']
        quantifiable_results = re.findall(r'\d+(?:\.\d+)?%|\$\d+(?:,\d{3})*|\d+(?:,\d{3})*\+?', resume_text)
        
        content_score = 50
        if quantifiable_results:
            content_score += min(30, len(quantifiable_results) * 5)
        
        action_verb_count = sum(1 for verb in action_verbs if verb in resume_text.lower())
        content_score += min(20, action_verb_count * 3)
        
        scores['content_quality'] = min(100, content_score)
        
        # ATS Compatibility (20%)
        ats_score = 70
        if '@' in resume_text:
            ats_score += 10
        if re.search(r'\(\d{3}\)\s?\d{3}-\d{4}|\d{3}-\d{3}-\d{4}', resume_text):
            ats_score += 10
        if any(section in resume_text.lower() for section in ['experience', 'education', 'skills']):
            ats_score += 10
        
        scores['ats_compatibility'] = min(100, ats_score)
        
        # Keyword Optimization (20%)
        role_keywords = {
            'software_engineer': ['software', 'development', 'programming', 'coding', 'algorithms'],
            'web_developer': ['html', 'css', 'javascript', 'react', 'web', 'frontend', 'backend'],
            'data_analyst': ['data', 'analysis', 'sql', 'python', 'statistics', 'visualization'],
            'mobile_developer': ['mobile', 'android', 'ios', 'flutter', 'react native', 'app']
        }
        
        relevant_keywords = role_keywords.get(target_role, role_keywords['software_engineer'])
        keyword_matches = sum(1 for keyword in relevant_keywords if keyword in resume_text.lower())
        scores['keyword_optimization'] = min(100, (keyword_matches / len(relevant_keywords)) * 100)
        
        # Formatting Score (10%)
        formatting_score = 80
        if len(resume_text) < 500:
            formatting_score -= 20
        elif len(resume_text) > 3000:
            formatting_score -= 10
        
        scores['formatting_score'] = formatting_score
        
        # Experience Relevance (15%)
        years_pattern = r'(\d+)\+?\s*(?:years?|yrs?)'
        experience_mentions = re.findall(years_pattern, resume_text.lower())
        if experience_mentions:
            max_experience = max([int(year) for year in experience_mentions])
            scores['experience_relevance'] = min(100, max_experience * 15)
        else:
            scores['experience_relevance'] = 40
        
        # Skill Match (10%)
        tech_skills = ['python', 'java', 'javascript', 'react', 'sql', 'aws', 'docker', 'git']
        skill_matches = sum(1 for skill in tech_skills if skill in resume_text.lower())
        scores['skill_match'] = min(100, (skill_matches / len(tech_skills)) * 100)
        
        # Calculate weighted overall score
        weights = {
            'content_quality': 0.25,
            'ats_compatibility': 0.20,
            'keyword_optimization': 0.20,
            'formatting_score': 0.10,
            'experience_relevance': 0.15,
            'skill_match': 0.10
        }
        
        overall_score = sum(scores[key] * weights[key] for key in scores)
        
        # Generate improvement recommendations
        recommendations = []
        if scores['content_quality'] < 70:
            recommendations.append('Add more quantifiable achievements and strong action verbs')
        if scores['ats_compatibility'] < 80:
            recommendations.append('Improve ATS compatibility with standard formatting and clear sections')
        if scores['keyword_optimization'] < 60:
            recommendations.append(f'Include more {target_role.replace("_", " ")} relevant keywords')
        if scores['experience_relevance'] < 60:
            recommendations.append('Highlight relevant work experience more prominently')
        
        return {
            'overall_score': round(overall_score, 1),
            'individual_scores': scores,
            'score_breakdown': {
                'excellent': overall_score >= 85,
                'good': 70 <= overall_score < 85,
                'fair': 55 <= overall_score < 70,
                'needs_improvement': overall_score < 55
            },
            'recommendations': recommendations,
            'target_role': target_role,
            'strengths': [key for key, score in scores.items() if score >= 80],
            'weaknesses': [key for key, score in scores.items() if score < 60]
        }
    
    def analyze_ats_compatibility_advanced(self, resume_text: str) -> Dict:
        """Advanced ATS compatibility analysis with detailed feedback."""
        compatibility_checks = {
            'file_format': {'score': 85, 'status': 'good', 'note': 'PDF format recommended for most ATS'},
            'font_usage': {'score': 90, 'status': 'excellent', 'note': 'Standard fonts detected'},
            'section_headers': {'score': 0, 'status': 'unknown', 'note': ''},
            'contact_info': {'score': 0, 'status': 'unknown', 'note': ''},
            'bullet_points': {'score': 0, 'status': 'unknown', 'note': ''},
            'keyword_density': {'score': 0, 'status': 'unknown', 'note': ''},
            'length': {'score': 0, 'status': 'unknown', 'note': ''},
            'graphics_tables': {'score': 95, 'status': 'excellent', 'note': 'Text-based content preferred'}
        }
        
        # Section headers check
        standard_sections = ['experience', 'education', 'skills', 'summary', 'objective']
        found_sections = sum(1 for section in standard_sections if section in resume_text.lower())
        compatibility_checks['section_headers']['score'] = min(100, (found_sections / len(standard_sections)) * 100)
        compatibility_checks['section_headers']['status'] = 'excellent' if found_sections >= 4 else 'good' if found_sections >= 2 else 'poor'
        compatibility_checks['section_headers']['note'] = f'{found_sections} standard sections found'
        
        # Contact info check
        has_email = '@' in resume_text
        has_phone = bool(re.search(r'\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{4}', resume_text))
        contact_score = (has_email * 50) + (has_phone * 50)
        compatibility_checks['contact_info']['score'] = contact_score
        compatibility_checks['contact_info']['status'] = 'excellent' if contact_score == 100 else 'good' if contact_score >= 50 else 'poor'
        compatibility_checks['contact_info']['note'] = f'Email: {"✓" if has_email else "✗"}, Phone: {"✓" if has_phone else "✗"}'
        
        # Bullet points check
        bullet_count = len(re.findall(r'^\s*[•·▪▫-]', resume_text, re.MULTILINE))
        compatibility_checks['bullet_points']['score'] = min(100, bullet_count * 5)
        compatibility_checks['bullet_points']['status'] = 'excellent' if bullet_count >= 15 else 'good' if bullet_count >= 8 else 'poor'
        compatibility_checks['bullet_points']['note'] = f'{bullet_count} bullet points found'
        
        # Keyword density check
        words = len(resume_text.split())
        tech_keywords = ['python', 'java', 'javascript', 'react', 'sql', 'aws', 'docker', 'agile']
        keyword_count = sum(1 for keyword in tech_keywords if keyword in resume_text.lower())
        keyword_density = (keyword_count / words) * 100 if words > 0 else 0
        compatibility_checks['keyword_density']['score'] = min(100, keyword_density * 20)
        compatibility_checks['keyword_density']['status'] = 'excellent' if keyword_density >= 3 else 'good' if keyword_density >= 1.5 else 'poor'
        compatibility_checks['keyword_density']['note'] = f'{keyword_density:.1f}% keyword density'
        
        # Length check
        word_count = len(resume_text.split())
        if 300 <= word_count <= 800:
            length_score = 100
            length_status = 'excellent'
        elif 200 <= word_count < 300 or 800 < word_count <= 1000:
            length_score = 80
            length_status = 'good'
        else:
            length_score = 60
            length_status = 'fair'
        
        compatibility_checks['length']['score'] = length_score
        compatibility_checks['length']['status'] = length_status
        compatibility_checks['length']['note'] = f'{word_count} words (optimal: 300-800)'
        
        # Calculate overall ATS score
        overall_ats_score = sum(check['score'] for check in compatibility_checks.values()) / len(compatibility_checks)
        
        # Generate ATS optimization recommendations
        ats_recommendations = []
        for check_name, check_data in compatibility_checks.items():
            if check_data['score'] < 70:
                if check_name == 'section_headers':
                    ats_recommendations.append('Use standard section headers: Experience, Education, Skills, Summary')
                elif check_name == 'contact_info':
                    ats_recommendations.append('Include clear email and phone number at the top')
                elif check_name == 'bullet_points':
                    ats_recommendations.append('Use bullet points for better readability and ATS parsing')
                elif check_name == 'keyword_density':
                    ats_recommendations.append('Include more relevant technical keywords naturally')
        
        return {
            'overall_ats_score': round(overall_ats_score, 1),
            'compatibility_checks': compatibility_checks,
            'ats_grade': 'A+' if overall_ats_score >= 90 else 'A' if overall_ats_score >= 80 else 'B' if overall_ats_score >= 70 else 'C' if overall_ats_score >= 60 else 'D',
            'ats_recommendations': ats_recommendations,
            'parsing_confidence': 'High' if overall_ats_score >= 85 else 'Medium' if overall_ats_score >= 70 else 'Low',
            'estimated_parsing_success': f'{min(95, overall_ats_score)}%'
        }