from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from typing import List
from pydantic import BaseModel
import logging
from rag.document_processor import process_document
from rag.llm import ask_question
from rag.vector_store import (
    delete_documents_by_source,
    add_documents_to_store,
    list_sources,
    load_vector_store,
    search_documents,
)

# configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="PDF RAG System API",
    description="Upload PDF files and query them using RAG",
    version="1.0.0",
)


# add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# create uploads directory if it's doesn't exist
UPLOAD_DIR = "pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# pydantic models for requests/responses
class QueryRequest(BaseModel):
    question: str
    top_k: int = 3


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources_used: int


class UploadResponse(BaseModel):
    status: str
    filename: str
    chunks_created: int
    message: str


class DeleteResponse(BaseModel):
    status: str
    filename: str
    chunks_deleted: int
    message: str


class DocumentInfo(BaseModel):
    filename: str


@app.get("/")
async def root():
    """Root endpoints - API info"""
    return {
        "message": "Multi-document RAG API",
        "version": 1.0,
        "endpoints": {
            "POST /upload-pdfs": "Upload a pdf document",
            "POST /query": "Ask a question",
            "GET /documents": "List of uploaded documents",
            "DELETE /documents/{filename}": "Delete a document",
            "GET /health": "Check API health",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "API is running"}


@app.post("/upload-pdfs", response_model=UploadResponse)
async def upload_pdfs(file: UploadFile = File(...)):
    """
    Upload and process a PDF document

    - Saves the PDF file
    - Extracts and chunks text
    - Creates embeddings
    - Stores in vector database
    """
    try:
        # validate file type
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        # save uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"Saved PDF: {file.filename}")

        # Process the PDF
        chunks = process_document(file_path)

        # Add to vector store with metadata
        add_documents_to_store(chunks, file.filename)

        logger.info(f"Processed {file.filename}: {len(chunks)} chunks created")

        return UploadResponse(
            status="success",
            filename=file.filename,
            chunks_created=len(chunks),
            message=f"Successfully processed {file.filename}",
        )

    except Exception as e:
        logger.error(f"Error uploading PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@app.post("/query", response_model=QueryResponse)
async def query_document(query: QueryRequest):
    """
    Ask a question about the uploaded document

    - Searches vector database for relevant chunks
    - Generates answers using LLM
    - Returns answer with source information

    """
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        if not os.path.exists("chroma_db"):
            raise HTTPException(
                status_code=404,
                detail="No document upload yet. Please upload a PDF first",
            )

        # load vector store and search
        vector_store = load_vector_store
        results = search_documents(request.question, vector_store, k=request.top_k)

        if not results:
            raise HTTPException(
                status_code=404, detail="No relevant information found in document"
            )

        # combine chunk with context
        context = "\n\n".join([doc.page_content for doc in results])

        # get answer from LLM
        answer = ask_question(request.question, context)

        logger.info(f"Answered query: {request.question[:50]}...")

        return QueryResponse(
            question=request.question, answer=answer, sources_used=len(results)
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error querying documents: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error querying documents: {str(e)}"
        )

@app.get("/documents", response_model=List[DocumentInfo])
async def list_documents():
    """
    List all uploaded PDF documents

    """

    try:
        sources = list_sources()
        return [DocumentInfo(filename=source) for source in sources]

    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error listing documents: {str(e)}"
            )

@app.delete("/documents/{filename}", response_model=DeleteResponse)
async def delete_document(filename: str):
    """
    Delete a PDF document and its embeddings

    - Removes PDF file from storage
    - Removes embeddings from vector database

    """

    try:
        file_path = os.path.join(UPLOAD_DIR, filename)

        # delete from vector store
        chunks_deleted = delete_documents_by_source(filename)

        # delete physical file
        if os.path.exists(file_path):
            os.remove(file_path)
        logger, info(f"Deleted file: {filename}")

        if chunks_deleted == 0 and not os.path.exists(file_path):
            raise HTTPException(
                status_code=404, detail=f"Document '{filename}' not found"
                )

        return DeleteResponse(
            status="success",
            filename=filename,
            chunks_deleted=chunks_deleted,
            message=f"Successfully deleted {filename}",
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error deleting document: {str(e)}"
            )
