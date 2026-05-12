import psycopg2, os
from dotenv import load_dotenv
load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()
cur.execute("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename")
tables = [r[0] for r in cur.fetchall()]
print(f"Tables in Supabase ({len(tables)} total):")
for t in tables:
    print(f"  - {t}")
cur.execute("SELECT workflow_name, from_status, to_status FROM workflow_transitions ORDER BY workflow_name, from_status")
rows = cur.fetchall()
print(f"\nWorkflow transitions seeded: {len(rows)}")
for r in rows:
    print(f"  {r[0]}: {r[1]} -> {r[2]}")
conn.close()
