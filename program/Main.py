import random 
from pokemon import Pokemon
from move import Move
from team import Team
from combat import*
from Archivo_funciones import*
from tqdm import tqdm


#Parametros iniciales
poblacion_inicial = 50
cant_rivales  = 400
corte_seleccion = 25
generaciones = 25


#Extraigo la lista de pokemos y movimientos del arhivo CSV. Y la tabla de efectividad    
lista_moves = lista_movimientos()
pokemones = lista_pokemones()
efectividad = effectiveness_dic()

#Creo poblacion inicial y rivales
poblacion = crear_poblaciones(poblacion_inicial , pokemones, lista_moves)
rivales = crear_poblaciones(cant_rivales , pokemones, lista_moves)

#Creo los archivos de salida
crear_archivo_best_teams("Best_teams_x_generation3.csv")  
crear_archivo_cant_pokemons("Cantidad_pokemones_x_gen3.csv")
crear_archivo_tipos("Cantidad_tipo_ult_gen3.csv")

#Ejecuto las generaciones del algoritmo genetico
print("Comienza el algoritmo genetico")
ultima_poblacion, ultimos_rivales, dict_vict_finales = algoritmo_completo(corte_seleccion,generaciones,lista_moves,pokemones,efectividad,poblacion,rivales)

#Cargo los datos de la ultima generacion
dict_tipos = contar_frecuencia_tipos(ultima_poblacion)
dict_tipos_ordenado = dict(sorted(dict_tipos.items(), key=lambda item: item[1], reverse=True))
cargar_tipos_en_csv(dict_tipos_ordenado,"Cantidad_tipo_ult_gen3.csv")




