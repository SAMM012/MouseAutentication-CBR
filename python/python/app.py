from flask import Flask, render_template, redirect, url_for, request, session, flash
import os
import threading
import time
from pynput import mouse
from db_config import ejecutar_consulta
from metricas import CalculoMetricas


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

    #Importante verificar si el mouse se ha movido
    ultimo_x, ultimo_y = None, None #Almacenar la ultima posición

    def on_move(x, y):
        nonlocal ultimo_x, ultimo_y
        timestamp = time.time()
    #Ignorar coordenadas que son iguales a las ultimas registradas
        if ultimo_x is not None and ultimo_y is not None:
            if x == ultimo_x and y == ultimo_y:
             return
        movimientos_usuario.append((x, y, timestamp))
    #Capturar coordendas por el tiempo especificado
    with mouse.Listener(on_move=on_move) as listener:
        time.sleep(duration)
        listener.stop()

        #guardar movimientos en la bd
    guardar_movimientos(username, movimientos_usuario, intento_id)

    #Calcular las metricas depués de guardar
    calcular_metricas(username, intento_id)

    print(f"Movimientos guardados en la base de datos para el usuario {username}")

    #Calcular las metricas y guardar en la db
def calcular_metricas(username, intento_id):
        
    #Validamos que la metrica a calcular no haya sido calculada previamente
    validar_query= "SELECT COUNT(*) FROM metricas WHERE intento_id = ?" 
    result = ejecutar_consulta(validar_query, (intento_id,), fetch_one=True)

    if result[0] > 0:
        print(f"Las métricas para el intento {intento_id} del usuario {username} ya existen.")
        return

    query = "SELECT x, y, timestamp FROM movimientos WHERE username = ? AND intento_id = ? ORDER BY timestamp"      # Extraer movimientos para el intento actual
    movimientos = ejecutar_consulta(query, (username, intento_id), fetch=True)

    if movimientos:

        calculo = CalculoMetricas(movimientos) # Crear una instancia de la clase Metricas

        # Calculamos las metricas
        velocidad_prom = calculo.velocidad_prom()
        aceleracion_prom = calculo.aceleracion_prom()
        tiempo_total = calculo.tiempo_total()
        desv_estandar_vel = calculo.desviacion_estandar_velocidad()
        desv_estandar_acel = calculo.desviacion_estandar_acelera()

        # Guardar las metricas en la db
        query = """
        INSERT INTO metricas (intento_id, username, velocidad_promedio, aceleracion_promedio, tiempo_total, desviacion_estandar_velocidad, desviacion_estandar_aceleracion)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        ejecutar_consulta(query, (intento_id, username, velocidad_prom, aceleracion_prom, tiempo_total, desv_estandar_vel, desv_estandar_acel))
        print(f"Métricas guardadas para el intento {intento_id} del usuario {username}.")
    else:
        print(f"No se encontraron movimientos para el intento {intento_id} del usuario {username}.")

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
