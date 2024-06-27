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
cant_rivales  = 50
corte_seleccion = 25

#Creo poblacion inicial y rivales
poblacion = crear_poblaciones(poblacion_inicial , pokemones, lista_moves)
rivales = crear_poblaciones(cant_rivales , pokemones, lista_moves)

def algoritmo_genetico(poblacion,rivales,efectividad,lista_moves,pokemones):
    #Simulo las batallas y extraigo las estadisticas
    victorias_padres = simu_batallas(poblacion,rivales,efectividad)

    #Selecciono los "X" mejores equipos y completo la poblacion con nuevos equipos randoms
    nueva_poblacion, futuros_rivales = seleccion_mejores(corte_seleccion, victorias_padres, pokemones, lista_moves)

    #Cruzo los pokemones de los equipos
    poblacion_cruzada = cruza_equipos(nueva_poblacion,pokemones,lista_moves)

    #Muto la poblacion
    poblacion_mutada = mutar_poblacion(poblacion_cruzada, pokemones,lista_moves)

    #Simulo las batallas y extraigo estadisticas
    victorias_hijos_ordenada = simu_batallas(poblacion_mutada, rivales, efectividad)

    #Combino el diccionario de victorias de padres e hijos
    victorias_combinadas = {**victorias_padres, **victorias_hijos_ordenada}

    #Ordenamiento del diccionario por aptitud
    vic_combinadas_ordenadas = dict(sorted(victorias_combinadas.items(), key=lambda item: item[1], reverse=True))

    # Seleccion de los mejores padres e hijos
    poblacion_futura = list(vic_combinadas_ordenadas.keys())[:50]

    #Mejoro los rivales con buenos equipos
    rivales_prox_gen = rivales[20:] + futuros_rivales

    return poblacion_futura, rivales_prox_gen, vic_combinadas_ordenadas

for _ in tqdm(range(20), desc="Procesando generaciones"):
    poblacion_futura, futuros_rivales, dict_vict_combinadas = algoritmo_genetico(poblacion, rivales, efectividad,lista_moves,pokemones)
    poblacion = poblacion_futura
    rivales = futuros_rivales
    print(f'Generación {_+1}')

imprimir_dict_equipos(dict_vict_combinadas)