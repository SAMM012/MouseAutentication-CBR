import os
import threading
import time
from pynput import mouse
from flask import Flask, render_template, redirect, url_for, request, session, flash
import sqlite3
from db_config import ejecutar_consulta

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clave secreta para la sesión



# Función para registrar movimientos del mouse
def capture_mouse_movement(username, duration=10):
    movimientos_usuario = []

    def on_move(x, y):
        movimientos_usuario.append((x, y))
        with mouse.Listener(on_move=on_move) as listener:
            time.sleep(duration) 
            listener.stop()  
    query = "INSERT INTO movimientos (username, x, y) VALUES (?, ?, ?)"
    for x, y in movimientos_usuario:
        ejecutar_consulta(query, (username, x, y))
    print(f"Movimientos guardados en la base de datos para el usuario {username}")

# Función para verificar credenciales
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
            session["username"] = username
            threading.Thread(target=capture_mouse_movement, args=(username, 10)).start()
            return render_template("loading.html")
        else:
            flash("Credenciales incorrectas. Inténtalo de nuevo.")
    return render_template("login.html")

@app.route("/pagina_principal")
def pagina_principal():
    if "username" not in session:
        return redirect(url_for("login"))

    current_user = session["username"]
    query = "SELECT x, y FROM movimientos WHERE username = ?"
    movements = ejecutar_consulta(query, (current_user,), fetch=True)
    return render_template("pagina_principal.html", movements=movements)



@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
