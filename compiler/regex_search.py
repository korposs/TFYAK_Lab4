import re

PATTERN_OGRN = r"\b[15]\d{12}\b"

PATTERN_PASCAL_COMMENT = r"\{[^}]*\}|\(\*.*?\*\)"

RGB_NUMBER = r"(25[0-5]|2[0-4]\d|1\d\d|\d\d?)"
PATTERN_RGB = r"rgb\(\s*" + RGB_NUMBER + r"\s*,\s*" + RGB_NUMBER + r"\s*,\s*" + RGB_NUMBER + r"\s*\)"

SEARCH_TASKS = [
    ("ОГРН юридического лица", PATTERN_OGRN),
    ("Комментарии Pascal", PATTERN_PASCAL_COMMENT),
    ("RGB-цвет", PATTERN_RGB),
]

class Match:
    def __init__(self, text, line, start_col, length):
        self.text = text
        self.line = line
        self.start = start_col
        self.length = length

    def __repr__(self):
        return f"Match('{self.text}', line={self.line}, pos={self.start}, len={self.length})"


def _line_col_from_pos(text, pos):
    line = text.count("\n", 0, pos) + 1
    line_start = text.rfind("\n", 0, pos) + 1
    col = pos - line_start + 1
    return line, col


def search(text, pattern):
    if not text.strip():
        return []

    results = []
    for m in re.finditer(pattern, text, re.MULTILINE):
        line, col = _line_col_from_pos(text, m.start())
        results.append(Match(m.group(0), line, col, len(m.group(0))))
    return results