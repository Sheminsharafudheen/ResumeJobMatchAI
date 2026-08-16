from langchain_chroma import Chroma
from embeddings import create_embedding_model


def create_vector_store(chunks):
    embeddings = create_embedding_model()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="../chroma_db"
    )

    return vector_store


if __name__ == "__main__":
    from document_loader import load_pdf
    from text_splitter import split_documents

    # Change this to your actual resume filename
    resume_path =r"C:\DATASCIENCE\MYPROJECTS\ResumeJobMatchAI\data\resume\Shemin_TS..pdf"

    # 1. Load resume
    documents = load_pdf(resume_path)

    # 2. Split resume into chunks
    chunks = split_documents(documents)

    print("Number of chunks:", len(chunks))

    # 3. Create ChromaDB
    vector_store = create_vector_store(chunks)

    print("ChromaDB created successfully!")