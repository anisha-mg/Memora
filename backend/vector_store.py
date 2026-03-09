"""
Vector Store using FAISS for semantic search
"""
import os
import pickle
import numpy as np
from typing import List, Dict
import PyPDF2
from openai import OpenAI


class VectorStore:
    """
    FAISS-based vector store for semantic document search
    """
    
    def __init__(self, data_dir: str = "./data"):
        """
        Initialize vector store
        
        Args:
            data_dir: Directory containing data files
        """
        self.data_dir = data_dir
        self.embeddings = []
        self.documents = []
        self.index = None
        
        # Initialize OpenAI for embeddings
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️  OPENAI_API_KEY not set, vector search will be disabled")
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)
        
        # FAISS will be initialized when needed
        self.faiss_available = False
        try:
            import faiss
            self.faiss = faiss
            self.faiss_available = True
        except ImportError:
            print("⚠️  FAISS not installed, using fallback search")
    
    def initialize(self):
        """
        Initialize the vector store by loading and indexing all documents
        """
        if not self.client:
            print("⚠️  Vector store initialization skipped (no OpenAI API key)")
            return
        
        print("📚 Loading documents...")
        
        # Load documents from all sources
        self._load_emails()
        self._load_pdfs()
        self._load_csvs()
        
        if not self.documents:
            print("⚠️  No documents found to index")
            return
        
        print(f"📄 Loaded {len(self.documents)} document chunks")
        
        # Create embeddings
        print("🔄 Creating embeddings...")
        self._create_embeddings()
        
        # Build FAISS index
        if self.faiss_available and self.embeddings:
            print("🔍 Building FAISS index...")
            self._build_index()
            print("✅ Vector store initialized successfully!")
        else:
            print("✅ Vector store initialized (using fallback search)")
    
    def _load_emails(self):
        """Load and chunk email data"""
        email_path = os.path.join(self.data_dir, "emails.txt")
        if os.path.exists(email_path):
            with open(email_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split into email chunks (by subject lines or paragraphs)
            chunks = content.split('\n\n')
            for chunk in chunks:
                if chunk.strip():
                    self.documents.append({
                        "content": chunk.strip(),
                        "source": "emails",
                        "type": "email"
                    })
    
    def _load_pdfs(self):
        """Load and chunk PDF documents"""
        pdf_path = os.path.join(self.data_dir, "notes.pdf")
        if os.path.exists(pdf_path):
            try:
                with open(pdf_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    
                    for page_num, page in enumerate(pdf_reader.pages):
                        text = page.extract_text()
                        
                        # Split into paragraphs
                        paragraphs = text.split('\n\n')
                        for para in paragraphs:
                            if para.strip() and len(para.strip()) > 50:
                                self.documents.append({
                                    "content": para.strip(),
                                    "source": f"notes.pdf (page {page_num + 1})",
                                    "type": "pdf"
                                })
            except Exception as e:
                print(f"⚠️  Error loading PDF: {str(e)}")
    
    def _load_csvs(self):
        """Load CSV data"""
        events_path = os.path.join(self.data_dir, "events.csv")
        if os.path.exists(events_path):
            try:
                import pandas as pd
                df = pd.read_csv(events_path)
                
                # Convert each row to a text document
                for _, row in df.iterrows():
                    content = f"Event: {row['event']}, Date: {row['date']}, Time: {row['time']}"
                    self.documents.append({
                        "content": content,
                        "source": "events.csv",
                        "type": "csv"
                    })
            except Exception as e:
                print(f"⚠️  Error loading CSV: {str(e)}")
    
    def _create_embeddings(self):
        """Create embeddings for all documents"""
        if not self.client:
            return
        
        try:
            # Batch process embeddings
            texts = [doc["content"] for doc in self.documents]
            
            print(f"🔄 Creating embeddings for {len(texts)} documents...")
            
            # OpenAI embeddings API
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=texts
            )
            
            self.embeddings = [item.embedding for item in response.data]
            print(f"✅ Created {len(self.embeddings)} embeddings")
            
        except Exception as e:
            error_msg = str(e)
            if "insufficient_quota" in error_msg or "429" in error_msg:
                print(f"⚠️  OpenAI quota exceeded. Vector search will use fallback keyword search.")
                print(f"📝 Please check your OpenAI billing at: https://platform.openai.com/account/billing/overview")
            else:
                print(f"⚠️  Error creating embeddings: {error_msg}")
            self.embeddings = []
    
    def _build_index(self):
        """Build FAISS index from embeddings"""
        if not self.embeddings or not self.faiss_available:
            return
        
        try:
            # Convert to numpy array
            embeddings_array = np.array(self.embeddings).astype('float32')
            
            # Create FAISS index
            dimension = embeddings_array.shape[1]
            self.index = self.faiss.IndexFlatL2(dimension)
            self.index.add(embeddings_array)
            
        except Exception as e:
            print(f"⚠️  Error building FAISS index: {str(e)}")
            self.index = None
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Search for relevant documents
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of relevant documents
        """
        if not self.client or not self.documents:
            return self._fallback_search(query, top_k)
        
        try:
            # Create query embedding
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=[query]
            )
            query_embedding = np.array([response.data[0].embedding]).astype('float32')
            
            # Search using FAISS
            if self.index and self.faiss_available:
                distances, indices = self.index.search(query_embedding, top_k)
                
                results = []
                for idx in indices[0]:
                    if idx < len(self.documents):
                        results.append(self.documents[idx])
                
                return results
            else:
                # Fallback: simple keyword search
                return self._fallback_search(query, top_k)
                
        except Exception as e:
            error_msg = str(e)
            if "insufficient_quota" in error_msg or "429" in error_msg:
                print(f"⚠️  Switching to keyword search (OpenAI quota exceeded)")
            else:
                print(f"⚠️  Error during search: {str(e)}")
            return self._fallback_search(query, top_k)
    
    def _fallback_search(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Fallback keyword-based search
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of relevant documents
        """
        query_lower = query.lower()
        scored_docs = []
        
        for doc in self.documents:
            content_lower = doc["content"].lower()
            score = sum(1 for word in query_lower.split() if word in content_lower)
            if score > 0:
                scored_docs.append((score, doc))
        
        # Sort by score and return top_k
        scored_docs.sort(reverse=True, key=lambda x: x[0])
        return [doc for score, doc in scored_docs[:top_k]]
    
    def get_document_count(self) -> int:
        """Return the number of documents indexed"""
        return len(self.documents)
    
    def save(self, filepath: str = "vector_store.pkl"):
        """Save the vector store to disk"""
        try:
            data = {
                "documents": self.documents,
                "embeddings": self.embeddings
            }
            with open(filepath, 'wb') as f:
                pickle.dump(data, f)
            print(f"✅ Vector store saved to {filepath}")
        except Exception as e:
            print(f"⚠️  Error saving vector store: {str(e)}")
    
    def load(self, filepath: str = "vector_store.pkl"):
        """Load the vector store from disk"""
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            
            self.documents = data["documents"]
            self.embeddings = data["embeddings"]
            
            if self.embeddings and self.faiss_available:
                self._build_index()
            
            print(f"✅ Vector store loaded from {filepath}")
        except Exception as e:
            print(f"⚠️  Error loading vector store: {str(e)}")
