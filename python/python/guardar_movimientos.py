import os
import threading
import time
from pynput import mouse
from flask import Flask, render_template, redirect, url_for, request, session, flash
import sqlite3
from db_config import ejecutar_consulta

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clave secreta para la sesión

user_mouse_movements = {}

def conectar_db():
    return sqlite3.connect("usuarios.db")

#Función filtrado de datos:
def filtrar_ruido_movimientos(movimientos):
    movimientos_filtrados = []
    
    if len(movimientos) < 2:
        return movimientos
    
    for i in range(1, len(movimientos) - 1):
        x_promedio = (movimientos[i - 1][0] + movimientos[i][0] + movimientos[i + 1][0]) / 3
        y_promedio = (movimientos[i - 1][1] + movimientos[i][1] + movimientos[i + 1][1]) / 3
        movimientos_filtrados.append((x_promedio, y_promedio))

    movimientos_filtrados.insert(0, movimientos[0])
    movimientos_filtrados.append(movimientos[-1])

    return movimientos_filtrados


# Función para guardar los movimientos en un archivo
def guardar_movimientos(username):
    movimientos = user_mouse_movements.get(username, [])
    query = "INSERT INTO movimientos (username, x, y) VALUES (?, ?, ?)"
    for x, y in movimientos:
        ejecutar_consulta(query, (username, x, y))
    print(f"Movimientos guardados para {username} en la base de datos")



# Función para registrar movimientos del mouse
def capture_mouse_movement(username, duration=10):
    global user_mouse_movements
    user_mouse_movements[username] = []  # Inicializar lista para el usuario

    def on_move(x, y):
        user_mouse_movements[username].append((x, y))

    with mouse.Listener(on_move=on_move) as listener:
        time.sleep(duration) 
        listener.stop()

    movimientos_filtrados = filtrar_ruido_movimientos(user_mouse_movements[username])
    user_mouse_movements[username] = movimientos_filtrados  # Actualizar la lista de movimientos filtrados
    guardar_movimientos(username)


def verificar_credenciales(username, password):
    query = "SELECT * FROM usuarios WHERE username = ? AND password = ?"
    result = ejecutar_consulta(query, (username, password), fetch_one=True)
    return result is not None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if verificar_credenciales(username, password):
            session["username"] = username  # Guardar el nombre de usuario en la sesión
            threading.Thread(
                target=capture_mouse_movement, args=(username, 10)
            ).start()  # Captura mouse por 3 segundos
            return render_template("loading.html")  # Página de carga
        else:
            flash("Credenciales incorrectas. Inténtalo de nuevo.")
    return render_template("login.html")



@app.route("/pagina_principal")
def pagina_principal():
    if "username" not in session:  # Verificar si el usuario está autenticado
        return redirect(url_for("login"))  # Redirigir a la página de inicio de sesión si no está autenticado

    # Mostrar los movimientos del mouse para el usuario actual (opcional)
    current_user = session["username"]
    movements = user_mouse_movements.get(current_user, [])
    return render_template("pagina_principal.html", movements=movements)

@app.route("/logout")
def logout():
    session.pop("username", None)  # Cerrar sesión
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
