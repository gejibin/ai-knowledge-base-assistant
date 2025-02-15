#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
本地大模型接口封装(ollama)
'''
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from langchain_ollama import ChatOllama

class ChatLocalAI():
    def __init__(self, model, base_url, temperature=0.0):
        self.base_url = base_url
        self.model_name = model
        self.llm = ChatOllama(base_url=base_url, model=model, temperature=temperature)
    
    def get_response(self, messages):
        response = self.llm.invoke(messages)
        #deepseek-r1:7b would output <think> and </think> ... remove it
        content = response.content
        print(self.model_name)
        print(f"messages: {messages}")
        print(f"content: {content}")
        return content.split("</think>")[-1]


# if __name__ == "__main__" :
#     #llm = ChatLocalAI(base_url="http://localhost:11434", model="deepseek-r1:7b")
#     llm = ChatLocalAI(base_url="http://localhost:11434", model="qwen2.5:7b")
#     content = llm.get_response("你是谁？")
#     print(content)
#     # print("\n")
#     # print(content.split("</think>")[-1])
