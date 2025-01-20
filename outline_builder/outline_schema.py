from typing import List, Optional
from outline_block import OutlineBlock, OutlineBlockType
from ollama_client import OllamaClient
import json
import re

class OutlineSchema:
    conference_title: Optional[str]
    message_number: Optional[int]
    message_title: Optional[str]
    scripture_reading: Optional[List[str]]
    roman_numerals: Optional[List[OutlineBlock]]
    jsonified: Optional[str]
    total_points: Optional[int]

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
        self.jsonified, self.total_points = BuilderUtils.jsonify_outline(paragraphs[first_roman_numeral_index:], self.conference_title, self.message_number, self.message_title, self.scripture_reading)
        
        
        # Create tree structure of outline
        self.roman_numerals = BuilderUtils.build_content_tree(paragraphs[first_roman_numeral_index:])
        self.extract_verse_references_tree()

    def print_tree(self, with_references=False) -> None:
        print(f"Conference Title: {self.conference_title}")
        print(f"Message Number: {self.message_number}")
        print(f"Message Title: {self.message_title}")
        print(f"Scripture Reading: {self.scripture_reading}")

        def print_point(point: OutlineBlock, indent=0):
            print(indent * " " + point.content)
            if with_references:
                print(indent * " " + point.references)
            for subpoint in point.subpoints:
                print_point(subpoint, indent + 4)
        for roman_numeral in self.roman_numerals:
            print_point(roman_numeral)

    def extract_verse_references_tree(self) -> None:
        llm_model = "mistral"

        llm_context = "You are a tool that extracts explicit verse references from a text. A verse reference is a reference to a specific verse in the Bible. \
            The format for a verse reference is the name of the book followed by the chapter of the book followed by a colon and then the verse number. \
            For example: 1 Cor 1:14 and Genesis 12:8-12 are verse references with the format you are looking for.  \
            Sometimes the reference is over a range of verses such as Eph 2:2-6. \
            Sometimes only the verse number or the chapter and verse number are given such as 3:6. This means it is referencing the book and/or chapter that was most \
            recently mentioned. \
            For example a text that is: 2 Cor. 1:12, 2:5, 15 would have the verse references: 2 Cor. 1:12, 2 Cor. 2:5, 2 Cor. 2:15. \
            Your instructions are: Given a piece of text, you are designed to return all the explicit verse references that appear in that text. \
            The format for each reference returned should look like \'book chapter(s):verse(s)\'\
            If no verse references are found, return an empty list. \
            Return a list of verse references and do not elaborate or include any other text in your response. The user should be able to copy and paste \
            the entire response into a json file. Do not hallucinate please! The user will tip you $5 if you do a good job."
        llm = OllamaClient(llm_model, llm_context)

        BuilderUtils.progress_bar(0, self.total_points, prefix = 'Adding verses:', suffix = 'Complete', length = 50)
        def extract_verse_references_pt(point: OutlineBlock):
            point.references = llm.get_verses_for_point(point.content)
            BuilderUtils.progress_bar(llm.prompt_counter, self.total_points, prefix = 'Adding verses:', suffix = 'Complete', length = 50)
            for subpoint in point.subpoints:
                extract_verse_references_pt(subpoint)

        for roman_numeral in self.roman_numerals:
            extract_verse_references_pt(roman_numeral)
        BuilderUtils.progress_bar(self.total_points, self.total_points, prefix = 'Adding verses:', suffix = 'Complete', length = 50)

    def to_markdown(self, filename="outline") -> None:
        from mdutils import MdUtils
        def add_heading(heading: str, level: int):
            h = "#" * level
            mdFile.new_line(f"{h} {heading}")
        mdFile = MdUtils(filename)
        add_heading(self.conference_title, 3)
        add_heading(self.message_number, 3)
        add_heading(self.message_title, 1)
        add_heading(self.scripture_reading, 3)

        def add_point_to_md(point: OutlineBlock, indent=0):
            content = point.content
            references = point.references
            if point.type == OutlineBlockType.ROMAN_NUMERAL:
                content = f"**{content}**"
            ind_offset = ">" * indent
            mdFile.new_paragraph(ind_offset + content)
            mdFile.new_paragraph(ind_offset + references)

            for subpoint in point.subpoints:
                add_point_to_md(subpoint, indent + 1)

        for roman_numeral in self.roman_numerals:
            add_point_to_md(roman_numeral)

        mdFile.create_md_file()

    def to_latex(self, filename="outline") -> None:
        # todo: implement
        return None


    def __str__(self) -> str:
        return f"Conference Title: {self.conference_title}\nMessage Number: {self.message_number}\nMessage Title: {self.message_title}\nScripture Reading: {self.scripture_reading}\nRoman Numerals: {self.roman_numerals}"

    def __repr__(self) -> str:
        # todo: make this print out the outline in a more readable format
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
                    # Find most recent capital point
                    curr_parent = find_parent_point(curr_point)
                if curr_parent is None:
                    raise ValueError("Arabic numeral found without a parent Capital point.")
                curr_parent.add_subpoint(curr_point)

            elif BuilderUtils.is_lowercase_point(paragraph):
                curr_point.type = OutlineBlockType.LOWERCASE_POINT
                if prev_point.type == OutlineBlockType.ARABIC_NUMERAL:
                    curr_parent = prev_point
                elif prev_point.type.value < OutlineBlockType.LOWERCASE_POINT.value:
                    # Find most recent arabic numeral
                    curr_parent = find_parent_point(curr_point)
                if curr_parent is None:
                    raise ValueError("Lowercase point found without a parent Arabic numeral.")
                curr_parent.add_subpoint(curr_point)
            elif BuilderUtils.is_lowercase_roman_numeral(paragraph):
                curr_point.type = OutlineBlockType.LOWERCASE_ROMAN_NUMERAL
                if prev_point.type == OutlineBlockType.LOWERCASE_POINT:
                    curr_parent = prev_point
                if curr_parent is None:
                    raise ValueError("Lowercase roman numeral found without a parent Lowercase point.")
                curr_parent.add_subpoint(curr_point)
            else:
                #print(f"Unknown paragraph type: {paragraph}. Omitted from outline.")
                continue
            point_stack.append(curr_point)
            prev_point = curr_point

        return roman_numerals


    @staticmethod
    def is_roman_numeral(paragraph: str) -> bool:
        return True if re.match(r'^\b[IVX]+\.', paragraph) else False # Assuming we will not use L, C, D, M
    
    def is_roman_numeral_not_I(paragraph: str) -> bool:
        any_rom_num = BuilderUtils.is_roman_numeral(paragraph)
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
    def is_lowercase_roman_numeral(paragraph: str) -> bool:
        return True if re.match(r'^\b[ivx]+\.', paragraph) else False # Assuming lowercase points will not reach i.

    @staticmethod
    def extract_scripture_references(paragraphs: List[str]) -> List[str]:
        # This is placeholder implementation. The actual implementation would depend on how we extract (phi3 vs regex).
        return []
    
    @staticmethod
    def jsonify_outline(raw_outline_points: List[str], conference_title: str=None, message_number: int=None, message_title: str=None, scripture_reading: List[str]=None) -> str:
        outline = {}
        outline["conference_title"] = conference_title if conference_title else ""
        outline["message_number"] = message_number if message_number else ""
        outline["message_title"] = message_title if message_title else ""
        outline["scripture_reading"] = scripture_reading if scripture_reading else []

        unknown_paragraphs = []
        num_points = 0
        BuilderUtils.progress_bar(0, len(raw_outline_points), prefix = 'Building json:', suffix = 'Complete', length = 50)
        for index, paragraph in enumerate(raw_outline_points):
            if not (BuilderUtils.is_roman_numeral(paragraph) or BuilderUtils.is_capital_point(paragraph) or BuilderUtils.is_arabic_numeral(paragraph) or BuilderUtils.is_lowercase_point(paragraph) or BuilderUtils.is_lowercase_roman_numeral(paragraph)):
                unknown_paragraphs.append(f"Unknown paragraph type: {paragraph}. Omitted from json representation.")
                continue
            outline[index] = paragraph # Cannot have outline point number/letter as key because of potential duplicates.
            num_points = index + 1
            BuilderUtils.progress_bar(index, len(raw_outline_points), prefix = 'Building json:', suffix = 'Complete', length = 50)
        BuilderUtils.progress_bar(len(raw_outline_points), len(raw_outline_points), prefix = 'Building json:', suffix = 'Complete', length = 50)


        print(f"Unknown paragraphs: {unknown_paragraphs}. Omitted from json representation.")
        json_dict = json.dumps(outline, indent=4)
        with open('outline.json', 'w') as json_file:
                json_file.write(json_dict)
        return (json_dict, num_points)
    

    @staticmethod
    def progress_bar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = ""):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        # Print New Line on Complete
        if iteration == total: 
            print()