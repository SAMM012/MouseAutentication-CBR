import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
from db_config import inicializar_tablas
from db_config import ejecutar_consulta

inicializar_tablas()

def usuario_existe(username):
    query = "SELECT 1 FROM usuarios WHERE username = ?"
    result = ejecutar_consulta(query, (username,), fetch_one=True)
    return result is not None


# Función para registrar un nuevo usuario
def registrar_usuario():
    username = entry_usuario.get()
    password = entry_contrasena.get()

    if not username or not password:
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
        return

    if usuario_existe(username):
        messagebox.showwarning("Advertencia", "El nombre de usuario ya existe.")
        return

    query = "INSERT INTO usuarios (username, password) VALUES (?, ?)"
    ejecutar_consulta(query, (username, password))

    messagebox.showinfo("Éxito", "Usuario registrado con éxito.")
    entry_usuario.delete(0, tk.END)
    entry_contrasena.delete(0, tk.END)


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
