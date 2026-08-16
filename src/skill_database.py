# Common AI/ML and software skills
# used for reliable skill detection.

SKILL_DATABASE = [
    # Programming
    "Python",
    "SQL",
    "R",
    "Java",
    "C++",

    # Machine Learning
    "Machine Learning",
    "Supervised Learning",
    "Unsupervised Learning",
    "Regression",
    "Classification",
    "Clustering",
    "Feature Engineering",
    "Scikit-learn",
    "XGBoost",

    # Deep Learning
    "Deep Learning",
    "ANN",
    "CNN",
    "RNN",
    "LSTM",
    "GRU",
    "TensorFlow",
    "Keras",
    "PyTorch",

    # Generative AI / LLM
    "Generative AI",
    "GenAI",
    "LLMs",
    "Large Language Models",
    "LangChain",
    "RAG",
    "Retrieval-Augmented Generation",
    "Prompt Engineering",
    "Ollama",
    "Embeddings",
    "Vector Databases",
    "ChromaDB",
    "FAISS",
    "Hugging Face",

    # NLP
    "NLP",
    "Natural Language Processing",
    "NLTK",
    "spaCy",
    "TF-IDF",
    "Sentiment Analysis",
    "Tokenization",

    # Computer Vision
    "OpenCV",
    "Computer Vision",
    "Image Processing",
    "Object Detection",
    "MediaPipe",

    # Data Science
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Seaborn",

    # Databases
    "MySQL",
    "MongoDB",
    "PostgreSQL",

    # APIs / Development
    "FastAPI",
    "Flask",
    "Django",
    "REST API",

    # Cloud
    "AWS",
    "Azure",
    "Google Cloud",

    # DevOps / Tools
    "Docker",
    "Git",
    "GitHub",
    "Jupyter Notebook",
    "VS Code",
]
if __name__ == "__main__":

    print("Number of skills in database:", len(SKILL_DATABASE))

    print("\nSample skills:")

    for skill in SKILL_DATABASE[:15]:
        print("-", skill)