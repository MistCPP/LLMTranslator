import ollama
import re

class TranslateString:
    def __init__(self, translate_str, callback):
        self.translate_str = translate_str
        self.callback = callback

class Translator_v2:
    current_elements:list[TranslateString] = []
    collections:list[list[TranslateString]] = []

    def __init__(self, max_tokens: int = 8192,max_str: int = 4096, model: str = 'deepseek-r1:14b'):
        self.max_tokens = max_tokens
        self.max_str = max_str
        self.model = model
        self.curr_str_len = 0

    def join_content_string(self, elements:list[TranslateString]):
        result = ''
        for element in elements:
            result = ''.join([result, element.translate_str])
        return result
    
    def translate_string(self,element:TranslateString,content:str):
        """
        调用大模型进行翻译工作
        :param text: 要翻译的文本
        :return: 翻译后的文本
        """
        # print(f"Content:{content} , Translate :{element.translate_str}")
        message = [
            {
                'role': 'system',
                'content': 'You are an expert in the field of computer graphics.'
            },
            {
                'role': 'user',
                'content': f"Translate \"{ element.translate_str}\" to chinese in context : \"{content}\"."
            }
        ]

        # 调用生成模型
        print(f"Calling LLM for translation: {element.translate_str}")
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
        element.callback(cleaned_response)
        print(f'LLM is done, respons is : {cleaned_response}')
        
    # 翻译列表中的所有段落文本
    def translating(self):
        # 将最后加入的文本单独插入到统计列表中去
        if self.current_elements:
            self.collections.append(self.current_elements.copy())
            self.current_elements.clear()

        # 按collections开始统计
        for elements in self.collections:
            content = self.join_content_string(elements)
            for element in elements:
                self.translate_string(element,content)
    
    # 记录
    def collection_string(self,target_str:str,callback = None):
        # 累计足够长度的上下文，当长度足够，则开始翻译
        target_len = len(target_str)
        if self.curr_str_len + target_len < self.max_str:
            # 累计待翻译文本长度（其实是累计上下文长度，需要获得一个尽可能长的上下文
            self.curr_str_len += target_len

            # 添加到待翻译列表中去
            self.current_elements.append(TranslateString(target_str,callback))
        else:
            # 添加到统计列表中去
            self.collections.append(self.current_elements.copy())
            self.current_elements.clear()

            # 重设当前字符串
            self._curr_str_len = target_len

            # 添加当前字符串
            self.current_elements.append(TranslateString(target_str,callback))

# debug ...  百度给我的语法顺序，得到的结果是翻译一整句的
# message = [
#     {
#         'role': 'system',
#         'content': 'You are an expert in the field of computer graphics.'
#     },
#     {
#         'role': 'user',
#         'content': f"Translate the \"{'''
# This parallelism exists at several levels on the GPU, as described in Chapter 29 of this book, "Streaming Architectures and Technology Trends." First, parallel execution on multiple data elements is a key design feature of modern GPUs
# '''}\" in {'''
# One of the biggest hurdles you'll face when first programming a GPU is learning how to get the most out of a data-parallel computing environment. This parallelism exists at several levels on the GPU, as described in Chapter 29 of this book, "Streaming Architectures and Technology Trends." First, parallel execution on multiple data elements is a key design feature of modern GPUs. Vertex and fragment processors operate on four-vectors, performing four-component instructions such as additions, multiplications, multiply-accumulates, or dot products in a single cycle. They can schedule more than one of these instructions per cycle per pipeline. This provides ample opportunities for the extraction of instruction-level parallelism within a GPU program. For example, a series of sequential but independent scalar multiplications might be combined into a single four-component vector multiplication. Furthermore, parallelism can often be extracted by rearranging the data itself. For example, operations on a large array of scalar data will be inherently scalar. Packing the data in such a way that multiple identical scalar operations can occur simultaneously provides another means of exploiting the inherent parallelism of the GPU. (See Chapter 44 of this book, "A GPU Framework for Solving Systems of Linear Equations," for examples of this idea in practice.)
# '''} to chinese."
#     }
# ]

# debug ...  中式英语的顺序，居然得到的结果是正确的
# message = [
#     {
#         'role': 'system',
#         'content': 'You are an expert in the field of computer graphics.'
#     },
#     {
#         'role': 'user',
#         'content': f"The content is {'''
# One of the biggest hurdles you'll face when first programming a GPU is learning how to get the most out of a data-parallel computing environment. This parallelism exists at several levels on the GPU, as described in Chapter 29 of this book, "Streaming Architectures and Technology Trends." First, parallel execution on multiple data elements is a key design feature of modern GPUs. Vertex and fragment processors operate on four-vectors, performing four-component instructions such as additions, multiplications, multiply-accumulates, or dot products in a single cycle. They can schedule more than one of these instructions per cycle per pipeline. This provides ample opportunities for the extraction of instruction-level parallelism within a GPU program. For example, a series of sequential but independent scalar multiplications might be combined into a single four-component vector multiplication. Furthermore, parallelism can often be extracted by rearranging the data itself. For example, operations on a large array of scalar data will be inherently scalar. Packing the data in such a way that multiple identical scalar operations can occur simultaneously provides another means of exploiting the inherent parallelism of the GPU. (See Chapter 44 of this book, "A GPU Framework for Solving Systems of Linear Equations," for examples of this idea in practice.)
# '''}, translate the \"{'''
# This parallelism exists at several levels on the GPU, as described in Chapter 29 of this book, "Streaming Architectures and Technology Trends." First, parallel execution on multiple data elements is a key design feature of modern GPUs
# '''}\" to chinese."
#     }
# ]

# # 调用生成模型
# client = ollama.chat(
#     model='deepseek-r1:14b',
#     messages=message,
#     keep_alive=60,
#     options={
#         'num_ptx': 8192,
#     })

# # 提取think标签内的内容
# pattern = re.compile(r'<think>.*?</think>', re.DOTALL)
# cleaned_response = re.sub(pattern, '', client.message.content).strip()
# print(f'LLM is done, respons is : {cleaned_response}')