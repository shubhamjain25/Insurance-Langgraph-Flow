from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def get_deterministic_llm():

    llm = ChatGroq(
        model='openai/gpt-oss-120b',
        temperature=0.1,
    )
    return llm

def get_creative_llm():

    llm = ChatGroq(
        model='openai/gpt-oss-120b',
        temperature=0.7,
    )

    return llm