# Alfredo Quezada ____ 191002
# 3/03/2020
# Ultima modificacion 4/03/2020

import simpy
import random
import numpy as np
import matplotlib.pyplot as plt



#___________________________VARIABLES INICIALES____________________________________________________________
Procesos = 200  # Se le da un limite a los procesos mediante la creacion de una variable.
TTotal = []  # Aca se guardara el promedio de los procesos
#___________________________________________________________________________________________________________

#_________________________________INICIO DE LA FUNCION_______________________________________________________
def sistema_operativo(env, name, ram, cpu, cant_memoria, cant_procesos,
                      tiempo_espera):  # Funcion que emplea la simulacion
    prosesos_restantes = cant_procesos

    yield env.timeout(tiempo_espera)
    tiempoInicial = env.now

    yield ram.get(
        cant_memoria)  # Empieza con la asigancion de recursos de la RAM
    print("%s esta listo para ser recibido por el CPU en %s" % (name, env.now))
    terminar = False
    u = 0

    while terminar == False:  # Ciclo para que todos los procesos se vuelvan 0

        with cpu.request() as req:
            inicio = env.now
            yield req

            prosesos_restantes = prosesos_restantes - 3
            yield env.timeout(1)
            print("%s ejecuto 3 procesos en %s" % (name, env.now))

            if prosesos_restantes <= 0:  # Si ya no existen procesos en cola, termina.
                terminar = True
            else:
                u = random.randint(1, 2) # creacion del random para el  proceso de entrada/salida
                if u == 1:
                    yield env.timeout(1)
                    print("%s esta en operaciones de entrada/salida en %s" % (name, env.now))

    print("%s termino sus procesos en %s" % (name, env.now))

    yield ram.put(cant_memoria)  # Como el proceso ya termino, se libera la cantidad de RAM utilizada.

    tiempoFinal = env.now
    tiempoTotal = tiempoFinal - tiempoInicial
    print(tiempoTotal)
    TTotal.append(tiempoTotal)

#____________________________________________________________FIN DE LA FUNCION_______________________________________________


random.seed(10)

env = simpy.Environment()
ram = simpy.Container(env, init=100, capacity=100)  # Container para la RAM y Resource para el CPU
cpu = simpy.Resource(env, 2)
for i in range(
        Procesos + 1):  # Aca es cuando el simulador lee la cantidad de procesos que tendra que hacer.
    tiempo_espera = random.expovariate(1.0 / 10)
    cant_memoria = random.randint(1, 10)
    cant_procesos = random.randint(1, 10)
    env.process(sistema_operativo(env, "proceso %s" % i, ram, cpu, cant_memoria, cant_procesos, tiempo_espera))

env.run()


# Calcular el tiempo total (en promedio)
promedio = 0
for j in range(Procesos + 1):
    promedio = promedio + TTotal[i]

print("Promedio de tiempo por proceso %s" % (promedio / Procesos))

var = np.asarray(TTotal)
varianza = var.std()  # Convierte la lista a un array y le aplica la funcion str() para calcular la desviacion estandar
print("Varianza : %s" % (varianza))

#Listas para la creacion de las graficas:

t = [7.1, 44.6, 120.8, 187.8, 250.6] #Esta variable es para los tiempos para cada serie de procesos.
cp = [25, 50, 100, 150, 200]# Esta es la cantidad de procesos a realizar.

# Descomentar la parte siguiente para graficar

print("Porcentaje de cada corrida: %s" % (t) )
plt.plot (t, cp)
plt.title("Procesos con respecto al tiempo")
plt.xlabel("Tiempo")
plt.ylabel("Cantidad de procesos ejecutados")
plt.show()


#Codigos de referencia:
# https://repl.it/@LuisMartin2/Simulador-estados-de-procesos
# https://simpy.readthedocs.io/en/latest/topical_guides/resources.html#res-type-container
# https://naps.com.mx/blog/simulacion-en-python-usando-simpy/

