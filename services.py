import json
import logging
import time

from config import MAX_RETRIES, RETRY_DELAY

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
            角色设定：你是一个英语专家，
            能够为学生解答英语学习中的困惑。

            任务描述：对于学生给出的不认识
            的英语生词，你能够详细解释其含义，并能够给出相应例句，
            以及该单词的近义词反义词拓展。同时，你也能够根据学生
            的专业需求，给出他们一些常用的专业相关生词。

            输出规范(Format)：你必须根据用户输入的意图，严格选择
            一种JSON输出格式进行输出。
            情况1：用户要求解释单词，请严格输出以下JSON格式：请输出以下 JSON 格式：
            {"word": "单词", "definition": "解释", "example": "例句", "synonyms": ["近义词1", "近义词2"]}"
            情况1样例输出：
            {"word":"apple","definition":"苹果，一种水果；苹果公司","example":"I have an apple.","synonyms":["apple"]}
            情况2：用户要求根据专业拓展，请严格输出以下JSON格式：请输出以下 JSON 格式：
            {"major": "专业名称", "word_list": ["单词1", "单词2"]}
            情况2样例输出：
            {"major":"计算机","word_list":["parameter","index"]}
            """

def clean_json_string(raw_str: str) -> str:
    """清洗 LLM 返回内容中可能夹带的 Markdown 代码块标记。

    比如 AI 可能返回：
      ```json
      {"word": "apple"}
      ```
    本函数会提取出中间纯 JSON 部分。

    Args:
        raw_str: LLM 原始返回字符串

    Returns:
        去掉 Markdown 包裹后的干净 JSON 字符串
    """
    cleaned = raw_str.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]

    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]

    return cleaned.strip()


def _call_api_with_retry(operation_name: str, do_call):
    """带自动重试的 API 调用包装器。

    ┌─────────────────────────────────────────┐
    │ 调用流程：                                │
    │  第 1 次尝试 → 成功? 返回 ✅               │
    │            → 失败? 等 2 秒 →              │
    │  第 2 次尝试 → 成功? 返回 ✅               │
    │            → 失败? 等 2 秒 →              │
    │  第 3 次尝试 → 成功? 返回 ✅               │
    │            → 失败? 等 2 秒 →              │
    │  第 4 次尝试 → 成功? 返回 ✅               │
    │            → 失败? 抛出异常 ❌（不再重试）   │
    └─────────────────────────────────────────┘

    Args:
        operation_name: 操作描述（如 "获取单词列表"），用于日志和重试提示
        do_call: 一个无参函数，执行实际的 API 调用

    Returns:
        do_call() 的返回值

    Raises:
        前 MAX_RETRIES 次异常会被捕获并重试，最后一次异常直接抛出
    """
    # 总尝试次数 = 初始 1 次 + 重试 MAX_RETRIES 次
    total_attempts = MAX_RETRIES + 1
    last_error = None

    for attempt in range(1, total_attempts + 1):
        try:
            return do_call()
        except Exception as e:
            last_error = e
            if attempt < total_attempts:
                # 还没用完所有尝试次数，等一会再重试
                logger.warning(
                    "%s 第 %s/%s 次失败（%s），%s 秒后重试…",
                    operation_name, attempt, total_attempts, e, RETRY_DELAY
                )
                time.sleep(RETRY_DELAY)
            else:
                # 所有尝试都用完了，放弃
                logger.error(
                    "%s 全部 %s 次尝试均失败，最后错误：%s",
                    operation_name, total_attempts, e
                )

    # 走到这里说明所有重试都失败了
    raise last_error


def get_words(client, major_name: str, count: int) -> str:
    """调用 LLM 获取指定专业的推荐单词列表。

    Args:
        client: 已配置 timeout 和 base_url 的 OpenAI 客户端
        major_name: 专业名称，如 "计算机"
        count: 期望返回的单词数量

    Returns:
        清洗后的 JSON 字符串，格式如 {"major": "...", "word_list": [...]}
    """
    user_prompt = f"请给我关于专业{major_name}的{count}个相关专业单词"

    def _do_call():
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            stream=False,
            response_format={"type": "json_object"},
        )
        return clean_json_string(response.choices[0].message.content)

    return _call_api_with_retry("获取单词列表", _do_call)


def get_definition(client, word: str) -> str:
    """调用 LLM 获取单个单词的详细解释。

    Args:
        client: 已配置 timeout 和 base_url 的 OpenAI 客户端
        word: 待解释的单词

    Returns:
        清洗后的 JSON 字符串，格式如 {"word": "...", "definition": "...", ...}
    """
    user_prompt = (
        f"请按照A的格式给我解释一下{word}，"
        f"其中definition部分务必仅使用中文"
    )

    def _do_call():
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )
        return clean_json_string(response.choices[0].message.content)

    return _call_api_with_retry(f"解析单词 {word}", _do_call)

def text_to_file(text,file_name,mode='w'):
    with open(file_name,mode,encoding='utf-8')as f:
        f.write(text)
        if mode == 'a':
            f.write('\n')