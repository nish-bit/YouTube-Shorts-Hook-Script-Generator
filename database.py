import sqlite3

# === Create Table ===
def create_table():
    conn = sqlite3.connect("shorts.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS shorts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            language TEXT,
            hooks TEXT,
            script TEXT,
            caption TEXT,
            platform TEXT,
            summary TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# === Save Content ===
def save_content(topic, language, hooks, script, caption, platform, summary):
    conn = sqlite3.connect("shorts.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO shorts (topic, language, hooks, script, caption, platform, summary)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (topic, language, hooks, script, caption, platform, summary))
    conn.commit()
    conn.close()

# === Get All Records ===
def get_all_records():
    conn = sqlite3.connect("shorts.db")
    c = conn.cursor()
    c.execute("SELECT * FROM shorts ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    return rows

# ✅ === Delete a Record by ID ===
def delete_record(record_id):
    conn = sqlite3.connect("shorts.db")
    c = conn.cursor()
    c.execute("DELETE FROM shorts WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()

