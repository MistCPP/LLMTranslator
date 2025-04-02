from bs4 import element, Tag
import ImageComponent
import TextComponent

# 广度优先遍历提取网页中的图片和文本
def interative_extract(soup,start_tag=None):
    if start_tag:
        target = soup.find(start_tag)
        if not target:
            print(f'No {start_tag} tag specified, using the whole soup.')
        else:
            soup = target
            print(f'Using {start_tag} tag as the starting point.')

    stack = [soup]
    results = []
    while stack:
        current = stack.pop()
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
                src = current.get('src') or current.get('data-src')
                if src:
                    results.append(ImageComponent.ImageLoader(src, timeout=10))
        elif isinstance(current, element.NavigableString):
            # 处理文本
            text = current.strip()
            if text:
                results.append(TextComponent.TextComponent(text, font=16, color='white', bold=False, italic=False, underline=False))
    return results

