from langchain_community.document_loaders import PyPDFLoader


def load_job_description(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    return documents


if __name__ == "__main__":
    job_path =r"C:\DATASCIENCE\MYPROJECTS\ResumeJobMatchAI\data\jobs\AI_Engineer_Job.pdf.pdf"
    documents = load_job_description(job_path)

    print("Number of job description pages:", len(documents))

    for document in documents:
        print("\n--- Job Description ---")
        print(document.page_content[:2000])