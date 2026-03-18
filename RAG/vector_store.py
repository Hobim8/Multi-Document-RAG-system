import os 
from typing import List
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings  




def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )

def create_vector_store(chunks: List[Document], persist_directory: str = "chromaDB"):  
    embeddings = get_embeddings()
    vector_store = Chroma.from_documents(
        documents=chunks,  #
        embedding=embeddings,
        persist_directory=persist_directory
    )
    return vector_store 


def load_vector_store(persist_directory: str = "chromaDB"):
    embeddings = get_embeddings()
    vector_store = Chroma(
        embedding_function=embeddings,
        persist_directory=persist_directory
    )
    return vector_store


def add_documents_to_store(chunks: List[Document], filename: str, persist_directory: str = "chromaDB"):  
    """
    Add documents to existing vector store with source metadata
    
    Args:
        chunks: Document chunks to add
        filename: Source filename for metadata
        persist_directory: Where vector DB is stored
    """
    
    # Add source metadata to each chunk
    for chunk in chunks:  
        chunk.metadata["source"] = filename 
    
    # Load existing store or create new one
    if os.path.exists(persist_directory):  
        vector_store = load_vector_store(persist_directory)
        vector_store.add_documents(chunks)
    else:
        vector_store = create_vector_store(chunks, persist_directory)
    
    return vector_store  


def delete_documents_by_source(filename: str, persist_directory: str = "chromaDB"):  
    """
    Delete all chunks from a specific source file
    
    Args:
        filename: Source filename to delete
        persist_directory: Where vector DB is stored
    
    Returns:
        Number of chunks deleted
    """
    if not os.path.exists(persist_directory):
        return 0
    
    vector_store = load_vector_store(persist_directory)
    
    # Get all documents with this source
    collection = vector_store._collection
    
    # Get all items
    results = collection.get()
    
    # Find IDs with matching source
    ids_to_delete = []
    for i, metadata in enumerate(results['metadatas']):
        if metadata.get('source') == filename:
            ids_to_delete.append(results['ids'][i])
    
    # Delete them
    if ids_to_delete:
        collection.delete(ids=ids_to_delete)
    
    return len(ids_to_delete)


def list_sources(persist_directory: str = "chromaDB") -> List[str]:  
    """
    List all unique source files in the vector store
    
    Returns:
        List of source filenames
    """
    if not os.path.exists(persist_directory):
        return []
    
    vector_store = load_vector_store(persist_directory)
    collection = vector_store._collection
    
    # Get all metadata
    results = collection.get()
    
    # Extract unique sources
    sources = set()
    for metadata in results['metadatas']:
        if 'source' in metadata:
            sources.add(metadata['source'])
    
    return sorted(list(sources))


def search_documents(query: str, vector_store, k: int = 3):
    """Search for relevant documents"""
    results = vector_store.similarity_search_with_score(query, k=k)
    return results

