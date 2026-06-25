from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = None

if GROQ_API_KEY:
    client = OpenAI(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1"
    )

# LLM Models

DEFAULT_LLM_MODEL = "llama-3.3-70b-versatile"
EMBEDDING_MODEL = "text-embedding-3-small"

# RAG Configuration
RAG_VECTOR_DB_PATH = "faiss_index"
RAG_CHUNK_SIZE = 500
RAG_CHUNK_OVERLAP = 100
RAG_TOP_K = 3

# Dashboard Configuration
CHART_COLORS = {
    "primary": "#1f77b4",
    "success": "#2ca02c",
    "warning": "#ff7f0e",
    "danger": "#d62728",
    "info": "#17a2b8",
}

# UI Configuration
PAGE_CONFIG = {
    "page_title": "Akku - AI Data Analytics",
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Sample Support Data
SAMPLE_FAQ = [
    {
        "question": "How do I upload a dataset?",
        "answer": "Click on 'Upload Dataset' in the sidebar, select your CSV or Excel file, and click upload. The system will validate and preview your data."
    },
    {
        "question": "What file formats are supported?",
        "answer": "We support CSV (.csv) and Excel (.xlsx, .xls) file formats. Maximum file size is 100MB."
    },
    {
        "question": "Can I ask questions about my data?",
        "answer": "Yes! Use the 'Chat with Data' feature to ask natural language questions. Our AI will analyze your dataset and provide insights."
    },
    {
        "question": "How does the AI generate insights?",
        "answer": "The AI uses machine learning to analyze patterns, trends, and anomalies in your data, then generates human-readable insights and recommendations."
    },
    {
        "question": "Is my data secure?",
        "answer": "Your data is processed securely and only used for your analysis. We don't store your datasets permanently."
    },
    {
        "question": "What can the RAG system help with?",
        "answer": "The RAG system provides intelligent customer support, answers FAQs, and helps troubleshoot issues using uploaded knowledge base documents."
    },
]
