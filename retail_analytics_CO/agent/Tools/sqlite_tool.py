import sqlite3
import os
from typing import List, Dict, Any, Tuple

class SQLiteTool:
    def __init__(self, db_path: str = "Data/northwind.sqlite.db"):
        self.db_path = db_path
        
    def get_schema(self) -> Dict[str, List[str]]:
        """Get database schema information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        schema = {}
        for table in tables:
            try:
                # Handle tables with spaces in names
                if ' ' in table or '-' in table:
                    table_name = f'"{table}"'
                else:
                    table_name = table
                    
                # Get column info for each table
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [row[1] for row in cursor.fetchall()]
                schema[table] = columns
            except Exception as e:
                print(f"Warning: Could not get schema for {table}: {e}")
                schema[table] = []
        
        conn.close()
        return schema
    
    def get_views(self) -> List[str]:
        """Get available views"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view';")
        views = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return views
    
    def run_query(self, query: str) -> Dict[str, Any]:
        """Execute SQL query and return results"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Execute query
            cursor.execute(query)
            
            # Get results
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            
            conn.close()
            
            return {
                "success": True,
                "columns": columns,
                "rows": rows,
                "row_count": len(rows),
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "columns": [],
                "rows": [],
                "row_count": 0,
                "error": str(e)
            }
    
    def get_sample_data(self, table_name: str, limit: int = 3) -> Dict[str, Any]:
        """Get sample data from a table"""
        # Handle tables with spaces
        if ' ' in table_name or '-' in table_name:
            table_name = f'"{table_name}"'
            
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        return self.run_query(query)

# Test the SQL tool
if __name__ == "__main__":
    tool = SQLiteTool()
    
    print(" Database Schema:")
    schema = tool.get_schema()
    for table, columns in schema.items():
        print(f"  {table}: {columns}")
    
    print(f"\n Available Views: {tool.get_views()}")
    
    # Test queries using views (no spaces)
    test_queries = [
        "SELECT * FROM products LIMIT 2",
        "SELECT * FROM orders LIMIT 2", 
        "SELECT * FROM order_items LIMIT 2"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing: {query}")
        result = tool.run_query(query)
        
        if result["success"]:
            print("✅ Query successful!")
            print(f"Columns: {result['columns']}")
            print(f"Rows: {result['rows']}")
        else:
            print(f"❌ Query failed: {result['error']}")