import random 
from pokemon import Pokemon
from move import Move
from team import Team
from combat import*
from Archivo_funciones import*


#Extraigo la lista de pokemos y movimientos del arhivo CSV. Y la tabla de efectividad    
lista_moves = lista_movimientos()
pokemones = lista_pokemones()
efectividad = create_effectiveness_dict()
      
#Parametros iniciales
poblacion_inicial = 50
cant_rivales  = 100
corte_seleccion = 25

#Creo poblacion inicial y rivales
poblacion = crear_poblaciones(poblacion_inicial , pokemones, lista_moves)
rivales = crear_poblaciones(cant_rivales , pokemones, lista_moves)

#Simulo las batallas y extraigo las estadisticas
victorias = simu_batallas(poblacion,rivales,efectividad)

#Selecciono los "X" mejores equipos y completo la poblacion con nuevos equipos randoms
nueva_poblacion = seleccion_mejores(corte_seleccion, victorias, pokemones, lista_moves)

#Cruzo los pokemones de los equipos
poblacion_cruzada = cruza_equipos(nueva_poblacion)

#Muto la poblacion
poblacion_mutada = mutar_poblacion(poblacion_cruzada, pokemones)

#Simulo las batallas y extraigo estadisticas

