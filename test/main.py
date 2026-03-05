import os
from openai import OpenAI


def main():
    client = OpenAI(
        api_key=os.getenv("ALIAI_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen3.5-plus",  #2026/05/16过期
        messages=[{'role': 'user', 'content': '我这个账号还有多少免费对话额度？'}]
    )
    print(completion.choices[0].message.content)
    

if __name__ == "__main__":
    main()