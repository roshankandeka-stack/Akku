# ⚡ Quick Start Guide - AKKU

Get up and running in 5 minutes!

## 1️⃣ Install Dependencies (2 min)

```bash
pip install -r requirements.txt
```

## 2️⃣ Configure API Key (1 min)

### Option A: Using .env file

1. Copy the example file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-key-here
```

Get API key from: https://platform.openai.com/api-keys

### Option B: No API Key (Limited Features)
You can use the app without API key, but AI chat features won't work.

## 3️⃣ Start Application (1 min)

```bash
streamlit run main.py
```

Opens automatically at: `http://localhost:8501`

## 4️⃣ First Steps (1 min)

### Step 1: Upload Sample Data
- Sidebar → "Upload CSV or Excel File"
- Choose `sample_data.csv` (included in project)
- Click upload

### Step 2: Explore Dashboard
- Click "📊 Dashboard" tab
- See dataset overview
- View insights and statistics

### Step 3: Create Visualizations
- Click "📈 Analytics" tab
- Select "Bar Chart"
- Choose columns for X and Y axes
- View interactive chart

### Step 4: Chat with Data
- Click "💬 Chat with Data" tab
- Ask: "What are the top products by sales?"
- See AI response

### Step 5: Try RAG Support
- Click "🆘 Customer Support (RAG)" tab
- Ask: "How do I upload a dataset?"
- See answer from knowledge base

## 📊 Sample Data

Included `sample_data.csv` has:
- **50 rows** of sales data
- **8 columns**: Date, Product, Category, Sales, Quantity, Region, Customer_Type, Profit_Margin
- **3 categories**: Electronics, Accessories, Furniture
- **4 regions**: North, South, East, West

Perfect for testing all features!

## 🎯 Example Queries

### For Chat with Data:
- "What's the total sales by region?"
- "Show me the most profitable products"
- "What are the trends over time?"
- "Which region has the highest sales?"

### For Customer Support:
- "How do I upload a dataset?"
- "What file formats are supported?"
- "Can I ask questions about my data?"
- "How does the AI generate insights?"

## 🖼️ Feature Overview

| Feature | Tab | What It Does |
|---------|-----|--------------|
| **Overview** | Dashboard | See dataset stats |
| **Charts** | Analytics | Create visualizations |
| **AI Chat** | Chat with Data | Ask questions |
| **Support** | Customer Support | Get help via RAG |
| **Info** | About | Learn about AKKU |

## ⚠️ Troubleshooting

### Can't start app?
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Try again
streamlit run main.py
```

### API key error?
```bash
# Verify .env file exists and is in project root
ls -la .env  # On Windows: dir .env

# Check format:
OPENAI_API_KEY=sk-xxxxx  # Don't use quotes

# Test key:
python -c "from config import OPENAI_API_KEY; print('OK' if OPENAI_API_KEY else 'MISSING')"
```

### File upload fails?
- Use CSV or Excel format only
- File must be < 100MB
- Ensure columns have headers

### AI Chat not working?
- Add OPENAI_API_KEY to .env
- Restart streamlit (Ctrl+C, then run again)
- Check API key is valid on OpenAI dashboard

## 📚 Next Steps

1. **Try different visualizations** - Bar, Line, Pie, Scatter
2. **Upload your own data** - Use your CSV/Excel file
3. **Explore AI features** - Generate insights, get recommendations
4. **Manage knowledge base** - Add documents to RAG system
5. **Read full README** - For advanced features

## 🚀 What's Next?

### Want to customize colors?
Edit `config.py`:
```python
CHART_COLORS = {
    "primary": "#your-color",
}
```

### Want to change AI model?
Edit `config.py`:
```python
DEFAULT_LLM_MODEL = "gpt-4"  # Or claude-3, etc
```

### Want to add more sample data?
1. Create CSV file with your data
2. Upload via sidebar
3. Explore!

## 💡 Pro Tips

✅ **Tip 1**: Use "Generate Insights" to get AI analysis automatically

✅ **Tip 2**: The RAG system learns from documents you add to KB

✅ **Tip 3**: Save processed data using "Data Cleaning" options

✅ **Tip 4**: Export cleaned data for use elsewhere

✅ **Tip 5**: Use keyboard shortcut `Ctrl+Enter` to submit queries

## 🎓 Learn More

- Full documentation: See `README.md`
- Code examples: Check individual `.py` files
- Streamlit docs: https://docs.streamlit.io
- OpenAI docs: https://platform.openai.com/docs

## ✅ Checklist

- [ ] Install dependencies
- [ ] Add API key to .env
- [ ] Start application
- [ ] Upload sample data
- [ ] View dashboard
- [ ] Create chart
- [ ] Chat with data
- [ ] Try RAG support

**You're ready to go! 🎉**

---

**Need Help?** Check the `README.md` for detailed documentation.

**Found a Bug?** Create an issue or check troubleshooting section.

**Have Suggestions?** We'd love to hear them!

Happy analyzing! 📊✨
