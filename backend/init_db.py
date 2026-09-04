import sys
import os

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.api.db_session import init_db

if __name__ == "__main__":
    print("Initializing SeismoDetect PostgreSQL database schema...")
    init_db()
    print("Database schema successfully initialized!")
