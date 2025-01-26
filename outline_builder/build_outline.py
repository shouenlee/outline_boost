if __name__ == "__main__":
    from azure.core.exceptions import HttpResponseError
    from dotenv import find_dotenv, load_dotenv
    from outline_ocr import analyze_read, document_paragraph_to_content_list
    from colorama import Fore, Style

    paragraphs = None
    outline_dir = "outlines" #input("Enter the relative directory of the outline images: ")
    try:
        load_dotenv(find_dotenv())
        print("Beginning document ocr")
        paragraphs = analyze_read(outline_dir)

    except HttpResponseError as error:
        if error.error is not None:
            if error.error.code == "InvalidImage":
                print(Fore.RED + f"Received an invalid image error: {error.error}" + Style.RESET_ALL)
            if error.error.code == "InvalidRequest":
                print(Fore.RED + f"Received an invalid request error: {error.error}" + Style.RESET_ALL)
            raise

        # If the inner error is None and then it is possible to check the message to get more information:
        if "Invalid request".casefold() in error.message.casefold():
            print(f"Uh-oh! Seems there was an invalid request: {error}")
        raise

    print(Fore.GREEN + "Outline OCR completed successfully" + Style.RESET_ALL)
    print("Building outline...")

    from outline_schema import OutlineSchema, BuilderUtils
    outline = OutlineSchema()
    
    content_list = document_paragraph_to_content_list(paragraphs)
    outline.build(content_list)
    #outline.print_tree()
    outline.to_markdown()