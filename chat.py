# Import modules
from llama_index.llms.ollama import Ollama
import qdrant_client
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Create Qdrant client and store
client = qdrant_client.QdrantClient(path="./qdrant_data")
vector_store = QdrantVectorStore(client=client, collection_name="polyrag_documents")
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Initialize Ollama and ServiceContext
Settings.llm = Ollama(model="mistral")
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# Create VectorStoreIndex and query engine
index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store
)
query_engine = index.as_query_engine()

# Perform a query and print the response
response = query_engine.query("What does the author think about Star Trek? In One line")
print(response)