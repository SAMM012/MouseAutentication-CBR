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
        #Crear la tabla para las metricas
        cursor.execute("""
          CREATE TABLE IF NOT EXISTS metricas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                intento_id INTEGER NOT NULL,
                username TEXT NOT NULL,
                velocidad_promedio REAL NOT NULL,
                aceleracion_promedio REAL NOT NULL,
                tiempo_total REAL NOT NULL,
                desviacion_estandar_velocidad REAL NOT NULL,
                desviacion_estandar_aceleracion REAL NOT NULL,
                FOREIGN KEY (intento_id) REFERENCES movimientos(intento_id)
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

