import os
import json

def get_words(page, line) -> list:
    result = []
    for word in page.words:
        if _in_span(word, line.spans):
            result.append(word)
    return result

# From https://aka.ms/spans 
def _in_span(word, spans) -> bool:
    for span in spans:
        if word.span.offset >= span.offset and (word.span.offset + word.span.length) <= (span.offset + span.length):
            return True
    return False

def document_paragraph_to_content_list(paragraphs) -> list:
    content_list = []
    for paragraph in paragraphs:
        content_list.append(paragraph.content)
    return content_list

def find_jpg_files(directory) -> list:
    jpg_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.jpg'):
                jpg_files.append(os.path.join(root, file))
    return sorted(jpg_files)

def analyze_read(images_path) -> list:
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.ai.documentintelligence.models import DocumentAnalysisFeature, AnalyzeResult, AnalyzeDocumentRequest

    #endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
    #key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]


    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    paragraphs = []
    image_paths = find_jpg_files(images_path)
    print(f"Found images: {image_paths} to analyze")
    for image_path in image_paths:
        with open(image_path, "rb") as f:
            poller = document_intelligence_client.begin_analyze_document(
                "prebuilt-read",
                body=f,
                features=[DocumentAnalysisFeature.LANGUAGES]
            )
        result: AnalyzeResult = poller.result()
        paragraphs.extend(result.paragraphs)

        # Save raw OCR result to file
        filename_raw = os.path.splitext(os.path.basename(image_path))[0]
        save_raw_ocr_to_file(result, "raw_ocr", filename_raw)
        
    print("----------------------------------------")
    return paragraphs

def save_raw_ocr_to_file(raw_ocr_result, directory, filename) -> None:
    raw_outline = json.dumps(raw_ocr_result.as_dict(), indent=4)
    with open(f'{directory}/{filename}.json', 'w') as json_file:
           json_file.write(raw_outline)