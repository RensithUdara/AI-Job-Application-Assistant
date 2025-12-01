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