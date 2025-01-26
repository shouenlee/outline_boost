# ollama_service Dockerfile
FROM ollama/ollama:latest

EXPOSE 11434

RUN ollama serve & sleep 5
RUN ollama pull Mistral