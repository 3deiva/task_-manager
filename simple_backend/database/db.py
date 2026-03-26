import sqlite3
from flask import g


def get_db(app):
    if "db" not in g:
        g.db = sqlite3.connect(
            app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(app, e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    with app.app_context():
        db = sqlite3.connect(app.config["DATABASE"])
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT    UNIQUE NOT NULL,
                email    TEXT    UNIQUE NOT NULL,
                password TEXT    NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                title       TEXT    NOT NULL,
                description TEXT,
                status      TEXT    DEFAULT 'pending',
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        db.commit()
        db.close()


def query_db(app, query, args=(), one=False):
    db  = sqlite3.connect(app.config["DATABASE"])
    cur = db.execute(query, args)
    rv  = cur.fetchall()
    db.commit()
    db.close()
    return (rv[0] if rv else None) if one else rv


def insert_db(app, query, args=()):
    db     = sqlite3.connect(app.config["DATABASE"])
    cursor = db.execute(query, args)
    db.commit()
    last_id = cursor.lastrowid
    db.close()
    return last_id
