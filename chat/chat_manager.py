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

    def generate_response(self, query: str, context: List[str]) -> str:
        """Generate response using Azure OpenAI with context."""
        # Prepare conversation history and context
        messages = [
            {"role": "system",
             "content": "You are a helpful assistant. Answer questions based only on the provided context. If you're unsure or the context doesn't contain the information, say so."},
            *self.conversation_history
        ]
        
        # Add context and query
        context_message = "\n".join(context)
        messages.append({"role": "user", "content": f"Context: {context_message}\n\nQuestion: {query}"})

        # Generate response
        response = self.client.chat.completions.create(
            model=self._deployment_name,
            messages=messages,
            temperature=0.1,
            max_tokens=80
        )
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": query})
        self.conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})
        
        return response.choices[0].message.content