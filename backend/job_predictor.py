import joblib

model = joblib.load("models/job_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")


def recommend_job_roles(resume_skills, top_n=3):

    text = " ".join(resume_skills)

    X = vectorizer.transform([text])

    probabilities = model.predict_proba(X)[0]

    roles = model.classes_

    role_scores = list(zip(roles, probabilities))

    role_scores = sorted(role_scores, key=lambda x: x[1], reverse=True)

    return role_scores[:top_n]