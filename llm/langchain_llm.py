#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
各个大模型的langchain接口封装
'''
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv, find_dotenv
from langchain.utils import get_from_dict_or_env

from langchain_openai import ChatOpenAI
from llm.ollama_llm import ChatLocalAI
from llm.local_llm import LocalModels



def get_completion(prompt :str, model :str, temperature=0.1,api_key=None, secret_key=None, access_token=None, appid=None, api_secret=None, max_tokens=2048):
    print("llm model is: ", model)
    local_models = LocalModels()
    if local_models.local_model_enable and model in local_models.llm_model_list:
        local_llm = ChatLocalAI(model, local_models.local_model_url, temperature)
        return local_llm.get_response(prompt)
    elif model in ["gpt-3.5-turbo", "gpt-3.5-turbo-16k-0613", "gpt-3.5-turbo-0613", "gpt-4", "gpt-4-32k"]:
        return get_completion_gpt(prompt, model, temperature, api_key, max_tokens)
    elif model in ["glm-4-plus", "glm-4-long", "glm-4-Air", "glm-4-flash"]:
        return get_completion_glm(prompt, model, temperature, api_key, max_tokens)
    else:
        print(f"mode {model} : 不正确的模型")
        return "不正确的模型"
 

    
def get_completion_gpt(prompt : str, model : str, temperature : float, api_key:str, max_tokens:int):
    if api_key == None:
        api_key = parse_llm_api_key("openai")
    api_key = api_key

    llm = ChatOpenAI(model = model, temperature = temperature , api_key = api_key)
    response = llm.invoke(prompt)
    return response.content

    # https://python.langchain.com/docs/integrations/chat/openai/
    '''
    llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # api_key="...",  # if you prefer to pass api key in directly instaed of using env vars
    # base_url="...",
    # organization="...",
    # other params...
    )
    ''' 


def get_completion_glm(prompt : str, model : str, temperature : float, api_key:str, max_tokens : int):
    if api_key == None:
        api_key = parse_llm_api_key("zhipuai")
    api_key = api_key
    base_url = "https://open.bigmodel.cn/api/paas/v4/"

    print("zhipu AI ...")

    llm = ChatOpenAI(
        model = model, 
        temperature = temperature, 
        api_key = api_key, 
        base_url = base_url
        )

    #llm = ChatZhipuAI(model_name = model, temperature = temperature , zhipuai_api_key = api_key)
    response = llm.invoke(prompt)
    return response.content

def parse_llm_api_key(model:str, env_file:dict()=None):
    """
    通过 model 和 env_file 的来解析平台参数
    """   
    if env_file == None:
        _ = load_dotenv(find_dotenv())
        env_file = os.environ
    if model == "openai":
        return env_file["OPENAI_API_KEY"]
    elif model == "wenxin":
        return env_file["wenxin_api_key"], env_file["wenxin_secret_key"]
    elif model == "spark":
        return env_file["spark_api_key"], env_file["spark_appid"], env_file["spark_api_secret"]
    elif model == "zhipuai":
        #return get_from_dict_or_env(env_file, "zhipuai_api_key", "ZHIPUAI_API_KEY")
        return env_file["ZHIPUAI_API_KEY"]
    else:
        raise ValueError(f"model{model} not support!!!")
   