import os
import pickle
from typing import List, Dict, Tuple

import numpy as np
import streamlit as st

try:
    from sentence_transformers import SentenceTransformer
    _sentence_transformers_available = True
except ImportError as e:
    SentenceTransformer = None
    _sentence_transformers_available = False
    _sentence_transformers_error = str(e)

try:
    import faiss
    _faiss_available = True
except ImportError as e:
    faiss = None
    _faiss_available = False
    _faiss_error = str(e)


class RAGSystem:
    """Retrieval Augmented Generation system for customer support."""

    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2"):
        self.embedding_model_name = embedding_model
        self.embedding_model = None
        self.knowledge_base: List[Dict] = []
        self.index = None
        self.embeddings = None
        self.db_path = "faiss_index"
        self.initialization_error = None

        if not _sentence_transformers_available:
            self.initialization_error = (
                f"SentenceTransformers not installed: {_sentence_transformers_error}"
            )
            st.warning(self.initialization_error)
        elif not _faiss_available:
            self.initialization_error = f"FAISS not installed: {_faiss_error}"
            st.warning(self.initialization_error)
        else:
            try:
                self.embedding_model = SentenceTransformer(self.embedding_model_name)
            except Exception as e:
                self.initialization_error = str(e)
                st.error(f"Error initializing embedding model: {self.initialization_error}")

    def add_document(self, doc_id: str, content: str, metadata: Dict = None) -> None:
        self.knowledge_base.append(
            {
                "id": doc_id,
                "content": content,
                "metadata": metadata or {},
            }
        )

    def add_faq(self, question: str, answer: str) -> None:
        self.add_document(
            doc_id=f"faq_{len(self.knowledge_base)}",
            content=f"Q: {question}\nA: {answer}",
            metadata={"type": "faq", "question": question},
        )

    def build_index(self) -> bool:
        try:
            if not self.knowledge_base:
                return False
            if self.embedding_model is None:
                st.error("Cannot build index: Embedding model is unavailable.")
                return False

            texts = [doc["content"] for doc in self.knowledge_base]
            self.embeddings = self.embedding_model.encode(texts, convert_to_numpy=True)

            dimension = self.embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(self.embeddings)
            return True
        except Exception as e:
            st.error(f"Error building index: {str(e)}")
            return False

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        try:
            if self.index is None or len(self.knowledge_base) == 0:
                return []
            if self.embedding_model is None:
                st.error("Cannot retrieve documents: Embedding model is unavailable.")
                return []

            query_embedding = self.embedding_model.encode(query, convert_to_numpy=True)
            query_embedding = query_embedding.reshape(1, -1).astype(np.float32)

            distances, indices = self.index.search(
                query_embedding, min(top_k, len(self.knowledge_base))
            )

            results: List[Dict] = []
            for idx_pos in range(indices.shape[1]):
                idx = int(indices[0][idx_pos])
                if 0 <= idx < len(self.knowledge_base):
                    doc = self.knowledge_base[idx]
                    dist = float(distances[0][idx_pos])
                    relevance = float(1 / (1 + dist))
                    results.append(
                        {
                            "id": doc["id"],
                            "content": doc["content"],
                            "metadata": doc["metadata"],
                            "relevance_score": relevance,
                        }
                    )

            return results
        except Exception as e:
            st.error(f"Error in retrieval: {str(e)}")
            return []

    def generate_response(self, query: str, context: List[Dict], llm_response: str = "") -> str:
        """Return an answer using retrieved content.

        The original implementation returned a prompt template, which makes the
        Streamlit UI show "prompts" instead of an actual answer.

        This method deterministically extracts the best answer from the top
        retrieved document:
        - For FAQs: extract the `A:` portion
        - Otherwise: return the top document content
        """
        if not context:
            return (
                "I couldn't find relevant information to answer your question. "
                "Please try rephrasing or contact support."
            )

        top = context[0]
        doc_type = top.get("metadata", {}).get("type", "document")
        content = (top.get("content") or "").strip()

        if doc_type == "faq":
            lines = content.splitlines()
            answer_lines: List[str] = []
            in_a = False
            for line in lines:
                s = line.strip()
                if s.startswith("A:"):
                    in_a = True
                    answer_lines.append(s[2:].strip())
                    continue
                if in_a:
                    if s.startswith("Q:"):
                        break
                    if s:
                        answer_lines.append(s)

            extracted = " ".join([x for x in answer_lines if x]).strip()
            if extracted:
                return extracted

        return content

    def save_index(self, path: str = None) -> bool:
        try:
            path = path or self.db_path
            os.makedirs(path, exist_ok=True)

            if self.index is not None:
                faiss.write_index(self.index, os.path.join(path, "faiss.index"))

            with open(os.path.join(path, "kb.pkl"), "wb") as f:
                pickle.dump(self.knowledge_base, f)

            with open(os.path.join(path, "embeddings.npy"), "wb") as f:
                np.save(f, self.embeddings)

            return True
        except Exception as e:
            st.error(f"Error saving index: {str(e)}")
            return False

    def load_index(self, path: str = None) -> bool:
        try:
            path = path or self.db_path
            if not os.path.exists(path):
                return False

            self.index = faiss.read_index(os.path.join(path, "faiss.index"))

            with open(os.path.join(path, "kb.pkl"), "rb") as f:
                self.knowledge_base = pickle.load(f)

            with open(os.path.join(path, "embeddings.npy"), "rb") as f:
                self.embeddings = np.load(f)

            return True
        except Exception as e:
            st.error(f"Error loading index: {str(e)}")
            return False

    def get_knowledge_base_size(self) -> int:
        return len(self.knowledge_base)

    def list_documents(self) -> List[Dict]:
        return [
            {
                "id": doc["id"],
                "type": doc["metadata"].get("type", "document"),
                "preview": (doc["content"] or "")[:100],
            }
            for doc in self.knowledge_base
        ]


class CustomerSupportBot:
    """Customer support bot using RAG."""

    def __init__(self, rag_system: RAGSystem):
        self.rag = rag_system
        self.conversation_history: List[Dict] = []

    def process_query(self, user_query: str) -> Tuple[str, List[Dict]]:
        retrieved_docs = self.rag.retrieve(user_query, top_k=3)
        response = self.rag.generate_response(user_query, retrieved_docs)

        self.conversation_history.append(
            {
                "query": user_query,
                "response": response,
                "sources": retrieved_docs,
            }
        )

        return response, retrieved_docs

    def get_conversation_history(self) -> List[Dict]:
        return self.conversation_history

    def clear_history(self) -> None:
        self.conversation_history = []

    def get_top_faqs(self, limit: int = 5) -> List[Dict]:
        return [
            doc
            for doc in self.rag.knowledge_base
            if doc["metadata"].get("type") == "faq"
        ][:limit]

