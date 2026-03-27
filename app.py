import requests
import os
import streamlit as st

# FASTAPI backend URL
Backend_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="PDF RAG system", page_icon="📄", layout="wide")

# title and description
st.title("PDF RAG system")
st.markdown("Upload your PDF files and ask questions about them using AI")


# sidebar for file upload and document management
with st.sidebar:
    st.header("Document Management")

# file uploader
uploaded_files = st.file_uploader("upload your PDF files here", type=["pdf"])

if uploaded_files is not None:
    if st.button("Upload and Process"):
        with st.spinner("Processing PDF"):
            try:
                files = {
                    "file": (uploaded_files.name, uploaded_files, "application/pdf")
                }
                response = requests.post(f"{Backend_URL}/upload_pdf", files=files)

                if response.status_code == 200:
                    data = response.json()
                    st.success("document processed successfully")
                else:
                    st.error("Failed to process document")
            except Exception as e:
                st.error(f"An error occurred: {e}")

st.divider()

st.subheader("Uploaded Documents")

if st.button("Refresh Document List"):
    st.rerun()

try:
    response = requests.get(f"{Backend_URL}/list_documents")
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
            st.warning("could not fetch documents")
except Exception as e:
    st.error(f"An error occurred: {e}")

# Query interface
st.header("Ask Questions")

# chat history
if "messages" not in st.session_state:
    st.session_stage.messages = []

# Displaying chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            st.caption(f"Used {message['sources']} source chunks")

# chat input
if prompt := st.chat_input("Ask a queation about your document....."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

# get response from API
with st.chat_message("assistant"):
    with st.spinner("Thinking...."):
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

                # add chat history
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer, "sources": sources}
                )
            else:
                error_msg = response.json()["detail"]
                st.error = f"{error_msg}"
                st.session_state.messages.append(
                    {"role": "assistant", "content": f"Error {error_msg}"}
                )
        except Exception as e:
            error_msg = f"Error connecting to API: {str(e)}"
            st.error(f"{error_msg}")
            st.session_state.messages.append(
                {"role": "assistant", "content": error_msg}
            )

# clear chat button
if st.session_state.messages:
    if st.button("Clear chat history"):
        st.session_state.messages = []
        st.rerun()

# footer
st.divider()
st.caption("Built with Streamlit + FastAPI + LangChain + Google Gemini")
