import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import streamlit as st
from typing import List, Optional

class DashboardGenerator:
    """Generate interactive visualizations"""
    
    @staticmethod
    def create_bar_chart(df: pd.DataFrame, x: str, y: str, title: str = "", color: str = "#1f77b4") -> go.Figure:
        """Create interactive bar chart"""
        fig = px.bar(
            df,
            x=x,
            y=y,
            title=title,
            color_discrete_sequence=[color],
            template="plotly_white"
        )
        fig.update_layout(
            height=400,
            hovermode='x unified',
            xaxis_title=x,
            yaxis_title=y
        )
        return fig
    
    @staticmethod
    def create_line_chart(df: pd.DataFrame, x: str, y: str, title: str = "") -> go.Figure:
        """Create interactive line chart"""
        fig = px.line(
            df,
            x=x,
            y=y,
            title=title,
            markers=True,
            template="plotly_white"
        )
        fig.update_layout(
            height=400,
            hovermode='x unified',
            xaxis_title=x,
            yaxis_title=y
        )
        return fig
    
    @staticmethod
    def create_pie_chart(df: pd.DataFrame, names: str, values: str, title: str = "") -> go.Figure:
        """Create interactive pie chart"""
        fig = px.pie(
            df,
            names=names,
            values=values,
            title=title,
            template="plotly_white"
        )
        fig.update_layout(height=500)
        return fig
    
    @staticmethod
    def create_scatter_plot(df: pd.DataFrame, x: str, y: str, title: str = "", color_col: Optional[str] = None) -> go.Figure:
        """Create interactive scatter plot"""
        fig = px.scatter(
            df,
            x=x,
            y=y,
            title=title,
            color=color_col,
            template="plotly_white"
        )
        fig.update_layout(
            height=400,
            hovermode='closest',
            xaxis_title=x,
            yaxis_title=y
        )
        return fig
    
    @staticmethod
    def create_histogram(df: pd.DataFrame, x: str, title: str = "", nbins: int = 30) -> go.Figure:
        """Create interactive histogram"""
        fig = px.histogram(
            df,
            x=x,
            title=title,
            nbins=nbins,
            color_discrete_sequence=["#1f77b4"],
            template="plotly_white"
        )
        fig.update_layout(height=400, xaxis_title=x, yaxis_title="Count")
        return fig
    
    @staticmethod
    def create_box_plot(df: pd.DataFrame, y: str, x: Optional[str] = None, title: str = "") -> go.Figure:
        """Create interactive box plot"""
        fig = px.box(
            df,
            y=y,
            x=x,
            title=title,
            template="plotly_white"
        )
        fig.update_layout(height=400, yaxis_title=y)
        return fig
    
    @staticmethod
    def create_heatmap(df: pd.DataFrame, title: str = "") -> go.Figure:
        """Create correlation heatmap"""
        numeric_df = df.select_dtypes(include=[np.number])
        corr_matrix = numeric_df.corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=np.round(corr_matrix.values, 2),
            texttemplate='%{text:.2f}',
            textfont={"size": 10},
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title=title or "Correlation Matrix",
            height=600,
            xaxis_title="Features",
            yaxis_title="Features"
        )
        return fig
    
    @staticmethod
    def create_kpi_card(label: str, value: str, change: Optional[str] = None, color: str = "#1f77b4") -> None:
        """Display KPI card in Streamlit"""
        col1, col2 = st.columns([3, 1])
        with col1:
            st.metric(label=label, value=value, delta=change)
    
    @staticmethod
    def create_summary_stats(df: pd.DataFrame) -> None:
        """Display summary statistics"""
        stats = df.describe().round(2)
        st.dataframe(stats, use_container_width=True)
    
    @staticmethod
    def create_multi_line_chart(df: pd.DataFrame, x: str, y_cols: List[str], title: str = "") -> go.Figure:
        """Create multi-line chart"""
        fig = go.Figure()
        
        for col in y_cols:
            fig.add_trace(go.Scatter(
                x=df[x],
                y=df[col],
                mode='lines+markers',
                name=col
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title=x,
            yaxis_title="Value",
            height=400,
            hovermode='x unified',
            template="plotly_white"
        )
        return fig
    
    @staticmethod
    def create_sunburst_chart(df: pd.DataFrame, labels: List[str], values: str, title: str = "") -> go.Figure:
        """Create sunburst chart for hierarchical data"""
        fig = px.sunburst(
            df,
            labels=labels[0],
            parents=labels[1] if len(labels) > 1 else None,
            values=values,
            title=title,
            template="plotly_white"
        )
        fig.update_layout(height=600)
        return fig
    
    @staticmethod
    def create_comparison_chart(df: pd.DataFrame, group_col: str, value_col: str, title: str = "") -> go.Figure:
        """Create grouped bar chart for comparison"""
        fig = px.bar(
            df,
            x=group_col,
            y=value_col,
            title=title,
            barmode='group',
            template="plotly_white"
        )
        fig.update_layout(
            height=400,
            xaxis_title=group_col,
            yaxis_title=value_col,
            hovermode='x unified'
        )
        return fig
