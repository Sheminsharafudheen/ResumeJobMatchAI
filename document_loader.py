from langchain_community.document_loaders import PyPDFLoader


def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents


if __name__ == "__main__":
    file_path = r"C:\DATASCIENCE\MYPROJECTS\ResumeJobMatchAI\data\resume\Shemin_TS..pdf"

    documents = load_pdf(file_path)

    print("Number of pages:", len(documents))

    for document in documents:
        print(document.page_content[:500])
        print("-" * 50)


