from typing import List, Optional
from enum import Enum

class OutlineBlockType(Enum):
    ROMAN_NUMERAL = 4
    CAPITAL_POINT = 3
    ARABIC_NUMERAL = 2
    LOWERCASE_POINT = 1
    LOWERCASE_ROMAN_NUMERAL = 0

class OutlineBlock():
    def __init__(self, content=None, references=None, verses=None, type=None):
        self.content = content
        self.references = references
        self.verses = verses
        self.type = type
        self.subpoints: List[OutlineBlock] = []

    def add_subpoint(self, subpoint):
        self.subpoints.append(subpoint)