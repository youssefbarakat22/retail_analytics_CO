#!/usr/bin/env python3
"""
Retail Analytics Copilot - Main Entry Point
"""

import json
import sys
import os
from typing import List, Dict, Any

# Add agent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agent'))

from agent.graph_simple import SimpleHybridAgent

def process_batch_questions(input_file: str, output_file: str):
    """Process a batch of questions from JSONL file"""
    print(f" Processing batch: {input_file}")
    
    agent = SimpleHybridAgent()
    results = []
    
    # Read questions from file
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    question_data = json.loads(line.strip())
                    question_id = question_data.get('id', 'unknown')
                    question = question_data.get('question', '')
                    format_hint = question_data.get('format_hint', 'text')
                    
                    print(f"\n Processing: {question_id}")
                    print(f"   Question: {question}")
                    
                    # Process the question
                    result = agent.run(question)
                    
                    # Prepare output according to contract
                    output = {
                        "id": question_id,
                        "final_answer": result["final_answer"],
                        "sql": result["sql"],
                        "confidence": result["confidence"],
                        "explanation": result["explanation"],
                        "citations": result["citations"]
                    }
                    
                    results.append(output)
                    print(f"   ✅ Completed: {question_id}")
                    
                except Exception as e:
                    print(f"   ❌ Error processing question: {e}")
                    # Add error result
                    results.append({
                        "id": question_data.get('id', 'unknown'),
                        "final_answer": f"Error: {str(e)}",
                        "sql": "",
                        "confidence": 0.0,
                        "explanation": "Processing failed",
                        "citations": []
                    })
    
    # Write results to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(json.dumps(result) + '\n')
    
    print(f"\n Batch processing complete!")
    print(f"   Input: {input_file}")
    print(f"   Output: {output_file}")
    print(f"   Processed: {len(results)} questions")

def process_single_question(question: str):
    """Process a single question interactively"""
    print(f" Processing: {question}")
    
    agent = SimpleHybridAgent()
    result = agent.run(question)
    
    print(f"\n Result:")
    print(f"Question: {result['question']}")
    print(f"Answer: {result['final_answer']}")
    print(f"SQL: {result['sql'][:100] if result['sql'] else 'None'}...")
    print(f"Confidence: {result['confidence']:.2f}")
    print(f"Citations: {result['citations']}")

def main():
    """Main CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Retail Analytics Copilot')
    parser.add_argument('--batch', type=str, help='Input JSONL file with questions')
    parser.add_argument('--out', type=str, help='Output JSONL file for results')
    parser.add_argument('--question', type=str, help='Single question to process')
    
    args = parser.parse_args()
    
    if args.batch and args.out:
        # Batch processing mode
        process_batch_questions(args.batch, args.out)
    elif args.question:
        # Single question mode
        process_single_question(args.question)
    else:
        # Interactive mode
        print(" Retail Analytics Copilot")
        print("Usage:")
        print("  --batch <input.jsonl> --out <output.jsonl>  # Process batch of questions")
        print("  --question \"Your question here\"            # Process single question")
        print("\nExamples:")
        print("  python run_agent_hybrid.py --batch sample_questions.jsonl --out results.jsonl")
        print("  python run_agent_hybrid.py --question \"What are the top products by revenue?\"")
        
        # Demo with a sample question
        print("\n Demo:")
        process_single_question("What is the return policy for beverages?")

if __name__ == "__main__":
    main()