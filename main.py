from config import get_client
from models import response_A,response_B
from services import get_words,get_definition,text_to_file

import os
import json

def main():
    
    if os.path.exists('result.json'):
        try:
            os.remove('result.json')
            print("[system]已清理result.json")
        except PermissionError:
            print("[system warning]无法清理result.json，请查看该文件是否被占用")
    try:
        client = get_client()
    except ValueError as e:
        print(e)
        return 
    
    while True:#增加鲁棒性测试
        major = input("请输入您的专业（如：计算机）： ").strip()
        if not major:
            print("[system] 专业不能为空，请重新输入。")
            continue
        if major.isdigit():
            print("[system] 专业名称不能全是数字，请输入文字（如：计科）。")
            continue
        break 
    
    while True:
        count_input = input("请输入您想获得的推荐单词个数 (1-10)： ").strip()#删除输入中空格
        if count_input.isdigit():
            count = int(count_input)
            if 1 <= count <= 10:
                break 
            else:
                print("[system] 为了保证生成质量，个数请限制在 1-10 之间。")#用于保保护API余额，防止超时
        else:
            print("[system] 请输入有效的数字数字，不要输入文字或符号。")
            
            
                #===阶段1：获取单词列表===
    print(f"正在请求关于{major}的{count}个专业词汇")
    try:
        word_list_json = get_words(client,major,count)#得到单词列表的json
        #json->实例
        #预加载，防止网络闪断输出了脏数据
        b_obj = json.loads(word_list_json,object_hook=response_B.dict_to_response_B)
        text_to_file(word_list_json,'word_list1.json','w')
        
        words_to_process = b_obj.word_list
        if not words_to_process:
            print("（阶段1）获取到的单词列表为空，请重试")   
            return
        
        print(f"获得单词列表：{(b_obj.word_list)}")
    
    except Exception as e:
        print(f"（阶段1）获取单词列表时发生错误，请重试：{e}")
        return 

                #===阶段2:解释单词===
    for word in words_to_process:
        print(f"正在解析单词：{word}...")
        try:
            #预加载
            def_json = get_definition(client,word)

            #将字符串解析为 Python 字典（过滤掉 LLM 自带的换行和格式）
            parsed_dict = json.loads(def_json)
            
            #强制将其序列化为紧凑的单行格式，并确保中文正常显示
            single_line_json = json.dumps(parsed_dict, ensure_ascii=False)

            text_to_file(single_line_json,'result.json','a')

        except Exception as e:
            print(f"（阶段2）解析单词{word}失败，请重试:{e}")

                #===阶段3：展示返回成果===
    print("===生成词库完毕===")
    if not os.path.exists('result.json'):
        print("[system]未生成有效数据")
        return 
    with open('result.json','r',encoding='utf-8')as f:
        for linenum,line in enumerate(f,1):
            #采用枚举enumerate，当解析报错时，能够报出是哪一行数据解析错误。便于后续调试运维
            clean_line = line.strip()
            if clean_line:#过滤空行
                try:
                    #一次只解析一行数据
                    a_obj = json.loads(clean_line, object_hook=response_A.dict_to_response_A)
                    a_obj.print_response()
                except Exception as e:
                    print(f"[system]第{linenum}行数据解析错误，请检查：{e}")

if __name__ == "__main__":
    main()

