if __name__ == "__main__":
    from azure.core.exceptions import HttpResponseError
    from dotenv import find_dotenv, load_dotenv
    from outline_ocr import analyze_read, document_paragraph_to_content_list

    paragraphs = None
    try:
        print("Beginning document read")
        load_dotenv(find_dotenv())
        paragraphs = analyze_read("outlines")

    except HttpResponseError as error:
        # Examples of how to check an HttpResponseError
        # Check by error code:
        if error.error is not None:
            if error.error.code == "InvalidImage":
                print(f"Received an invalid image error: {error.error}")
            if error.error.code == "InvalidRequest":
                print(f"Received an invalid request error: {error.error}")
            # Raise the error again after printing it
            raise
        # If the inner error is None and then it is possible to check the message to get more information:
        if "Invalid request".casefold() in error.message.casefold():
            print(f"Uh-oh! Seems there was an invalid request: {error}")
        # Raise the error again
        raise
    print(r"‾‾‾‾\ Document read completed\n")
    
    print("Building outline...")



    from outline_schema import OutlineSchema, BuilderUtils
    outline = OutlineSchema()
    content_list = document_paragraph_to_content_list(paragraphs)
    for c in content_list:
        print(c)
    outline.build(content_list)
    outline.print_tree()
    outline.to_markdown()