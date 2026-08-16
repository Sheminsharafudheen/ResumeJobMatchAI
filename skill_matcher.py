# Skill normalization and matching

SKILL_ALIASES = {
    "ml": "machine learning",
    "machine learning": "machine learning",

    "dl": "deep learning",
    "deep learning": "deep learning",

    "genai": "generative ai",
    "generative ai": "generative ai",

    "llm": "llms",
    "llms": "llms",
    "large language models": "llms",

    "vector database": "vector databases",
    "vector databases": "vector databases",
    "chromadb": "vector databases",
    "faiss": "vector databases",

    "embedding": "embeddings",
    "embeddings": "embeddings",

    "langchain": "langchain",
    "rag": "rag",

    "python": "python",
    "sql": "sql",
    "fastapi": "fastapi",
    "git": "git",
    "github": "github",

    "tensorflow": "tensorflow",
    "pytorch": "pytorch",
    "docker": "docker",
    "aws": "aws",
    "azure": "azure",
    "hugging face": "hugging face",
}


def normalize_skill(skill):
    skill = skill.strip().lower()

    return SKILL_ALIASES.get(skill, skill)


def match_skills(job_skills, resume_skills):
    normalized_resume = {
        normalize_skill(skill)
        for skill in resume_skills
    }

    matched = []
    missing = []

    for skill in job_skills:
        normalized_skill = normalize_skill(skill)

        if normalized_skill in normalized_resume:
            matched.append(skill)
        else:
            missing.append(skill)

    return matched, missing


if __name__ == "__main__":

    job_required = [
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

    resume_skills = [
        "Python",
        "SQL",
        "TensorFlow",
        "Keras",
        "Scikit-learn",
        "LangChain",
        "Ollama",
        "RAG",
        "MySQL",
        "Git",
        "GitHub"
    ]

    matched, missing = match_skills(
        job_required,
        resume_skills
    )

    print("\n===== MATCHED SKILLS =====")

    for skill in matched:
        print("✓", skill)

    print("\n===== MISSING SKILLS =====")

    for skill in missing:
        print("✗", skill)