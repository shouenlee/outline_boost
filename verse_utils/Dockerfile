# verse_requestor and verse_search Dockerfile
FROM swift:5.7

WORKDIR /app

COPY . .

# Compile verse_requestor
RUN swiftc verse_requestor/Sources/main.swift verse_requestor/Sources/Utils.swift -o Release/verse_requestor
RUN chmod +x Release/verse_requestor

# Compile verse_search
RUN swiftc verse_search/Sources/main.swift verse_search/Sources/Utils.swift -o Release/verse_search
RUN chmod +x Release/verse_search

EXPOSE 5001

RUN apt update && apt install -y python3 python3-pip
RUN apt install -y curl
RUN pip install -r requirements.txt

CMD ["python3", "verse_utils.py"]