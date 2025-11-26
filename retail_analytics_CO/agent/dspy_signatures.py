import dspy
from typing import List, Optional

# Initialize DSPy with local model (we'll set this up later)
# For now, we'll create the signature classes

class RouteQuery(dspy.Signature):
    """Classify whether a query needs RAG, SQL, or both"""
    question: str = dspy.InputField(desc="The user's question")
    route: str = dspy.OutputField(desc="One of: 'rag', 'sql', 'hybrid'")

class GenerateSQL(dspy.Signature):
    """Generate SQL query from natural language"""
    question: str = dspy.InputField(desc="The user's question about data")
    schema: str = dspy.InputField(desc="Relevant database schema information")
    sql_query: str = dspy.OutputField(desc="SQL query to answer the question")

class ExtractConstraints(dspy.Signature):
    """Extract constraints and parameters from the question"""
    question: str = dspy.InputField(desc="The user's question")
    context: str = dspy.InputField(desc="Relevant document context")
    date_ranges: List[str] = dspy.OutputField(desc="Date ranges mentioned")
    kpi_formulas: List[str] = dspy.OutputField(desc="KPI formulas needed")
    categories: List[str] = dspy.OutputField(desc="Product categories mentioned")
    entities: List[str] = dspy.OutputField(desc="Other entities mentioned")

class SynthesizeAnswer(dspy.Signature):
    """Synthesize final answer from SQL results and document context"""
    question: str = dspy.InputField(desc="The original question")
    sql_results: str = dspy.InputField(desc="Results from SQL query")
    document_context: str = dspy.InputField(desc="Relevant document chunks")
    format_hint: str = dspy.InputField(desc="Expected output format")
    final_answer: str = dspy.OutputField(desc="Formatted final answer")
    explanation: str = dspy.OutputField(desc="Brief explanation of the answer")
    citations: List[str] = dspy.OutputField(desc="List of sources used")

# DSPy Modules
class QueryRouter(dspy.Module):
    def __init__(self):
        super().__init__()
        self.route = dspy.Predict(RouteQuery)
    
    def forward(self, question):
        return self.route(question=question)

class SQLGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate_sql = dspy.Predict(GenerateSQL)
    
    def forward(self, question, schema):
        return self.generate_sql(question=question, schema=schema)

class AnswerSynthesizer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.synthesize = dspy.Predict(SynthesizeAnswer)
    
    def forward(self, question, sql_results, document_context, format_hint):
        return self.synthesize(
            question=question,
            sql_results=sql_results,
            document_context=document_context,
            format_hint=format_hint
        )

# Test the signatures
if __name__ == "__main__":
    print("✅ DSPy signatures created successfully!")
    print("Available signatures:")
    print("  - RouteQuery: Classifies query type")
    print("  - GenerateSQL: Creates SQL from natural language") 
    print("  - ExtractConstraints: Extracts parameters from question")
    print("  - SynthesizeAnswer: Creates final answer with citations")
    
    print("\nAvailable modules:")
    print("  - QueryRouter")
    print("  - SQLGenerator")
    print("  - AnswerSynthesizer")