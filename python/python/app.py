from flask import Flask, render_template, redirect, url_for, request, session, flash
import os
import threading
import time
from pynput import mouse
from db_config import ejecutar_consulta

app = Flask(__name__)
app.secret_key = os.urandom(24)

user_mouse_movements = {}

#Generar intento id
def generar_intento_id(username):
    query = "SELECT COALESCE(MAX(intento_id), 0) + 1 FROM movimientos WHERE username = ?"
    result = ejecutar_consulta(query, (username,), fetch_one=True)
    return result[0]

def verificar_credenciales(username, password):
    query = "SELECT * FROM usuarios WHERE username = ? AND password = ?"
    result = ejecutar_consulta(query, (username, password), fetch_one=True)
    return result is not None
 
 #Funcion para guardar los movimientos
def guardar_movimientos(username, movimientos_usuario, intento_id):
    query = "INSERT INTO movimientos (username, intento_id, x, y, timestamp) VALUES (?, ?, ?, ?, ?)"
    for x, y, timestamp  in movimientos_usuario:
        ejecutar_consulta(query, (username, intento_id, x, y, timestamp))
    print(f"Movimientos guardados en la base de datos para el usuario {username}, intento {intento_id}")

def capture_mouse_movement(username, duration=10):  # Cambiamos a 10 segundos para la captura
    movimientos_usuario = []
    intento_id = generar_intento_id(username)

    def on_move(x, y):
        timestamp = time.time()
        movimientos_usuario.append((x, y, timestamp))

    with mouse.Listener(on_move=on_move) as listener:
        time.sleep(duration)
        listener.stop()
        #guardar movimientos en la bd
    guardar_movimientos(username, movimientos_usuario, intento_id)
    print(f"Movimientos guardados en la base de datos para el usuario {username}")

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
            ).start() 
            return render_template("loading.html")  # Página de carga
        else:
            flash("Credenciales incorrectas. Inténtalo de nuevo.")
    return render_template("login.html")


@app.route("/pagina_principal")
def pagina_principal():
    if "username" not in session:  
        return redirect(url_for("login")) 

    # Mostrar los movimientos del mouse para el usuario actual
    current_user = session["username"]
    query = "SELECT x, y FROM movimientos WHERE username = ?"
    movements = ejecutar_consulta(query, (current_user,), fetch=True)  # Obtener movimientos de la base de datos
    return render_template("pagina_principal.html", movements=movements)

@app.route("/logout")
def logout():
    session.pop("username", None)  # Cerrar sesión
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
