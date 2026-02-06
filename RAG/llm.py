import os 
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from prompts import SYSTEM_PROMPT


load_dotenv()

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key = os.getenv("GOOGLE_API_KEY"),
        temperature = 0.7
    )

def ask_question(question: str, context: str = "") -> str:
    llm = get_llm()
    prompt = SYSTEM_PROMPT.format(question=question, context=context)
    response = llm.invoke(prompt)
    return response.content


def test_llm():
    print("TEST 1: With Context ")
    context = "Cleopatra was the last pharaoh of Egypt, ruling from 51-30 BC."
    answer = ask_question("Who was Cleopatra?", context)
    print(answer)
    print("\n")
    
    print("TEST 2: Without Context")
    answer = ask_question("What is the story behind Cleopatra?", context="")
    print(answer)

if __name__ == "__main__":
    test_llm()


