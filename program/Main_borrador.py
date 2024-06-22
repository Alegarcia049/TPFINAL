import random 
from pokemon import Pokemon
from move import Move
from team import Team
from combat import*
from Archivo_funciones import*
from tqdm import tqdm


#Extraigo la lista de pokemos y movimientos del arhivo CSV. Y la tabla de efectividad    
lista_moves = lista_movimientos()
pokemones = lista_pokemones()
efectividad = create_effectiveness_dict()


      
#Parametros iniciales
poblacion_inicial = 50
cant_rivales  = 100
corte_seleccion = 25
generaciones = 30

#Creo poblacion inicial y rivales
poblacion = crear_poblaciones(poblacion_inicial , pokemones, lista_moves)
rivales = crear_poblaciones(cant_rivales , pokemones, lista_moves)

print("Comienza el algoritmo genetico")

def algoritmo_genetico(lista_moves, pokemones, efectividad, poblacion, rivales):
    #Simulo las batallas y extraigo las estadisticas
    victorias = simu_batallas(poblacion,rivales,efectividad)

    #Selecciono los "X" mejores equipos y completo la poblacion con nuevos equipos randoms
    nueva_poblacion, futuros_rivales = seleccion_mejores(corte_seleccion, victorias, pokemones, lista_moves)

    #Cruzo los pokemones de los equipos
    poblacion_cruzada = cruza_equipos(nueva_poblacion, pokemones, lista_moves)

    #Muto la poblacion
    poblacion_mutada = mutar_poblacion(poblacion_cruzada, pokemones)

    #Simulo las batallas y extraigo estadisticas
    victorias_mutacion = simu_batallas(poblacion,rivales, efectividad)


    #Combino las victorias de la poblacion original y la mutada
    victorias_combinadas = {**victorias, **victorias_mutacion}
    victorias_combinadas_ordenadas = dict(sorted(victorias_combinadas.items(), key=lambda item: item[1], reverse=True))

    #Selecciono la mejor poblacion y proximos rivales
    poblacion_seleccionada = list(victorias_combinadas_ordenadas.keys())[:50]
    rivales_prox_gen = rivales[15:] + futuros_rivales 

    return poblacion_seleccionada, rivales_prox_gen, victorias_combinadas_ordenadas

for _ in tqdm(range(generaciones), desc="Procesando generaciones"):
    nueva_poblacion, nuevos_rivales, dict_vict_combinadas = algoritmo_genetico(lista_moves, pokemones, efectividad, poblacion, rivales)
    poblacion = nueva_poblacion
    rivales = nuevos_rivales
    print(f'Generación {_+1}')

imprimir_dict_equipos(dict_vict_combinadas)

