from typing import List, Optional
from outline_block import OutlineBlock, OutlineBlockType
import json
import re

class OutlineSchema:
    conference_title: Optional[str]
    message_number: Optional[int]
    message_title: Optional[str]
    scripture_reading: Optional[List[str]]
    roman_numerals: Optional[List[OutlineBlock]]
    jsonified: Optional[str]

    def __init__(self, conference_title=None, message_number=None, message_title=None, scripture_reading=None, roman_numerals=None):
        self.conference_title = conference_title
        self.message_number = message_number
        self.message_title = message_title
        self.scripture_reading = scripture_reading
        self.roman_numerals = roman_numerals

    def missing_fields(self) -> List[str]:
        missing_fields = []
        if self.conference_title is None:
            missing_fields.append("conference_title")
        if self.message_number is None:
            missing_fields.append("message_number")
        if self.message_title is None:
            missing_fields.append("message_title")
        if self.scripture_reading is None:
            missing_fields.append("scripture_reading")
        if self.roman_numerals is None:
            missing_fields.append("roman_numerals")
        return missing_fields

    # Build the outline according to the schema from extracted paragraphs.
    def build(self, paragraphs: List[str]) -> None:
        # Unsure if every outline has the same topic/message/title/scripture structure. Will find first roman numeral and work backwards to fill in the rest of the fields.
        first_roman_numeral_index = BuilderUtils.extract_first_roman_numeral_index(paragraphs)
        if first_roman_numeral_index == -1:
            raise ValueError("No Roman numeral I. found in the paragraphs.")
        
        # Generally expect roman 1 to be 5th paragraph. Assign the rest of the fields relative to first roman numeral.
        self.scripture_reading = paragraphs[first_roman_numeral_index - 1] if first_roman_numeral_index > 0 else None
        self.message_title = paragraphs[first_roman_numeral_index - 2] if first_roman_numeral_index > 1 else None
        self.message_number = paragraphs[first_roman_numeral_index - 3] if first_roman_numeral_index > 2 else None
        self.conference_title = paragraphs[first_roman_numeral_index - 4] if first_roman_numeral_index > 3 else None

        # Create json representation of outline
        self.jsonified = BuilderUtils.jsonify_outline(paragraphs[first_roman_numeral_index:], self.conference_title, self.message_number, self.message_title, self.scripture_reading)
        with open('outline.json', 'w') as json_file:
            json_file.write(self.jsonified)
        
        # Create tree structure of outline
        self.roman_numerals = BuilderUtils.build_content_tree(paragraphs[first_roman_numeral_index:])

    def print_tree(self) -> None:
        def print_point(point: OutlineBlock, indent=0):
            print(indent * " " + point.content)
            for subpoint in point.subpoints:
                print_point(subpoint, indent + 4)
        for roman_numeral in self.roman_numerals:
            print_point(roman_numeral)

    def __str__(self) -> str:
        return f"Conference Title: {self.conference_title}\nMessage Number: {self.message_number}\nMessage Title: {self.message_title}\nScripture Reading: {self.scripture_reading}\nRoman Numerals: {self.roman_numerals}"

    def __repr__(self) -> str:
        #todo: make this print out the outline in a more readable format
        return f"OutlineSchema(conference_title={self.conference_title}, message_number={self.message_number}, message_title={self.message_title}, scripture_reading={self.scripture_reading}, roman_numerals={self.roman_numerals})"

class BuilderUtils:
    @staticmethod
    def extract_first_roman_numeral_index(paragraphs: List[str]) -> List[str]:
        roman_numeral_pattern = re.compile(r'^\bI+\.')
        for index, paragraph in enumerate(paragraphs):
            if roman_numeral_pattern.match(paragraph):
                return index
        return -1

    @staticmethod
    def build_content_tree(paragraphs: List[str]) -> List[OutlineBlock]:
        roman_numerals = []
        point_stack = []
        prev_point = None
        curr_parent = None

        def find_parent_point(curr_point: OutlineBlock) -> OutlineBlock:
            for point in reversed(point_stack):
                if point.type.value > curr_point.type.value:
                    return point
            return None

        # First point is always roman numeral I.
        curr_point = OutlineBlock(paragraphs[0], None, None, None)
        curr_point.type = OutlineBlockType.ROMAN_NUMERAL
        roman_numerals.append(curr_point)
        point_stack.append(curr_point)
        prev_point = curr_point

        for paragraph in paragraphs[1:]:
            curr_point = OutlineBlock(paragraph, None, None, None)
            if BuilderUtils.is_roman_numeral_not_I(paragraph):
                curr_point.type = OutlineBlockType.ROMAN_NUMERAL
                roman_numerals.append(curr_point)
                curr_parent = None
            elif BuilderUtils.is_capital_point(paragraph):
                curr_point.type = OutlineBlockType.CAPITAL_POINT
                if prev_point.type == OutlineBlockType.ROMAN_NUMERAL:
                    curr_parent = prev_point
                elif prev_point.type.value < OutlineBlockType.CAPITAL_POINT.value:
                    # Find most recent roman numeral
                    curr_parent = find_parent_point(curr_point)
                if curr_parent is None:
                    raise ValueError("Capital point found without a parent Roman numeral.")
                curr_parent.add_subpoint(curr_point)                    
            elif BuilderUtils.is_arabic_numeral(paragraph):
                curr_point.type = OutlineBlockType.ARABIC_NUMERAL
                if prev_point.type == OutlineBlockType.CAPITAL_POINT:
                    curr_parent = prev_point
                elif prev_point.type.value < OutlineBlockType.ARABIC_NUMERAL.value:
                    # Find most recent arabic capital point
                    curr_parent = find_parent_point(curr_point)
                if curr_parent is None:
                    raise ValueError("Arabic numeral found without a parent Capital point.")
                curr_parent.add_subpoint(curr_point)

            elif BuilderUtils.is_lowercase_point(paragraph):
                curr_point.type = OutlineBlockType.LOWERCASE_POINT
                if prev_point.type == OutlineBlockType.ARABIC_NUMERAL:
                    curr_parent = prev_point
                if curr_parent is None:
                    raise ValueError("Lowercase point found without a parent Arabic numeral.")
                curr_parent.add_subpoint(curr_point)
            else:
                raise ValueError(f"Unknown paragraph type: {paragraph}")
            point_stack.append(curr_point)
            prev_point = curr_point

        return roman_numerals


    @staticmethod
    def is_roman_numeral(paragraph: str) -> bool:
        return True if re.match(r'^\b[IVX]+\.', paragraph) else False # Assuming we will not use L, C, D, M
    
    def is_roman_numeral_not_I(paragraph: str) -> bool:
        any_rom_num = BuilderUtils.is_rom_numeral(paragraph)
        i = re.match(r'^\bI\.', paragraph)
        return True if any_rom_num and not i else False

    @staticmethod
    def extract_roman_numeral(paragraph: str) -> Optional[str]:
        match = re.match(r'^\b[IVXLCDM]+\.', paragraph)
        return match.group(0) if match else None

    @staticmethod
    def is_capital_point(paragraph: str) -> bool:
        return True if re.match(r'^\b[A-Z]+\.', paragraph) else False
    
    @staticmethod
    def extract_capital_point(paragraph: str) -> Optional[str]:
        match = re.match(r'^\b[A-Z]+\.', paragraph)
        return match.group(0) if match else None

    @staticmethod
    def is_arabic_numeral(paragraph: str) -> bool:
        return True if re.match(r'^\b[0-9]+\.', paragraph) else False
    
    @staticmethod
    def extract_arabic_numeral(paragraph: str) -> Optional[str]:
        match = re.match(r'^\b[0-9]+\.', paragraph)
        return match.group(0) if match else None

    @staticmethod
    def is_lowercase_point(paragraph: str) -> bool:
        return True if re.match(r'^\b[a-z]+\.', paragraph) else False
    
    @staticmethod
    def extract_lowercase_point(paragraph: str) -> Optional[str]:
        match = re.match(r'^\b[a-z]+\.', paragraph)
        return match.group(0) if match else None

    @staticmethod
    def extract_scripture_references(paragraphs: List[str]) -> List[str]:
        # This is a placeholder implementation. The actual implementation would depend on the format of the scripture references.
        scripture_references = []
        for paragraph in paragraphs:
            if "John" in paragraph or "Genesis" in paragraph:  # Example check for scripture references
                scripture_references.append(paragraph)
        return scripture_references
    
    @staticmethod
    def jsonify_outline(outline_points: List[str], conference_title: str=None, message_number: int=None, message_title: str=None, scripture_reading: List[str]=None) -> str:
        outline = {}
        outline["conference_title"] = conference_title if conference_title else ""
        outline["message_number"] = message_number if message_number else ""
        outline["message_title"] = message_title if message_title else ""
        outline["scripture_reading"] = scripture_reading if scripture_reading else []

        for paragraph in outline_points:
            pt_number = None
            if BuilderUtils.is_roman_numeral(paragraph):
                pt_number = BuilderUtils.extract_roman_numeral(paragraph)
            elif BuilderUtils.is_capital_point(paragraph):
                pt_number = BuilderUtils.extract_capital_point(paragraph)
            elif BuilderUtils.is_arabic_numeral(paragraph):
                pt_number = BuilderUtils.extract_arabic_numeral(paragraph)
            elif BuilderUtils.is_lowercase_point(paragraph):
                pt_number = BuilderUtils.extract_lowercase_point(paragraph)
            else:
                pt_number = "Unknown"

            outline[pt_number] = paragraph

        return json.dumps(outline, indent=4)