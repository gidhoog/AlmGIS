# see: https://www.perplexity.ai/search/get-the-body-of-a-html-string-sBFz6hkDQsq3yWjFNLalkA

from html.parser import HTMLParser
import re

class BodyExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.recording = False
        self.body_content = []

    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.recording = True
        elif self.recording:
            attrs_str = ' '.join(f'{k}="{v}"' for k, v in attrs)
            if attrs_str == '':
                self.body_content.append(f"<{tag}>".strip())
            else:
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
        content = ''.join(self.body_content)
        # Remove leading spaces/tabs from each line
        return re.sub(r'^\s+', '', content, flags=re.MULTILINE)

# Example usage
html_string = """
<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body>
    <h1>Hello, World!</h1>
    <p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">This is a <strong>test</strong>.</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
</body>
</html>
"""

parser = BodyExtractor()
parser.feed(html_string)
body_content = parser.get_body_content()
print(body_content)
