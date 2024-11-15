import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt


# Función para graficar las coordenadas
def graficar():
    try:
        # Obtener el nombre del archivo del usuario
        username = entry_usuario.get()
        with open(f"movimientos_{username}.txt", "r") as file:
            data = file.readlines()

        # Procesar las coordenadas
        coordenadas = [tuple(map(float, line.strip().split(","))) for line in data]

        # Separar las coordenadas en listas X y Y
        x, y = zip(*coordenadas)

        # Crear el gráfico
        plt.figure(figsize=(8, 6))
        plt.scatter(x, y, color="blue", marker="o")
        plt.title("Gráfico de Movimientos del Mouse")
        plt.xlabel("Eje X")
        plt.ylabel("Eje Y")
        plt.grid()
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error: {str(e)}")


# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Gráfico de Movimientos")

# Etiqueta de instrucción
etiqueta = tk.Label(
    ventana, text="Ingresa tu nombre de usuario para graficar tus movimientos:"
)
etiqueta.pack(pady=10)

# Entrada de texto para el nombre de usuario
entry_usuario = tk.Entry(ventana)
entry_usuario.pack(pady=5)

# Botón para graficar
boton_graficar = tk.Button(ventana, text="Graficar Movimientos", command=graficar)
boton_graficar.pack(pady=10)

# Iniciar la interfaz gráfica
ventana.mainloop()
