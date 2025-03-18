from html.parser import HTMLParser

class BodyContentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.recording = False
        self.body_content = []

    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.recording = True
        elif self.recording:
            attrs_str = ' '.join([f'{attr[0]}="{attr[1]}"' for attr in attrs])
            self.body_content.append(f"<{tag} {attrs_str}>".strip())

    def handle_endtag(self, tag):
        if tag == 'body':
            self.recording = False
        elif self.recording:
            self.body_content.append(f"</{tag}>")

    def handle_data(self, data):
        if self.recording:
            self.body_content.append(data)

    def get_body_content(self):
        return ''.join(self.body_content)

# Usage example
html_content = """
<html>
<head><title>Example</title></head>
<body>
<h1>Hello, World!</h1>
<p>This is a paragraph.</p>
</body>
</html>
"""

parser = BodyContentParser()
parser.feed(html_content)
body_content = parser.get_body_content()
print(body_content)
