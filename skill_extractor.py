from job_loader import load_job_description
from llm import create_llm
import json


def extract_skills(job_text):
    llm = create_llm()

    prompt = f"""
You are an expert technical recruiter.

Analyze the following job description and extract the technical skills.

Return ONLY valid JSON in exactly this format:

{{
    "required_skills": [],
    "preferred_skills": []
}}

Rules:
- Include only technical skills, tools, frameworks, platforms, databases,
  programming languages, and AI/ML technologies.
- Do not include soft skills.
- Do not add skills that are not mentioned in the job description.
- Keep skill names concise.
- Do not write explanations outside the JSON.

Job Description:
{job_text}
"""

    response = llm.invoke(prompt)

    return response


if __name__ == "__main__":
    # Change this filename to your actual job PDF
    job_path = r"C:\DATASCIENCE\MYPROJECTS\ResumeJobMatchAI\data\jobs\AI_Engineer_Job.pdf.pdf"

    documents = load_job_description(job_path)

    job_text = "\n".join(
        document.page_content for document in documents
    )

    result = extract_skills(job_text)

    print("\n===== EXTRACTED JOB SKILLS =====\n")
    print(result)