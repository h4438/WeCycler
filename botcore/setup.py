from langchain.llms import OpenAI, AI21
from langchain.chat_models import ChatOpenAI, PromptLayerChatOpenAI
import os
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceHubEmbeddings

def load_my_env():
    env_path = os.path.dirname(__file__)
    load_dotenv(f'{env_path}/../.streamlit/.env')

## TRACE
def trace_ai21(session: str = "vechai", max_tokens = 1000, model_name="j2-mid") -> AI21:
    enable_tracing(session)
    return get_ai21_model(model_name=model_name,max_tokens = max_tokens)

## MODELS
def get_huggingface_embeddings(repo_id = "sentence-transformers/all-distilroberta-v1"):
    load_my_env()
    key = os.getenv("HUGGING")
    os.environ['HUGGINGFACEHUB_API_TOKEN'] = key
    emb = HuggingFaceHubEmbeddings(repo_id = repo_id)
    print("HuggingFace Embedding is ready")
    return emb

def get_ai21_model(model_name: str = 'j2-jumbo-instruct', max_tokens: int = 256) -> AI21:
    load_my_env()
    ai_pass = os.getenv("AI21")
    model = AI21(ai21_api_key=ai_pass, model=model_name, maxTokens=max_tokens, temperature=0.0, topP=1.0)
    print("AI21 ready")
    return model

def enable_tracing(session:str='pitch') -> bool:
    load_my_env()
    lang_key = os.getenv("LANGCHAIN")
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com" 
    os.environ["LANGCHAIN_API_KEY"] = lang_key
    os.environ["LANGCHAIN_SESSION"] = session
    print(f"Enable tracing at {session}")
    return True

