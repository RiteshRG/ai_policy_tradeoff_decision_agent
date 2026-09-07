from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv(override=True)

model = ChatGroq(model='openai/gpt-oss-120b')

def get_model():
    return model