# sk-e7705e49d2b44cbf802d272b93250e70
from openai import OpenAI

client = OpenAI(api_key="sk-b81f411c4d7f4f13b1ce97768fdf8b6c", base_url="https://api.deepseek.com/v1")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你喜欢什么"},
        # {"role": "user", "content": "你叫什么名字"},
    ],
    stream=False
)

print(response.choices[0].message.content)
