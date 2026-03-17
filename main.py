from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware  
import os 
import shutil
from typing import List
from pydantic import BaseModel 
 

app = FastAPI(
    title = "Multi-Document RAG System",
    description= "Upload PDF files and query them using RAG",
    version= "1.0.0"
)









def main():
    print("Hello from multi-document-rag-system!")


if __name__ == "__main__":
    main()
