import re

def tokenize(text: str) -> list[str]:
    return re.findall(r'[a-z]+', text.lower())


