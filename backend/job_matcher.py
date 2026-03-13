from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from resume_parser import extract_resume_text
from skill_extractor import extract_skills, load_skills
from job_analyzer import extract_job_skills


def calculate_match_score(resume_skills, job_skills):

    documents = [
        " ".join(resume_skills),
        " ".join(job_skills)
    ]

    vectorizer = TfidfVectorizer(stop_words="english")

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    score = similarity[0][0] * 100

    return round(score, 2)


if __name__ == "__main__":

    resume_path = "C:/Users/jatin/Desktop/skill_gap_analyzer/data/Resume final.pdf"

    resume_text = extract_resume_text(resume_path)

    skills_list = load_skills(r"C:\Users\jatin\Desktop\skill_gap_analyzer\data\skills.txt")

    resume_skills = extract_skills(resume_text, skills_list)

    job_description = """
    Looking for a Data Scientist with Python, SQL, Machine Learning,
    Docker and AWS experience.
    """

    job_skills = extract_job_skills(job_description, skills_list)

    match_score = calculate_match_score(resume_skills, job_skills)
    missing_skills = [skill for skill in job_skills if skill not in resume_skills]
    print("Resume Skills:", resume_skills)
    print("Job Skills:", job_skills)
    print("Missing skills",missing_skills)
    print("Resume Match Score:", match_score, "%")