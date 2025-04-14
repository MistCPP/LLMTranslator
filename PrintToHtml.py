import requests
import Tools
from bs4 import BeautifulSoup
from Component import TranslateComponent

# 调试网页结构用(自己看看哪些节点下的东西不需要参与翻译，提前过滤掉)
def debug_html(soup, nodes):
    # 检查
    for component in nodes:
        if isinstance(component,Tools.TextComponent.TextComponent):
            component.DebugTranslate()

    # 测试重新保存为html
    with open('debug.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

def main_sync(url):
    # 发送HTTP请求并获取响应
    response = requests.get(url)

    # 获取文件名（URL的最后一部分）
    fileName = url.split('/')[-1]

    # Check if the request was successful
    if response.status_code == 200:
        # 解析网页内容
        soup = BeautifulSoup(response.content, 'html.parser')

        # extactor 2 debug
        # Tools.ExtractorWithOutOrder(soup)

        # 提取网页的图片和文本
        results = Tools.Extractor(soup, start_tag='main',refuse_tags={'meta','script','link','code','style','svg','canvas','video','audio','iframe','a'})

        # 调试输出
        # debug_html(soup, results)

        # 创建翻译器
        translator = TranslateComponent.Translator_v2(max_tokens=8192, max_str=4096, model='deepseek-r1:14b')

        # 统计文本、下载图片
        for component in results:
            if isinstance(component,Tools.UnknowComponent.UnknowComponent):
                print(f"Unknown component: {component}")
            elif isinstance(component,Tools.TextComponent.TextComponent):
                component.send_to_translate_service(translator)
            elif isinstance(component,Tools.ImageComponent.ImageLoader):
                component.send_to_image_download_service()

        # 翻译文本
        translator.translating()

        # 重新保存为html
        with open(f'{fileName}.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        
        print(f"Successfully fetched the URL: {url}")
    else:
        print(f"Failed to fetch the URL: {url}")

    return 0

if __name__ == '__main__':
    main_sync("https://developer.nvidia.com/gpugems/gpugems2/part-iv-general-purpose-computation-gpus-primer/chapter-35-gpu-program-optimization")