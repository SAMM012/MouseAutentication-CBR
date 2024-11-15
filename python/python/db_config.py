import sqlite3

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