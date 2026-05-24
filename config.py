import os
from openai import OpenAI
from dotenv import load_dotenv
import json



def get_client():
    print("欢迎使用单词助手！\n")
    load_dotenv()
    
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        raise ValueError("未找到API key，请检查 .env文件")

    return  OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )
    