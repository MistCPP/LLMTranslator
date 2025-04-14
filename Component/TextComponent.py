from bs4 import element
from Component import TranslateComponent

class TextComponent:
    def __init__(self,origin:element.NavigableString,index):
        self.origin = origin
        self.index = index

    def DebugTranslate(self):
        txt = self.origin.get_text()
        self.origin.replace_with(f"DebugTranslate:{txt}")
    
    # 接收翻译完成的文本
    def _translate_complated(self,translate):
        self.origin.replace_with(translate)

    # 发送翻译请求
    def send_to_translate_service(self,translator:TranslateComponent.Translator_v2):
        translator.collection_string(self.origin.get_text().strip(),callback=self._translate_complated)