import sys 
sys.path.append("../llm")

from langchain_community.chat_models import QianfanChatEndpoint

from langchain_community.chat_models import ChatSparkLLM


from langchain_community.chat_models import ChatZhipuAI
from langchain_community.chat_models import ChatOpenAI
from langchain_ollama import ChatOllama

from llm.langchain_llm import parse_llm_api_key
from llm.local_llm import LocalModels


def model_to_llm(model:str=None, temperature:float=0.0, appid:str=None, api_key:str=None,Spark_api_secret:str=None,Wenxin_secret_key:str=None):
        print(model)
        local_modes = LocalModels()
        if local_modes.local_model_enable and model in local_modes.llm_model_list:
            llm = ChatOllama(base_url=local_modes.local_model_url, model=model, temperature = temperature)
            #llm = ChatOllama(base_url="http://localhost:11434", model="llama3:latest", temperature = temperature)      
        elif model in ["gpt-3.5-turbo", "gpt-3.5-turbo-16k-0613", "gpt-3.5-turbo-0613", "gpt-4", "gpt-4-32k"]:
            if api_key == None:
                api_key = parse_llm_api_key("openai")
            llm = ChatOpenAI(model_name = model, temperature = temperature , openai_api_key = api_key)
        elif model in ["ERNIE-Bot", "ERNIE-Bot-4", "ERNIE-Bot-turbo"]:
            if api_key == None or Wenxin_secret_key == None:
                api_key, Wenxin_secret_key = parse_llm_api_key("wenxin")
            llm = QianfanChatEndpoint(model=model, temperature = temperature, api_key=api_key, secret_key=Wenxin_secret_key)
        elif model in ["Spark-1.5", "Spark-2.0"]:
            if api_key == None or appid == None and Spark_api_secret == None:
                api_key, appid, Spark_api_secret = parse_llm_api_key("spark")
            llm = ChatSparkLLM(model=model, temperature = temperature, appid=appid, api_secret=Spark_api_secret, api_key=api_key)
        elif model in ["glm-4-plus", "glm-4-long", "glm-4-Air", "glm-4-flash"]:
            if api_key == None:
                api_key = parse_llm_api_key("zhipuai")
            llm = ChatZhipuAI(model="glm-4-flash", zhipuai_api_key=api_key, temperature = temperature)
        else:
            raise ValueError(f"model{model} not support!!!")
        return llm