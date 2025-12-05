import sqlite3

def get_db():
    conn = sqlite3.connect("questoes.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS questoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            enunciado TEXT NOT NULL,
            alternativa_a TEXT NOT NULL,
            alternativa_b TEXT NOT NULL,
            alternativa_c TEXT NOT NULL,
            alternativa_d TEXT NOT NULL,
            correta TEXT NOT NULL,
            disciplina TEXT NOT NULL,
            dificuldade TEXT NOT NULL
        );
    """)
    db.commit()
