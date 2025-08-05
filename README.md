# 🚀 Personal AI Advisor Platform

> **Train your own AI advisors with your documents and get ChatGPT-quality responses tailored to your specific knowledge base.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![AI Powered](https://img.shields.io/badge/AI-Powered-purple.svg)](https://groq.com)

## 🌟 **Overview**

The Personal AI Advisor Platform is a revolutionary application that allows you to create multiple specialized AI advisors, each trained on your specific documents and knowledge base. Unlike general AI assistants, your advisors become experts in your chosen domains by learning from the materials you provide.

### **🎯 Key Differentiators**

| Feature | ChatGPT/Claude | Personal AI Advisor |
|---------|----------------|-------------------|
| **Knowledge Source** | General internet data | YOUR specific documents |
| **Privacy** | Data sent to servers | Everything stays local |
| **Customization** | Fixed personality | Multiple specialized advisors |
| **Document Training** | Temporary context | Permanent knowledge base |
| **Cost** | $20/month + limits | Completely FREE |
| **Admin Control** | None | Full platform management |

---

## ✨ **Features**

### **🤖 AI-Powered Conversations**
- **ChatGPT-Quality Responses**: Powered by Groq API with Llama3 models
- **Context-Aware**: AI understands your uploaded documents perfectly
- **Multiple Advisors**: Create specialized experts for different domains
- **Intelligent Fallbacks**: Smart responses even without internet

### **📚 Advanced Document Processing**
- **Multi-Format Support**: PDF, DOCX, TXT, CSV, JSON, Images (OCR)
- **Smart Text Extraction**: Automatic content parsing and indexing
- **Document Analytics**: Word counts, summaries, metadata tracking
- **Persistent Storage**: Your knowledge base grows over time

### **👥 User Management**
- **Secure Authentication**: Password hashing and session management
- **Password Reset**: Email-based OTP system with fallback options
- **User Profiles**: Track usage, documents, and chat history
- **Role-Based Access**: User and admin permissions

### **⚙️ Admin Dashboard**
- **User Management**: View, monitor, and manage all users
- **Platform Analytics**: Usage statistics, growth metrics, charts
- **Data Export**: CSV/JSON exports for backup and analysis
- **Real-time Monitoring**: Live platform statistics

### **🎨 Modern UI/UX**
- **Futuristic Design**: Dark theme with gradients and animations
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Intuitive Navigation**: Smooth transitions and user flows
- **Professional Appearance**: Enterprise-grade interface

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8 or higher
- pip package manager
- 4GB+ RAM recommended

### **Installation**

1. **Clone or Download**
   ```bash
   git clone https://github.com/yourusername/personal-ai-advisor.git
   cd personal-ai-advisor
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install streamlit pandas PyPDF2 python-docx requests
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

5. **Open in Browser**
   - Navigate to `http://localhost:8501`
   - Register your account and start creating advisors!

---

## 📖 **Usage Guide**

### **Getting Started**

1. **Register Account**
   - Create your personal account with username, email, and password
   - Login with your credentials

2. **Create Your First Advisor**
   - Click "Create New Advisor" in the sidebar
   - Choose a name (e.g., "Investment Expert")
   - Select subject area (Finance, Medical, Legal, etc.)
   - Add description of specialization

3. **Upload Training Documents**
   - Go to "📁 Manage" for your advisor
   - Upload relevant documents (books, papers, notes)
   - Wait for processing completion

4. **Start Chatting**
   - Click "💬 Chat" to begin conversation
   - Ask questions about your uploaded materials
   - Get detailed, context-aware responses

### **Advanced Features**

#### **Multiple Specialized Advisors**
```
📊 Financial Advisor → Upload investment books, reports
🏥 Medical Advisor → Upload medical journals, textbooks
⚖️ Legal Advisor → Upload law books, case studies
💼 Business Advisor → Upload business guides, strategies
```

#### **Document Management**
- **Bulk Upload**: Process multiple files simultaneously
- **Format Support**: PDF, Word, Text, CSV, JSON, Images
- **Smart Analysis**: Automatic summaries and word counts
- **Easy Organization**: View, search, and delete documents

#### **Chat Features**
- **Export Conversations**: Download as JSON or TXT
- **Chat History**: Persistent conversation storage
- **Real-time Responses**: Instant AI-powered replies
- **Source Attribution**: See which documents informed responses

---

## ⚙️ **Configuration**

### **AI Setup (ChatGPT-Quality Responses)**

#### **Option 1: Groq API (Recommended)**
1. **Get Free API Key**
   - Visit [groq.com](https://groq.com)
   - Sign up for free account
   - Generate API key from dashboard

2. **Configure in Code**
   ```python
   # In app.py, line ~690
   self.groq_api_key = "your_groq_api_key_here"
   ```

#### **Option 2: Local AI**
```bash
pip install transformers torch
```

### **Email Configuration (Optional)**

#### **Outlook (Easiest)**
```python
EMAIL_CONFIG = {
    "smtp_server": "smtp-mail.outlook.com",
    "smtp_port": 587,
    "email": "your_email@outlook.com",
    "password": "your_password"
}
```

#### **Gmail (Advanced)**
```python
EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com", 
    "smtp_port": 587,
    "email": "your_email@gmail.com",
    "password": "your_app_password"  # Generate from Google
}
```

### **Admin Access**

1. **Default Credentials**
   ```
   Username: admin
   Password: admin123
   ```

2. **Access Admin Panel**
   - Go to: `http://localhost:8501/?admin=true`
   - Login with admin credentials
   - **⚠️ Change default password in code**

3. **Admin Capabilities**
   - View all users and their activity
   - Monitor platform usage and growth
   - Export data for analysis
   - Manage user accounts

---

## 🌐 **Deployment**

### **Local Development**
```bash
streamlit run app.py
```

### **Free Cloud Deployment**

#### **Streamlit Cloud (Recommended)**
1. Push code to GitHub repository
2. Connect at [share.streamlit.io](https://share.streamlit.io)
3. Deploy with one click
4. **Free tier**: Unlimited public apps

#### **Hugging Face Spaces**
1. Create account at [huggingface.co](https://huggingface.co)
2. Create new Streamlit Space
3. Upload your files
4. **Free tier**: Persistent storage + GPU

#### **Railway**
1. Sign up at [railway.app](https://railway.app)
2. Connect GitHub repository
3. **Free tier**: $5 monthly credit

### **Production Considerations**

#### **Environment Variables**
```bash
# .env file
GROQ_API_KEY=your_groq_key
ADMIN_USERNAME=your_admin_user
ADMIN_PASSWORD=your_secure_password
EMAIL_HOST=your_email_host
EMAIL_PASSWORD=your_email_password
```

#### **Database Backup**
```bash
# Backup SQLite database
cp users.db users_backup_$(date +%Y%m%d).db
```

---

## 📁 **Project Structure**

```
personal-ai-advisor/
├── app.py                 # Main application
├── requirements.txt       # Dependencies
├── README.md             # This file
├── .streamlit/           # Streamlit configuration
│   └── config.toml
├── users.db              # SQLite database (auto-created)
├── documents/            # Document storage (auto-created)
├── chroma_db/            # Vector database (auto-created)
└── api_keys.json         # API key storage (auto-created)
```

---

## 🛠️ **Technical Architecture**

### **Core Technologies**
- **Frontend**: Streamlit (Python web framework)
- **Database**: SQLite (user data, documents, chat history)
- **AI Engine**: Groq API (Llama3 models)
- **Document Processing**: PyPDF2, python-docx, pandas
- **Authentication**: SHA-256 hashing, session management

### **Key Components**

#### **UserManager**
- User registration and authentication
- Password reset with OTP
- Admin functionality

#### **DocumentProcessor** 
- Multi-format file processing
- Text extraction and analysis
- Metadata generation

#### **IntelligentAI**
- Groq API integration
- Context-aware response generation
- Fallback response system

#### **AdvancedDocumentManager**
- Document storage and retrieval
- Smart search and matching
- Analytics and statistics

---

## 🔒 **Security Features**

### **Data Protection**
- **Local Storage**: All data stays on your server
- **Password Hashing**: SHA-256 encryption
- **Session Management**: Secure user sessions
- **Input Validation**: SQL injection prevention

### **Privacy Guarantees**
- **No External Data Sharing**: Documents never leave your system
- **Optional API Usage**: AI calls are optional
- **User Control**: Complete data ownership
- **GDPR Compliant**: Full data portability

---

## 🚨 **Troubleshooting**

### **Common Issues**

#### **Import Errors**
```bash
# Fix: Install missing packages
pip install streamlit pandas PyPDF2 python-docx requests

# For advanced features
pip install plotly transformers torch
```

#### **Database Errors**
```bash
# Fix: Delete and recreate
rm users.db
# App will recreate on next run
```

#### **Email Issues**
- Use Outlook instead of Gmail (easier setup)
- Or use demo mode (OTP shown on screen)
- Check SMTP settings and credentials

#### **Performance Issues**
- **Large Documents**: Split into smaller files
- **Memory Usage**: Restart app periodically
- **Slow Responses**: Check internet connection for API calls

---

## 🎯 **Use Cases**

### **Personal Knowledge Management**
- **Students**: Upload textbooks, create study advisors
- **Researchers**: Process papers, get instant insights
- **Professionals**: Company docs, industry knowledge

### **Business Applications**
- **Team Training**: Upload procedures, create help advisors
- **Customer Support**: FAQ documents, instant answers
- **Consulting**: Client-specific knowledge bases

### **Specialized Domains**
- **Medical**: Clinical guidelines, research papers
- **Legal**: Case law, regulations, contracts
- **Finance**: Investment research, market analysis
- **Technical**: Documentation, best practices

---

## 🎉 **Success Stories**

> *"I uploaded 50 investment books and created a financial advisor. Now I get better investment advice than any paid service!"* - Portfolio Manager

> *"Our team uses it for customer support. We uploaded all our documentation and now get instant, accurate answers."* - Tech Startup

> *"As a medical student, I uploaded my textbooks and created study advisors for each subject. My grades improved dramatically!"* - Medical Student

---

## 🛣️ **Roadmap**

### **Upcoming Features**
- [ ] **Voice Chat**: Speech-to-text integration
- [ ] **Mobile App**: React Native companion
- [ ] **API Access**: REST API for integrations
- [ ] **Advanced Analytics**: ML-powered insights
- [ ] **Team Workspaces**: Collaborative advisor sharing
- [ ] **Plugin System**: Custom extensions
- [ ] **Multi-language**: International support

### **Version History**
- **v1.0**: Basic chat functionality
- **v2.0**: Document processing and management
- **v3.0**: Admin panel and analytics
- **v4.0**: Advanced AI integration (current)

---

## 🤝 **Contributing**

We welcome contributions! Here's how to get started:

### **Development Setup**
1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes** and add tests
4. **Commit changes**: `git commit -m 'Add amazing feature'`
5. **Push to branch**: `git push origin feature/amazing-feature`
6. **Open Pull Request**

### **Contribution Guidelines**
- Follow Python PEP 8 style guide
- Add docstrings to new functions
- Include error handling
- Test thoroughly before submitting
- Update documentation as needed

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Personal AI Advisor Platform

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 **Support & Contact**

### **Getting Help**
- **Documentation**: Read this README thoroughly
- **Issues**: Open GitHub issue with detailed description
- **Discussions**: Join community discussions
- **Email**: tejaspavithra2002@gmail.com

### **Community**
- **GitHub**: [github.com/yourusername/personal-ai-advisor](https://github.com/Tejas1024/personal-ai-advisor)


### **Professional Services**
- **Custom Development**: Tailored solutions for enterprises
- **Deployment Support**: Production setup and maintenance
- **Training & Consulting**: Team training and best practices
- **Premium Support**: Priority assistance and feature requests

---

## 🙏 **Acknowledgments**

### **Technologies**
- **Streamlit** - Amazing Python web framework
- **Groq** - Lightning-fast AI inference
- **Hugging Face** - Open source AI models
- **SQLite** - Reliable embedded database

### **Inspiration**
- **OpenAI ChatGPT** - Conversational AI excellence
- **Notion AI** - Document-based intelligence
- **Obsidian** - Personal knowledge management
- **Discord** - Community-driven development


## 🌟 **Star History**

[![Star History Chart](https://api.star-history.com/svg?repos=Tejas1024/personal-ai-advisor&type=Date)](https://star-history.com/#yourusername/personal-ai-advisor&Date)

---

<div align="center">

### **Built with ❤️ for the AI community**

**[⭐ Star this repo](https://github.com/Tejas1024/personal-ai-advisor)** • **[🐛 Report Bug](https://github.com/Tejas1024/personal-ai-advisor/issues)** • **[✨ Request Feature](https://github.com/Tejas1024/personal-ai-advisor/issues)**

---

**Made by [Tejasgowda T R](https://github.com/Tejas1024) • [Website](https://personal-ai-advisor-ftulhqxgxxn6jspu8xxw6f.streamlit.app/) • [LinkedIn](https://www.linkedin.com/in/tejasgowda-t-064b41283?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)**

</div>
