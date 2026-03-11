from pymilvus import connections

# 连接 Milvus 服务
connections.connect(
    alias="default",
    host="localhost",
    port="19530"
)
print("✅ Milvus 连接成功！服务正常运行")