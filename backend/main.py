from resume_parser import extract_resume_text
from skill_extractor import extract_skills, load_skills
from skill_gap import find_skill_gap
from visualizer import plot_skill_gap
from job_predictor import recommend_job_roles
from match_score import calculate_match_percentage

import pandas as pd


# Load dataset
df = pd.read_csv("data/dataset.csv")

# Normalize column names
df.columns = df.columns.str.lower().str.replace(" ", "_")


# Load resume
resume_path = "C:/Users/jatin/Desktop/skill_gap_analyzer/data/Resume final.pdf"

resume_text = extract_resume_text(resume_path)


# Load global skill list
skills_list = load_skills("data/skills.txt")


# Extract skills from resume
resume_skills = extract_skills(resume_text, skills_list)

resume_skills = [skill.strip().lower() for skill in resume_skills]


print("\nResume Skills:", resume_skills)


# Get job recommendations
recommendations = recommend_job_roles(resume_skills)

print("\nTop Career Matches:")

for role, score in recommendations:
    print(f"{role} — {round(score*100,2)}%")


# Best predicted role
predicted_role = recommendations[0][0]

print("\nPredicted Job Role:", predicted_role)


# Retrieve required skills for predicted role
required_skills = df[df["job_title"] == predicted_role]["skills"].values[0]

required_skills = [skill.strip().lower() for skill in required_skills.split(",")]


print("\nRequired Skills:", required_skills)
match_score, matched_skills = calculate_match_percentage(
    resume_skills,
    required_skills
)

print("\nMatched Skills:", matched_skills)

print("\nMatch Score:", match_score, "%")

# Skill gap detection
missing_skills = find_skill_gap(resume_skills, required_skills)

print("\nMissing Skills:", missing_skills)


# Visualization
plot_skill_gap(resume_skills, required_skills)