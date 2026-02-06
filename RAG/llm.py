import os 
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key = os.getenv("GOOGLE_API_KEY"),
        temperature = 0.7
    )

# testing llm function

def test_llm():

    llm = get_llm()
    response = llm.invoke("what the story behind cleopatra?")
    print(response.content)

# run this if the function works 
if __name__ == "__main__":
    test_llm()

