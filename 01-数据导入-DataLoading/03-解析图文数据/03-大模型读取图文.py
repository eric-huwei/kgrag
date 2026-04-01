import base64
import os
from pathlib import Path

import fitz
from openai import OpenAI
from langchain_core.documents import Document


client = OpenAI(
    api_key=os.getenv("ALIAI_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

pdf_path = Path("90-文档-Data/黑悟空/黑神话悟空.pdf")
output_dir = Path("temp_images")
output_dir.mkdir(exist_ok=True)

# 1. PDF 转图片（不依赖 Poppler）
doc = fitz.open(pdf_path)
image_paths = []
for i, page in enumerate(doc, start=1):
    # 使用 2x 缩放提高识别质量
    mat = fitz.Matrix(2, 2)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    image_path = output_dir / f"page_{i}.jpg"
    pix.save(str(image_path))
    image_paths.append(image_path)
doc.close()

print(f"成功转换 {len(image_paths)} 页")

# 2. 逐页调用多模态模型分析
print("\n开始分析图片...")
results = []
for image_path in image_paths:
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="qwen3.5-plus",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "请详细描述这张PPT幻灯片的内容，包括标题、正文和图片内容。",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    results.append(response.choices[0].message.content)

# 3. 转换为 LangChain Document
source = str(pdf_path)
documents = [
    Document(page_content=result or "", metadata={"source": source, "page_number": i + 1})
    for i, result in enumerate(results)
]

print("\n分析结果:")
for doc in documents:
    print(f"内容: {doc.page_content}\n元数据: {doc.metadata}\n")
    print("-" * 80)

# 清理临时文件
for image_path in image_paths:
    os.remove(image_path)
os.rmdir(output_dir)
