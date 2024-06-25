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

> Setting up Qdrant
First you need to run the qdrant server associated with the app using docker-compose
```
docker compose up -d
```

Then you must create the collection polyrag_documents inside qdrant, this vector dimension is what the default embedding model `BAAI/bge-small-en-v1.5` produces, so make sure to check the documentation of your embedding model and create a collection with the matching vector dimensions:

Access the qdrant web UI (`http://localhost:6333/dashboard`) and run the following request:
```
PUT /collections/polyrag_documents
{
    "vectors": {
      "size": 384,
      "distance": "Cosine"
    }
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

# FastAPI server
This tool can also be served as an API powered by FastAPI, to do that, ensure you've installed all dependencies and run the following:
```
fastapi run server.py
```

The swagger api docs are served with the application, and can be accessed in the url
`http://localhost:8000/docs`

## Example API request/response:
> http://0.0.0.0:8000/query/?q=what%20does%20the%20author%20think%20about%20star%20trek
```
{
  "question": "what does the author think about star trek",
  "response": " The author appears to hold Star Trek in high regard, considering it as a \"rare beast\" that offers both visual appeal and genuine emotional depth."
}
```