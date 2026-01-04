# 🤖 Personal AI Advisor Platform

> Intelligent AI-powered advisory system with document processing and conversational interface
[![CI Pipeline](https://github.com/tejas1024/personal-ai-advisor/actions/workflows/ci.yml/badge.svg)](https://github.com/tejas1024/personal-ai-advisor/actions)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11-green?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.46-red?logo=streamlit)](https://streamlit.io/)

## 📖 Overview

Personal AI Advisor is a containerized web application that allows users to create specialized AI advisors for different domains (finance, career, health, etc.). Users can upload documents to train their advisors and interact through an intelligent chat interface.

## ✨ Features

- **👥 Multi-User System**: Secure authentication with user registration and login
- **🤖 Custom AI Advisors**: Create specialized advisors for different domains
- **📄 Document Processing**: Upload and process PDF, DOCX, TXT, CSV, JSON files
- **💬 Intelligent Chat**: Context-aware conversations with document search
- **🔄 Dual AI Modes**: 
  - Document Mode: Extract exact content from uploaded documents
  - AI Mode: ChatGPT-like responses using Groq API (optional)
- **💾 Persistent Storage**: SQLite database for users, advisors, documents, and chat history
- **🎨 Modern UI**: Futuristic, responsive Streamlit interface
- **🐳 Dockerized**: Fully containerized for easy deployment

## 🏗️ Architecture
```
┌─────────────────────────────────────────────────────────┐
│                     User Interface                       │
│                   (Streamlit Frontend)                   │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Backend Services                        │
│  • UserManager      • DocumentProcessor                 │
│  • DocManager       • IntelligentAI                     │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                 SQLite Database                          │
│  • users    • advisors    • documents    • chat_history │
└──────────────────────────────────────────────────────────┘
```

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.11
- **Database**: SQLite
- **Document Processing**: PyPDF2, python-docx, pandas
- **AI Integration**: Groq API (optional)
- **Containerization**: Docker
- **Version Control**: Git & GitHub

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker Desktop
- Git

### Local Development
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/personal-ai-advisor.git
cd personal-ai-advisor

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

Access at: `http://localhost:8501`

### Docker Deployment
```bash
# Build Docker image
docker build -t personal-ai-advisor:latest .

# Run container
docker run -d -p 8501:8501 --name ai-advisor personal-ai-advisor:latest

# Access application
# Open: http://localhost:8501
```

## 📁 Project Structure
```
personal-ai-advisor/
├── documentation/          # Phase-by-phase documentation
│   ├── phase-1/           # Environment setup
│   ├── phase-2/           # Docker configuration
│   └── phase-3/           # GitHub setup
├── .streamlit/
│   └── config.toml        # Streamlit configuration
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── .dockerignore         # Docker exclusions
├── .gitignore            # Git exclusions
├── test_ai.py            # AI setup testing
└── README.md             # This file
```

## 🎯 Key Features Explained

### 1. Multi-Advisor System
Create unlimited AI advisors, each specialized in different areas:
- Finance & Investment
- Career & HR
- Medical & Health
- Legal
- Technology
- And more...

### 2. Document Intelligence
Upload documents to train your advisors:
- **PDF**: Research papers, reports, manuals
- **DOCX**: Articles, documentation
- **TXT**: Notes, transcripts
- **CSV**: Data tables, spreadsheets
- **JSON**: Structured data

### 3. Intelligent Search
Advanced document search with:
- Keyword matching
- Context relevance scoring
- Sentence-level extraction
- Multi-document aggregation

### 4. Dual AI Modes

**Document Mode** (Default - Free):
- Extracts exact content from your documents
- No API required
- Perfect for fact retrieval

**AI Mode** (Optional - Requires Groq API):
- ChatGPT-like intelligent responses
- Synthesizes information
- Answers general questions
- Free API available at [console.groq.com](https://console.groq.com)

## 🔧 Configuration

### Streamlit Settings
Configured in `.streamlit/config.toml`:
- Theme colors
- Upload size limits (200MB)
- Server settings

### API Configuration (Optional)
To enable AI mode:
1. Get free API key from [Groq](https://console.groq.com)
2. Open app → Settings → Enable API mode
3. Enter your API key
4. Test connection

## 📊 Database Schema

### Users Table
- id, username, email, password_hash, full_name, created_at

### Advisors Table
- id, user_id, name, description, subject_area, created_at

### Documents Table
- id, advisor_id, filename, content, file_type, upload_date

### Chat History Table
- id, advisor_id, user_message, ai_response, timestamp

## 🐳 Docker Details

### Image Specifications
- **Base**: python:3.11-slim
- **Size**: ~500MB
- **Port**: 8501
- **Health Check**: Included
- **Startup Time**: ~5 seconds

### Build Optimizations
- Layer caching for faster rebuilds
- No-cache pip install
- Minimal system dependencies
- .dockerignore for smaller context

## 📚 Documentation

Detailed phase-by-phase documentation available in `/documentation`:

- **Phase 1**: Environment Setup & Verification
- **Phase 2**: Docker Configuration
- **Phase 3**: GitHub Repository Setup
- **Phase 4**: CI/CD Pipeline (Coming Soon)
- **Phase 5**: Cloud Deployment (Coming Soon)

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Your Name**
- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/your-profile)

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - Amazing Python web framework
- [Groq](https://groq.com/) - Fast AI inference API
- [Docker](https://docker.com/) - Containerization platform

## 📞 Support

For issues or questions:
- Open an [Issue](https://github.com/YOUR_USERNAME/personal-ai-advisor/issues)
- Check [Documentation](./documentation/)

---

**⭐ If you find this project useful, please give it a star!**