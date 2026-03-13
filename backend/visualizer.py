import matplotlib.pyplot as plt


def plot_skill_gap(resume_skills, job_skills):

    matching_skills = [skill for skill in job_skills if skill in resume_skills]
    missing_skills = [skill for skill in job_skills if skill not in resume_skills]

    labels = ['Matching Skills', 'Missing Skills']
    values = [len(matching_skills), len(missing_skills)]

    plt.bar(labels, values)

    plt.title("Resume vs Job Skill Comparison")
    plt.ylabel("Number of Skills")

    plt.show()