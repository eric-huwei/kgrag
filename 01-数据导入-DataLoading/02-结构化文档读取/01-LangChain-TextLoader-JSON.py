from langchain_community.document_loaders import TextLoader

print("=== TextLoader 加载结果 ===")

text_loader = TextLoader(
    file_path="90-文档-Data/灭神纪/人物角色.json",
    encoding="utf-8",
)

text_documents = text_loader.load()
print(f"文档数量: {len(text_documents)}")
if text_documents:
    print(text_documents[0].page_content[:200])
