import os
import json
from fastapi import FastAPI, HTTPException
from llama_index.core import Document, Settings, IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from query import run_query

app = FastAPI()

# Load .env file contents into environment variables
load_dotenv('.env')

# Initialize ElasticsearchStore
es_vector_store = ElasticsearchStore(index_name="calls",
                                     vector_field='conversation_vector',
                                     text_field='conversation',
                                     es_cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
                                     es_api_key=os.getenv("ELASTIC_API_KEY"))

def get_documents_from_file(file):
   """Reads a json file and returns list of Documents"""
   with open(file=file, mode='rt') as f:
       conversations_dict = json.loads(f.read())
      
   # Build Document objects using fields of interest.
   documents = [Document(text=item['conversation'],
                         metadata={"conversation_id": item['conversation_id']})
                for
                item in conversations_dict]
   return documents

def run_ingestion_pipeline():
    # Embedding Model to do local embedding using Ollama.
    ollama_embedding = OllamaEmbedding("mistral")

    # LlamaIndex Pipeline configured to take care of chunking, embedding
    # and storing the embeddings in the vector store.
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=350, chunk_overlap=50),
            ollama_embedding,
        ],
        vector_store=es_vector_store
    )

    # Load data from a json file into a list of LlamaIndex Documents
    documents = get_documents_from_file(file="conversations.json")

    pipeline.run(documents=documents)
    print(".....Done running pipeline.....\n")

@app.post("/ingest")
def run_pipeline():
    try:
        run_ingestion_pipeline()
        return {"message": "Data ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def process_query(query_request: QueryRequest):
    try:
        result = run_query(query_request.query)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
