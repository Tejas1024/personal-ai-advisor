# Ultimate Personal AI Advisor Platform - Fixed Version
# Improved with settings, better persistence, API toggle, and fixed uploads

import streamlit as st
import hashlib
import os
import json 
import sqlite3
import pandas as pd
import PyPDF2
import docx
from datetime import datetime
from typing import List, Dict, Any
import requests

# Configuration
USER_DB_PATH = "./users.db"
DOCS_DIR = "./documents"
CONFIG_PATH = "./user_config.json"

# Ensure directories exist
os.makedirs(DOCS_DIR, exist_ok=True)

# Configuration Management
def save_user_config(user_id: int, config: dict):
    """Save user configuration persistently"""
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                all_configs = json.load(f)
        else:
            all_configs = {}
        
        all_configs[str(user_id)] = config
        
        with open(CONFIG_PATH, 'w') as f:
            json.dump(all_configs, f)
    except Exception as e:
        st.error(f"Error saving config: {str(e)}")

def load_user_config(user_id: int) -> dict:
    """Load user configuration"""
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                all_configs = json.load(f)
            return all_configs.get(str(user_id), {"api_key": "", "use_api": False})
    except:
        pass
    return {"api_key": "", "use_api": False}

class UserManager:
    def __init__(self):
        self.init_user_db()
    
    def init_user_db(self):
        """Initialize SQLite database for user and advisor management"""
        conn = sqlite3.connect(USER_DB_PATH)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Advisors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS advisors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT NOT NULL,
                description TEXT,
                subject_area TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Documents table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                advisor_id INTEGER,
                filename TEXT NOT NULL,
                content TEXT,
                file_type TEXT,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (advisor_id) REFERENCES advisors (id)
            )
        ''')
        
        # Chat history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                advisor_id INTEGER,
                user_message TEXT,
                ai_response TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (advisor_id) REFERENCES advisors (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def register_user(self, username: str, email: str, password: str, full_name: str) -> Dict[str, Any]:
        """Register a new user"""
        conn = sqlite3.connect(USER_DB_PATH)
        cursor = conn.cursor()
        
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name) 
                VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, full_name))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {"success": True, "user_id": user_id, "message": "Registration successful!"}
        
        except sqlite3.IntegrityError as e:
            conn.close()
            if "username" in str(e):
                return {"success": False, "message": "Username already exists"}
            elif "email" in str(e):
                return {"success": False, "message": "Email already exists"}
            else:
                return {"success": False, "message": "Registration failed"}
    
    def authenticate(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user and return user info"""
        conn = sqlite3.connect(USER_DB_PATH)
        cursor = conn.cursor()
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute('''
            SELECT id, username, email, full_name FROM users 
            WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "authenticated": True,
                "user_id": result[0],
                "username": result[1],
                "email": result[2],
                "full_name": result[3]
            }
        return {"authenticated": False}
    
    def create_advisor(self, user_id: int, name: str, description: str, subject_area: str) -> int:
        """Create a new advisor for a user"""
        conn = sqlite3.connect(USER_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO advisors (user_id, name, description, subject_area) 
            VALUES (?, ?, ?, ?)
        ''', (user_id, name, description, subject_area))
        
        advisor_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return advisor_id
    
    def get_user_advisors(self, user_id: int) -> List[Dict]:
        """Get all advisors for a user"""
        conn = sqlite3.connect(USER_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, description, subject_area, created_at 
            FROM advisors WHERE user_id = ?
        ''', (user_id,))
        
        advisors = []
        for row in cursor.fetchall():
            advisors.append({
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "subject_area": row[3],
                "created_at": row[4]
            })
        
        conn.close()
        return advisors
    
    def delete_advisor(self, advisor_id: int):
        """Delete an advisor and all associated data"""
        conn = sqlite3.connect(USER_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM chat_history WHERE advisor_id = ?', (advisor_id,))
        cursor.execute('DELETE FROM documents WHERE advisor_id = ?', (advisor_id,))
        cursor.execute('DELETE FROM advisors WHERE id = ?', (advisor_id,))
        
        conn.commit()
        conn.close()

class DocumentProcessor:
    @staticmethod
    def extract_text_from_pdf(file) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            return f"Error extracting text from PDF: {str(e)}"
    
    @staticmethod
    def extract_text_from_docx(file) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            return f"Error extracting text from DOCX: {str(e)}"
    
    @staticmethod
    def process_file(file) -> str:
        """Process uploaded file and extract text"""
        filename = file.name.lower()
        
        if filename.endswith('.pdf'):
            return DocumentProcessor.extract_text_from_pdf(file)
        elif filename.endswith('.docx'):
            return DocumentProcessor.extract_text_from_docx(file)
        elif filename.endswith('.txt'):
            return str(file.read(), 'utf-8')
        elif filename.endswith('.csv'):
            df = pd.read_csv(file)
            return df.to_string()
        elif filename.endswith('.json'):
            return str(file.read(), 'utf-8')
        else:
            return str(file.read(), 'utf-8')

class SimpleDocumentManager:
    def __init__(self, advisor_id: int):
        self.advisor_id = advisor_id
    
    def document_exists(self, filename: str) -> bool:
        """Check if document already exists"""
        try:
            conn = sqlite3.connect(USER_DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT COUNT(*) FROM documents 
                WHERE advisor_id = ? AND filename = ?
            ''', (self.advisor_id, filename))
            
            count = cursor.fetchone()[0]
            conn.close()
            return count > 0
        except:
            return False
    
    def add_document(self, content: str, filename: str) -> bool:
        """Add document to database"""
        try:
            # Check if already exists
            if self.document_exists(filename):
                return False
            
            conn = sqlite3.connect(USER_DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO documents (advisor_id, filename, content, file_type, upload_date) 
                VALUES (?, ?, ?, ?, ?)
            ''', (self.advisor_id, filename, content, filename.split('.')[-1], datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            st.error(f"Error saving document: {str(e)}")
            return False
    
    def search_documents(self, query: str) -> str:
        """Enhanced text search in documents"""
        try:
            conn = sqlite3.connect(USER_DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT content, filename FROM documents WHERE advisor_id = ?
            ''', (self.advisor_id,))
            
            documents = cursor.fetchall()
            conn.close()
            
            if not documents:
                return ""
            
            # Enhanced keyword matching
            query_words = set(query.lower().split())
            relevant_content = []
            
            for content, filename in documents:
                if content:
                    # Split into sentences
                    sentences = content.replace('\n', ' ').split('.')
                    for sentence in sentences:
                        if len(sentence.strip()) > 30:
                            sentence_words = set(sentence.lower().split())
                            overlap = len(query_words.intersection(sentence_words))
                            if overlap > 0:
                                relevant_content.append((sentence.strip(), overlap))
            
            # Sort by relevance and return top results
            relevant_content.sort(key=lambda x: x[1], reverse=True)
            return "\n\n".join([content for content, _ in relevant_content[:10]]) if relevant_content else ""
            
        except Exception as e:
            return ""
    
    def get_all_documents(self) -> List[str]:
        """Get list of all uploaded documents"""
        try:
            conn = sqlite3.connect(USER_DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT filename FROM documents WHERE advisor_id = ?
            ''', (self.advisor_id,))
            
            documents = [row[0] for row in cursor.fetchall()]
            conn.close()
            return documents
        except Exception as e:
            return []
    
    def delete_document(self, filename: str) -> bool:
        """Delete a document"""
        try:
            conn = sqlite3.connect(USER_DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM documents WHERE advisor_id = ? AND filename = ?
            ''', (self.advisor_id, filename))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False

class IntelligentAI:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.config = load_user_config(user_id)
        
    def generate_with_groq(self, prompt: str, system_prompt: str = None) -> str:
        """Generate response using Groq API"""
        api_key = self.config.get("api_key", "")
        
        if not api_key or not self.config.get("use_api", False):
            return None
        
        if not system_prompt:
            system_prompt = "You are an expert AI advisor. Provide detailed, insightful, and professional responses. Be conversational, helpful, and thorough in your explanations."
        
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 2000,
                "top_p": 1
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                error_msg = response.json().get("error", {}).get("message", "Unknown error")
                st.error(f"API Error: {error_msg}")
                return None
                
        except requests.exceptions.Timeout:
            st.error("API request timed out. Please try again.")
            return None
        except Exception as e:
            st.error(f"API error: {str(e)}")
            return None
    
    def generate_intelligent_response(self, query: str, context: str, advisor_name: str) -> str:
        """Generate intelligent AI response"""
        
        # Check if API is enabled
        use_api = self.config.get("use_api", False)
        
        if use_api:
            # Use AI to generate intelligent response
            if context.strip():
                # Question with document context - synthesize answer
                system_prompt = f"""You are {advisor_name}, an expert AI advisor. 
You have access to document content that has been uploaded by the user. 
Analyze the context provided and answer the user's question in a clear, professional, and helpful manner.
Provide detailed explanations, insights, and actionable advice based on the information.
If the context doesn't fully answer the question, use your knowledge to provide the best possible answer while noting what information is from the documents."""
                
                user_prompt = f"""Context from uploaded documents:
{context[:4000]}

User's question: {query}

Please provide a comprehensive answer based on the context above. Be specific, detailed, and helpful."""
            else:
                # General question without documents - use AI knowledge
                system_prompt = f"""You are {advisor_name}, an expert AI advisor. 
The user hasn't uploaded relevant documents yet, but you can still help with general questions using your knowledge.
Be helpful, informative, and conversational. If documents would be helpful for more specific advice, mention that politely."""
                
                user_prompt = query
            
            # Try to get AI response
            ai_response = self.generate_with_groq(user_prompt, system_prompt)
            
            if ai_response:
                return ai_response
            else:
                # API failed, fall through to fallback
                pass
        
        # Fallback mode (API disabled or failed)
        if context.strip():
            # Return structured context with note about API
            sentences = [s.strip() + "." for s in context.split('.') if s.strip() and len(s.strip()) > 20]
            
            response = f"**Information from your documents:**\n\n"
            
            # Take top relevant sentences
            for i, sentence in enumerate(sentences[:8], 1):
                response += f"{i}. {sentence}\n\n"
            
            if not use_api:
                response += "\n💡 *Enable API in Settings for AI-powered analysis and ChatGPT-like responses*"
            else:
                response += "\n⚠️ *API temporarily unavailable - showing document content*"
            
            return response
        else:
            # No context available
            if not use_api:
                return f"""I don't have any documents uploaded to answer your question about "{query}".

**To get started:**
1. Upload relevant documents in the Documents section
2. Or enable API in Settings for AI-powered responses even without documents

💡 *With API enabled, I can answer general questions using AI knowledge*"""
            else:
                return "I couldn't find relevant information in your documents, and the API request failed. Please try again or check your API key in Settings."

def apply_futuristic_theme():
    """Apply advanced futuristic theme"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary-bg: #0a0a0f;
        --secondary-bg: #1a1a2e;
        --accent-color: #00d4ff;
        --text-color: #e6e6e6;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%);
        color: var(--text-color);
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    .stDeployButton {display: none;}
    footer {visibility: hidden;}
    
    .main-header {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .main-header h1 {
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

def login_register_page():
    """Display login and registration page"""
    apply_futuristic_theme()
    
    st.markdown("""
    <div class="main-header">
        <h1>🚀 AI Advisor Platform</h1>
        <p>Your Personal AI Advisors with Advanced Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        st.markdown("### Welcome Back!")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                user_manager = UserManager()
                auth_result = user_manager.authenticate(username, password)
                
                if auth_result["authenticated"]:
                    st.session_state.user = auth_result
                    st.success("Welcome back!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
    
    with tab2:
        st.markdown("### Create Your Account")
        
        with st.form("register_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                reg_username = st.text_input("Username*")
                reg_email = st.text_input("Email*")
            
            with col2:
                reg_full_name = st.text_input("Full Name*")
                reg_password = st.text_input("Password*", type="password")
            
            reg_submit = st.form_submit_button("Create Account", use_container_width=True)
            
            if reg_submit:
                if all([reg_username, reg_email, reg_full_name, reg_password]):
                    user_manager = UserManager()
                    result = user_manager.register_user(reg_username, reg_email, reg_password, reg_full_name)
                    
                    if result["success"]:
                        st.success(result["message"])
                    else:
                        st.error(result["message"])
                else:
                    st.error("Please fill in all required fields")

def settings_page():
    """Settings page for API configuration"""
    apply_futuristic_theme()
    
    st.markdown("""
    <div class="main-header">
        <h1>⚙️ Settings</h1>
        <p>Configure your AI advisor</p>
    </div>
    """, unsafe_allow_html=True)
    
    user_id = st.session_state.user["user_id"]
    config = load_user_config(user_id)
    
    st.markdown("### 🤖 AI Response Mode")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **📋 Document Mode (API Off)**
        - Returns exact content from documents
        - No AI generation
        - Free to use
        - Good for exact quotes/data
        """)
    
    with col2:
        st.success("""
        **🚀 AI Mode (API On)**
        - ChatGPT-like responses
        - Intelligent analysis
        - Answers general questions
        - Synthesizes information
        """)
    
    st.markdown("---")
    
    use_api = st.toggle(
        "🔥 Enable AI-Powered Responses", 
        value=config.get("use_api", False),
        help="When enabled, get ChatGPT-like intelligent responses using Groq API"
    )
    
    if use_api:
        st.markdown("### 🔑 API Configuration")
        st.info("💡 **Get your FREE API key:** Visit [console.groq.com](https://console.groq.com) → Create account → API Keys → Create new key")
        
        current_key = config.get("api_key", "")
        key_display = f"{current_key[:10]}..." if current_key else "No key set"
        
        st.text_input("Current Key", value=key_display, disabled=True, help="Your saved API key")
        
        with st.expander("🔄 Update API Key"):
            new_api_key = st.text_input(
                "New Groq API Key", 
                type="password",
                placeholder="gsk_...",
                help="Paste your Groq API key here"
            )
            
            if st.button("💾 Save New Key", use_container_width=True):
                if new_api_key and new_api_key.startswith("gsk_"):
                    new_config = {
                        "api_key": new_api_key,
                        "use_api": True
                    }
                    save_user_config(user_id, new_config)
                    st.success("✅ API key saved successfully!")
                    st.rerun()
                else:
                    st.error("❌ Please enter a valid Groq API key (starts with 'gsk_')")
        
        # Test API button
        if current_key and st.button("🧪 Test API Connection", use_container_width=True):
            with st.spinner("Testing API..."):
                ai = IntelligentAI(user_id)
                test_response = ai.generate_with_groq("Say 'API is working!' in a friendly way.", "You are a helpful assistant.")
                
                if test_response:
                    st.success("✅ API is working perfectly!")
                    st.info(f"Response: {test_response}")
                else:
                    st.error("❌ API test failed. Please check your API key.")
        
        if st.button("💾 Save Settings", use_container_width=True, type="primary"):
            new_config = {
                "api_key": current_key,
                "use_api": True
            }
            save_user_config(user_id, new_config)
            st.success("✅ Settings saved! AI mode is now ENABLED.")
            st.rerun()
    else:
        st.info("ℹ️ API is currently disabled. You'll get exact content from documents without AI processing.")
        
        if st.button("💾 Save Settings", use_container_width=True, type="primary"):
            new_config = {
                "api_key": config.get("api_key", ""),
                "use_api": False
            }
            save_user_config(user_id, new_config)
            st.success("✅ Settings saved! Document mode is active.")
            st.rerun()
    
    st.markdown("---")
    st.markdown("### ℹ️ About Data Persistence")
    
    with st.expander("📖 Important Information"):
        st.warning("""
        **For Streamlit Cloud Users:**
        
        Streamlit Cloud (streamlit.io) uses temporary file storage that resets after periods of inactivity.
        
        **What this means:**
        - User accounts may be lost after a few days of inactivity
        - Documents and chat history may be cleared
        - API settings are usually preserved
        
        **Solutions:**
        1. **For demos/college projects:** This is fine - recreate data as needed
        2. **For production:** Use cloud database (PostgreSQL, MongoDB, Supabase)
        3. **Self-hosting:** Deploy on your own server for permanent storage
        
        **Your API key is stored in a JSON file and usually persists longer than the database.**
        """)
    
    if st.button("← Back to Advisors", use_container_width=True):
        st.session_state.page = "advisors"
        st.rerun()

def advisor_management():
    """Advisor management interface"""
    apply_futuristic_theme()
    
    st.markdown("""
    <div class="main-header">
        <h1>🧠 Your AI Advisors</h1>
        <p>Create and manage your intelligent AI advisors</p>
    </div>
    """, unsafe_allow_html=True)
    
    user_manager = UserManager()
    advisors = user_manager.get_user_advisors(st.session_state.user["user_id"])
    
    # Sidebar for creating new advisor
    with st.sidebar:
        st.markdown("### ➕ Create New Advisor")
        
        with st.form("create_advisor"):
            advisor_name = st.text_input("Advisor Name*", placeholder="e.g., Career Counselor")
            subject_area = st.selectbox(
                "Subject Area*",
                ["Finance & Investment", "Career & HR", "Medical & Health", "Legal", "Technology", 
                 "Education", "Marketing", "Science", "Business", "Other"]
            )
            description = st.text_area("Description", placeholder="What this advisor specializes in...")
            
            if st.form_submit_button("Create Advisor", use_container_width=True):
                if advisor_name and subject_area:
                    advisor_id = user_manager.create_advisor(
                        st.session_state.user["user_id"],
                        advisor_name,
                        description,
                        subject_area
                    )
                    st.success(f"✅ {advisor_name} created!")
                    st.rerun()
                else:
                    st.error("Please fill in required fields")
    
    # Display existing advisors
    if advisors:
        st.markdown("### Your Advisors")
        
        for advisor in advisors:
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.markdown(f"**🤖 {advisor['name']}**")
                    st.caption(f"{advisor['subject_area']} • {advisor['description'] or 'General AI advisor'}")
                
                with col2:
                    if st.button("💬 Chat", key=f"chat_{advisor['id']}"):
                        st.session_state.current_advisor = advisor['id']
                        st.session_state.page = "chat"
                        st.rerun()
                
                with col3:
                    if st.button("📁 Docs", key=f"manage_{advisor['id']}"):
                        st.session_state.current_advisor = advisor['id']
                        st.session_state.page = "manage_documents"
                        st.rerun()
                
                with col4:
                    if st.button("🗑️ Del", key=f"delete_{advisor['id']}"):
                        user_manager.delete_advisor(advisor['id'])
                        st.success(f"Deleted {advisor['name']}")
                        st.rerun()
                
                st.markdown("---")
    else:
        st.info("No advisors yet. Create your first AI advisor using the sidebar!")

def document_management():
    """Document management for specific advisor"""
    apply_futuristic_theme()
    
    advisor_id = st.session_state.current_advisor
    user_manager = UserManager()
    advisors = user_manager.get_user_advisors(st.session_state.user["user_id"])
    current_advisor = next((a for a in advisors if a["id"] == advisor_id), None)
    
    if not current_advisor:
        st.error("Advisor not found!")
        return
    
    st.markdown(f"""
    <div class="main-header">
        <h1>📚 Document Management</h1>
        <p>Training materials for {current_advisor['name']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    doc_manager = SimpleDocumentManager(advisor_id)
    
    # File upload section
    st.markdown("### 📤 Upload Training Documents")
    
    # Use a form to prevent automatic processing
    with st.form("upload_form", clear_on_submit=True):
        uploaded_files = st.file_uploader(
            "Upload documents to train your advisor",
            accept_multiple_files=True,
            type=['txt', 'pdf', 'docx', 'csv', 'json'],
            help="Supported: PDF, DOCX, TXT, CSV, JSON"
        )
        
        upload_button = st.form_submit_button("Upload Documents", use_container_width=True)
        
        if upload_button and uploaded_files:
            for uploaded_file in uploaded_files:
                try:
                    # Check if already exists
                    if doc_manager.document_exists(uploaded_file.name):
                        st.warning(f"⚠️ {uploaded_file.name} already exists. Skipping.")
                        continue
                    
                    with st.spinner(f"Processing {uploaded_file.name}..."):
                        content = DocumentProcessor.process_file(uploaded_file)
                        
                        if content.strip():
                            if doc_manager.add_document(content, uploaded_file.name):
                                st.success(f"✅ {uploaded_file.name} uploaded successfully!")
                            else:
                                st.error(f"❌ Failed to save {uploaded_file.name}")
                        else:
                            st.warning(f"⚠️ No text found in {uploaded_file.name}")
                
                except Exception as e:
                    st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
            
            st.rerun()
    
    # Existing documents
    st.markdown("### 📄 Uploaded Documents")
    documents = doc_manager.get_all_documents()
    
    if documents:
        st.write(f"**Total Documents:** {len(documents)}")
        
        for i, doc in enumerate(documents):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.write(f"📄 {doc}")
            
            with col2:
                if st.button("🗑️", key=f"del_{i}_{doc}", help="Delete"):
                    if doc_manager.delete_document(doc):
                        st.success(f"Deleted {doc}")
                        st.rerun()
    else:
        st.info("No documents uploaded yet.")
    
    if st.button("← Back to Advisors"):
        st.session_state.page = "advisors"
        st.rerun()

def chat_interface():
    """Enhanced chat interface"""
    apply_futuristic_theme()
    
    advisor_id = st.session_state.current_advisor
    user_manager = UserManager()
    advisors = user_manager.get_user_advisors(st.session_state.user["user_id"])
    current_advisor = next((a for a in advisors if a["id"] == advisor_id), None)
    
    if not current_advisor:
        st.error("Advisor not found!")
        return
    
    st.markdown(f"""
    <div class="main-header">
        <h1>💬 Chat with {current_advisor['name']}</h1>
        <p>Your intelligent {current_advisor['subject_area']} advisor</p>
    </div>
    """, unsafe_allow_html=True)
    
    doc_manager = SimpleDocumentManager(advisor_id)
    ai = IntelligentAI(st.session_state.user["user_id"])
    
    # Initialize chat history
    if f"messages_{advisor_id}" not in st.session_state:
        st.session_state[f"messages_{advisor_id}"] = [
            {"role": "assistant", "content": f"Hello! I'm {current_advisor['name']}, your AI advisor specializing in {current_advisor['subject_area']}. How can I help you today?"}
        ]
    
    # Display chat messages
    for message in st.session_state[f"messages_{advisor_id}"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Sidebar
    with st.sidebar:
        config = load_user_config(st.session_state.user["user_id"])
        
        st.markdown("### 🎛️ AI Status")
        if config.get("use_api", False):
            if config.get("api_key", ""):
                st.success("✅ AI Mode Active")
                st.caption("Using Groq API for intelligent responses")
            else:
                st.error("⚠️ API Enabled but No Key")
                st.caption("Add API key in Settings")
        else:
            st.info("📋 Document Mode")
            st.caption("Returning exact document content")
        
        if st.button("⚙️ Go to Settings", use_container_width=True):
            st.session_state.page = "settings"
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📄 Available Documents")
        documents = doc_manager.get_all_documents()
        
        if documents:
            for doc in documents:
                st.write(f"• {doc}")
        else:
            st.warning("No documents uploaded yet.")
            if st.button("📁 Upload Documents", use_container_width=True):
                st.session_state.page = "manage_documents"
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 🎛️ Controls")
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state[f"messages_{advisor_id}"] = [
                {"role": "assistant", "content": f"Hello! I'm {current_advisor['name']}, your AI advisor. How can I help you?"}
            ]
            st.rerun()
        
        if st.button("← Back to Advisors", use_container_width=True):
            st.session_state.page = "advisors"
            st.rerun()
    
    # Chat input
    if prompt := st.chat_input(f"Ask {current_advisor['name']} anything..."):
        # Add user message
        st.session_state[f"messages_{advisor_id}"].append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner(f"{current_advisor['name']} is thinking..."):
                # Search for relevant context
                context = doc_manager.search_documents(prompt)
                
                # Generate intelligent AI response
                response = ai.generate_intelligent_response(prompt, context, current_advisor['name'])
                
                st.markdown(response)
        
        # Add assistant response
        st.session_state[f"messages_{advisor_id}"].append({"role": "assistant", "content": response})

def main():
    """Main application function"""
    st.set_page_config(
        page_title="AI Advisor Platform",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if "user" not in st.session_state:
        st.session_state.user = None
    if "page" not in st.session_state:
        st.session_state.page = "advisors"
    if "current_advisor" not in st.session_state:
        st.session_state.current_advisor = None
    
    # Check if user is logged in
    if st.session_state.user is None:
        login_register_page()
    else:
        # Sidebar with user info
        with st.sidebar:
            st.markdown(f"### 👋 {st.session_state.user['full_name']}")
            st.markdown(f"**@{st.session_state.user['username']}**")
            
            st.markdown("---")
            
            if st.button("⚙️ Settings", use_container_width=True):
                st.session_state.page = "settings"
                st.rerun()
            
            if st.button("🚪 Logout", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        # Route to appropriate page
        if st.session_state.page == "settings":
            settings_page()
        elif st.session_state.page == "advisors":
            advisor_management()
        elif st.session_state.page == "manage_documents":
            document_management()
        elif st.session_state.page == "chat":
            chat_interface()

if __name__ == "__main__":
    main()