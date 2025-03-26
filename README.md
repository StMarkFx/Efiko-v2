# Efiko AI Chatbot - MVP (Version 2)

Efiko AI Chatbot is an intelligent AI-powered chatbot that leverages Retrieval-Augmented Generation (RAG) to provide accurate responses based on uploaded documents and real-time interactions. This Minimum Viable Product (MVP) is built using **FastAPI (Backend) and Next.js (Frontend)**, with **FAISS/ElasticSearch** for vector search.

## 🚀 Features
- 🔐 **User Authentication** (Firebase Auth)
- 💬 **AI Chatbot with Gemini API**
- 📄 **RAG-Based Document Querying**
- 🧠 **Vector Search for Efficient Retrieval**
- 🎨 **Modern UI with Next.js and Tailwind CSS**
- ☁️ **Dockerized Deployment with Vercel & Railway**

---

## 📂 Project Structure

```
Efiko-AI-Chatbot/
│── backend/                  # FastAPI Backend
│   ├── app/                  # Main application folder
│   │   ├── models/           # Pydantic models for requests/responses
│   │   ├── routes/           # API routes (authentication, chat, RAG, etc.)
│   │   ├── services/         # Business logic (auth, chat processing, RAG retrieval)
│   │   ├── database/         # Firebase connection, vector database (FAISS/ElasticSearch)
│   │   ├── utils/            # Helper functions
│   │   ├── main.py           # FastAPI entry point
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile            # Docker configuration
│   ├── .env                  # Environment variables (API keys, DB configs)
│   ├── README.md             # Backend documentation
│
│── frontend/                 # Next.js Frontend
│   ├── src/
│   │   ├── components/       # Reusable UI components (Chatbox, FileUpload, etc.)
│   │   ├── pages/            # Next.js pages (Home, Chat, Dashboard)
│   │   ├── hooks/            # Custom React hooks for API calls, auth handling
│   │   ├── context/          # Context API for global state management
│   │   ├── styles/           # Tailwind CSS styles
│   │   ├── utils/            # Helper functions for frontend
│   │   ├── config/           # API endpoints, constants
│   ├── public/               # Static assets (logos, icons)
│   ├── .env.local            # Frontend environment variables
│   ├── package.json          # Dependencies
│   ├── README.md             # Frontend documentation
│
│── vector_db/                # Vector Search System (FAISS/ElasticSearch)
│   ├── embeddings.py         # Document embeddings
│   ├── retrieval.py          # Search and retrieval functions
│   ├── vector_store/         # Indexed study materials
│
│── tests/                    # Unit & Integration Tests
│
│── deployment/               # Deployment configurations
│   ├── vercel.json           # Vercel config for frontend
│   ├── railway.json          # Railway deployment config
│   ├── docker-compose.yml    # Docker setup for local development
│
│── .gitignore                # Ignore sensitive files
│── README.md                 # Main documentation
│── LICENSE                   # Open-source license (if applicable)
```

---

## 🛠️ Installation & Setup

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-username/Efiko-AI-Chatbot.git
cd Efiko-AI-Chatbot
```

### 2️⃣ Backend Setup
#### Install dependencies
```sh
cd backend
pip install -r requirements.txt
```
#### Start FastAPI Server
```sh
uvicorn app.main:app --reload
```
- Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for API documentation.

### 3️⃣ Frontend Setup
#### Install dependencies
```sh
cd frontend
npm install
```
#### Start Next.js App
```sh
npm run dev
```
- Open [http://localhost:3000](http://localhost:3000) to view the frontend.

---

## 🚀 Deployment
### Docker (Local Development)
```sh
docker-compose up --build
```
### Vercel (Frontend)
```sh
vercel --prod
```
### Railway (Backend)
```sh
git push railway main
```

---

## 📌 API Endpoints
| Method | Endpoint        | Description                 |
|--------|---------------|-----------------------------|
| `POST` | `/auth/register` | User Registration         |
| `POST` | `/auth/login`    | User Login                |
| `POST` | `/chat`         | AI Chat Interaction       |
| `POST` | `/retrieval`    | RAG-Based Document Search |

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 🤝 Contributing
Feel free to contribute to Efiko AI! Fork the repo, create a branch, and submit a PR.

---

## 🎯 Roadmap
- ✅ MVP Development
- 🚀 Enhanced Retrieval System
- 🔐 JWT Authentication & Authorization
- 📈 Dashboard Analytics
- 🌍 Multi-Language Support

---

## 📞 Contact
For questions or collaborations, reach out via email at `your-email@example.com` or open an issue on GitHub!

---

### 🚀 Happy Building! 🔥
