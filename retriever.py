from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def create_retriever():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma(
        persist_directory="../chroma_db",
        embedding_function=embeddings
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    return retriever


if __name__ == "__main__":
    retriever = create_retriever()

    query = "What programming skills does the candidate have?"

    results = retriever.invoke(query)

    print("Number of retrieved chunks:", len(results))

    for i, document in enumerate(results, start=1):
        print(f"\n--- Result {i} ---")
        print(document.page_content)