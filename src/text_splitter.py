from langchain_text_splitters import RecursiveCharacterTextSplitter
from document_loader import load_pdf


def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = text_splitter.split_documents(documents)

    return chunks


if __name__ == "__main__":

    file_path = r"C:\DATASCIENCE\MYPROJECTS\ResumeJobMatchAI\data\resume\Shemin_TS..pdf"

    documents = load_pdf(file_path)

    chunks = split_documents(documents)

    print("Number of chunks:", len(chunks))

    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i + 1} ---")
        print(chunk.page_content)