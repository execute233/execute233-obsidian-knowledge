---
title: langchain
tags: [Python, langchain, LLM, AI]
aliases: [LangChain]
---

# langchain

提示词模板参考 [[AI/LLM/Prompt Engineering|Prompt Engineering]]。图状态化扩展见 [[LangGraph]]。

## 概述

一般使用 `langchain` 包，如果要用第三方 Chat 模型的话使用 `langchain-<模型名>`。

## 模型对话

可以直接使用或者 template：

```python
import os
os.environ["OPENAI_API_KEY"]  = os.getenv("OPENAI_API_KEY", "your-api-key-here")
os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com"

model = ChatOpenAI(
    model="deepseek-v4-flash",
    temperature=0.1,
    max_tokens=1000,
)
r = model.invoke("你好，你是什么模型？")
print(r)
```

```python
import os
os.environ["OPENAI_API_KEY"]  = os.getenv("OPENAI_API_KEY", "your-api-key-here")
os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com"

model = ChatOpenAI(
    model="deepseek-v4-flash",
    temperature=0.1,
    max_tokens=1000,
)
prompt = ChatPromptTemplate.from_messages([
    {
        "role": "system",
        "content": "你是一个 AI 助手"
    }, {
        "role": "user",
        "content": "{input}"
    }
])
chain = prompt | model
r = chain.invoke({"input": "大模型的 RAG 是什么？"})
print(r)
```

可使用以下方式来让输出结果为字符串而不是 ChatMessage：

```python
output_parser = JsonOutputParser()
chain = prompt | model | output_parser
```

## RAG

```python
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(model="qwen3.6-plus")
loader = PyPDFLoader(file_path='./PDFs/test.pdf')
docs = loader.load()
embeddings = OpenAIEmbeddings(
    model="text-embedding-v4",
    check_embedding_ctx_length=False,
    chunk_size=10,
)
splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=128)
documents = splitter.split_documents(docs)
print(len(documents))
# 存储在 FAISS 向量数据库中
vector = FAISS.from_documents(documents, embeddings)
retriever = vector.as_retriever()
retriever.search_kwargs = {'k': 3}
prompt_template = """
你是一个问答机器人。
你的任务是根据下述给定的已知信息回答用户问题。
确保你的回复完全依据下述已知信息。不要编造答案。
如果下述已知信息不足以回答用户的问题，请直接回复"我无法回答您的问题"。
已知信息：
{info}
用户问：
{question}
请用中文回答用户问题。
"""
template = PromptTemplate.from_template(prompt_template)
prompt = template.format(info=docs, question="会计师事务所怎样选聘用")
response = llm.invoke(prompt)
print(response.content)
```
