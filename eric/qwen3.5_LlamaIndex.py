import os

# 第一步：强制清空所有 OpenAI 相关环境变量（核心！避免残留配置干扰）
os.environ.pop("OPENAI_API_KEY", None)
os.environ.pop("OPENAI_BASE_URL", None)

# 第一行代码：导入相关的库
from llama_index.core import Settings
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.openai_like import OpenAILikeEmbedding

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader 


ALI_API_KEY = os.getenv("ALIAI_API_KEY")  # 直接写死测试（避免环境变量读取错误）
ALI_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# ① 配置千问大模型（用OpenAILike适配）
Settings.llm = OpenAILike(
    model="qwen3.5-plus", # 使用最新的推理模型R1
    api_key=ALI_API_KEY,  # 从环境变量获取API key
    base_url=ALI_BASE_URL,
    is_chat_model=True,
    temperature=0.1,  # 降低随机性，回答更精准
    max_tokens=2000,   # 最大回复长度
    # 额外兜底：禁用 OpenAI 相关配置读取
    api_base=ALI_BASE_URL  # 部分版本需用 api_base 替代 base_url
)
# ② 配置千问嵌入模型（替代OpenAI嵌入模型，核心修正点）
Settings.embed_model = OpenAILikeEmbedding(
    model_name="text-embedding-v1",  # 阿里云通义千问嵌入模型名
    api_key=ALI_API_KEY,
    base_url=ALI_BASE_URL,
    api_base=ALI_BASE_URL  # 兜底参数，确保不走 OpenAI
)

# 第二行代码：加载数据
documents = SimpleDirectoryReader(input_files=["../90-文档-Data/黑悟空/设定.txt"]).load_data() 
# 第三行代码：构建索引
index = VectorStoreIndex.from_documents(documents)
# 第四行代码：创建问答引擎
query_engine = index.as_query_engine()
# 第五行代码: 开始问答
print(query_engine.query("黑神话悟空中有哪些战斗工具?"))
