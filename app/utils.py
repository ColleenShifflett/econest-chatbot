import re

def sanitize_input(text: str) -> str:
    """Remove any potentially harmful characters from input"""
    return re.sub(r'[^\w\s?.,!]', '', text)
