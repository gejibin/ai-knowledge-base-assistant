import os
import sys
import re
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import tempfile
from dotenv import load_dotenv, find_dotenv
from embedding.call_embedding import get_embedding
from langchain_community.document_loaders import UnstructuredFileLoader
#from langchain_unstructured import UnstructuredLoader

from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
#from  langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
# 首先实现基本配置

DEFAULT_DB_PATH = "./knowledge_db"
DEFAULT_PERSIST_PATH = "./vector_db"


def get_files(dir_path):
    file_list = []
    for filepath, dirnames, filenames in os.walk(dir_path):
        for filename in filenames:
            file_list.append(os.path.join(filepath, filename))
    return file_list


def file_loader(file, loaders):
    if isinstance(file, tempfile._TemporaryFileWrapper):
        file = file.name
    if not os.path.isfile(file):
        [file_loader(os.path.join(file, f), loaders) for f in  os.listdir(file)]
        return
    file_type = file.split('.')[-1]
    if file_type == 'pdf':
        loaders.append(PyMuPDFLoader(file))
    elif file_type == 'md':
        pattern = r"不存在|风控"
        match = re.search(pattern, file)
        if not match:
            loaders.append(UnstructuredMarkdownLoader(file))
    elif file_type == 'txt':
        print("UnstructuredFileLoader: load file")
        loaders.append(UnstructuredFileLoader(file))
        #loaders.append(UnstructuredLoader(file)) #会出错
        print("UnstructuredFileLoader: after load file")
    elif file_type == 'docx':
        print("UnstructuredWordDocumentLoader: load file")
        #loaders.append(UnstructuredLoader(file)) #会出错
        loaders.append(UnstructuredWordDocumentLoader(file))
        print("UnstructuredWordDocumentLoader: after load file")
    return


def create_db_info(files=DEFAULT_DB_PATH, embeddings="openai", persist_directory=DEFAULT_PERSIST_PATH):
    if embeddings == 'openai' or embeddings == 'm3e' or embeddings =='zhipuai':
        vectordb = create_db(files, persist_directory, embeddings)
    return ""


def create_db(files=DEFAULT_DB_PATH, persist_directory=DEFAULT_PERSIST_PATH, embeddings="openai"):
    """
    该函数用于加载 PDF 文件，切分文档，生成文档的嵌入向量，创建向量数据库。

    参数:
    file: 存放文件的路径。
    embeddings: 用于生产 Embedding 的模型

    返回:
    vectordb: 创建的数据库。
    """
    print(f"create_db: files:{files}")
    if files == None:
        print("can't load empty file")
        return "can't load empty file"
    if type(files) != list:
        files = [files]
    loaders = []
    [file_loader(file, loaders) for file in files]
    docs = []
    for loader in loaders:
        if loader is not None:
            docs.extend(loader.load())
    print("切分文档")
    # 切分文档
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=150)
    split_docs = text_splitter.split_documents(docs)
    if type(embeddings) == str:
        embeddings = get_embedding(embedding=embeddings)
    # 定义持久化路径
    persist_directory = './vector_db/chroma'
    print("加载数据库")
    # 加载数据库
    vectordb = Chroma.from_documents(
    documents=split_docs,
    embedding=embeddings,
    persist_directory=persist_directory  # 允许我们将persist_directory目录保存到磁盘上
    ) 
    print("加载数据库完成")

    #vectordb.persist() //自动持久化到磁盘
    return vectordb


def presit_knowledge_db(vectordb):
    """
    该函数用于持久化向量数据库。

    参数:
    vectordb: 要持久化的向量数据库。
    """
    vectordb.persist()


def load_knowledge_db(path, embeddings):
    """
    该函数用于加载向量数据库。

    参数:
    path: 要加载的向量数据库路径。
    embeddings: 向量数据库使用的 embedding 模型。

    返回:
    vectordb: 加载的数据库。
    """
    vectordb = Chroma(
        persist_directory=path,
        embedding_function=embeddings
    )
    return vectordb


if __name__ == "__main__":
    create_db(embeddings="m3e")
