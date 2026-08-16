from llm import create_llm


def generate_recommendations(
    missing_required,
    missing_preferred,
    matched_skills,
    match_score
):
    llm = create_llm()

    prompt = f"""
You are an expert AI/ML career advisor.

Analyze the candidate's resume-job match information below.

Match Score:
{match_score}%

Matched Skills:
{", ".join(matched_skills)}

Missing Required Skills:
{", ".join(missing_required)}

Missing Preferred Skills:
{", ".join(missing_preferred)}

Provide practical recommendations to improve the candidate's
fit for this job.

Your response must contain exactly these sections:

1. Priority Skills to Learn
2. Resume Improvement Suggestions
3. Project Suggestions
4. Interview Preparation

Rules:
- Focus mainly on missing required skills.
- Then discuss preferred skills.
- Do not recommend skills that are already matched.
- Give practical and realistic advice for a fresher.
- Keep the answer concise and actionable.
"""

    response = llm.invoke(prompt)

    return response


if __name__ == "__main__":

    missing_required = [
        "Embeddings",
        "FastAPI"
    ]

    missing_preferred = [
        "AWS",
        "Azure",
        "Docker",
        "Hugging Face",
        "PyTorch"
    ]

    matched_skills = [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "Generative AI",
        "LLMs",
        "RAG",
        "LangChain",
        "Vector Databases",
        "SQL",
        "Git",
        "GitHub",
        "TensorFlow"
    ]

    match_score = 62.56

    recommendations = generate_recommendations(
        missing_required,
        missing_preferred,
        matched_skills,
        match_score
    )

    print("\n========================================")
    print("       AI IMPROVEMENT RECOMMENDATIONS")
    print("========================================\n")

    print(recommendations)