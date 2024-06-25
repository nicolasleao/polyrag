# Import modules
from llama_index.llms.ollama import Ollama
import qdrant_client
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
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

# Create VectorStoreIndex and query engine
index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store
)
query_engine = index.as_query_engine()

print('PolyRAG started, ask any questions about your documents or type \'bye\' to leave')
# chat loop to perform a query and print the response
running = True
while running:
    query = input('$ you -> ')
    if query == 'quit' or query == 'exit' or query == 'bye' or query == 'close':
        running = False
    else:
        response = query_engine.query(query)
        print('$ polyrag -> ', response)