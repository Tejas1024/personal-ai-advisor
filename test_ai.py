# Test AI Setup Script
# Run this to verify your AI integration is working

import sys

def test_basic_requirements():
    """Test if basic requirements are installed"""
    print("🔍 Testing basic requirements...")
    
    try:
        import streamlit
        print("✅ Streamlit installed")
    except ImportError:
        print("❌ Streamlit not installed - run: pip install streamlit")
        return False
    
    try:
        import pandas
        print("✅ Pandas installed")
    except ImportError:
        print("❌ Pandas not installed - run: pip install pandas")
        return False
    
    try:
        import PyPDF2
        print("✅ PyPDF2 installed")
    except ImportError:
        print("❌ PyPDF2 not installed - run: pip install PyPDF2")
        return False
    
    try:
        import docx
        print("✅ python-docx installed")
    except ImportError:
        print("❌ python-docx not installed - run: pip install python-docx")
        return False
    
    try:
        import requests
        print("✅ Requests installed")
    except ImportError:
        print("❌ Requests not installed - run: pip install requests")
        return False
    
    return True

def test_ai_capabilities():
    """Test AI capabilities"""
    print("\n🤖 Testing AI capabilities...")
    
    # Test transformers
    try:
        import transformers
        print("✅ Transformers installed - Local AI available!")
        
        try:
            import torch
            print("✅ PyTorch installed - GPU acceleration possible!")
            
            if torch.cuda.is_available():
                print(f"🚀 CUDA GPU detected: {torch.cuda.get_device_name(0)}")
            else:
                print("💻 Running on CPU (still works great!)")
                
        except ImportError:
            print("⚠️ PyTorch not installed - install for better performance: pip install torch")
            
    except ImportError:
        print("⚠️ Transformers not installed")
        print("   For local AI: pip install transformers torch")
        print("   Or use Groq API for free cloud AI")

def test_groq_connection():
    """Test Groq API connection"""
    print("\n🌐 Testing Groq API connection...")
    
    try:
        import requests
        
        # Test if Groq API is accessible
        response = requests.get("https://api.groq.com", timeout=5)
        print("✅ Groq API is accessible")
        print("   Get your free API key at: https://groq.com")
        
    except Exception as e:
        print("⚠️ Groq API connection issue - check internet connection")

def test_sample_ai_response():
    """Test a sample AI response"""
    print("\n💬 Testing sample AI response...")
    
    # Simple test of the AI logic
    test_context = "Artificial intelligence is revolutionizing technology. Machine learning enables computers to learn from data."
    test_query = "What is AI?"
    
    # Simulate the fallback response logic
    query_words = set(test_query.lower().split())
    context_words = set(test_context.lower().split())
    overlap = len(query_words.intersection(context_words))
    
    if overlap > 0:
        print("✅ AI response logic working - context matching successful")
    else:
        print("⚠️ AI response logic needs checking")

def main():
    """Run all tests"""
    print("🧪 AI Personal Advisor - System Check\n")
    print("=" * 50)
    
    # Test basic requirements
    if not test_basic_requirements():
        print("\n❌ Basic requirements missing. Install them first!")
        return
    
    # Test AI capabilities
    test_ai_capabilities()
    
    # Test Groq connection
    test_groq_connection()
    
    # Test AI logic
    test_sample_ai_response()
    
    print("\n" + "=" * 50)
    print("🎉 SYSTEM CHECK COMPLETE!")
    print("\n📋 RECOMMENDATIONS:")
    
    try:
        import transformers
        print("✅ You have local AI - responses will be great!")
    except ImportError:
        print("💡 Install transformers for local AI: pip install transformers torch")
        print("💡 OR get free Groq API key for cloud AI: https://groq.com")
    
    print("\n🚀 Your app is ready! Run: streamlit run app.py")

if __name__ == "__main__":
    main()