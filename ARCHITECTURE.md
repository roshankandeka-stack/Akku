# 🏗️ AKKU Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    AKKU Application                          │
│                   (Streamlit Frontend)                       │
└─────────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        ↓                     ↓                     ↓
    ┌────────────┐     ┌────────────┐     ┌─────────────┐
    │Data        │     │Dashboard   │     │AI/LLM       │
    │Processor   │     │Generator   │     │Chatbot      │
    └────────────┘     └────────────┘     └─────────────┘
        ↓                   ↓                     ↓
    ┌────────────────────────────────────────────────────┐
    │         Data Layer & Processing                     │
    │    (Pandas, NumPy, Statistics)                      │
    └────────────────────────────────────────────────────┘
        ↓
    ┌────────────────────────────────────────────────────┐
    │     External Services                              │
    │  OpenAI API  │  FAISS Index  │  Embeddings         │
    └────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. **Frontend Layer** (main.py)
- Streamlit web interface
- Multi-page navigation
- Real-time data visualization
- User interaction handling

**Key Features:**
- Sidebar file upload
- Navigation tabs
- Session state management
- Error handling

### 2. **Data Processing Layer** (data_processor.py)

```
DataProcessor Class
├── load_file()
│   ├── CSV support
│   ├── Excel support
│   └── Validation
├── clean_data()
│   ├── Drop missing
│   ├── Fill mean
│   └── Forward fill
├── analyze()
│   ├── Statistics
│   ├── Correlations
│   ├── Outliers
│   └── Insights
└── export()
    └── CSV export
```

**Capabilities:**
- Supports CSV, XLSX, XLS formats
- Data type detection
- Missing value handling
- Statistical calculations
- Automatic insight generation

### 3. **Visualization Layer** (dashboard.py)

```
DashboardGenerator
├── Chart Types
│   ├── Bar Chart
│   ├── Line Chart
│   ├── Pie Chart
│   ├── Scatter Plot
│   ├── Histogram
│   ├── Box Plot
│   ├── Heatmap
│   ├── Multi-line
│   └── Sunburst
├── Components
│   ├── KPI Cards
│   ├── Summary Stats
│   └── Comparison Charts
└── Styling
    ├── Color schemes
    ├── Templates
    └── Hover info
```

**Libraries Used:**
- Plotly Express - Interactive charts
- Plotly Graph Objects - Advanced customization
- Matplotlib - Static plots
- Seaborn - Statistical visualization

### 4. **AI/LLM Layer** (ai_chatbot.py)

```
DataChatbot
├── analyze_dataframe()
│   ├── Dataset context
│   ├── OpenAI API call
│   └── Response generation
├── generate_insights()
│   ├── Statistics calculation
│   ├── Pattern detection
│   └── AI summary
├── get_recommendations()
│   ├── Data analysis
│   ├── Business logic
│   └── Actionable insights
└── get_visualization_suggestion()
    ├── Column analysis
    └── Chart recommendations

InsightGenerator
├── generate_summary()
├── format_insights()
└── Dataset analysis
```

**Features:**
- GPT-3.5-Turbo integration
- Conversational context awareness
- Dataset-specific responses
- Recommendation generation

### 5. **RAG System Layer** (rag_system.py)

```
┌─────────────────────────────────────────┐
│     RAG (Retrieval Augmented Generation)│
└─────────────────────────────────────────┘
                      ↓
        ┌─────────────┴──────────────┐
        ↓                            ↓
   ┌─────────────┐            ┌──────────────┐
   │Retrieval    │            │Generation    │
   │- User Query │            │- LLM Prompt  │
   │- Embedding  │            │- Context     │
   │- FAISS      │            │- Response    │
   │- Top-K      │            │              │
   └─────────────┘            └──────────────┘

RAGSystem Class
├── Knowledge Base Management
│   ├── add_document()
│   ├── add_faq()
│   └── list_documents()
├── Indexing
│   ├── build_index()
│   │   ├── Sentence embeddings
│   │   ├── FAISS index creation
│   │   └── Persistence
│   ├── save_index()
│   └── load_index()
├── Retrieval
│   ├── retrieve()
│   │   ├── Query embedding
│   │   ├── Similarity search
│   │   └── Ranking
│   └── generate_response()
└── Support Bot
    ├── process_query()
    ├── get_conversation_history()
    └── clear_history()
```

## RAG System in Detail

### How RAG Works in AKKU

```
Step 1: User Query
    ↓
"How do I upload a dataset?"
    ↓
Step 2: Embedding
    ├── SentenceTransformer encodes query
    ├── Creates vector representation
    └── Dimension: ~384 dimensions
    ↓
Step 3: FAISS Search
    ├── Find similar documents
    ├── Using L2 distance metric
    ├── Return top-3 results
    └── Calculate relevance scores
    ↓
Step 4: Context Assembly
    ├── Retrieve document content
    ├── Get metadata
    ├── Format for LLM
    └── Calculate similarity
    ↓
Step 5: Generate Response
    ├── Pass context to ChatGPT
    ├── Include user query
    ├── Generate natural response
    └── Return with sources
    ↓
Step 6: Display
    ├── Show main response
    ├── List sources
    ├── Relevance scores
    └── Store in history
```

### Vector Database (FAISS)

**Index Type:** IndexFlatL2
- Uses L2 distance (Euclidean)
- Exact search (no approximation)
- Suitable for small-medium datasets
- Persistence: Binary file format

**Knowledge Base Structure:**
```python
{
    "id": "faq_0",
    "content": "Q: How do I upload?\nA: Click upload button...",
    "metadata": {
        "type": "faq",
        "question": "How do I upload a dataset?"
    }
}
```

### Embedding Model

**Model:** all-MiniLM-L6-v2
- Lightweight (22MB)
- Fast inference
- 384-dimensional embeddings
- Pre-trained on large text corpus
- Good for customer support domain

**Embedding Process:**
```
Text Input
    ↓
Tokenization (max 512 tokens)
    ↓
BERT Encoding
    ↓
Pooling (mean of last layer)
    ↓
Normalization
    ↓
384-d Vector Output
```

## Data Flow Diagram

### Data Upload Flow
```
User Upload
    ↓
File Validation
├── Format check (CSV/Excel)
├── Size check
└── Header validation
    ↓
Load into Pandas
    ├── Type inference
    ├── Memory allocation
    └── Index creation
    ↓
Data Cleaning Options
├── Remove missing (drop)
├── Fill numeric (mean)
├── Forward fill
    ↓
Store in Session State
└── Ready for analysis
```

### Visualization Flow
```
Select Chart Type
    ↓
Choose Columns
├── X-axis
├── Y-axis
└── Color/Size (optional)
    ↓
DataProcessor extracts data
    ↓
DashboardGenerator creates chart
├── Prepare data format
├── Configure Plotly figure
└── Add hover info
    ↓
Streamlit renders
└── Interactive display
```

### AI Chat Flow
```
User Question
    ↓
Prepare Dataset Context
├── Shape & columns
├── Sample rows
├── Statistics
└── Data types
    ↓
Build Prompt
├── System message
├── Context
└── User query
    ↓
OpenAI API Call
├── Stream response
└── Handle errors
    ↓
Store in History
├── User message
└── Assistant response
    ↓
Display Response
└── Format output
```

### RAG Flow
```
User Question
    ↓
Encode Query
├── SentenceTransformer
└── 384-d embedding
    ↓
FAISS Search
├── L2 distance calculation
├── Find top-k results
└── Get relevance scores
    ↓
Format Context
├── Retrieve documents
├── Get metadata
└── Prepare text
    ↓
Generate Response
├── Pass to LLM
├── Include context
└── Return answer
    ↓
Display & Store
├── Show sources
├── Relevance scores
└── Save to history
```

## Session State Management

```
st.session_state
├── data_processor (DataProcessor)
│   ├── df (current dataframe)
│   ├── original_df (backup)
│   └── methods...
├── chatbot (DataChatbot)
│   ├── conversation_history
│   ├── api_key
│   └── methods...
├── rag_system (RAGSystem)
│   ├── knowledge_base
│   ├── index (FAISS)
│   ├── embeddings
│   └── methods...
├── support_bot (CustomerSupportBot)
│   ├── rag reference
│   ├── conversation_history
│   └── methods...
└── current_page (str)
    └── Navigation state
```

## Technology Stack

### Frontend
- **Streamlit 1.28.1** - Web framework
- **Session State** - State management
- **Custom CSS** - Styling

### Data Processing
- **Pandas 2.0.3** - Data manipulation
- **NumPy 1.24.3** - Numerical computing
- **SciPy** - Statistical functions

### Visualization
- **Plotly 5.16.1** - Interactive charts
- **Matplotlib 3.7.2** - Static plots
- **Seaborn 0.12.2** - Statistical viz

### AI/LLM
- **OpenAI 1.3.0** - GPT API
- **LangChain 0.1.0** - LLM framework
- **Sentence Transformers 2.2.2** - Embeddings

### RAG System
- **FAISS 1.7.4** - Vector search
- **FAISS CPU** - No GPU required
- **Pickle** - Index serialization

### Utilities
- **python-dotenv 1.0.0** - Env variables
- **Requests 2.31.0** - HTTP client
- **BeautifulSoup4 4.12.2** - HTML parsing
- **python-docx 0.8.11** - Word documents

## Performance Considerations

### Memory Usage
- **Small datasets**: <10MB
- **Medium datasets**: 10-100MB
- **Large datasets**: Consider sampling

### API Costs
- **Embeddings**: ~$0.02 per 1M tokens
- **Chat**: ~$0.002 per 1K tokens
- **Usage**: Depends on query frequency

### Speed Optimization
- FAISS index loaded once
- Embeddings cached
- Streamlit reruns minimized
- Chart caching enabled

## Security

### API Key Protection
```
.env file
├── Contains OPENAI_API_KEY
├── Never committed to git
├── Loaded via python-dotenv
└── Not exposed in logs
```

### Data Privacy
- Files not permanently stored
- Processing local only
- No external logging
- Session-based isolation

### Error Handling
- Try-catch blocks
- User-friendly messages
- Detailed logging
- Graceful degradation

## Scalability

### Current Limitations
- Single-user (Streamlit limitation)
- Memory limited to available RAM
- FAISS limited to ~1M vectors
- OpenAI rate limits

### Future Improvements
- Multi-user architecture
- Database backend
- Distributed processing
- Batch API calls
- Vector DB clustering

## Development Workflow

```
main.py (Entry point)
    ↓
sidebar (Navigation & Upload)
    ├→ config.py (Load settings)
    └→ session_state (Initialize)
    ↓
Navigation Handler
├→ Dashboard Tab
│   └→ data_processor.py
├→ Analytics Tab
│   ├→ data_processor.py
│   └→ dashboard.py
├→ Chat Tab
│   ├→ data_processor.py
│   └→ ai_chatbot.py
├→ Support Tab
│   └→ rag_system.py
└→ About Tab
    └→ Static content
```

## Testing Approach

### Unit Testing Areas
- Data loading and cleaning
- Statistical calculations
- Embedding generation
- FAISS retrieval
- Response generation

### Integration Testing
- File upload → Dashboard
- Data → Chart generation
- Query → AI response
- RAG retrieval → Display

### User Testing
- Use sample_data.csv
- Test each tab
- Try edge cases
- Verify error handling

---

**Architecture Design:** Modular, scalable, AI-enhanced  
**Framework:** Streamlit with external services  
**Database:** File-based + Vector DB  
**Security:** API key protection, local processing  
**Performance:** Optimized for single-user, small-medium datasets  

**Version:** 1.0.0  
**Last Updated:** 2024
