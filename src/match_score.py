from skill_matcher import match_skills


def calculate_score(required_skills, preferred_skills, resume_skills):
    # Match required skills
    required_matched, required_missing = match_skills(
        required_skills,
        resume_skills
    )

    # Match preferred skills
    preferred_matched, preferred_missing = match_skills(
        preferred_skills,
        resume_skills
    )

    # Calculate coverage
    required_score = (
        len(required_matched) / len(required_skills) * 100
        if required_skills else 0
    )

    preferred_score = (
        len(preferred_matched) / len(preferred_skills) * 100
        if preferred_skills else 0
    )

    # Weighted final score
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

    # Job requirements
    required_skills = [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "Generative AI",
        "LLMs",
        "RAG",
        "LangChain",
        "Embeddings",
        "Vector Databases",
        "SQL",
        "FastAPI",
        "Git",
        "GitHub"
    ]

    preferred_skills = [
        "AWS",
        "Azure",
        "Docker",
        "Hugging Face",
        "PyTorch",
        "TensorFlow"
    ]

    # Resume skills
    resume_skills = [
        "Python",
        "SQL",
        "R",
        "TensorFlow",
        "Keras",
        "Scikit-learn",
        "LangChain",
        "Ollama",
        "RAG",
        "Prompt Engineering",
        "MySQL",
        "Git",
        "GitHub",
        "Jupyter Notebook",
        "VS Code",
        "OpenCV",
        "MediaPipe",
        "NLTK",
        "TF-IDF",
        "Sentiment Analysis",
        "Pandas",
        "NumPy",
        "Matplotlib",
        "Seaborn"
    ]

    result = calculate_score(
        required_skills,
        preferred_skills,
        resume_skills
    )

    print("\n========================================")
    print("       RESUME ↔ JOB MATCH REPORT")
    print("========================================")

    print(f"\nFinal Match Score: {result['final_score']}%")

    print(f"\nRequired Skills Score: {result['required_score']}%")
    print(
        f"Matched: {len(result['required_matched'])}"
        f" / {len(required_skills)}"
    )

    print(f"\nPreferred Skills Score: {result['preferred_score']}%")
    print(
        f"Matched: {len(result['preferred_matched'])}"
        f" / {len(preferred_skills)}"
    )

    print("\n===== MATCHED REQUIRED SKILLS =====")

    for skill in result["required_matched"]:
        print("✓", skill)

    print("\n===== MISSING REQUIRED SKILLS =====")

    for skill in result["required_missing"]:
        print("✗", skill)

    print("\n===== MATCHED PREFERRED SKILLS =====")

    for skill in result["preferred_matched"]:
        print("✓", skill)

    print("\n===== MISSING PREFERRED SKILLS =====")

    for skill in result["preferred_missing"]:
        print("✗", skill)