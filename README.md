# PolyRAG
## A simple RAG solution in python to enhance local LLMs using your documents as context

This tool is extremely lightweight and can be configured to use any LLM available in Ollama
and any embedding model available in HuggingFace.

## Installation:
```
git clone https://github.com/nicolasleao/polyrag.git
pip install -r requirements.txt
```

## Configuration:
> config.json
```json
{
	"llm": "mistral",
	"embedding_model": "BAAI/bge-small-en-v1.5"
}
```

## Indexing:

Simply running:
```
python indexer.py
```
Will create embeddings for all documents inside the data/ directory (markdown or pdf supported)
and save them to a local qdrant database.

# Querying
You can run a simple chat loop to ask questions about your documents by running:
```
python chat.py
```
