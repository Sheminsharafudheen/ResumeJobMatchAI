import json

from document_loader import load_pdf
from job_loader import load_job_description
from skill_database import SKILL_DATABASE
from skill_matcher import match_skills
from llm import create_llm


def detect_resume_skills(resume_text):
    """Detect known skills directly from resume text."""

    resume_text_lower = resume_text.lower()

    detected_skills = []

    for skill in SKILL_DATABASE:
        if skill.lower() in resume_text_lower:
            detected_skills.append(skill)

    return detected_skills


def extract_job_skills_with_llm(job_text):
    """Extract required and preferred skills using Gemini."""

    llm = create_llm()

    prompt = f"""
You are an expert technical recruiter.

Analyze the following job description and extract the technical skills.

Separate the skills into:
1. Required skills
2. Preferred skills

Return ONLY valid JSON.
Do not include explanations.
Do not use Markdown code fences.

Use exactly this format:

{{
    "required_skills": [],
    "preferred_skills": []
}}

Job Description:
{job_text}
"""

    response = llm.invoke(prompt)

    # Handle LangChain AIMessage
    if hasattr(response, "content"):
        response = response.content

    response = str(response).strip()

    # Remove Markdown code fences if Gemini adds them
    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    try:
        return json.loads(response)

    except json.JSONDecodeError:

        # Try to extract JSON from additional Gemini text
        start = response.find("{")
        end = response.rfind("}") + 1

        if start != -1 and end > start:

            try:
                return json.loads(
                    response[start:end]
                )

            except json.JSONDecodeError:
                pass

        raise ValueError(
            "Could not parse job skills from Gemini response."
        )


def calculate_match(
    required_skills,
    preferred_skills,
    resume_skills
):
    """Calculate skill coverage and final score."""

    required_matched, required_missing = match_skills(
        required_skills,
        resume_skills
    )

    preferred_matched, preferred_missing = match_skills(
        preferred_skills,
        resume_skills
    )

    required_score = (
        len(required_matched)
        / len(required_skills)
        * 100
        if required_skills
        else 0
    )

    preferred_score = (
        len(preferred_matched)
        / len(preferred_skills)
        * 100
        if preferred_skills
        else 0
    )

    # Required skills are more important than preferred skills
    final_score = (
        required_score * 0.70
        + preferred_score * 0.20
    )

    return {
        "final_score": round(final_score, 2),
        "required_score": round(required_score, 2),
        "preferred_score": round(preferred_score, 2),

        "required_matched": required_matched,
        "required_missing": required_missing,

        "preferred_matched": preferred_matched,
        "preferred_missing": preferred_missing,
    }


def generate_recommendations(
    missing_required,
    missing_preferred,
    matched_skills,
    match_score
):
    """Generate AI-powered improvement recommendations using Gemini."""

    llm = create_llm()

    prompt = f"""
You are an AI/ML career advisor.

Analyze this resume-job match.

Match Score:
{match_score}%

Matched Skills:
{", ".join(matched_skills) if matched_skills else "None"}

Missing Required Skills:
{", ".join(missing_required) if missing_required else "None"}

Missing Preferred Skills:
{", ".join(missing_preferred) if missing_preferred else "None"}

Give concise and practical recommendations.

Use exactly these sections:

1. Priority Skills to Learn
2. Resume Improvement Suggestions
3. Project Suggestions
4. Interview Preparation

Focus mainly on missing required skills.

Do not recommend skills that are already matched.
"""

    response = llm.invoke(prompt)

    if hasattr(response, "content"):
        return response.content

    return str(response)


def analyze(resume_path, job_path):

    print("\nLoading resume...")

    resume_documents = load_pdf(resume_path)

    resume_text = "\n".join(
        document.page_content
        for document in resume_documents
    )

    print("Detecting resume skills...")

    resume_skills = detect_resume_skills(
        resume_text
    )

    print(
        f"Resume skills detected: "
        f"{len(resume_skills)}"
    )

    print("\nLoading job description...")

    job_documents = load_job_description(
        job_path
    )

    job_text = "\n".join(
        document.page_content
        for document in job_documents
    )

    print("Extracting job skills using Gemini...")

    job_data = extract_job_skills_with_llm(
        job_text
    )

    required_skills = job_data.get(
        "required_skills",
        []
    )

    preferred_skills = job_data.get(
        "preferred_skills",
        []
    )

    print(
        f"Required skills found: "
        f"{len(required_skills)}"
    )

    print(
        f"Preferred skills found: "
        f"{len(preferred_skills)}"
    )

    print("Calculating match score...")

    result = calculate_match(
        required_skills,
        preferred_skills,
        resume_skills
    )

    # Combine matched required + preferred skills
    matched_skills = (
        result["required_matched"]
        + result["preferred_matched"]
    )

    print("Generating AI recommendations...")

    recommendations = generate_recommendations(
        result["required_missing"],
        result["preferred_missing"],
        matched_skills,
        result["final_score"]
    )

    result["resume_skills"] = resume_skills

    result["required_skills"] = required_skills

    result["preferred_skills"] = preferred_skills

    result["recommendations"] = recommendations

    return result


if __name__ == "__main__":

    resume_path = (
        r"C:\DATASCIENCE\MYPROJECTS\ResumeJobMatchAI"
        r"\data\resume\Shemin_TS..pdf"
    )

    job_path = (
        r"C:\DATASCIENCE\MYPROJECTS\ResumeJobMatchAI"
        r"\data\jobs\AI_Engineer_Job.pdf.pdf"
    )

    result = analyze(
        resume_path,
        job_path
    )

    print("\n")
    print("=" * 60)
    print("          RESUME ↔ JOB MATCH REPORT")
    print("=" * 60)

    print(
        f"\n🎯 FINAL MATCH SCORE: "
        f"{result['final_score']}%"
    )

    print(
        f"\nRequired Skill Coverage: "
        f"{result['required_score']}%"
    )

    print(
        f"Preferred Skill Coverage: "
        f"{result['preferred_score']}%"
    )

    print("\n" + "-" * 60)

    print("\n✅ MATCHED REQUIRED SKILLS")

    for skill in result["required_matched"]:
        print("✓", skill)

    print("\n❌ MISSING REQUIRED SKILLS")

    for skill in result["required_missing"]:
        print("✗", skill)

    print("\n⭐ MATCHED PREFERRED SKILLS")

    for skill in result["preferred_matched"]:
        print("✓", skill)

    print("\n⚠️ MISSING PREFERRED SKILLS")

    for skill in result["preferred_missing"]:
        print("✗", skill)

    print("\n" + "=" * 60)

    print("\n🤖 AI IMPROVEMENT RECOMMENDATIONS")
    print("=" * 60)

    print(result["recommendations"])

    print("\n" + "=" * 60)