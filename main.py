# main.py

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import sqlite3
import random

app = FastAPI()

# ✅ Root route for health check
@app.get("/")
def root():
    return {"message": "Gym Quotes API is running!"}

# ✅ /quote route to return a random quote
@app.get("/quote")
def get_random_quote():
    try:
        conn = sqlite3.connect("quotes.db")
        cursor = conn.cursor()
        cursor.execute("SELECT text, author FROM quotes ORDER BY RANDOM() LIMIT 1")
        result = cursor.fetchone()
        conn.close()

        if result:
            return {"quote": result[0], "author": result[1]}
        else:
            return JSONResponse(status_code=404, content={"error": "No quotes found"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
