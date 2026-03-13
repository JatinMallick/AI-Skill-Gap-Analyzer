def calculate_match_percentage(resume_skills, required_skills):

    matched = [skill for skill in required_skills if skill in resume_skills]

    score = (len(matched) / len(required_skills)) * 100

    return round(score, 2), matched