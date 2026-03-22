from model.preprocessing import parse_skills, get_skill_similarity
import re

def extract_stipend_value(stipend_str):
    """
    Tries to extract a numeric stipend value for sorting purposes.
    """
    if not stipend_str:
        return 0
    # Find all numbers in the string
    numbers = re.findall(r'\d+', stipend_str.replace(',', ''))
    if numbers:
        return int(numbers[0])
    return 0

def rank_internships(student_profile, internships):
    """
    Ranks a list of internships against a student's profile.
    Args:
        student_profile (dict): {'skills': 'Python, HTML', 'preferred_location': 'Remote'}
        internships (list of dicts): List of internship rows from DB.
    Returns:
        list of dicts: The internships sorted by match score.
    """
    student_skills_str = student_profile.get('skills', '')
    student_location = student_profile.get('preferred_location', '').lower()
    
    parsed_student_skills = parse_skills(student_skills_str)
    
    ranked_list = []
    
    for internship in internships:
        internship_skills_str = internship.get('skills_required', '')
        parsed_internship_skills = parse_skills(internship_skills_str)
        
        # Calculate skill score (0 to 1)
        skill_score = get_skill_similarity(parsed_student_skills, parsed_internship_skills)
        
        # Calculate location score (bonus for matching location or if internship is remote/WFH)
        loc = internship.get('location', '').lower()
        location_score = 0.0
        if student_location and (student_location in loc or 'work from home' in loc or 'remote' in loc):
            location_score = 0.5
        elif not student_location: # No preference
            location_score = 0.2
            
        # Optional: stipend score could also be a factor
        stipend_base = extract_stipend_value(internship.get('stipend', ''))
        stipend_score = min(stipend_base / 50000.0, 0.5) # Cap at 0.5
        
        # Total score combining factors
        total_score = (skill_score * 0.7) + (location_score * 0.2) + (stipend_score * 0.1)
        
        internship_dict = dict(internship)
        internship_dict['match_score'] = round(total_score * 100, 2)
        
        ranked_list.append(internship_dict)
        
    # Sort descending by match_score
    ranked_list.sort(key=lambda x: x['match_score'], reverse=True)
    return ranked_list
