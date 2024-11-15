import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

# Crear o abrir la base de datos
def get_connection():
    # Guardar la base de datos en el mismo directorio que el script
    conn = sqlite3.connect("usuarios.db")
    return conn

# Crear la tabla de usuarios si no existe
def crear_tabla():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            movimiento_num INTEGER,
            x REAL,
            y REAL
        )
    """)
        conn.commit()

# Verificar si el usuario existe en la base de datos
def usuario_existe(username):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM usuarios WHERE username = ?", (username,))
        return cursor.fetchone() is not None

# Función para registrar un nuevo usuario
def registrar_usuario():
    username = entry_usuario.get()
    password = entry_contrasena.get()

    # Verificar que los campos no estén vacíos
    if not username or not password:
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
        return

    if usuario_existe(username):
        messagebox.showwarning("Advertencia", "El nombre de usuario ya existe.")
        return

    # Guardar usuario en la base de datos
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
        conn.commit()

    messagebox.showinfo("Éxito", "Usuario registrado con éxito.")
    entry_usuario.delete(0, tk.END)
    entry_contrasena.delete(0, tk.END)

# Crear la tabla de usuarios al iniciar el programa
crear_tabla()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Registro")

# Etiquetas y entradas para el usuario
tk.Label(ventana, text="Nombre de Usuario").pack(pady=10)
entry_usuario = tk.Entry(ventana)
entry_usuario.pack(pady=5)

tk.Label(ventana, text="Contraseña").pack(pady=10)
entry_contrasena = tk.Entry(ventana, show="*")
entry_contrasena.pack(pady=5)

# Botón para registrar
boton_registrar = tk.Button(ventana, text="Registrar", command=registrar_usuario)
boton_registrar.pack(pady=10)

ventana.mainloop()
