import ollama
import re

# 调用大模型进行翻译工作

class Translator:
    def __init__(self, max_tokens: int = 8192,max_str: int = 4096, model: str = 'deepseek-r1:14b'):
        self.max_tokens = max_tokens
        self.max_str = max_str
        self.model = model
        self.curr_str = ''

    def translate_string(self, str,force: bool = False):
        translate_str = ''
        if not force and len(self.curr_str) + len(str) < self.max_str:
            self.curr_str = ''.join([self.curr_str, str])
        else:
            # 翻译一次
            translate_str = self._translate(self.curr_str)

            # 重设当前字符串
            self.curr_str = str
        return translate_str


    def _translate(self,text):
        if not text:
            return ''
        
        """
        调用大模型进行翻译工作
        :param text: 要翻译的文本
        :return: 翻译后的文本
        """
        message = [
            {
                'role': 'system',
                'content': '首先你要用中文回答，你是一个计算机领域专家，其次你要将我提交给你的英文翻译为中文（不需要输出思考过程，只提交给我翻译结果），并尽量保持专业术语和代码为原文，供我学习使用；'
            },
            {
                'role': 'user',
                'content': text
            }
        ]

        print(f'LLM is working text len = {len(text)}')
        # 调用生成模型
        client = ollama.chat(
            model=self.model,
            messages=message,
            keep_alive=60,
            options={
                'num_ptx': self.max_tokens,
            })
        
        # 提取think标签内的内容
        pattern = re.compile(r'<think>.*?</think>', re.DOTALL)
        cleaned_response = re.sub(pattern, '', client.message.content).strip()
        print(f'LLM is done, respons is : {cleaned_response}')
        
        return cleaned_response