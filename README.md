# RAG Chatbot with Azure OpenAI

A Retrieval Augmented Generation (RAG) chatbot that can understand and answer questions about uploaded PDF documents. Built with Azure OpenAI, FastAPI, and React.

## 🌟 Features

### PDF Processing Engine
- Intelligent text extraction from PDF documents
- Advanced text chunking with customizable overlap
- Optimized document processing using LangChain's RecursiveCharacterTextSplitter

### Vector Storage System
- Efficient document storage using ChromaDB
- Full metadata support for enhanced document tracking
- Fast similarity search for accurate information retrieval

### Advanced Chat Management
- Persistent conversation history
- Context-aware response generation
- Hallucination prevention system
- Powered by Azure OpenAI API

### Modern Architecture
- RESTful API endpoints using FastAPI
- Full CORS support for cross-origin requests
- React-based frontend with real-time updates
- Responsive UI with modern design principles

## 🛠️ Technical Stack

- **Backend**: FastAPI, Python 3.8+
- **Frontend**: React, Tailwind CSS
- **Vector Database**: ChromaDB
- **LLM**: Azure OpenAI
- **PDF Processing**: PyPDF2
- **Text Processing**: LangChain

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- Azure OpenAI API access
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone https://github.com/dandandan1983/rag-chatbot.git
cd rag-chatbot
```

2. Install backend dependencies:
```bash
pip install -r requirements.txt
```

3. Install frontend dependencies (see manual in frontend folder)


4. Create and set values in the `.env` file in the root directory:

AZURE OPEN AI Parameters
```env
AZURE_API_KEY=your_api_key
AZURE_ENDPOINT=your_endpoint
AZURE_DEPLOYMENT_NAME=your_deployment_name
AZURE_API_VERSION=YYYY-mm-dd
```
Chroma DB Parameters
```env
CHROMADB_DIR=./chroma_db
CHROMADB_COLLECTION_NAME=pdf_chunks_collection
```
You can see example in demo_.env file.

### Running the Application

1. Start the backend server:
```bash
python api/main.py
```

The application will be available at `http://localhost:8000`


2. Start the frontend development server:
```bash
cd frontend
npm start
```

The application will be available at `http://127.0.0.1:3000`

## 🔍 How It Works

0. ** You can talk directly with Open AI by API

1. **Document Upload**:
   - Upload PDF documents through the UI
   - Documents are processed and chunked automatically
   - Text chunks are vectorized and stored in ChromaDB

2. **Query Processing**:
   - User questions are vectorized
   - Relevant context is retrieved from the vector store. By default 3 top results return.
   - Azure OpenAI generates accurate, context-aware responses

3. **Hallucination Prevention**:
   - Explicit context inclusion in prompts
   - Strict context-based response generation
   - Conversation history tracking for consistency

## 📝 API Endpoints

- `POST /upload`: Upload and process PDF files
- `POST /query`: Submit questions and receive answers
- `POST /clear_db`: Clear DB (collection will be recreated)

## ✨ Acknowledgments

- Azure OpenAI for the language model
- LangChain for text processing utilities
- ChromaDB for vector storage
- FastAPI for the backend framework
- React for the frontend framework