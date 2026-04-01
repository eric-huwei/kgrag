from langchain_core.documents import Document
from unstructured.partition.pptx import partition_pptx

ppt_path = "90-文档-Data/黑悟空/黑神话悟空.pptx"

# 直接解析 PPTX，不依赖 LibreOffice/soffice
ppt_elements = partition_pptx(filename=ppt_path)
print("PPT 内容片段:")

# 转换为 LangChain Documents
documents = [
    Document(page_content=element.text or "", metadata={"source": ppt_path})
    for element in ppt_elements
]

print(documents[:3])
