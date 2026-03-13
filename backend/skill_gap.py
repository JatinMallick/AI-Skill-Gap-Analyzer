def find_skill_gap(resume_skills, required_skills):

    missing_skills = []

    missing_skills = [skill for skill in required_skills if skill not in resume_skills]

    return missing_skills