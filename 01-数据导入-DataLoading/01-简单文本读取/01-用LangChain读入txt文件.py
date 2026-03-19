from langchain_community.document_loaders import TextLoader

# 读取单个 txt 文件
from pathlib import Path

# 获取当前脚本文件所在目录
script_dir = Path(__file__).resolve().parent

# 结合相对路径构建完整路径，并标准化
file_path = (script_dir / "../../90-文档-Data/黑悟空/设定.txt").resolve()

# 默认按 utf-8 读取，同时开启编码自动检测，兼容常见中文 txt 编码
loader = TextLoader(str(file_path), encoding="utf-8", autodetect_encoding=True)
documents = loader.load()
print(documents)
