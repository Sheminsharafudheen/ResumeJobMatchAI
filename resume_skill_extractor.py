from document_loader import load_pdf
from llm import create_llm
import json


def extract_resume_skills(resume_text):
    llm = create_llm()

    prompt = f"""
You are an expert technical recruiter.

Analyze the following resume and extract ONLY the technical skills
that the candidate actually lists or demonstrates.

Return ONLY valid JSON in exactly this format:

{{
    "skills": []
}}

Rules:
- Include programming languages.
- Include AI/ML/DL technologies.
- Include frameworks and libraries.
- Include databases.
- Include developer tools.
- Include cloud/platform technologies if mentioned.
- Do not include soft skills.
- Do not invent skills.
- Keep skill names concise.
- Do not write explanations outside the JSON.

Resume:
{resume_text}
"""

    response = llm.invoke(prompt)

    return response


if __name__ == "__main__":
    # Change this to your actual resume filename
    resume_path = r"C:\DATASCIENCE\MYPROJECTS\ResumeJobMatchAI\data\resume\Shemin_TS..pdf"

    documents = load_pdf(resume_path)

    resume_text = "\n".join(
        document.page_content for document in documents
    )

    result = extract_resume_skills(resume_text)

    print("\n===== EXTRACTED RESUME SKILLS =====\n")
    print(result)