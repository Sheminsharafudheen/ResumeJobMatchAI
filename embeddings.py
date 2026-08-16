from langchain_huggingface import HuggingFaceEmbeddings


def create_embedding_model():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return embeddings


if __name__ == "__main__":
    embeddings = create_embedding_model()

    test_text = "Python and machine learning"

    vector = embeddings.embed_query(test_text)

    print("Embedding created successfully!")
    print("Vector length:", len(vector))
    print("First 10 values:", vector[:10])