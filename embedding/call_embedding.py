import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

#from embedding.zhipuai_embedding import ZhipuAIEmbeddings
from langchain_community.embeddings.zhipuai import ZhipuAIEmbeddings
#from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
#from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from llm.langchain_llm import parse_llm_api_key

def get_embedding(embedding: str, embedding_key: str=None, env_file: str=None):
    print(embedding)
    if embedding == 'm3e':
        return HuggingFaceEmbeddings(model_name="moka-ai/m3e-base")
    if embedding_key == None:
        embedding_key = parse_llm_api_key(embedding)
    if embedding == "openai":
        return OpenAIEmbeddings(api_key=embedding_key)
    elif embedding == "zhipuai":
        return ZhipuAIEmbeddings(api_key=embedding_key)
    else:
        raise ValueError(f"embedding {embedding} not support ")
