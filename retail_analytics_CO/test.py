import os

print("🔍 Testing document retrieval...")

# Check if Docs folder exists
if not os.path.exists("Docs"):
    print("❌ Docs folder not found!")
    print("Current directory:", os.getcwd())
    print("Files in current directory:", os.listdir("."))
else:
    print("✅ Docs folder found!")
    files = os.listdir("Docs")
    print(f"Files in Docs: {files}")
    
    # Test reading a file
    if files:
        first_file = os.path.join("Docs", files[0])
        try:
            with open(first_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"✅ Successfully read {files[0]}")
            print(f"First 200 chars: {content[:200]}...")
        except Exception as e:
            print(f"❌ Error reading file: {e}")

print("Test completed!")