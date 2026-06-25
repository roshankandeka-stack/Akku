import json
from typing import List, Dict, Optional

import pandas as pd
from openai import OpenAI

from config import DEFAULT_LLM_MODEL, GROQ_API_KEY


class DataChatbot:
    """Conversational AI for data analysis."""

    def __init__(self, api_key: str = None, model: str = DEFAULT_LLM_MODEL):

        self.api_key = api_key or GROQ_API_KEY
        self.model = model

        self.conversation_history: List[Dict] = []

        self.client: Optional[OpenAI] = None
        self.openai_available = False
        self.openai_error: Optional[str] = None

        try:
            if self.api_key:

                # GROQ CLIENT
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://api.groq.com/openai/v1",
                )

                self.openai_available = True

            else:
                self.openai_error = "GROQ API key not configured."

        except Exception as e:
            self.openai_error = str(e)

    def is_api_configured(self) -> bool:
        return bool(
            self.api_key and
            self.client and
            self.openai_available
        )

    def analyze_dataframe(self, df: pd.DataFrame, user_query: str) -> str:

        try:

            df = df.copy()
            df.columns = df.columns.str.strip()

            dataset_info = {
                "shape": df.shape,
                "columns": df.columns.tolist(),

                "dtypes": {
                    col: str(dtype)
                    for col, dtype in df.dtypes.items()
                },

                # SMALL SAMPLE ONLY
                "sample": df.head(3).astype(str).to_dict(orient="records"),

                # SAFE STRING VERSION
                "describe": str(
                    df.describe(include="all").fillna("")
                ),

                "null_counts": {
                    col: int(count)
                    for col, count in df.isnull().sum().items()
                },
            }

            context_message = f"""
You are an expert data analyst.

Dataset Shape:
{dataset_info['shape']}

Columns:
{', '.join(dataset_info['columns'])}

Data Types:
{json.dumps(dataset_info['dtypes'], indent=2)}

Sample Rows:
{json.dumps(dataset_info['sample'], indent=2)}

Summary Statistics:
{dataset_info['describe']}

Missing Values:
{json.dumps(dataset_info['null_counts'], indent=2)}

User Question:
{user_query}

IMPORTANT:
- Answer ONLY from dataset
- Do NOT hallucinate
- If information is missing, clearly say so
- Keep answer concise and analytical
"""

            if not self.is_api_configured():
                return (
                    "GROQ API key is not configured "
                    "or client unavailable."
                )

            completion = self.client.chat.completions.create(
                model=self.model,

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a professional AI "
                            "data analyst."
                        ),
                    },
                    {
                        "role": "user",
                        "content": context_message,
                    },
                ],

                temperature=0.2,
                max_tokens=500,
            )

            assistant_response = (
                completion.choices[0].message.content
            )

            self.conversation_history.append(
                {
                    "role": "user",
                    "content": user_query,
                }
            )

            self.conversation_history.append(
                {
                    "role": "assistant",
                    "content": assistant_response,
                }
            )

            return assistant_response

        except Exception as e:
            return f"Error analyzing data: {str(e)}"

    def get_visualization_suggestion(
        self,
        df: pd.DataFrame,
        columns: List[str]
    ) -> str:

        if not self.is_api_configured():
            return "GROQ API key not configured."

        try:

            prompt = f"""
Dataset Columns:
{columns}

Suggest best chart types for this dataset.
Explain briefly why.
"""

            completion = self.client.chat.completions.create(
                model=self.model,

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a data visualization expert."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],

                temperature=0.5,
                max_tokens=300,
            )

            return completion.choices[0].message.content

        except Exception as e:
            return f"Visualization suggestion error: {str(e)}"

    def generate_insights(self, df: pd.DataFrame) -> List[str]:

        if not self.is_api_configured():
            return ["GROQ API key not configured."]

        try:

            numeric_cols = list(
                df.select_dtypes(include=["number"]).columns
            )

            categorical_cols = list(
                df.select_dtypes(include=["object"]).columns
            )

            correlation_text = "No numeric columns available."

            if len(numeric_cols) > 1:
                correlation_text = (
                    df[numeric_cols]
                    .corr()
                    .round(2)
                    .to_string()
                )

            insights_prompt = f"""
Analyze this dataset and generate 5 insights.

Dataset Shape:
{df.shape}

Numeric Columns:
{numeric_cols}

Categorical Columns:
{categorical_cols}

Correlation Matrix:
{correlation_text}

Provide concise insights only.
"""

            completion = self.client.chat.completions.create(
                model=self.model,

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert data analyst."
                        ),
                    },
                    {
                        "role": "user",
                        "content": insights_prompt,
                    },
                ],

                temperature=0.5,
                max_tokens=500,
            )

            insights_text = (
                completion.choices[0].message.content or ""
            )

            insights = [
                line.strip("-• \t")
                for line in insights_text.splitlines()
                if line.strip()
            ]

            return insights[:5]

        except Exception as e:
            return [f"Insight generation error: {str(e)}"]

    def get_recommendations(
        self,
        df: pd.DataFrame,
        query: str
    ) -> str:

        if not self.is_api_configured():
            return "GROQ API key not configured."

        try:

            recommendation_prompt = f"""
Dataset Shape:
{df.shape}

Columns:
{', '.join(df.columns)}

User Query:
{query}

Provide actionable recommendations.
"""

            completion = self.client.chat.completions.create(
                model=self.model,

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a business analyst."
                        ),
                    },
                    {
                        "role": "user",
                        "content": recommendation_prompt,
                    },
                ],

                temperature=0.5,
                max_tokens=500,
            )

            return completion.choices[0].message.content

        except Exception as e:
            return f"Recommendation error: {str(e)}"

    def get_conversation_history(self) -> List[Dict]:
        return self.conversation_history

    def clear_history(self) -> None:
        self.conversation_history = []


class InsightGenerator:
    """Generate formatted insights."""

    @staticmethod
    def generate_summary(
        df: pd.DataFrame,
        title: str = ""
    ) -> str:

        try:

            summary = f"""
==================================================
DATASET SUMMARY: {title}
==================================================

Dataset Dimensions:
{df.shape[0]} rows × {df.shape[1]} columns

Column Information:
{df.dtypes.to_string()}

Missing Values:
{df.isnull().sum().sum()}

Complete Rows:
{len(df) - df.isnull().any(axis=1).sum()}

Statistics:
{df.describe(include='all').fillna('').to_string()}

==================================================
"""

            return summary

        except Exception as e:
            return f"Summary generation error: {str(e)}"

    @staticmethod
    def format_insights(insights: List[str]) -> str:

        formatted = "### Key Insights\n\n"

        for i, insight in enumerate(insights, 1):
            formatted += f"{i}. {insight}\n\n"

        return formatted

