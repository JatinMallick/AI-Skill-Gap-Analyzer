def extract_job_skills(job_description, skills_list):

    job_description = job_description.lower()

    job_skills = []

    for skill in skills_list:
        if skill in job_description:
            job_skills.append(skill)

    return job_skills


if __name__ == "__main__":

    from skill_extractor import load_skills

    skills = load_skills(r"C:\Users\jatin\Desktop\skill_gap_analyzer\data\skills.txt")

    job_description = """
    We are hiring a Data Scientist with Python, SQL, Machine Learning,
    Docker and AWS experience.
    """

    job_skills = extract_job_skills(job_description, skills)

    print("Required Job Skills:")
    print(job_skills)