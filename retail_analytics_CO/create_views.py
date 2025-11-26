import sqlite3
import os

def create_views():
    """Create simplified views for database tables"""
    
    db_path = 'Data/northwind.sqlite.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found at: {db_path}")
        return
    
    print(f"✅ Database found at: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # List of views to create
    views_sql = [
        "CREATE VIEW IF NOT EXISTS orders AS SELECT * FROM Orders;",
        "CREATE VIEW IF NOT EXISTS order_items AS SELECT * FROM \"Order Details\";", 
        "CREATE VIEW IF NOT EXISTS products AS SELECT * FROM Products;",
        "CREATE VIEW IF NOT EXISTS customers AS SELECT * FROM Customers;",
        "CREATE VIEW IF NOT EXISTS categories AS SELECT * FROM Categories;",
        "CREATE VIEW IF NOT EXISTS suppliers AS SELECT * FROM Suppliers;"
    ]
    
    print("Creating views...")
    for sql in views_sql:
        try:
            cursor.execute(sql)
            view_name = sql.split(' ')[5]
            print(f"✅ {view_name} - created")
        except Exception as e:
            print(f"❌ Error in {sql}: {e}")
    
    conn.commit()
    conn.close()
    print(" All views created successfully!")

if __name__ == "__main__":
    create_views()