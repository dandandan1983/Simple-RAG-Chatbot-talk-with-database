import React, { useState, useRef } from 'react';
import { Send, Upload, Loader2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Alert, AlertDescription } from './ui/alert';

const ChatbotUI = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('');
  const [hoveredDebug, setHoveredDebug] = useState(null);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setUploadStatus('Please upload a PDF file');
      return;
    }

    setIsLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        setUploadStatus(`Successfully processed ${data.chunks} chunks from ${file.name}`);
      } else {
        setUploadStatus(`Error: ${data.detail}`);
      }
    } catch (error) {
      setUploadStatus('Error uploading file');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    const newMessage = { role: 'user', content: inputText };
    setMessages(prev => [...prev, newMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: inputText }),
      });

      const data = await response.json();
      if (response.ok) {
        setMessages(prev => [...prev, { role: 'assistant', content: data.response, debug_response: data.debug_response || 'No debug info available' }]);
      } else {
        setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error.' }]);
      }
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error.' }]);
    } finally {
      setIsLoading(false);
      scrollToBottom();
    }
  };

  const handleDelete = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/clear_db', {
        method: 'POST', // Используйте POST, если удаление требует тела запроса
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: 'delete' }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json(); // Предполагаем, что сервер возвращает JSON
      console.log('Response:', result);
      setUploadStatus('Database cleared successfully!');
    } catch (error) {
      console.error('Error clearing database:', error);
      setUploadStatus(`Error: 'Files were not cleared!'`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto p-4">
      <Card className="flex-1 flex flex-col">
        <CardHeader>
          <CardTitle className="flex justify-between items-center">
            <span>Database RAG Chatbot</span>
            <button
              onClick={handleDelete}
              className="flex items-center gap-2 px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition-colors"
              disabled={isLoading}
            >
              {isLoading ? 'Processing...' : 'Delete files'}
            </button>

            <button
              onClick={() => fileInputRef.current?.click()}
              className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
              disabled={isLoading}
            >
              <Upload size={16} />
              Upload PDF
            </button>
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileUpload}
              className="hidden"
              accept=".pdf"
            />
          </CardTitle>
        </CardHeader>

        <CardContent className="flex-1 flex flex-col gap-4 overflow-hidden">
          {uploadStatus && (
            <Alert>
              <AlertDescription>{uploadStatus}</AlertDescription>
            </Alert>
          )}

          <div className="flex-1 overflow-y-auto mb-4 space-y-4">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`relative max-w-[80%] rounded-lg p-3 ${
                    message.role === 'user'
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-100 text-gray-900'
                  }`}
                  style={{ whiteSpace: 'pre-wrap' }}
                  onDoubleClick={() => setHoveredDebug(index)}
                  onClick={() => setHoveredDebug(null)}
                >
                  {message.content}
            {hoveredDebug === index && message.debug_response && (
              <div
                className="relative left-full ml-2 p-2 bg-white border border-gray-300 rounded shadow-lg z-[10000]"
                style={{ whiteSpace: 'pre-wrap' }}
                dangerouslySetInnerHTML={{ __html: message.debug_response.replace(/\n/g, '<br>') }}
              />
            )}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleSubmit} className="flex gap-2">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Ask a question..."
              className="flex-1 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={isLoading}
            />
            <button
              type="submit"
              className="p-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors disabled:opacity-50"
              disabled={isLoading || !inputText.trim()}
            >
              {isLoading ? <Loader2 className="animate-spin" /> : <Send />}
            </button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default ChatbotUI;