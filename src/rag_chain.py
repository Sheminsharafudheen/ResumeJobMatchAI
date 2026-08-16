from retriever import create_retriever
from llm import create_llm


def ask_resume(question):
    # 1. Retrieve relevant resume chunks
    retriever = create_retriever()
    documents = retriever.invoke(question)

    # 2. Combine retrieved chunks
    context = "\n\n".join(
        document.page_content for document in documents
    )

    # 3. Create prompt
    prompt = f"""
You are a resume analysis assistant.

Answer the question using ONLY the information provided
in the resume context below.

If the answer is not present in the context, say:
"I could not find this information in the resume."

Resume Context:
{context}

Question:
{question}

Answer:
"""

    # 4. Send prompt to Ollama
    llm = create_llm()
    response = llm.invoke(prompt)

    return response


if __name__ == "__main__":
    question = "What programming and AI skills does the candidate have?"

    answer = ask_resume(question)

    print("\n===== RESUME RAG ANSWER =====\n")
    print(answer)