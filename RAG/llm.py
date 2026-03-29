import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from .prompts import SYSTEM_PROMPT


load_dotenv()


def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.7,
    )


def ask_question(question: str, context: str = "", chat_history: list = None) -> str:
    """
    Ask a question with optional context and chat history.

    Args:
        question: The user's question.
        context: Retrive contxt from the PDF
        chat_history: Previous conversation messages

    Returns:
        The LLM's response
    """

    llm = get_llm()

    history_text = ""

    if chat_history:
        recent_history = chat_history[-5:]
        history_lines = []
        for msg in recent_history:
            role = msg.get("role", "")
            content = msg.get("content", "")
            if role == "user":
                history_lines.append(f"User:{content}")
            elif role == "assistant":
                history_lines.append(f"Assistant:{content}")

        if history_lines:
            history_text = (
                "Previous conversation:\n" + "\n".join(history_lines) + "\n\n"
            )

    prompt = SYSTEM_PROMPT.format(
        chat_history=history_text, context=context, question=question
    )

    # get response
    response = llm.invoke(prompt)
    return response.content

    # def test_llm():
    print("TEST 1: With Context ")
    context = "Cleopatra was the last pharaoh of Egypt, ruling from 51-30 BC."
    answer = ask_question("Who was Cleopatra?", context)
    print(answer)
    print("\n")

    print("TEST 2: Without Context")
    answer = ask_question("What is the story behind Cleopatra?", context="")
    print(answer)

    # if __name__ == "__main__":
    test_llm()
