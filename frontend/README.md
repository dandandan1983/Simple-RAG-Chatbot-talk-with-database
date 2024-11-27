# RAG Chatbot Frontend

A modern, responsive React-based user interface for the RAG Chatbot system. This frontend provides an intuitive interface for document uploads and conversational interactions.

## ✨ Features

### File Upload Interface
- PDF upload functionality by button  
- Real-time upload status notifications  
- File type validation
- Visual feedback during processing  
- Support for multiple file formats in a future  

### Chat Interface
- Real-time message display  
- Distinct user and assistant message bubbles  
- Automatic scroll to latest messages  
- Loading states and typing indicators

## 🛠️ Technical Stack
- **Framework**: React 18+  
- **UI Components**:
- **Icons**:
- **Styling**: Tailwind CSS  
- **State Management**: React Hooks  

## 📦 Dependencies

```json
{
  "dependencies": {
    "lucide-react": "latest",
    "@radix-ui/react-alert": "latest",
    "@radix-ui/react-card": "latest",
    "tailwindcss": "latest"
  }
}
```
---

## 🏗️ Getting Started

### Prerequisites
Ensure you have the following installed:
- Node.js (v16 or later)
- npm or yarn

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/dandandan1983/rag-chatbot-frontend.git
   cd rag-chatbot-frontend
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npx shadcn-ui@latest init
   npx shadcn-ui@latest add card
   npx shadcn-ui@latest add alert
   npm install @radix-ui/react-slot class-variance-authority clsx tailwind-merge tailwindcss-animate lucide-react
   npm install -D tailwindcss postcss autoprefixer
   npm install @headlessui/react @heroicons/react
   npx tailwindcss init
   npx shadcn-ui@latest init
   npm install react-dom
   npm install
    ```
3. Start the development server::
   ```bash
   npm start
    ```
4. Build for production:
   ```bash
    npm run build
    ```

