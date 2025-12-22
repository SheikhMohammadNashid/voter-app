import os
import psycopg2
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing)
# This allows our Frontend running on port 80 to talk to this API on port 5000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Model for Data Validation
# FastAPI uses this to ensure the 'vote' request contains a string named 'name'
class Vote(BaseModel):
    name: str

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD')
    )
    return conn

@app.get("/api/tools")
def get_tools():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name, votes FROM tools ORDER BY votes DESC;')
    tools = cur.fetchall()
    cur.close()
    conn.close()
    # FastAPI automatically serializes lists and dicts to JSON
    return [{'name': t[0], 'votes': t[1]} for t in tools]

@app.post("/api/vote")
def vote(vote_data: Vote):
    # We access data using dot notation: vote_data.name
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE tools SET votes = votes + 1 WHERE name = %s;', (vote_data.name,))
    conn.commit()
    cur.close()
    conn.close()
    return {'message': 'Vote cast!'}

if __name__ == '__main__':
    # We run Uvicorn programmatically so the original Dockerfile 
    # command (CMD ["python", "app.py"]) still works!
    uvicorn.run(app, host='0.0.0.0', port=5000)