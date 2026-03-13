import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


df = pd.read_csv("data/dataset.csv")
df.columns = df.columns.str.lower().str.replace(" ", "_")

X = df["combined_text"]
y = df["job_title"]

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=3000,
    ngram_range=(1,2)
)

X_vectorized = vectorizer.fit_transform(X)

model = LogisticRegression(max_iter=1000)

model.fit(X_vectorized, y)

joblib.dump(model, "models/job_model.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("Model trained successfully")