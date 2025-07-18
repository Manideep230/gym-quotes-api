import sqlite3
import json

conn = sqlite3.connect("quotes.db")
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote TEXT NOT NULL,
    used INTEGER DEFAULT 0,
    date_used TEXT
)
''')

# Load from JSON
with open("quotes.json", "r") as f:
    quotes = json.load(f)

# Insert quotes only if table is empty
c.execute("SELECT COUNT(*) FROM quotes")
if c.fetchone()[0] == 0:
    for quote in quotes:
        c.execute("INSERT INTO quotes (quote) VALUES (?)", (quote,))
    print("✅ Quotes inserted successfully.")
else:
    print("⚠️ Quotes already exist in database.")

conn.commit()
conn.close()
