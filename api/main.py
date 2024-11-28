from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import openai

from utils.pdf_processor import extract_text_from_pdf, chunk_text
from utils.sql_query_processor import get_ddl_list
from vectorstore.chromadb_manager import ChromaDBManager
from chat.chat_manager import ChatManager
from config import AZURE_API_KEY, AZURE_API_VERSION, AZURE_ENDPOINT, AZURE_DEPLOYMENT_NAME
from config import SQLITE_PATH
from sqlite.sqlite import execute_query

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

    total_records = db_manager.get_total_records()
    if total_records == 0:
        # Extract and process text from BD
        chunks = get_ddl_list()
        # Store in vector database
        db_manager.add_documents(chunks, metadata=[{"source": "DDL Database"}] * len(chunks))
        total_records = db_manager.get_total_records()
        print("total_records in vector DB: ", total_records)

    # Search for relevant documents
    results = db_manager.search_documents(request.query)
    results_list = results['documents'][0] if len(results['documents']) > 0 else list()

    # Generate response using context
    try:
        sql_response = "SELECT Artist.Name FROM Artist JOIN Album ON Artist.ArtistId = Album.ArtistId JOIN Track ON " \
                       "Album.AlbumId = Track.AlbumId WHERE Track.Name = \"Prenda Minha\""
        sql_response = chat_manager.get_sql_response(request.query, results_list)
        debug_response = sql_response
        if str(sql_response) == "False":
            return {"response": "No information", "debug_response": debug_response}


        is_it_sql = chat_manager.check_sql_response(sql_response, list())
        debug_response += "\n It is SQL: " + is_it_sql
        if str(is_it_sql) == "False":
            return {"response": "SQL query was not generated or it was hacked query.", "debug_response": debug_response}


        sql_result_text = execute_query(SQLITE_PATH, sql_response)
        debug_response += "\n" + sql_result_text

        response_text = chat_manager.get_answer(request.query, [sql_result_text])
        debug_response += "\n" + response_text

        return {"response": response_text, "debug_response": debug_response}
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
