# see: https://www.perplexity.ai/search/get-the-body-of-a-html-string-sBFz6hkDQsq3yWjFNLalkA

import re

def extract_body_with_tags(html_string):
    body_pattern = r'<body[^>]*>(.*?)</body>'
    match = re.search(body_pattern, html_string, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(0)  # Return the entire <body> tag and its contents
    return None

# Example usage
html_string = """
<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body>
    <h1>Hello, World!</h1>
    <p>This is a <strong>test</strong>.</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
</body>
</html>
"""

body_content = extract_body_with_tags(html_string)
print(body_content)

