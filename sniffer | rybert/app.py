from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

def get_db_connection():
    # pake path absolut supaya database selalu ketemu
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'judol_archive.db')
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    suspects = cursor.execute(
        'SELECT * FROM suspects ORDER BY detected_at DESC'
    ).fetchall()
    
    # Hitung total situs yang berhasil ditangkap
    total_scanned = len(suspects)
    
    conn.close()
    
    return render_template(
        'index.html', 
        suspects=suspects, 
        total_scanned=total_scanned
    )

if __name__ == '__main__':
    # Berjalan di port 5000 secara default
    app.run(debug=True)