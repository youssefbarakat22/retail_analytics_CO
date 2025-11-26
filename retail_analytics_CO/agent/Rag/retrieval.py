import os
import re
from typing import List, Dict

class SimpleRetriever:
    def __init__(self, docs_folder: str = "Docs"):
        self.docs_folder = docs_folder
        self.chunks = []
        self.chunk_info = []
        
    def load_documents(self):
        """Load and chunk all documents"""
        print("Loading documents...")
        
        # Get all markdown files
        md_files = [f for f in os.listdir(self.docs_folder) if f.endswith('.md') or f.endswith('.txt')]
        
        for file_name in md_files:
            file_path = os.path.join(self.docs_folder, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Split content into chunks (paragraphs)
                paragraphs = self._split_into_chunks(content)
                
                for i, paragraph in enumerate(paragraphs):
                    if paragraph.strip():
                        self.chunks.append(paragraph.strip())
                        self.chunk_info.append({
                            'source': file_name.replace('.txt', ''),
                            'chunk_id': f"{file_name.replace('.txt', '')}::chunk{i}",
                            'content': paragraph.strip()
                        })
            except Exception as e:
                print(f"Error loading {file_name}: {e}")
        
        print(f"✅ Loaded {len(self.chunks)} chunks from {len(md_files)} files")
    
    def _split_into_chunks(self, text: str) -> List[str]:
        """Split text into chunks (paragraphs)"""
        chunks = re.split(r'\n\s*\n|#+ ', text)
        return [chunk.strip() for chunk in chunks if chunk.strip()]
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search for relevant chunks using keyword matching"""
        if not self.chunks:
            self.load_documents()
        
        query_words = query.lower().split()
        results = []
        
        for i, chunk in enumerate(self.chunks):
            chunk_lower = chunk.lower()
            score = 0
            
            # Simple scoring: count matching words
            for word in query_words:
                if len(word) > 2 and word in chunk_lower:  # Only words longer than 2 chars
                    score += 1
            
            if score > 0:
                results.append({
                    **self.chunk_info[i],
                    'score': score
                })
        
        # Sort by score and return top-k
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]

# Test the retriever
if __name__ == "__main__":
    retriever = SimpleRetriever()
    
    # Test different searches
    test_queries = [
        "beverages return policy",
        "summer beverages 1997", 
        "average order value",
        "gross margin definition"
    ]
    
    for query in test_queries:
        print(f"\n Searching: '{query}'")
        results = retriever.search(query)
        
        if results:
            print(f"✅ Found {len(results)} results:")
            for i, result in enumerate(results):
                print(f"   {i+1}. {result['chunk_id']} (score: {result['score']})")
                print(f"      {result['content'][:80]}...")
        else:
            print("❌ No results found")