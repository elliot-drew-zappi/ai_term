import chromadb
from chromadb.config import Settings
import os

chroma_dir = os.getenv("AI_TERM_DIR", os.getcwd()) 

def create_db(chroma_dir = chroma_dir):
    client = chromadb.Client(
            Settings(
                persist_directory=chroma_dir,
                chroma_db_impl="duckdb",
                )
            )
    client.persist()
    return client


