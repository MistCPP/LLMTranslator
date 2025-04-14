from bs4 import element, Tag, BeautifulSoup
from Component import ImageComponent
from Component import TextComponent
from Component import UnknowComponent

# 广度优先分类器（将节点分类，以用于将来的图片下载、文本翻译工作
def Extractor(soup,start_tag=None,refuse_tags:list=None):
    if start_tag:
        target = soup.find(start_tag)
        if not target:
            print(f'No \"{start_tag}\" tag specified, using the whole soup.')
        else:
            soup = target
            print(f'Using {start_tag} tag as the starting point.')

    stack = [soup]
    results = []
    while stack:
        current = stack.pop()

        # 跳过拒绝的标签
        if refuse_tags and current.name in refuse_tags:
            print(f'Skipping {current.name}')
            continue
        
        # p 标签内的文本元素，直接存为一个文本元素
        if current.name == 'p' or isinstance(current, element.NavigableString):
            text = current.get_text()
            # 保存文本信息
            if text and not all(c.isspace() for c in text):
                results.append(TextComponent.TextComponent(current,len(results)))
            continue
        elif isinstance(current, Tag):
            currentClass = current.get('class')
            # 跳过广告
            if currentClass and 'ad-class' in currentClass:
                continue
            
            # 跳过视频
            if currentClass and 'video' in currentClass:
                continue
            
            # 跳过隐藏元素
            if current.get('style') == 'display:none':
                continue

            # 子节点入栈(怎么办呢，<tt>这种富文本符号，也被算入了文本中)
            stack.extend(reversed(list(current.children)))

            # 保存图片信息
            if current.name == 'img':
                attri_name = 'src' if current.get('src') else 'data-src'
                src = current.get(attri_name)
                if src:
                    results.append(ImageComponent.ImageLoader(src,index=len(results),origin=current,attri_name=attri_name))
            continue

        # 插入未定义类型的元素
        UnknowComponent.UnknowComponent(current,len(results))
    return results

# 不按节点顺序返回数组，只提取图片和文本
def ExtractorWithOutOrder(soup:BeautifulSoup):
    txt_tag = soup.find_all('p')
    img_tag = soup.find_all('img')
    for txt in txt_tag:
        if txt and not all(c.isspace() for c in txt.get_text()):
            print(f"Text: {txt.get_text()}")
    for img in img_tag:
        if img and img.get('src'):
            print(f"Image: {img.get('src')}")

    return 0