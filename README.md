# 🚀 AKKU - AI-Powered Data Analytics Platform

An intelligent platform that combines data analytics, interactive dashboards, conversational AI, and RAG-based customer support.

## ✨ Features

### 1. **📊 Analytics Dashboard**
- Upload CSV/Excel datasets
- View dataset overview and statistics
- Quick insights and data quality checks
- Missing value analysis

### 2. **📈 Advanced Analytics**
- Multiple visualization types:
  - Bar Charts
  - Line Charts
  - Pie Charts
  - Scatter Plots
  - Histograms
  - Box Plots
  - Correlation Heatmaps
- Data cleaning options
- Statistical analysis

### 3. **💬 Chat with Data**
- Ask natural language questions about your data
- AI-generated insights from dataset
- Get recommendations based on data
- Receive visualization suggestions

### 4. **🆘 RAG-Based Customer Support**
- Intelligent question answering using retrieval augmented generation
- FAQ management
- Knowledge base creation and management
- Conversation history tracking
- Context-aware responses

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- OpenAI API key (for AI features)

### Step 1: Clone or Download Project

```bash
# Create project directory
mkdir akku-project
cd akku-project

# Copy all project files here
```

### Step 2: Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `streamlit` - Web UI framework
- `pandas` - Data processing
- `plotly` - Interactive visualizations
- `openai` - LLM integration
- `langchain` - AI framework
- `faiss-cpu` - Vector database for RAG
- `sentence-transformers` - Embeddings
- And other dependencies

### Step 4: Configure API Keys

1. Create a `.env` file in the project root:

```bash
# On Windows
copy .env.example .env

# On macOS/Linux
cp .env.example .env
```

2. Edit `.env` and add your API keys:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
```

### Get OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com)
2. Sign up or log in
3. Go to API keys section
4. Create new secret key
5. Copy and paste in `.env` file

### Step 5: Run Application

```bash
streamlit run main.py
```

The application will open at `http://localhost:8501`

## 📖 Usage Guide

### 1. **Loading Data**

```
1. Click on the sidebar
2. Click "Upload CSV or Excel File"
3. Select your file (CSV, XLSX, or XLS)
4. Wait for confirmation
```

### 2. **View Dashboard**

- **📊 Dashboard Tab**: See overview and statistics
- View row count, columns, missing values
- See data preview and quick insights

### 3. **Create Visualizations**

- Go to **📈 Analytics** tab
- Select visualization type
- Choose columns for X and Y axes
- View interactive charts

Supported visualizations:
- **Bar Chart**: Compare values across categories
- **Line Chart**: Show trends over time
- **Pie Chart**: Display proportions
- **Scatter Plot**: Analyze relationships
- **Histogram**: View distributions
- **Box Plot**: Detect outliers
- **Heatmap**: See correlations

### 4. **Chat with Data**

- Go to **💬 Chat with Data** tab
- Ask questions in natural language
- Examples:
  - "What are the top 5 categories?"
  - "Show me sales trends"
  - "What's the average value?"
- Get AI-generated insights
- Receive recommendations

### 5. **Customer Support (RAG)**

#### Ask Questions
1. Go to **🆘 Customer Support (RAG)** tab
2. Click "Ask Question" tab
3. Type your question
4. System searches knowledge base
5. Get relevant answers with sources

#### Manage Knowledge Base
1. Click "Knowledge Base" tab
2. View existing documents
3. Add new documents with content
4. Choose document type
5. Rebuild index if needed

#### Browse FAQs
1. Click "FAQs" tab
2. View frequently asked questions
3. See chat history
4. Clear history if needed

## 📁 Project Structure

```
akku-project/
├── main.py                    # Main Streamlit application
├── config.py                  # Configuration and constants
├── data_processor.py          # Data loading and processing
├── dashboard.py               # Visualization components
├── ai_chatbot.py              # LLM integration
├── rag_system.py              # RAG system for support
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── .env                       # Your API keys (create from example)
├── faiss_index/               # RAG vector database (auto-created)
└── README.md                  # This file
```

## 🔑 Key Components

### DataProcessor
Handles data loading, cleaning, and analysis
- `load_file()` - Load CSV/Excel
- `clean_data()` - Clean missing values
- `get_statistical_summary()` - Generate stats
- `get_insights()` - Auto insights

### DashboardGenerator
Creates interactive visualizations
- `create_bar_chart()`
- `create_line_chart()`
- `create_pie_chart()`
- `create_scatter_plot()`
- `create_histogram()`
- `create_box_plot()`
- `create_heatmap()`

### DataChatbot
Conversational AI for data analysis
- `analyze_dataframe()` - Answer questions
- `generate_insights()` - AI insights
- `get_recommendations()` - Data recommendations
- `get_visualization_suggestion()` - Chart suggestions

### RAGSystem
Retrieval Augmented Generation for support
- `add_document()` - Add to knowledge base
- `retrieve()` - Find relevant documents
- `build_index()` - Create vector index
- `save_index()` / `load_index()` - Persist data

## 🚀 Quick Start Example

```python
# Example: Load data and chat
1. Upload "sales_data.csv" via sidebar
2. Go to "Chat with Data" tab
3. Ask: "What are the top selling products?"
4. Get AI response with analysis
5. Ask: "Show me growth trends"
6. Receive visualization suggestions
7. Go to Analytics tab and create chart
```

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# LLM Model
DEFAULT_LLM_MODEL = "gpt-3.5-turbo"

# RAG Settings
RAG_CHUNK_SIZE = 500
RAG_TOP_K = 3

# Chart Colors
CHART_COLORS = {
    "primary": "#1f77b4",
    "success": "#2ca02c",
    ...
}
```

## 🐛 Troubleshooting

### Issue: "API key not found"
**Solution**: Check `.env` file has `OPENAI_API_KEY` set correctly

### Issue: "Module not found"
**Solution**: Reinstall dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "File upload fails"
**Solution**: Ensure file is CSV or Excel format, under 100MB

### Issue: "Chat not responding"
**Solution**: 
1. Check API key is valid
2. Check internet connection
3. Check OpenAI API account has credits

### Issue: "RAG system not finding answers"
**Solution**: 
1. Go to Knowledge Base tab
2. Add more documents
3. Rebuild index

## 📊 Sample Data

Test with sample datasets:

**Sales Data** (sales_data.csv)
```
Date,Product,Category,Sales,Region
2024-01-01,Laptop,Electronics,1200,North
2024-01-02,Phone,Electronics,800,South
...
```

**Customer Data** (customers.csv)
```
CustomerID,Name,Age,Location,Spent
1,John,28,NYC,2500
2,Jane,35,LA,3200
...
```

## 🔐 Security

- Data is processed locally
- No permanent storage of uploaded files
- API keys stored in `.env` (not committed to git)
- Add `.env` to `.gitignore`

```bash
# .gitignore
.env
faiss_index/
__pycache__/
*.pyc
.streamlit/
```

## 📈 Performance Tips

- For large datasets (>100K rows):
  - Use data filtering
  - Sample data for visualization
  - Consider data chunking

- For slow responses:
  - Check internet connection
  - Verify API key validity
  - Reduce RAG top_k value

## 🤝 Contributing

Improvements welcome! Feel free to:
- Add new visualization types
- Enhance RAG system
- Improve UI/UX
- Add more analytics features

## 📝 License

This project is provided as-is for educational and commercial use.

## 🙏 Acknowledgments

- **Streamlit** - Amazing web framework
- **OpenAI** - Powerful LLM API
- **Plotly** - Beautiful visualizations
- **FAISS** - Efficient similarity search
- **Sentence Transformers** - High-quality embeddings

## 📞 Support

### Getting Help

1. **Check FAQs** - Use Customer Support tab
2. **Review README** - This guide
3. **Check Issues** - Common problems above
4. **Update Packages** - Run `pip install -r requirements.txt --upgrade`

### Common Questions

**Q: Can I use different LLM models?**
A: Yes, modify `config.py` and use `gpt-4`, `claude`, etc.

**Q: How do I add custom RAG documents?**
A: Use Knowledge Base tab in Customer Support section

**Q: Can I export processed data?**
A: Yes, use the export button in Dashboard

**Q: Is there a database backend?**
A: Currently file-based, you can add SQLite/PostgreSQL

## 🎓 Learning Resources

- [Streamlit Docs](https://docs.streamlit.io)
- [OpenAI API Guide](https://platform.openai.com/docs)
- [Plotly Tutorial](https://plotly.com/python)
- [FAISS Documentation](https://faiss.ai)

## 🚀 Future Enhancements

- [ ] PDF document support
- [ ] Voice-based queries
- [ ] Real-time analytics
- [ ] Multi-user collaboration
- [ ] Predictive analytics
- [ ] Database integration
- [ ] Custom ML models
- [ ] Export to PowerPoint

---

**Version:** 1.0.0  
**Last Updated:** 2024  
**Built with ❤️ using Python & Streamlit**

**Ready to transform your data into intelligence? 🚀**
