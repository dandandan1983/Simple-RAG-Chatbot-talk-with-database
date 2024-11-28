from openai import AzureOpenAI
from typing import List, Dict


class ChatManager:
    def __init__(self, api_key, api_version, azure_endpoint, deployment_name):
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint
        )
        self._deployment_name = deployment_name
        self.conversation_history = []

    def generate_response(self, query: str, context: List[str], content: str, save_context:bool) -> str:
        """Generate response using Azure OpenAI with context."""
        # Prepare conversation history and context
        messages = [
            {"role": "system",
             "content": content},
            *self.conversation_history
        ]

        # Add context and query
        if save_context:
            context_message = "\n".join(context)
            messages.append({"role": "user", "content": f"Context: {context_message}\n\nQuestion: {query}"})
        else:
            messages.append({"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"})


        # Generate response
        response = self.client.chat.completions.create(
            model=self._deployment_name,
            messages=messages,
            temperature=0.1,
            max_tokens=1000
        )
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": query})
        self.conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})

        return response.choices[0].message.content

    def get_sql_response(self, query, results_list):
        text_query = """You are a helpful sqlite assistant. You can work with SQL Queries, generate SQL queries.
                        Answer questions based only on the provided context. All users question is about database.
                        Take a look foreign keys for tables and how do they related.
                        Add Distinct to the query if it doesn't crash query.
                        If you're unsure or the context doesn't contain the information just return False otherwise
                        return just SQL query. No need to send any additional text!
                        Just send SQL query or False !!!"""

        response = self.generate_response(
            query,
            results_list,
            text_query,
            False
        )
        return response

    def check_sql_response(self, query, results_list):
        text_query = """You are a helpful sqlite assistant. You can work with SQL Queries, moderate SQL queries.
                        You can protect SQL queries from hacking. It should be just SELECT .... queries. Nothing else.
                        If you see another type SQL queries which is not SELECT, which can modify, delete, drop etc
                        database just return False. Otherwise return True. No need to send any additional text!
                        Just return True or False."""

        response = self.generate_response(
            query,
            results_list,
            text_query,
            False
        )
        return response

    def get_answer(self, query, results_list):
        text_query = """You are a helpful assistant. Answer questions based only on the provided context. 
        If you're unsure or the context doesn't contain the information, say so."""

        response = self.generate_response(
            query,
            results_list,
            text_query,
            True
        )
        return response
