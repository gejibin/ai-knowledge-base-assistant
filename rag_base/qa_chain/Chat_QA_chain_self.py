from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

from  langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import sys
sys.path.append('/Users/lta/Desktop/llm-universe/project')
from qa_chain.model_to_llm import model_to_llm
from qa_chain.get_vectordb import get_vectordb
import re

class Chat_QA_chain_self:
    """"
    带历史记录的问答链  
    - model：调用的模型名称
    - temperature：温度系数，控制生成的随机性
    - top_k：返回检索的前k个相似文档
    - chat_history：历史记录，输入一个列表，默认是一个空列表
    - history_len：控制保留的最近 history_len 次对话
    - file_path：建库文件所在路径
    - persist_path：向量数据库持久化路径
    - appid：星火
    - api_key：星火、百度文心、OpenAI、智谱都需要传递的参数
    - Spark_api_secret：星火秘钥
    - Wenxin_secret_key：文心秘钥
    - embeddings：使用的embedding模型
    - embedding_key：使用的embedding模型的秘钥（智谱或者OpenAI）  
    """
    def __init__(self,model:str, temperature:float=0.0, top_k:int=4, chat_history:list=[], file_path:str=None, persist_path:str=None, appid:str=None, api_key:str=None, Spark_api_secret:str=None,Wenxin_secret_key:str=None, embedding = "openai",embedding_key:str=None):
        self.model = model
        self.temperature = temperature
        self.top_k = top_k
        self.chat_history = chat_history
        #self.history_len = history_len
        self.file_path = file_path
        self.persist_path = persist_path
        self.appid = appid
        self.api_key = api_key
        self.Spark_api_secret = Spark_api_secret
        self.Wenxin_secret_key = Wenxin_secret_key
        self.embedding = embedding
        self.embedding_key = embedding_key


        self.vectordb = get_vectordb(self.file_path, self.persist_path, self.embedding,self.embedding_key)
        
    
    def clear_history(self):
        "清空历史记录"
        return self.chat_history.clear()

    
    def change_history_length(self,history_len:int=1):
        """
        保存指定对话轮次的历史记录
        输入参数：
        - history_len ：控制保留的最近 history_len 次对话
        - chat_history：当前的历史对话记录
        输出：返回最近 history_len 次对话
        """
        n = len(self.chat_history)
        return self.chat_history[n-history_len:]

 
    def answer(self, question:str=None,temperature = None, top_k = 4):
        """"
        核心方法，调用问答链
        arguments: 
        - question：用户提问
        """
        
        if len(question) == 0:
            return "", self.chat_history
        
        if len(question) == 0:
            return ""
        
        if temperature == None:
            temperature = self.temperature
        llm = model_to_llm(self.model, temperature, self.appid, self.api_key, self.Spark_api_secret,self.Wenxin_secret_key)

        #self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        qa_template = """
            You are an assistant for question-answering tasks.
            Use the following pieces of retrieved context to answer
            the question. If you don't know the answer, say that you
            don't know. Use three sentences maximum and keep the
            answer concise. DO not output the reasoning process.
            请不要输出推理过程！
            不要输出'<think>'的过程！
            不要输出'<think>'！
            Please answer in Chinese！请用中文回答！


            Chat History:
            {chat_history}

            Other context:
            {context}

            Question: {question}
        """
        qa_prompt = ChatPromptTemplate.from_template(qa_template)

        docs = self.vectordb.similarity_search(question,k=3)
        print(f"检索到的内容数：{len(docs)}")
        for i, doc in enumerate(docs):
            print(f"检索到的第{i}个内容: \n {doc.page_content}", end="\n-----------------------------------------------------\n")

        retriever = self.vectordb.as_retriever(search_type="similarity",   
                                        search_kwargs={'k': top_k})  #默认similarity，k=4

        qa = ConversationalRetrievalChain.from_llm(
            llm = llm,
            retriever = retriever,
            combine_docs_chain_kwargs={"prompt": qa_prompt}
        )
        
        #print(self.llm)
        result = qa.invoke({"question": question,"chat_history": self.chat_history})
        #result = qa({"question": question,"chat_history": self.chat_history})       #result里有question、chat_history、answer
        print(f"result: {result}")
        answer =  result['answer']
        print(f"answer: {answer}")
        #deepseek-r1:7b would output <think> and </think> ... remove it
        answer = answer.split("</think>")[-1]
        answer = re.sub(r"\\n", '<br/>', answer)
        self.chat_history.append((question,answer)) #更新历史记录

        return self.chat_history  #返回本次回答和更新后的历史记录
        
















