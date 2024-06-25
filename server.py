from fastapi import FastAPI, BackgroundTasks
from llama_index.llms.ollama import Ollama
import qdrant_client
from llama_index.core import VectorStoreIndex, StorageContext, SimpleDirectoryReader, Document, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor
from llama_index.core.ingestion import IngestionPipeline
import json
import uuid

config = {}
with open('config.json') as f:
    config = json.load(f)

# Create Qdrant client and store
client = qdrant_client.QdrantClient(url="http://localhost:6333")
vector_store = QdrantVectorStore(client=client, collection_name="polyrag_documents")
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Initialize Ollama and ServiceContext
Settings.llm = Ollama(model=config["llm"])
Settings.embed_model = HuggingFaceEmbedding(model_name=config["embedding_model"])

# create the pipeline with transformations
pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=25, chunk_overlap=0),
        TitleExtractor(),
        HuggingFaceEmbedding(model_name=config["embedding_model"]),
    ],
    vector_store=vector_store
)

async def index_from_data_folder():
    reader = SimpleDirectoryReader(input_dir="./data", required_exts=[".pdf", ".md"])
    documents = reader.load_data()
    pipeline.run(documents=documents)

async def index_single_document(id, body):
    doc = Document(doc_id=id, text=body)
    pipeline.run(documents=[doc])

# Create fastAPI backend
app = FastAPI()

@app.get("/index_data_folder")
async def index_data_folder(background_tasks: BackgroundTasks):
    background_tasks.add_task(index_from_data_folder)
    return {"success": True, "message": "successfully queued the indexing of documents in the /data/ folder"}

@app.get("/index_document")
async def index_document(body: str, background_tasks: BackgroundTasks):
    doc_id = str(uuid.uuid4())
    background_tasks.add_task(index_single_document, doc_id, body)
    return {"success": True, "message": "successfully queued the indexing of document with id: " + doc_id}

@app.get("/query/")
def query(q: str):
    # Create VectorStoreIndex and query engine
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store
    )
    query_engine = index.as_query_engine()
    query_result = query_engine.query(q)
    return {"question": q, "response": query_result.response}