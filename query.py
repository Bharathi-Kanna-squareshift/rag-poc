# query.py
from llama_index.core import VectorStoreIndex, QueryBundle, Response, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from main import es_vector_store

def run_query(query: str):
    # Local LLM to send user query to
    local_llm = Ollama(model="mistral")
    Settings.embed_model = OllamaEmbedding("mistral")

    index = VectorStoreIndex.from_vector_store(es_vector_store)
    query_engine = index.as_query_engine(local_llm, similarity_top_k=10)

    bundle = QueryBundle(query, embedding=Settings.embed_model.get_query_embedding(query))
    result = query_engine.query(bundle)
    return result

# Usage example:
query = "Give me summary of water related issues"
result = run_query(query)
print(result)
