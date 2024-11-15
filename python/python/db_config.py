import sqlite3

def conectar_db():
    return sqlite3.connect("usuarios.db")

def inicializar_tablas():
    with conectar_db() as conn:
        cursor = conn.cursor()
        # Crear tabla de usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        # Crear tabla de movimientos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                intento_id INTEGER NOT NULL,
                x REAL,
                y REAL,
                timestamp  REAL
            )
        """)
        conn.commit()

def ejecutar_consulta(query, params=(), fetch=False, fetch_one=False):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    
    if fetch_one:
        result = cursor.fetchone() 
    elif fetch:
        result = cursor.fetchall()
    else:
        result = None 
    
    conn.commit() 
    conn.close()
    
    return result

