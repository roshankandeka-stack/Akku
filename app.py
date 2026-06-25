import streamlit as st
import pandas as pd
from datetime import datetime
import os

from config import PAGE_CONFIG, SAMPLE_FAQ, GROQ_API_KEY
from data_processor import DataProcessor
from dashboard import DashboardGenerator
from ai_chatbot import DataChatbot, InsightGenerator

# Configure Streamlit
st.set_page_config(**PAGE_CONFIG)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }

    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }

    .insight-card {
        background: #f0f2f6;
        padding: 1rem;
        border-left: 4px solid #667eea;
        border-radius: 5px;
        margin: 0.5rem 0;
    }

    .success {
        color: #2ecc71;
    }

    .warning {
        color: #f39c12;
    }

    .error {
        color: #e74c3c;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()

if 'chatbot' not in st.session_state:
    st.session_state.chatbot = DataChatbot(api_key=GROQ_API_KEY)

# Sidebar
with st.sidebar:
    st.title("🚀 AKKU")
    st.caption("AI-Powered Data Analytics Platform")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "📊 Dashboard",
            "📈 Analytics",
            "💬 Chat with Data",
            "📋 About"
        ]
    )

    st.divider()

    # File Upload
    st.subheader("📁 Dataset Management")

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel File",
        type=["csv", "xlsx", "xls"]
    )

    if uploaded_file is not None:

        if st.session_state.data_processor.load_file(uploaded_file):

            st.success("✅ File loaded successfully!")

            info = st.session_state.data_processor.get_basic_info()

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Rows", f"{info['shape'][0]:,}")

            with col2:
                st.metric("Columns", f"{info['shape'][1]}")

    st.divider()

    # API Status
    if GROQ_API_KEY:
        st.success("✅ GROQ API Configured")
    else:
        st.warning("⚠️ Add GROQ_API_KEY to .env file")

    st.divider()

    st.caption(
        f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

# =========================
# DASHBOARD PAGE
# =========================
if page == "📊 Dashboard":

    st.title("📊 Analytics Dashboard")

    if st.session_state.data_processor.df is None:

        st.info("👉 Please upload a dataset from the sidebar.")

    else:

        info = st.session_state.data_processor.get_basic_info()

        st.subheader("📋 Dataset Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Rows", f"{info['shape'][0]:,}")

        with col2:
            st.metric("Columns", info['shape'][1])

        with col3:
            missing = st.session_state.data_processor.get_missing_data_report()
            st.metric("Missing", len(missing))

        with col4:
            st.metric("Memory", f"{info['memory_usage']:.2f} MB")

        # Data Preview
        st.subheader("📄 Data Preview")

        st.dataframe(
            st.session_state.data_processor.get_data_sample(10),
            use_container_width=True
        )

        # Insights
        st.subheader("💡 Quick Insights")

        insights = st.session_state.data_processor.get_insights()

        for insight in insights:
            st.info(insight)

        # Summary Tables
        col1, col2 = st.columns(2)

        with col1:

            st.subheader("📊 Statistical Summary")

            st.dataframe(
                st.session_state.data_processor.get_statistical_summary(),
                use_container_width=True
            )

        with col2:

            st.subheader("⚠️ Missing Data Report")

            if len(missing) > 0:
                st.dataframe(missing, use_container_width=True)
            else:
                st.success("✅ No Missing Values")

# =========================
# ANALYTICS PAGE
# =========================
elif page == "📈 Analytics":

    st.title("📈 Advanced Analytics")

    if st.session_state.data_processor.df is None:

        st.info("👉 Please upload a dataset first.")

    else:

        df = st.session_state.data_processor.df

        chart_type = st.selectbox(
            "Select Chart Type",
            [
                "Bar Chart",
                "Line Chart",
                "Pie Chart",
                "Scatter Plot",
                "Histogram",
                "Box Plot",
                "Correlation Heatmap"
            ]
        )

        # BAR CHART
        if chart_type == "Bar Chart":

            col1, col2 = st.columns(2)

            with col1:
                x_col = st.selectbox("X-axis", df.columns)

            with col2:
                y_col = st.selectbox(
                    "Y-axis",
                    st.session_state.data_processor.get_numeric_columns()
                )

            if x_col and y_col:

                fig = DashboardGenerator.create_bar_chart(
                    df,
                    x_col,
                    y_col,
                    f"{y_col} by {x_col}"
                )

                st.plotly_chart(fig, use_container_width=True)

        # LINE CHART
        elif chart_type == "Line Chart":

            col1, col2 = st.columns(2)

            with col1:
                x_col = st.selectbox("X-axis", df.columns)

            with col2:
                y_col = st.selectbox(
                    "Y-axis",
                    st.session_state.data_processor.get_numeric_columns()
                )

            if x_col and y_col:

                fig = DashboardGenerator.create_line_chart(
                    df,
                    x_col,
                    y_col,
                    f"{y_col} over {x_col}"
                )

                st.plotly_chart(fig, use_container_width=True)

        # PIE CHART
        elif chart_type == "Pie Chart":

            col1, col2 = st.columns(2)

            with col1:
                names_col = st.selectbox("Category", df.columns)

            with col2:
                values_col = st.selectbox(
                    "Values",
                    st.session_state.data_processor.get_numeric_columns()
                )

            if names_col and values_col:

                agg_df = df.groupby(names_col)[values_col].sum().reset_index()

                fig = DashboardGenerator.create_pie_chart(
                    agg_df,
                    names_col,
                    values_col,
                    f"{values_col} Distribution"
                )

                st.plotly_chart(fig, use_container_width=True)

        # SCATTER PLOT
        elif chart_type == "Scatter Plot":

            col1, col2 = st.columns(2)

            with col1:
                x_col = st.selectbox(
                    "X-axis",
                    st.session_state.data_processor.get_numeric_columns()
                )

            with col2:
                y_col = st.selectbox(
                    "Y-axis",
                    st.session_state.data_processor.get_numeric_columns()
                )

            if x_col and y_col:

                fig = DashboardGenerator.create_scatter_plot(
                    df,
                    x_col,
                    y_col,
                    f"{y_col} vs {x_col}"
                )

                st.plotly_chart(fig, use_container_width=True)

        # HISTOGRAM
        elif chart_type == "Histogram":

            col = st.selectbox(
                "Column",
                st.session_state.data_processor.get_numeric_columns()
            )

            if col:

                fig = DashboardGenerator.create_histogram(
                    df,
                    col,
                    f"Distribution of {col}"
                )

                st.plotly_chart(fig, use_container_width=True)

        # BOX PLOT
        elif chart_type == "Box Plot":

            col = st.selectbox(
                "Column",
                st.session_state.data_processor.get_numeric_columns()
            )

            if col:

                fig = DashboardGenerator.create_box_plot(
                    df,
                    col,
                    None,
                    f"Box Plot - {col}"
                )

                st.plotly_chart(fig, use_container_width=True)

        # HEATMAP
        elif chart_type == "Correlation Heatmap":

            fig = DashboardGenerator.create_heatmap(
                df,
                "Correlation Matrix"
            )

            st.plotly_chart(fig, use_container_width=True)

# =========================
# CHAT WITH DATA PAGE
# =========================
elif page == "💬 Chat with Data":

    st.title("💬 Chat with Your Data")

    if st.session_state.data_processor.df is None:

        st.info("👉 Please upload a dataset first.")

    else:

        df = st.session_state.data_processor.df

        if not st.session_state.chatbot.is_api_configured():

            st.error(
                "⚠️ GROQ API key not configured. Add GROQ_API_KEY to .env file."
            )

        else:

            st.subheader("🗨️ Ask Questions")

            user_query = st.text_input(
                "Ask your question",
                placeholder="Example: Which category has highest sales?"
            )

            if user_query:

                with st.spinner("🤖 Analyzing..."):

                    response = st.session_state.chatbot.analyze_dataframe(
                        df,
                        user_query
                    )

                    st.markdown("### AI Response")
                    st.write(response)

            st.subheader("✨ Generate AI Insights")

            if st.button("Generate Insights"):

                with st.spinner("Generating insights..."):

                    insights = st.session_state.chatbot.generate_insights(df)

                    for insight in insights:
                        st.info(insight)

            st.subheader("📊 Visualization Suggestions")

            if st.button("Get Visualization Suggestions"):

                with st.spinner("Thinking..."):

                    suggestion = st.session_state.chatbot.get_visualization_suggestion(
                        df,
                        list(df.columns)
                    )

                    st.write(suggestion)

# =========================
# ABOUT PAGE
# =========================
elif page == "📋 About":

    st.title("📋 About AKKU")

    st.markdown("""
    ## 🚀 AKKU - AI Powered Analytics Platform

    AKKU helps users:

    - Upload datasets
    - Analyze data
    - Create dashboards
    - Chat with data using AI
    - Generate insights automatically

    ---

    ## 🛠 Tech Stack

    - Streamlit
    - Pandas
    - Plotly
    - Python
    - GROQ LLM API

    ---

    ## 🎯 Features

    ✅ CSV & Excel Upload  
    ✅ Interactive Charts  
    ✅ AI Data Chatbot  
    ✅ Automated Insights  
    ✅ Statistical Reports  

    ---

    ## 🔐 Privacy

    Your uploaded files are processed securely during the session.
    """)

# Footer
st.divider()

st.markdown("""
<div style='text-align:center; color:gray; padding:20px;'>
    🚀 <b>AKKU</b> - Transforming Data into Intelligence
</div>
""", unsafe_allow_html=True)
