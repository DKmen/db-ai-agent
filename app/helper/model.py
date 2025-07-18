from langchain_openai import ChatOpenAI
from app.constants import config

llm = ChatOpenAI(
    model=config["OPENAI_MODEL_ID"],
    temperature=0.9,
    api_key=config["OPENAI_API_KEY"],
)
