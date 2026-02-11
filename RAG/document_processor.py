from typing import List
from xml.dom.minidom import Document
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents  import Document


# load the pdf file 
def load_pdf(file_path: str) -> List[Document]:
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents

#split the document into smaller chunks for better processing for LLM 
def split_document(
        document: List[Document],
        chunk_size: int = 1000,
        chunk_overlap: int = 200
) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len 
    )
    chunks = text_splitter.split_documents(document)
    return chunks 


# combine the loading and splitting into one function so it will be a clean pipeline for processing the document 
def process_document(file_path: str) -> List[Document]:
    documents = load_pdf(file_path)
    chunks = split_document(documents)
    return chunks


