from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

# Added : str and : float type hints below
def get_gemini(model_name: str = "gemini-2.5-flash", temperature: float = 0.1) -> ChatGoogleGenerativeAI:
    """
    Initializes and returns a LangChain ChatGoogleGenerativeAI model instance
    configured with the specified model name and temperature.
    """
    if os.getenv("GOOGLE_API_KEY") is None:
        raise ValueError("API Key not found. Please set GOOGLE_API_KEY in your .env file.")

    llm = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)
    return llm

# Added : float type hint
def get_gemini_for_routing(temperature: float = 0.0) -> ChatGoogleGenerativeAI:
    """
    Get a more deterministic model instance for query classification/routing.
    Lower temperature for consistent classification results.
    """
    return get_gemini(temperature=temperature)

# Added : float type hint
def get_gemini_for_conversation(temperature: float = 0.7) -> ChatGoogleGenerativeAI:
    """
    Get a slightly more creative model instance for general conversation.
    Higher temperature for more natural, varied responses.
    """
    return get_gemini(temperature=temperature)