from pdfminer.high_level import extract_text

def extract_resume_text(pdf_path):
    text = extract_text(pdf_path)
    return text.lower()

if __name__ == "__main__":
    resume_text = extract_resume_text(r"C:\Users\jatin\Desktop\skill_gap_analyzer\data\Resume final.pdf")
    print(resume_text)