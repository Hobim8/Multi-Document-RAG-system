import os 
from typing import List
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings



def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )

def create_vector_store(documents: List[Document], persist_directory: str = "chromaDB"):
    embeddings = get_embeddings()
    vector_store = Chroma.from_documents(
        documents=documents,
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

def search_documents(query: str, vector_store, k: int = 5):
    results = vector_store.similarity_search(query, k=k)
    return results 






