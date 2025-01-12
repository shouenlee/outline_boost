import os


def get_words(page, line):
    result = []
    for word in page.words:
        if _in_span(word, line.spans):
            result.append(word)
    return result

# To learn the detailed concept of "span" in the following codes, visit: https://aka.ms/spans 
def _in_span(word, spans):
    for span in spans:
        if word.span.offset >= span.offset and (word.span.offset + word.span.length) <= (span.offset + span.length):
            return True
    return False

def document_paragraph_to_content_list(paragraphs):
    content_list = []
    for paragraph in paragraphs:
        content_list.append(paragraph.content)
    return content_list

def analyze_read():
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.ai.documentintelligence.models import DocumentAnalysisFeature, AnalyzeResult, AnalyzeDocumentRequest
    import json

    # For how to obtain the endpoint and key, please see PREREQUISITES above.
    #endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
    #key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]

    endpoint = "https://ai-verseapp434316061029.cognitiveservices.azure.com/"
    key = ""

    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    
    # If analyzing a local document, remove the comment markers (#) at the beginning of these 11 lines.
    # Delete or comment out the part of "Analyze a document at a URL" above.
    # Replace <path to your sample file>  with your actual file path.
    path_to_sample_document = "msg4.jpg"
    with open(path_to_sample_document, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-read",
            body=f,
            features=[DocumentAnalysisFeature.LANGUAGES],
            content_type="application/octet-stream",
        )
    result: AnalyzeResult = poller.result()
    
    # [START analyze_read]
    # Detect languages.
    # print("----Languages detected in the document----")
    # if result.languages is not None:
    #     for language in result.languages:
    #         print(f"Language code: '{language.locale}' with confidence {language.confidence}")
    
    # To learn the detailed concept of "bounding polygon" in the following content, visit: https://aka.ms/bounding-region
    # Analyze pages.
    # for page in result.pages:
    #     print(f"----Analyzing document from page #{page.page_number}----")
    #     print(f"Page has width: {page.width} and height: {page.height}, measured with unit: {page.unit}")

    #     # Analyze lines.
    #     if page.lines:
    #         for line_idx, line in enumerate(page.lines):
    #             words = get_words(page, line)
    #             print(
    #                 f"...Line # {line_idx} has {len(words)} words and text '{line.content}' within bounding polygon '{line.polygon}'"
    #             )

    #             # Analyze words.
    #             for word in words:
    #                 print(f"......Word '{word.content}' has a confidence of {word.confidence}")
        
    # Analyze paragraphs.
    # if result.paragraphs:
    #     #print(f"----Detected #{len(result.paragraphs)} paragraphs in the document----")
    #     for paragraph in result.paragraphs:
    #         #print(f"Found paragraph within {paragraph.bounding_regions} bounding region")
    #         #print(f"...with content: '{paragraph.content}'")
    #         print(paragraph.content)

    #raw_outline = json.dumps(result.as_dict(), indent=4)
    #with open('raw_outline.json', 'w') as json_file:
    #        json_file.write(raw_outline)
        
    print("----------------------------------------")
    # [END analyze_read]
    return result

# Next steps:
# Learn more about Layout model: https://aka.ms/di-read
# Find more sample code: https://aka.ms/doc-intelligence-samples