"""
RAG Engine (Retrieval-Augmented Generation) - Semantic Version
Role: Store and retrieve relevant "experience snippets" using semantic vector embeddings.
"""

import os
import json
import logging
import numpy as np
import google.generativeai as genai
from typing import List, Dict, Any, Optional

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGEngine:
    """
    A Vector-based Retrieval Engine that uses Google's embeddings 
    to retrieve the most semantically relevant experience snippets.
    """

    def __init__(self, profile_path: str = "data/master_profile.json", api_key: Optional[str] = None):
        self.profile_path = profile_path
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.snippets = []
        self.embeddings = [] # Store as list, convert to np array for search
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = "models/text-embedding-004"
        else:
            logger.warning("⚠️ GOOGLE_API_KEY not found. RAG will fall back to keyword matching.")
            self.model = None

        self._initialize_snippets()

    def _initialize_snippets(self):
        """Parse the profile and generate embeddings for snippets."""
        try:
            if not os.path.exists(self.profile_path):
                logger.error(f"❌ Profile file not found: {self.profile_path}")
                return

            with open(self.profile_path, 'r', encoding='utf-8') as f:
                profile = json.load(f)
            
            # 1. Standardize Experience Snippets
            for role in profile.get('experience', []):
                company = role.get('company', 'Unknown')
                title = role.get('title', 'Position')
                
                # Create a snippet for each achievement
                items = role.get('achievements', role.get('responsibilities', []))
                for ach in items:
                    self.snippets.append({
                        "content": f"At {company} as {title}: {ach}",
                        "metadata": {
                            "type": "experience",
                            "company": company,
                            "title": title
                        }
                    })
            
            # 2. Project Snippets
            for project in profile.get('projects', []):
                self.snippets.append({
                    "content": f"Project {project.get('name')}: {project.get('description')}",
                    "metadata": {"type": "project", "name": project.get('name')}
                })
            
            # 3. Generate Embeddings (if API key available)
            if self.model and self.snippets:
                logger.info(f"🧠 RAG: Generating semantic embeddings for {len(self.snippets)} snippets...")
                texts = [s["content"] for s in self.snippets]
                
                # Batch embed for efficiency
                response = genai.embed_content(
                    model=self.model,
                    content=texts,
                    task_type="retrieval_document"
                )
                self.embeddings = np.array(response['embedding'])
                logger.info("✅ RAG: Semantic Index initialized successfully.")
            
        except Exception as e:
            logger.error(f"⚠️ RAG Initialization failed: {e}")

    def retrieve_relevant_experience(self, job_query: str, top_k: int = 15) -> List[Dict[str, Any]]:
        """
        Retrieve segments that are semantically relevant to the job query.
        Falls back to keyword matching if embeddings are not available.
        """
        if not self.snippets:
            return []

        # Use semantic search if embeddings exist
        if len(self.embeddings) > 0:
            try:
                # Embed the query
                query_response = genai.embed_content(
                    model=self.model,
                    content=job_query,
                    task_type="retrieval_query"
                )
                query_vec = np.array(query_response['embedding'])

                # Vector Cosine Similarity (dot product since embeddings are normalized)
                scores = np.dot(self.embeddings, query_vec)
                
                # Get top K indices
                top_indices = np.argsort(scores)[::-1][:top_k]
                
                results = [self.snippets[i] for i in top_indices]
                logger.info(f"🎯 RAG: Retrieved {len(results)} semantically relevant snippets.")
                return results
                
            except Exception as e:
                logger.error(f"❌ Semantic search failed: {e}. Falling back to keyword search.")

        # Fallback: Basic Keyword Matching (BM25 Lite)
        scored_snippets = []
        words = job_query.lower().split()
        
        for snippet in self.snippets:
            score = sum(1 for word in words if word in snippet['content'].lower())
            if score > 0:
                scored_snippets.append((score, snippet))
        
        scored_snippets.sort(key=lambda x: x[0], reverse=True)
        results = [s[1] for s in scored_snippets[:top_k]]
        logger.info(f"🎯 RAG: Retrieved {len(results)} snippets via keyword fallback.")
        return results
