import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
import streamlit as st

class DataProcessor:
    """Handle data loading, cleaning, and analysis"""
    
    def __init__(self):
        self.df = None
        self.original_df = None
        
    def load_file(self, uploaded_file) -> bool:
        """Load CSV or Excel file"""
        try:
            if uploaded_file.name.endswith('.csv'):
                self.df = pd.read_csv(uploaded_file)
            else:
                self.df = pd.read_excel(uploaded_file)
            
            self.original_df = self.df.copy()
            return True
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            return False
    
    def get_basic_info(self) -> Dict[str, Any]:
        """Get basic information about the dataset"""
        if self.df is None:
            return {}
        
        return {
            "shape": self.df.shape,
            "columns": list(self.df.columns),
            "data_types": dict(self.df.dtypes),
            "missing_values": dict(self.df.isnull().sum()),
            "memory_usage": self.df.memory_usage(deep=True).sum() / 1024**2  # MB
        }
    
    def get_statistical_summary(self) -> pd.DataFrame:
        """Get statistical summary of numeric columns"""
        if self.df is None:
            return pd.DataFrame()
        
        return self.df.describe().round(2)
    
    def get_missing_data_report(self) -> Dict[str, Any]:
        """Generate missing data report"""
        if self.df is None:
            return {}
        
        missing = self.df.isnull().sum()
        missing_percent = (missing / len(self.df)) * 100
        
        missing_df = pd.DataFrame({
            'Column': self.df.columns,
            'Missing_Count': missing.values,
            'Percentage': missing_percent.values
        }).sort_values('Missing_Count', ascending=False)
        
        return missing_df[missing_df['Missing_Count'] > 0]
    
    def clean_data(self, strategy: str = "drop") -> bool:
        """Clean dataset by handling missing values"""
        try:
            if strategy == "drop":
                self.df = self.df.dropna()
            elif strategy == "fill_mean":
                numeric_cols = self.df.select_dtypes(include=[np.number]).columns
                self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].mean())
            elif strategy == "fill_forward":
                self.df = self.df.fillna(method='ffill')
            
            return True
        except Exception as e:
            st.error(f"Error cleaning data: {str(e)}")
            return False
    
    def get_numeric_columns(self) -> List[str]:
        """Get list of numeric columns"""
        if self.df is None:
            return []
        return self.df.select_dtypes(include=[np.number]).columns.tolist()
    
    def get_categorical_columns(self) -> List[str]:
        """Get list of categorical columns"""
        if self.df is None:
            return []
        return self.df.select_dtypes(include=['object']).columns.tolist()
    
    def calculate_correlations(self) -> pd.DataFrame:
        """Calculate correlation matrix for numeric columns"""
        if self.df is None:
            return pd.DataFrame()
        
        numeric_df = self.df.select_dtypes(include=[np.number])
        return numeric_df.corr().round(2)
    
    def get_outliers(self, column: str, method: str = "iqr") -> List[int]:
        """Detect outliers using IQR or Z-score method"""
        if column not in self.df.columns:
            return []
        
        if method == "iqr":
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            outliers = self.df[(self.df[column] < Q1 - 1.5*IQR) | (self.df[column] > Q3 + 1.5*IQR)].index.tolist()
        else:  # z-score
            z_scores = np.abs((self.df[column] - self.df[column].mean()) / self.df[column].std())
            outliers = self.df[z_scores > 3].index.tolist()
        
        return outliers
    
    def get_top_values(self, column: str, top_n: int = 10) -> pd.Series:
        """Get top N values for a column"""
        if column not in self.df.columns:
            return pd.Series()
        
        return self.df[column].value_counts().head(top_n)
    
    def get_data_sample(self, n: int = 5) -> pd.DataFrame:
        """Get sample of data"""
        if self.df is None:
            return pd.DataFrame()
        
        return self.df.head(n)
    
    def export_data(self, filename: str = "processed_data.csv") -> bytes:
        """Export processed data to CSV"""
        if self.df is None:
            return b""
        
        return self.df.to_csv(index=False).encode()
    
    def get_insights(self) -> List[str]:
        """Generate automatic insights from data"""
        insights = []
        
        if self.df is None:
            return insights
        
        # Check for missing data
        missing_pct = (self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))) * 100
        if missing_pct > 0:
            insights.append(f"⚠️ Dataset contains {missing_pct:.1f}% missing values. Consider data cleaning.")
        
        # Numeric columns analysis
        numeric_cols = self.get_numeric_columns()
        if numeric_cols:
            for col in numeric_cols:
                skewness = self.df[col].skew()
                if abs(skewness) > 1:
                    insights.append(f"📊 Column '{col}' shows significant skewness ({skewness:.2f})")
        
        # Categorical analysis
        categorical_cols = self.get_categorical_columns()
        if categorical_cols:
            for col in categorical_cols:
                unique_count = self.df[col].nunique()
                insights.append(f"🏷️ Column '{col}' has {unique_count} unique values")
        
        # Data quality
        if len(self.df) > 10000:
            insights.append(f"📈 Large dataset detected: {len(self.df):,} rows. Consider sampling for visualization.")
        
        return insights
