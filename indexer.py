# Import modules
from llama_index.llms.ollama import Ollama
import qdrant_client
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor
from llama_index.core.ingestion import IngestionPipeline
import json

config = {}
with open('config.json') as f:
    config = json.load(f)

# Initialize Ollama and ServiceContext
Settings.llm = Ollama(model=config["llm"])
Settings.embed_model = HuggingFaceEmbedding(model_name=config["embedding_model"])

# Create Qdrant client and store
client = qdrant_client.QdrantClient(url="http://localhost:6333")
vector_store = QdrantVectorStore(client=client, collection_name="polyrag_documents")
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# create the pipeline with transformations
pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=1024, chunk_overlap=64),
        TitleExtractor(),
        HuggingFaceEmbedding(model_name=config["embedding_model"]),
    ],
    vector_store=vector_store
)

# Load markdown and pdf documents
reader = SimpleDirectoryReader(input_dir="./data", required_exts=[".pdf", ".md"])
documents = reader.load_data()

pipeline.run(documents=documents)

print("Document indexing completed.")