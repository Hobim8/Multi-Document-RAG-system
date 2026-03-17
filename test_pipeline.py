from rag.document_processor import process_document
from rag.vector_store import create_vector_store, search_documents 
from rag.llm import ask_question 


def test_rag_pipeline():
    
    print("=== STARTING RAG PIPELINE TEST ===\n")
    
    # step 1: process the document 
    print("Step 1: Processing PDF...")
    document_path = "pdfs/sample.pdf"
    chunks = process_document(document_path)
    print(f"Created {len(chunks)} chunks\n")
    
    # step 2: create vector store 
    print("Step 2: Creating vector store (this may take 1-2 min first time)...")
    vector_store = create_vector_store(chunks)
    print("Vector store created!\n")
    
    # step 3: test with query 
    print("Step 3: Searching for relevant chunks...")
    query = "What is the capital of Nigeria?"
    
    # search for relevant chunks 
    results = search_documents(query, vector_store, k=3)
    
    # Combine chunks into context
    context = "\n\n".join([doc.page_content for doc in results])
    
    print(f"Found {len(results)} relevant chunks\n")
    print(f"Context preview: {context[:200]}...\n")  

    # step 4: ask the question
    print("Step 4: Getting answer from LLM...")
    print(f"Question: {query}")
    answer = ask_question(query, context)
    print(f"\nAnswer:\n{answer}\n")
    
    print("=== TEST COMPLETE ===")


if __name__ == "__main__":
    test_rag_pipeline() 

