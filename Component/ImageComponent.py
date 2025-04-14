import requests
import base64
from io import BytesIO
from PIL import Image
from bs4 import Tag

class ImageLoader:
    def __init__(self, url,timeout = 10,headers = None,index = 0,origin:Tag = None,attri_name :str = 'src'):
        if not url.startswith('https'):
            url = 'https:' + url
        self.origin = origin
        self.index = index
        self.url = url
        self.timeout = timeout
        self.attri_name = attri_name
        self.filename = url.split('/')[-1]
        self.extension = self.filename.split('.')[-1].lower()
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        self.img = None
        self.buffer = None
        self.base64 = None
        self.type_mapping = {
            'jpg' : 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png' : 'image/png',
            'gif' : 'image/gif',
            'bmp' : 'image/bmp',
            'webp': 'image/webp',
        }

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
            # self.buffer = BytesIO(response.content)
            # self.img = Image.open(self.buffer)

            # debug 用，会调用系统默认应用显示图片
            # self.img.show()

            self.base64 = base64.b64encode(response.content).decode('utf-8')
            
            print(f'Image downloaded completed: {self.filename}')
        except requests.exceptions.RequestException as e:
            print(f'Error downloading image: {e}')
    
    def apply_image(self):
        it = self.type_mapping[self.extension] or 'image/jpeg'
        self.origin[self.attri_name] = f"data:{it};base64,{self.base64}"

    def send_to_image_download_service(self,service=None):
        # 这里可以添加调用图片下载服务的代码(目前不需要，只是接口统一
        self.download_image()
        self.apply_image()