import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def create_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0
    )


if __name__ == "__main__":
    llm = create_llm()

    response = llm.invoke("Say hello")

    print("Gemini Response:")
    print(response.content)