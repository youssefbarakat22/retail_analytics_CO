# Retail Analytics Copilot

AI agent for retail analytics using RAG + SQL with DSPy optimization.

##  Results Summary

**Batch Processing Results:**
- ✅ 6/6 questions processed successfully
- ✅ 4/6 questions with specific, accurate answers  
- ✅ All SQL queries executed successfully
- ✅ Proper citations for all answers

**Sample Answers:**
- Return policy: "14" (RAG-only)
- Top products: "[{'product': 'Côte de Blaye', 'revenue': 53265895.24}, ...]" (SQL)
- AOV Winter 1997: "1452.75" (Hybrid)
- Beverages revenue: "45236.75" (Hybrid)

##  Architecture

- **6-Node LangGraph**: Route → Retrieve → Generate SQL → Execute → Synthesize → Repair
- **RAG**: Keyword-based document retrieval
- **SQL**: SQLite with Northwind database
- **DSPy**: Optimized SQL generator module

##  Usage

```bash
# Single question
python run_agent_hybrid.py --question "What are the top products by revenue?"

# Batch processing (official)
python run_agent_hybrid.py --batch sample_questions_hybrid_eval.jsonl --out outputs_hybrid.jsonl