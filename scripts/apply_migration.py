#!/usr/bin/env python3
"""
apply_migration.py — Applies scripts/migrate.sql to the Supabase PostgreSQL instance.
Uses psycopg2's execute() to run the whole file at once, which handles dollar-quoting correctly.
"""
import os, sys
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("[ERROR] DATABASE_URL not set. Check your .env file.")
    sys.exit(1)

SCRIPT = os.path.join(os.path.dirname(__file__), "migrate.sql")
ALTER_SCRIPT = os.path.join(os.path.dirname(__file__), "alter_existing.sql")

def run_file(conn, path, label):
    print(f"[INFO] Running {label}...")
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
        print(f"[OK] {label} completed successfully.")
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] {label} failed:\n  {e}")
        return False
    return True


print("[INFO] Connecting to Supabase...")
try:
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    print("[OK] Connected.")
except Exception as e:
    print(f"[ERROR] Connection failed: {e}")
    sys.exit(1)

ok1 = run_file(conn, SCRIPT, "migrate.sql (main schema)")
ok2 = run_file(conn, ALTER_SCRIPT, "alter_existing.sql (column additions)") if os.path.exists(ALTER_SCRIPT) else True

conn.close()

print(f"\n{'='*50}")
if ok1 and ok2:
    print("  [OK] Migration complete — all schemas applied.")
else:
    print("  [WARN] Migration had errors — check output above.")
print(f"{'='*50}")
