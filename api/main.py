from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import openai

from utils.pdf_processor import extract_text_from_pdf, chunk_text
from vectorstore.chromadb_manager import ChromaDBManager
from chat.chat_manager import ChatManager
from config import AZURE_API_KEY, AZURE_API_VERSION, AZURE_ENDPOINT, AZURE_DEPLOYMENT_NAME

app = FastAPI()
db_manager = ChromaDBManager()
chat_manager = ChatManager(AZURE_API_KEY,
                            AZURE_API_VERSION,
                            AZURE_ENDPOINT,
                            AZURE_DEPLOYMENT_NAME
                           )

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and process a PDF file."""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Extract and process text
        text = extract_text_from_pdf(file.file)
        chunks = chunk_text(text)
        
        # Store in vector database
        db_manager.add_documents(chunks, metadata=[{"source": file.filename}] * len(chunks))
        
        return {"message": "File processed successfully", "chunks": len(chunks)}
    except openai.APITimeoutError:
        return {"response": "No connection. Timeout. Turn on VPN!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_documents(request: QueryRequest):
    """Query the chatbot."""

    # Search for relevant documents
    results = db_manager.search_documents(request.query)
    # print(results)
    results_list = results['documents'][0] if len(results['documents']) > 0 else list()
    # Generate response using context
    try:
        response = chat_manager.generate_response(
            request.query,
            results_list
        )
        return {"response": response}
    except openai.APITimeoutError:
        return {"response": "No connection. Timeout. Turn on VPN!"}
    except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear_db")
async def clear_database():
    """Query the chatbot."""
    try:
        db_manager.clear_db()
        return {"response": "Files were deleted"}
    except openai.APITimeoutError:
        return {"response": "No connection. Timeout. Turn on VPN!"}
    except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)