from flask import Flask, render_template, request

import pandas as pd

from backend.resume_parser import extract_resume_text
from backend.skill_extractor import extract_skills, load_skills
from backend.job_predictor import recommend_job_roles
from backend.skill_gap import find_skill_gap
from backend.match_score import calculate_match_percentage


app = Flask(__name__)

df = pd.read_csv("data/dataset.csv")
df.columns = df.columns.str.lower().str.replace(" ", "_")

def _skills_from_dataset(dataframe: pd.DataFrame):
    if "skills" not in dataframe.columns:
        return []
    out = set()
    for cell in dataframe["skills"].dropna().astype(str).tolist():
        for s in cell.split(","):
            s = s.strip().lower()
            if s:
                out.add(s)
    return sorted(out)


# Use dataset skills as the primary dictionary, and merge in skills.txt (optional extra).
skills_list = sorted(set(_skills_from_dataset(df)) | set(load_skills("data/skills.txt")))


@app.route("/", methods=["GET", "POST"])
def index():

    result = None

    if request.method == "POST":

        resume_file = request.files["resume"]

        resume_path = "temp_resume.pdf"
        resume_file.save(resume_path)

        resume_text = extract_resume_text(resume_path)

        resume_skills = extract_skills(resume_text, skills_list)

        resume_skills = [skill.strip().lower() for skill in resume_skills]

        recommendations = recommend_job_roles(resume_skills)

        predicted_role = recommendations[0][0]

        required_skills = df[df["job_title"] == predicted_role]["skills"].values[0]

        required_skills = [skill.strip().lower() for skill in required_skills.split(",")]

        missing_skills = find_skill_gap(resume_skills, required_skills)

        match_score, matched_skills = calculate_match_percentage(
            resume_skills,
            required_skills
        )

        result = {
            "resume_skills": resume_skills,
            "recommended_roles": recommendations,
            "predicted_role": predicted_role,
            "required_skills": required_skills,
            "missing_skills": missing_skills,
            "match_score": match_score
        }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)