import re
from typing import List, Dict, Any

def clean_text(text: str) -> str:
    """Clean and normalize text for processing."""
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep alphanumeric and basic punctuation
    text = re.sub(r'[^\w\s@.\-+()]', ' ', text)
    
    return text.strip()

def extract_email(text: str) -> str:
    """Extract email address from text."""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else None

def extract_phone(text: str) -> str:
    """Extract phone number from text."""
    phone_patterns = [
        r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\+?\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\d{10,}'
    ]
    
    for pattern in phone_patterns:
        phones = re.findall(pattern, text)
        if phones:
            # Clean up the phone number
            phone = ''.join(phones[0]) if isinstance(phones[0], tuple) else phones[0]
            return re.sub(r'[^\d+]', '', phone)
    
    return None

def calculate_match_percentage(matched: int, total: int) -> float:
    """Calculate match percentage."""
    if total == 0:
        return 0.0
    return round((matched / total) * 100, 2)

def format_skills_list(skills: List[str], max_display: int = 10) -> str:
    """Format skills list for display."""
    if not skills:
        return "None"
    
    if len(skills) <= max_display:
        return ", ".join(skills)
    else:
        displayed = skills[:max_display]
        remaining = len(skills) - max_display
        return f"{', '.join(displayed)} and {remaining} more..."

def get_priority_color(priority: str) -> str:
    """Get color code for priority levels."""
    color_map = {
        'high': '🔴',
        'medium': '🟡', 
        'low': '🟢'
    }
    return color_map.get(priority.lower(), '⚪')

def get_match_score_color(score: float) -> str:
    """Get color indication for match scores."""
    if score >= 80:
        return '🟢'  # Green
    elif score >= 60:
        return '🟡'  # Yellow
    elif score >= 40:
        return '🟠'  # Orange
    else:
        return '🔴'  # Red

def format_experience_range(exp_text: str) -> str:
    """Format experience range text."""
    if not exp_text or exp_text.lower() == 'not specified':
        return "Experience level not specified"
    return f"Required experience: {exp_text}"

def get_section_status_icon(present: bool) -> str:
    """Get icon for section presence status."""
    return "✅" if present else "❌"

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def format_skill_categories(skills_by_category: Dict[str, List[str]]) -> Dict[str, str]:
    """Format skills by category for display."""
    formatted = {}
    for category, skills in skills_by_category.items():
        # Format category name
        category_name = category.replace('_', ' ').title()
        formatted[category_name] = format_skills_list(skills)
    return formatted

def validate_file_type(filename: str, allowed_types: List[str]) -> bool:
    """Validate if file type is allowed."""
    if not filename:
        return False
    
    file_extension = filename.lower().split('.')[-1]
    return file_extension in [ext.lower() for ext in allowed_types]

def safe_divide(numerator: float, denominator: float) -> float:
    """Safely divide two numbers, returning 0 if denominator is 0."""
    if denominator == 0:
        return 0.0
    return numerator / denominator

def extract_years_of_experience(text: str) -> int:
    """Extract years of experience from text."""
    patterns = [
        r'(\d+)\s*years?\s*(?:of\s*)?experience',
        r'(\d+)\+?\s*years?',
        r'minimum\s*(\d+)\s*years?'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        if matches:
            return int(matches[0])
    
    return 0

def categorize_seniority(years: int) -> str:
    """Categorize seniority level based on years of experience."""
    if years == 0:
        return "Entry Level"
    elif years <= 2:
        return "Junior"
    elif years <= 5:
        return "Mid Level"
    elif years <= 8:
        return "Senior"
    else:
        return "Principal/Lead"

def format_recommendation_priority(recommendations: List[Dict]) -> List[Dict]:
    """Sort and format recommendations by priority."""
    priority_order = {'high': 1, 'medium': 2, 'low': 3}
    
    sorted_recs = sorted(recommendations, 
                        key=lambda x: priority_order.get(x.get('priority', 'low'), 3))
    
    for rec in sorted_recs:
        rec['priority_icon'] = get_priority_color(rec.get('priority', 'low'))
    
    return sorted_recs