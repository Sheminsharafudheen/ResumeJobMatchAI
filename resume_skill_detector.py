from document_loader import load_pdf
from skill_database import SKILL_DATABASE


def detect_skills(resume_text):
    resume_text_lower = resume_text.lower()

    detected_skills = []

    for skill in SKILL_DATABASE:
        if skill.lower() in resume_text_lower:
            detected_skills.append(skill)

    return detected_skills


if __name__ == "__main__":

    resume_path = r"C:\DATASCIENCE\MYPROJECTS\ResumeJobMatchAI\data\resume\Shemin_TS..pdf"

    documents = load_pdf(resume_path)

    resume_text = "\n".join(
        document.page_content for document in documents
    )

    skills = detect_skills(resume_text)

    print("\n===== DETECTED RESUME SKILLS =====")
    print("Total skills found:", len(skills))

    for skill in skills:
        print("✓", skill)