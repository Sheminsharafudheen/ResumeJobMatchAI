from document_loader import load_pdf
from job_loader import load_job_description
from skill_database import SKILL_DATABASE
from skill_matcher import match_skills
from skill_extractor import extract_skills
from llm import create_llm


def detect_resume_skills(resume_text):
    """
    Detect skills directly from the resume text.
    This is more reliable than relying only on LLM extraction.
    """
    resume_text_lower = resume_text.lower()

    detected_skills = []

    for skill in SKILL_DATABASE:
        if skill.lower() in resume_text_lower:
            detected_skills.append(skill)

    return detected_skills


def extract_job_skills(job_text):
    """
    Use Ollama to extract required and preferred skills.
    """
    result = extract_skills(job_text)

    # We expect JSON from Ollama.
    import json

    try:
        return json.loads(result)
    except json.JSONDecodeError:
        # If Ollama adds extra text, try to find the JSON section.
        start = result.find("{")
        end = result.rfind("}") + 1

        if start != -1 and end != 0:
            return json.loads(result[start:end])

        raise ValueError("Could not parse job skills from LLM response.")


def calculate_match(required_skills, preferred_skills, resume_skills):

    required_matched, required_missing = match_skills(
        required_skills,
        resume_skills
    )

    preferred_matched, preferred_missing = match_skills(
        preferred_skills,
        resume_skills
    )

    # Required skill coverage
    required_score = (
        len(required_matched) / len(required_skills) * 100
        if required_skills else 0
    )

    # Preferred skill coverage
    preferred_score = (
        len(preferred_matched) / len(preferred_skills) * 100
        if preferred_skills else 0
    )

    # Final weighted score
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


if __name__ == "__main__":

    # =====================================================
    # FILE PATHS
    # =====================================================

    resume_path = r"C:\DATASCIENCE\MYPROJECTS\ResumeJobMatchAI\data\resume\Shemin_TS..pdf"
    job_path = r"C:\DATASCIENCE\MYPROJECTS\ResumeJobMatchAI\data\jobs\AI_Engineer_Job.pdf.pdf"

    # =====================================================
    # LOAD RESUME
    # =====================================================

    print("\nLoading resume...")

    resume_documents = load_pdf(resume_path)

    resume_text = "\n".join(
        document.page_content
        for document in resume_documents
    )

    # =====================================================
    # DETECT RESUME SKILLS
    # =====================================================

    print("Detecting resume skills...")

    resume_skills = detect_resume_skills(resume_text)

    print(f"Resume skills detected: {len(resume_skills)}")

    # =====================================================
    # LOAD JOB DESCRIPTION
    # =====================================================

    print("Loading job description...")

    job_documents = load_job_description(job_path)

    job_text = "\n".join(
        document.page_content
        for document in job_documents
    )

    # =====================================================
    # EXTRACT JOB SKILLS
    # =====================================================

    print("Extracting job skills using Ollama...")

    job_data = extract_job_skills(job_text)

    required_skills = job_data.get(
        "required_skills",
        []
    )

    preferred_skills = job_data.get(
        "preferred_skills",
        []
    )

    # =====================================================
    # CALCULATE MATCH
    # =====================================================

    print("Calculating match score...")

    result = calculate_match(
        required_skills,
        preferred_skills,
        resume_skills
    )

    # =====================================================
    # DISPLAY REPORT
    # =====================================================

    print("\n")
    print("=" * 60)
    print("             RESUME ↔ JOB MATCH REPORT")
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
        print(f"✓ {skill}")

    print("\n❌ MISSING REQUIRED SKILLS")

    for skill in result["required_missing"]:
        print(f"✗ {skill}")

    print("\n⭐ MATCHED PREFERRED SKILLS")

    for skill in result["preferred_matched"]:
        print(f"✓ {skill}")

    print("\n⚠️ MISSING PREFERRED SKILLS")

    for skill in result["preferred_missing"]:
        print(f"✗ {skill}")

    print("\n" + "=" * 60)