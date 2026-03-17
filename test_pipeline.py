from rag.document_processor import process_document
from rag.vector_store import create_vector_store, search_documents 
from rag.llm import ask_question 


def test_rag_pipeline():

    # step 1: process the document 
    document_path = r"C:\Users\Xybascem1\Multi Document RAG system\pdfs\sample.pdf"
    chunks = process_document(document_path)

    # step 2: create vector store 
    vector_store =  create_vector_store(chunks)

    # step 3: test with query 
    query = "what is the main topic of the document?"

    # search for relevant chunks 
    results = search_documents(query, vector_store, k=3)

    # Combine chunks into context
    context = "\n\n".join([doc.page_content for doc, score in results])
    
    print(f"Found {len(results)} relevant chunks")

    # step 4: ask the question
    answer = ask_question(query, context)
    print(answer)


    if __name__ == "__main__":
        test_rag_pipeline() 



    