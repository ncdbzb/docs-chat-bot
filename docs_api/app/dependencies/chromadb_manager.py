from app.clients.chromadb_client import ChromaDBManager


chromadb_manager = ChromaDBManager()

def get_chromadb_manager() -> ChromaDBManager:
    return chromadb_manager