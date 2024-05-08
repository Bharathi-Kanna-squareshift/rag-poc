from llama_index.core import VectorStoreIndex, QueryBundle, Response, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.store.elasticsearch import ElasticsearchStore
from dotenv import load_dotenv
import os

class MyService:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv('.env')

        # Initialize ElasticsearchStore with credentials from .env
        self.es_vector_store = ElasticsearchStore(
            index_name="calls",
            vector_field='conversation_vector',
            text_field='conversation',
            es_cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
            es_api_key=os.getenv("ELASTIC_API_KEY")
        )

        # Initialize OllamaEmbedding and LLM model
        self.ollama_embedding = OllamaEmbedding("mistral")
        self.local_llm = Ollama(model="mistral")
        Settings.embed_model = self.ollama_embedding

        # Initialize VectorStoreIndex and query engine
        self.index = VectorStoreIndex.from_vector_store(self.es_vector_store)
        self.query_engine = self.index.as_query_engine(
            self.local_llm, similarity_top_k=10)

    def query_vector_store(self, query: str) -> Response:
        # Create QueryBundle with the provided query
        bundle = QueryBundle(
            query, embedding=Settings.embed_model.get_query_embedding(query))

        # Query the vector store index
        result = self.query_engine.query(bundle)
        return result
