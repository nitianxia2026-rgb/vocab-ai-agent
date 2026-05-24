


class response_A(object):
    def __init__(self,word,definition,example,synonyms):
        self.word = word
        self.definition = definition
        self.example = example
        self.synonyms = synonyms
    def print_response(self):
        print(f"\n--- 单词详情 ---")
        print(f"单词: {self.word}")
        print(f"解释: {self.definition}")
        print(f"例句: {self.example}")
        print(f"近义词: {self.synonyms}")
    
    @staticmethod
    def dict_to_response_A(d):
        return response_A(
            d.get('word','未知单词'),
            d.get('definition', '暂无解释'),
            d.get('example', '暂无例句'),
            d.get('synonyms', [])#防止AI的回复漏掉了某个字段，用默认值使程序能够继续运行
        )
class response_B(object):
    def __init__(self,major,word_list):
        self.major = major
        self.word_list = word_list
   
    @staticmethod
    def dict_to_response_B(d):
        return response_B(
            d.get('major','未知专业'),
            d.get('word_list',[])
        )

    