import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# --- API 调用配置 ---
# 为什么需要这些参数？看下面讲解
API_TIMEOUT = 30.0        # 单次 API 请求的超时秒数（超过这个时间没响应就放弃）
MAX_RETRIES = 3            # 失败后最多重试几次
RETRY_DELAY = 2.0          # 每次重试之间等待的秒数（避免瞬间把 API 打爆）


def get_client() -> OpenAI:
    """创建并返回配置好的 DeepSeek API 客户端。

    Returns:
        已配置 timeout 的 OpenAI 客户端实例

    Raises:
        ValueError: 未找到 DEEPSEEK_API_KEY 环境变量
    """
    logger.info("欢迎使用单词助手！")
    load_dotenv()

    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        raise ValueError("未找到API key，请检查 .env文件")

    return OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
        timeout=API_TIMEOUT,  # 所有通过这个 client 发出的请求都会受此超时限制
    )
    