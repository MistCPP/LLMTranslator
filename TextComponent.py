class TextComponent:
    def __init__(self, text: str, font = 16, color: str = "white", bold: bool = False, italic: bool = False, underline: bool = False):
        self.text = text
        self.font = font
        self.color = color
        self.bold = bold
        self.italic = italic
        self.underline = underline

    def print_text(self):
        print(f"Text: {self.text}")
