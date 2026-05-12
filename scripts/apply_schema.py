import os
import sqlalchemy
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("Error: DATABASE_URL not found in .env")
    exit(1)

# Ensure the URL is in a format SQLAlchemy likes
if DATABASE_URL.startswith("postgresql://") and not DATABASE_URL.startswith("postgresql://postgres"):
    # This might be needed for some SQLAlchemy versions if the driver isn't specified
    # but standard postgresql:// usually works if psycopg2 is installed.
    pass

engine = sqlalchemy.create_engine(DATABASE_URL)

def apply_schema():
    schema_file = os.path.join(os.path.dirname(__file__), 'supabase_schema.sql')
    
    if not os.path.exists(schema_file):
        print(f"Error: {schema_file} not found")
        return

    with open(schema_file, 'r') as f:
        sql = f.read()

    print("Connecting to Supabase...")
    with engine.connect() as conn:
        print("Applying schema...")
        # Split by semicolon to execute individual statements if needed,
        # but SQLAlchemy's execute can often handle blocks if the driver supports it.
        # For Supabase/Postgres, we can usually execute the whole block or use a transaction.
        transaction = conn.begin()
        try:
            # We use text() to wrap the raw SQL
            conn.execute(text(sql))
            transaction.commit()
            print("Successfully refined the database schema in Supabase.")
        except Exception as e:
            transaction.rollback()
            print(f"Failed to apply schema: {e}")

if __name__ == "__main__":
    apply_schema()
