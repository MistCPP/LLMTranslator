import requests
import Tools
import ImageComponent
import TextComponent
import TranslateComponent
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle


# 要读取的网页URL
url = 'https://www.uproomgames.com/dev-log/procedural-terrain'

# 发送HTTP请求并获取响应
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    # 解析网页内容
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 提取网页的图片和文本
    results = Tools.interative_extract(soup,start_tag='main')

    # 设置中文字体
    pdfmetrics.registerFont(TTFont('雅黑-细', 'msyh.ttc'))

    # 样式
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='ChineseStyle', 
        fontName='雅黑-细',
        fontSize=12, 
        leading=15,
        ))
    target_style = styles['ChineseStyle']

    # 创建PDF
    doc = SimpleDocTemplate('output.pdf', pagesize=letter)

    # 空的PDF元素列表
    story = []

    # LLM 翻译器
    translator = TranslateComponent.Translator(max_tokens=8192, max_str=4096, model='deepseek-r1:14b')

    # 打印结果
    for result in results:
        if isinstance(result, ImageComponent.ImageLoader):
            result.download_image()
            result.print_image()
            if result.img:
                # 输出图片之前，必须先走一次强制翻译逻辑
                trans_str = translator.translate_string('', True)
                if trans_str:
                    story.append(Paragraph(trans_str, target_style))
                    story.append(Spacer(1, 0.2 * inch))
                else:
                    print('No translation string.')
                # 必须指定图片大小，否则会报错
                story.append(Image(result.buffer, width=6 * inch, height=4 * inch))
                story.append(Spacer(1, 0.2 * inch))
        elif isinstance(result, TextComponent.TextComponent):
            result.print_text()
            trans_str = translator.translate_string(result.text, False)
            if trans_str:
                story.append(Paragraph(trans_str, target_style))
                story.append(Spacer(1, 0.2 * inch))
            else:
                print('No translation string.')
        else:
            print('Unknown component type.')

    # debug 字体内容    
    # story.append(Paragraph('网页内容', target_style))

    # 构建PDF
    doc.build(story)
    print('PDF generated successfully.')
else:
    print(f'Error: {response.status_code}')
    exit(1)