## ai-knowledge-base-assistant
AI RAG for personal AI knowledge base assistant (only used for study)
0.1.0 version
### 个人知识库助手项目
```
LLM + Embedding + ChromaDB + Gradio

1. 目前支持OpenAI和ZHUIAI的LLM
2. 支持本地大模型调用（通过ollama支持）
3. 支持pdf、md、docx、txt等格式的文件
4. 支持OpenAI和智普的Embedding模型
5. windows环境下测试通过
6. 后续测试其他LLM、Embedding模型和向量库
```
**演示界面**
![问答演示界面](./figures/QA.png)

**Installation:**
- The Poetry package manager is required for installation. [Poetry Installation](https://python-poetry.org/docs/#installation) Depending on your environment, this might work:

```
pip install poetry
```

- A .env file with a OPENAI_API_KEY or ZHIPUAI_API_KEY is required to run the demo.

```
git clone git@github.com:gejibin/ai-knowledge-base-assistant.git
cd ai-knowledge-base-assistant
poetry install
poetry shell # activates virtual environment
```

**Running**

```
python serve/run_gradio.py

http://127.0.0.1:9990

切换大模型的时候，需要清理历史记录（"Clear console"按钮），否则历史记录会传递到新模型里面。

```

**Local Model config**

```
在.env文件中添加以下内容：

LOCAL_MODEL_ENABLE = True
LOCAL_MODEL_URL = "http://localhost:11434"
LOCAL_MODELS="deepseek-r1:7b,llama3:latest,glm4:latest,qwen2.5:7b"
LOCAL_MODEL_DEFAULT = "llama3:latest"

如果不使用于本地模型，可以设置：
LOCAL_MODEL_ENABLE = False
并重新启动服务
```

**Next Steps**
```
1. 后续优先支持 DeepSeek
2. 继续把一些接口更新到最新
3. 支持Milvus向量库
```

**NOTE**
```
有些信息来自网上，有些地方有问题，仅供参考学习用，可自行下载学习和调试。
only used for study！！！
```