from sqlite.sqlite import get_ddl_dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import SQLITE_PATH, CHUNK_SIZE, CHUNK_OVERLAP


def get_ddl_list():
    """Extract text from uploaded PDF file."""
    text_list = []
    dict_queries = get_ddl_dict(SQLITE_PATH)
    for table, sql in dict_queries["tables"].items():
        text_list.append(f"Table: {table}. SQL: {sql}")

    for table, sql in dict_queries["views"].items():
        text_list.append(f"View: {table}. SQL: {sql}")
    return text_list


def get_max_chunk_size(text_list):
    max_chunk_size = 0
    for text in text_list:
        cur_size = len(text)
        if cur_size > max_chunk_size:
            max_chunk_size = cur_size


def sql_chunk_text(text_list):
    """Split text into chunks using LangChain's text splitter."""

    max_chunk_size = get_max_chunk_size(text_list)
    for text_i in text_list:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=max_chunk_size if max_chunk_size > 0 else CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len
        )
    chunks = text_list
    return chunks
