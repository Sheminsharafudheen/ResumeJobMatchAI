from langchain_ollama import OllamaLLM


def create_llm():
    llm = OllamaLLM(
        model="llama3.2:latest"
    )

    return llm


if __name__ == "__main__":
    llm = create_llm()

    question = "What is machine learning?"

    response = llm.invoke(question)

    print("LLM Response:")
    print(response)