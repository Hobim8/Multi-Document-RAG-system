import requests
import os
import streamlit as st

# FASTAPI backend URL
Backend_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="PDF RAG system", page_icon="📄", layout="wide")

# title and description
st.title("PDF RAG System")
st.markdown("Upload your PDF files and ask questions about them using AI")


# sidebar for file upload and document management
with st.sidebar:
    st.header("Document Management")

    # file uploader
    uploaded_files = st.file_uploader("Upload your PDF files here", type=["pdf"])

    if uploaded_files is not None:
        if st.button("Upload and Process"):
            with st.spinner("Processing PDF..."):
                try:
                    files = {
                        "file": (uploaded_files.name, uploaded_files, "application/pdf")
                    }
                    response = requests.post(f"{Backend_URL}/upload-pdfs", files=files)

                    if response.status_code == 200:
                        data = response.json()
                        st.success(f"Success: {data['message']}")
                        st.info(f"Created {data['chunks_created']} chunks")
                    else:
                        error_detail = response.json().get("detail", "Unknown error")
                        st.error(f"Failed to process: {error_detail}")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to API. Make sure FastAPI is running!")
                    st.info("Run: uvicorn main:app --reload in another terminal")
                # Fixed:
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    st.divider()

    # List documents section
    st.subheader("Uploaded Documents")

    if st.button("Refresh List"):
        st.rerun()

    try:
        response = requests.get(f"{Backend_URL}/documents")
        if response.status_code == 200:
            documents = response.json()

            if documents:
                for doc in documents:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.text(doc["filename"])
                    with col2:
                        if st.button("Delete", key=f"delete_{doc['filename']}"):
                            del_response = requests.delete(
                                f"{Backend_URL}/documents/{doc['filename']}"
                            )
                            if del_response.status_code == 200:
                                st.success(f"Deleted {doc['filename']}")
                                st.rerun()
                            else:
                                st.error("Error deleting document")
            else:
                st.info("No documents uploaded yet")
        else:
            st.warning("Could not fetch documents")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Main area - Query interface
st.header("Ask Questions")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            st.caption(f"Used {message['sources']} source chunks")

# Chat input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{Backend_URL}/query", json={"question": prompt, "top_k": 3}
                )

                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    sources = data["sources_used"]

                    st.markdown(answer)
                    st.caption(f"Used {sources} source chunks")

                    # Add to chat history
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer, "sources": sources}
                    )
                elif response.status_code == 404:
                    error_msg = (
                        "Please upload a PDF document first before asking questions."
                    )
                    st.warning(error_msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg}
                    )
                else:
                    error_msg = response.json().get("detail", "Unknown error")
                    st.error(f"{error_msg}")
                    st.session_state.messages.append(
                        {"role": "assistant", "content": f"Error: {error_msg}"}
                    )
            except requests.exceptions.ConnectionError:
                error_msg = "Cannot connect to API. Make sure FastAPI is running on http://127.0.0.1:8000"
                st.error(error_msg)
                st.info("Run: uvicorn main:app --reload in another terminal")
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )
            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )

# Clear chat button
if st.session_state.messages:
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Footer
st.divider()
st.caption(
    "PDF RAG System - Built with Streamlit + FastAPI + LangChain + Google Gemini"
)
