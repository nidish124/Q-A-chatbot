import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

class config:
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    LLM_MODEL = "openai:gpt-4"

    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    
    @classmethod
    def get_llm(cls):
        try:
            os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
            return init_chat_model(cls.LLM_MODEL)
        except Exception as e:
            print("the issue is in congif",e)

