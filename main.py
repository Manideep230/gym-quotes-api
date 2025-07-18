from fastapi import FastAPI
from fastapi.responses import JSONResponse
import sqlite3
import datetime
import random

app = FastAPI()
DB = "quotes.db"

def get_connection():
    return sqlite3.connect(DB)

@app.get("/daily-quote")
def get_daily_quote():
    today = str(datetime.date.today())
    conn = get_connection()
    c = conn.cursor()

    # Check if quote already given today
    c.execute("SELECT quote FROM quotes WHERE date_used = ?", (today,))
    row = c.fetchone()
    if row:
        conn.close()
        return JSONResponse({"quote": row[0], "date": today})

    # Get a random unused quote
    c.execute("SELECT id, quote FROM quotes WHERE used = 0")
    unused = c.fetchall()

    # Reset all if no unused quotes left
    if not unused:
        c.execute("UPDATE quotes SET used = 0, date_used = NULL")
        conn.commit()
        c.execute("SELECT id, quote FROM quotes WHERE used = 0")
        unused = c.fetchall()

    selected = random.choice(unused)
    quote_id, quote_text = selected

    # Mark selected quote as used
    c.execute("UPDATE quotes SET used = 1, date_used = ? WHERE id = ?", (today, quote_id))
    conn.commit()
    conn.close()

    return JSONResponse({"quote": quote_text, "date": today})
