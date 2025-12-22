import os
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS so our Frontend (different port) can talk to us
CORS(app) 

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD')
    )
    return conn

@app.route('/api/tools', methods=['GET'])
def get_tools():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name, votes FROM tools ORDER BY votes DESC;')
    tools = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{'name': t[0], 'votes': t[1]} for t in tools])

@app.route('/api/vote', methods=['POST'])
def vote():
    data = request.json
    tool_name = data.get('name')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE tools SET votes = votes + 1 WHERE name = %s;', (tool_name,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Vote cast!'})

if __name__ == '__main__':
    # Run on 0.0.0.0 to be accessible outside the container
    app.run(host='0.0.0.0', port=5000)