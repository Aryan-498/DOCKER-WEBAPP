from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")

def get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/items")
def create_item(name: str):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("INSERT INTO items (name) VALUES (%s)", (name,))
    conn.commit()

    cur.close()
    conn.close()

    return {"message": "Item inserted"}

@app.get("/items")
def get_items():

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM items")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows