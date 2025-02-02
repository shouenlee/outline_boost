# ollama_service Dockerfile
FROM ollama/ollama:latest

EXPOSE 11434

Run nohup bash -c "ollama serve &" && sleep 5 && ollama pull mistral