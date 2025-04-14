from bs4 import element, Tag
from Component import ImageComponent
from Component import TextComponent
from Component import UnknowComponent

# 广度优先分类器（将节点分类，以用于将来的图片下载、文本翻译工作
def Extractor(soup,start_tag=None ,refuse_tags:list=None):
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
            print(f'Skipping {current.name} tag.')
            continue
        
        if isinstance(current, Tag):
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

            # 子节点入栈
            stack.extend(reversed(list(current.children)))

            # 处理图片
            if current.name == 'img':
                attri_name = 'src' if current.get('src') else 'data-src'
                src = current.get(attri_name)
                if src:
                    results.append(ImageComponent.ImageLoader(src,index=len(results),origin=current,attri_name=attri_name))
            continue
        elif isinstance(current, element.NavigableString):
            text = current.getText()
            if text and not all(c.isspace() for c in text):
                # 处理文本
                results.append(TextComponent.TextComponent(current,len(results)))
            continue

        # 插入未定义类型的元素
        UnknowComponent.UnknowComponent(current,len(results))
    return results

