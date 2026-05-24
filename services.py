import json

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
            情况1样例输出：{"word":"apple","definition":"苹果，一种水果；苹果公司","example":"I have an apple.","synonyms":["apple"]}
            情况2：用户要求根据专业拓展，请严格输出以下JSON格式：请输出以下 JSON 格式：
{"major": "专业名称", "word_list": ["单词1", "单词2"]}
            情况2样例输出：{"major":"计算机","word_list":["parameter","index"]}
            """

def clean_json_string(raw_str):
    #清洗AI可能返回的md格式
    cleaned = raw_str.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]#运用字符串切片，从第8位获取输出
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
        
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
        
    return cleaned.strip()

def get_words(client,major_name,count):
    user_prompt=f"""
    请给我关于专业{major_name}的{count}个相关专业单词
    """
    response = client.chat.completions.create(
        model = 'deepseek-v4-flash',
        messages = [
            {'role':'system','content':SYSTEM_PROMPT},
            {'role':'user','content':user_prompt}
        ],
        stream = False,
        response_format = {'type':'json_object'}
    )

    return clean_json_string(response.choices[0].message.content)
    #清洗数据后，返回全部的输出json内容，在main中再调用反序列化和文件写入

def get_definition(client,word):#仅书写对于单个单词的解释
    user_prompt = f"请按照A的格式给我解释一下{word},其中definition部分务必仅使用中文"
    
    response = client.chat.completions.create(
        model='deepseek-v4-flash',
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        response_format={'type': 'json_object'}
    )
    return clean_json_string(response.choices[0].message.content)

def text_to_file(text,file_name,mode='w'):
    with open(file_name,mode,encoding='utf-8')as f:
        f.write(text)
        if mode == 'a':
            f.write('\n')