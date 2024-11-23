import numpy as np
from db_config import ejecutar_consulta
import math


class CalculoMetricas:
    def __init__(self):
        self.velocidades = []  # Para las velocidades 
        self.aceleraciones = [] # Para almacenar las aceleraciones
    #Función para calcular la velocidad promedio
    def calcular_velocidad_promedio(self, movimientos):
        self.velocidades = [] 
        for i in range(1, len(movimientos)):
            x1, y1, t1 = movimientos[i - 1]
            x2, y2, t2 = movimientos[i]

            distancia = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
            tiempo = t2 - t1

            if tiempo > 0:
                velocidad = distancia / tiempo
                self.velocidades.append((velocidad, t2))

        velocidades = [v for v, _ in self.velocidades]
        return np.mean(velocidades) if velocidades else 0

    #Función para calcular la aceleración promedio
    def calcular_aceleracion_promedio(self):
        aceleraciones = []

        for i in range(1, len(self.velocidades)):
            v1, t1 = self.velocidades[i - 1]
            v2, t2 = self.velocidades[i]

            delta_velocidad = v2 - v1
            delta_tiempo = t2 - t1

            if delta_tiempo > 0:
                aceleracion = delta_velocidad / delta_tiempo
                aceleraciones.append(aceleracion)

        return np.mean(aceleraciones) if aceleraciones else 0

        #Función para calcular tiempo total
    def calcular_tiempo_t(self, movimientos):
        if not movimientos:
            print("No hay movimientos disponibles para calcular el tiempo total.")
            return 0.0

        # Extraer el primer y la ultima marca de tiempo
        timestamps = [movimiento[5] for movimiento in movimientos]  # Obtener solo los tienmpos
        tiempo_total = max(timestamps) - min(timestamps)  # Calcular tiempo total

        return tiempo_total


        #CALCULAR LA DESVIACION ESTANDAR DE LA ACELERACIÓN
    def desviacion_estandar_acelera(self):

        if len(self.aceleraciones) > 1:
            aceleracion_media = sum(self.aceleraciones) / len(self.aceleraciones)
            varianza = sum((a - aceleracion_media) ** 2 for a in self.aceleraciones) / len(self.aceleraciones)
            desviacion_estandar = math.sqrt(varianza)
            return desviacion_estandar
        else:
            return 0
    
    #Calcular la desviación estandar de la velocidad
    def desviacion_estandar_velocidad(self):
         if len(self.velocidades) > 1:
            velocidad_media = sum(self.velocidades) / len(self.velocidades)
            varianza = sum((v - velocidad_media) ** 2 for v in self.velocidades) / len(self.velocidades)
            desviacion_estandar = math.sqrt(varianza)
            return desviacion_estandar
         else:
            return 0