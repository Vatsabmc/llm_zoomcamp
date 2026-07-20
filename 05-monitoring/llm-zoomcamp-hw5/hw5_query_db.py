import sqlite3

conn = sqlite3.connect("traces.db")
conn.row_factory = sqlite3.Row

rows = conn.execute("SELECT * FROM spans ORDER BY start_time").fetchall()
for row in rows:
    print(dict(row))

duration_rows = conn.execute("""
    SELECT name, SUM(end_time - start_time) / 1e6 AS total_duration_ms
    FROM spans
    WHERE name != 'rag'
    GROUP BY name
    ORDER BY total_duration_ms DESC
""").fetchall()

print()
for row in duration_rows:
    print(dict(row))
