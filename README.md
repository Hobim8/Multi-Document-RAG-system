# PDF RAG System

A production-ready Retrieval-Augmented Generation (RAG) system for querying PDF documents using AI. Built with FastAPI, Streamlit, LangChain, and Google Gemini.

## Features

- **PDF Document Upload & Processing**: Upload and process PDF documents with automatic text extraction and chunking
- **Semantic Search**: Uses HuggingFace embeddings and ChromaDB for efficient vector similarity search
- **Intelligent Question Answering**: Leverages Google Gemini LLM for natural language responses
- **Source Attribution**: Clearly indicates whether answers come from uploaded documents or general knowledge
- **Conversation Memory**: Maintains context across multiple queries for natural dialogue
- **Document Management**: Upload, view, and delete documents through an intuitive interface
- **RESTful API**: FastAPI backend with automatic interactive documentation
- **Modern UI**: Clean Streamlit interface with real-time chat functionality

## Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- LangChain - LLM orchestration framework
- Google Gemini (gemini-2.5-flash) - Large language model
- ChromaDB - Vector database for embeddings
- HuggingFace Transformers - Local embeddings (all-MiniLM-L6-v2)

**Frontend:**
- Streamlit - Interactive web application framework

**Infrastructure:**
- UV - Fast Python package manager
- Python 3.13

## Architecture

The system follows a stateless API design pattern:
```
User Interface (Streamlit)
    ↓
REST API (FastAPI)
    ↓
RAG Pipeline (LangChain)
    ↓
├── Document Processing (PyPDF)
├── Vector Storage (ChromaDB)
├── Embeddings (HuggingFace)
└── LLM (Google Gemini)
```

## Project Structure
```
pdf-rag-system/
├── main.py                 # FastAPI application
├── app.py                  # Streamlit frontend
├── rag/
│   ├── llm.py             # LLM configuration and prompting
│   ├── prompts.py         # System prompts
│   ├── document_processor.py  # PDF loading and chunking
│   └── vector_store.py    # ChromaDB operations
├── pdfs/                   # Uploaded PDF storage
├── chromaDB/              # Vector database (gitignored)
└── pyproject.toml         # Dependencies
```

## Installation

### Prerequisites

- Python 3.13+
- UV package manager
- Google Gemini API key

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/pdf-rag-system.git
cd pdf-rag-system
```

2. **Install UV:**
```bash
# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. **Install dependencies:**
```bash
uv add fastapi "uvicorn[standard]" python-multipart streamlit \
    langchain langchain-community langchain-google-genai \
    langchain-text-splitters langchain-huggingface \
    chromadb sentence-transformers python-dotenv
```

4. **Set up environment variables:**

Create a `.env` file:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

## Usage

### Running the Application

You need two terminals:

**Terminal 1 - Start the backend:**
```bash
uvicorn main:app --reload
```

**Terminal 2 - Start the frontend:**
```bash
streamlit run app.py
```

The application will be available at:
- Frontend: http://localhost:8501
- API Documentation: http://localhost:8000/docs

### Using the System

1. **Upload Documents**: Use the sidebar to upload PDF files
2. **Ask Questions**: Type questions in the chat interface
3. **View Sources**: Each answer shows how many source chunks were used
4. **Manage Documents**: View and delete uploaded documents from the sidebar

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/upload-pdfs` | Upload and process PDF |
| POST | `/query` | Ask questions about documents |
| GET | `/documents` | List uploaded documents |
| DELETE | `/documents/{filename}` | Delete a document |

Full API documentation available at `/docs` when running.

## Key Design Decisions

**Stateless API Design**: Chat history is managed client-side and sent with each request, enabling horizontal scaling and multi-user support.

**Local Embeddings**: Uses HuggingFace's sentence-transformers for embeddings, eliminating external API dependencies and costs for this component.

**Modular Architecture**: Separation of concerns with distinct modules for document processing, vector storage, and LLM interaction.

**Source Transparency**: Clear distinction between document-based answers and general knowledge responses to maintain trust and accuracy.

## Development

### Running Tests
```bash
# Test the RAG pipeline
uv run python test_pipeline.py
```

### Code Structure

- `main.py`: FastAPI routes, request/response models, error handling
- `rag/llm.py`: LLM configuration and conversation management
- `rag/prompts.py`: System prompts and prompt templates
- `rag/document_processor.py`: PDF loading and text chunking
- `rag/vector_store.py`: Vector database operations and metadata management

## Future Enhancements

- [ ] Support for additional file formats (Word, TXT, Markdown)
- [ ] Multi-language support
- [ ] Advanced chunking strategies
- [ ] Query analytics and logging
- [ ] User authentication
- [ ] Deployment configuration (Docker, cloud platforms)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Built with [LangChain](https://www.langchain.com/)
- Powered by [Google Gemini](https://ai.google.dev/)
- Embeddings from [HuggingFace](https://huggingface.co/)
- Vector storage by [ChromaDB](https://www.trychroma.com/)

---

**Built by [Victor Komolafe]** | [Portfolio](https://yourportfolio.com) | [LinkedIn](https://linkedin.com/in/VictorKomolafe)
```
