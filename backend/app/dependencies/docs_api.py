from app.clients.docs_api_client import DocsApiClient


docs_api_client = DocsApiClient()

def get_docs_api_client() -> DocsApiClient:
    return docs_api_client
