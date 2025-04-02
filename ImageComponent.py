import requests
from io import BytesIO
from PIL import Image

class ImageLoader:
    def __init__(self, url,timeout = 10,headers = None):
        if not url.startswith('https'):
            url = 'https:' + url
        
        self.url = url
        self.timeout = timeout
        self.filename = url.split('/')[-1]
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        self.img = None
        self.buffer = None

    def download_image(self):
        try:
            # 发送HTTP请求并获取响应
            response = requests.get(
                self.url,
                stream=True,
                timeout=self.timeout,
                headers=self.headers)
            
            # 检查请求是否成功
            response.raise_for_status()

            # 生成图片引用
            self.buffer = BytesIO(response.content)
            self.img = Image.open(self.buffer)

            # debug 用，会调用系统默认应用显示图片
            # self.img.show()
            
            print(f'Image downloaded completed: {self.filename}')
        except requests.exceptions.RequestException as e:
            print(f'Error downloading image: {e}')
    
    def print_image(self):
        if self.img:
            print(f'Image: {self.filename}')
            print(f'Image size: {self.img.size}')
        else:
            print('No image to display.')
