import ast

def parse_skills(skills_str):
    """
    Parses a string representation of a list of skills into a clean python list.
    Args:
        skills_str (str): E.g., "['MS-Excel', 'HTML']" or a clean comma-separated string.
    Returns:
        list: Clean list of skills in lowercase.
    """
    if not skills_str:
        return []
    
    # Check if it looks like a stringified list
    if skills_str.startswith('[') and skills_str.endswith(']'):
        try:
            parsed_list = ast.literal_eval(skills_str)
            if isinstance(parsed_list, list):
                return [str(skill).strip().lower() for skill in parsed_list]
        except (ValueError, SyntaxError):
            pass
            
    # Fallback to simple comma splitting
    return [s.strip().lower() for s in skills_str.split(',') if s.strip()]

def get_skill_similarity(student_skills, internship_skills):
    """
    Computes a simple Jaccard similarity score between two skill sets.
    """
    if not internship_skills:
        return 0.0
    
    set1 = set(student_skills)
    set2 = set(internship_skills)
    
    if not set2:
        return 0.0
        
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    
    return len(intersection) / len(union) if union else 0.0
