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
efectividad = effectiveness_dic()

  
#Parametros iniciales
poblacion_inicial = 50
cant_rivales  = 100
corte_seleccion = 25
generaciones = 25

#Creo poblacion inicial y rivales
poblacion = crear_poblaciones(poblacion_inicial , pokemones, lista_moves)
rivales = crear_poblaciones(cant_rivales , pokemones, lista_moves)



print("Comienza el algoritmo genetico")

for _ in tqdm(range(generaciones), desc="Procesando generaciones"):
    nueva_poblacion, nuevos_rivales, dict_vict_combinadas = algoritmo_genetico(corte_seleccion,lista_moves, pokemones, efectividad, poblacion, rivales)
    poblacion = nueva_poblacion
    rivales = nuevos_rivales
    print(f'Generación {_+1}')


imprimir_dict_equipos(dict_vict_combinadas)
# for i in range(generaciones):
#     nueva_poblacion, nuevos_rivales, dict_vict_combinadas = algoritmo_genetico(corte_seleccion,lista_moves, pokemones, efectividad, poblacion, rivales)
#     poblacion = nueva_poblacion
#     rivales = nuevos_rivales
#     print("Generacion: ",i)





'''
nueva_poblacion, nuevos_rivales, dict_vict_combinadas = algoritmo_genetico(corte_seleccion,lista_moves, pokemones, efectividad, poblacion, rivales)
print("1")
nueva_poblacion1, nuevos_rivales1, dict_vict_combinadas1 = algoritmo_genetico(corte_seleccion,lista_moves, pokemones, efectividad, nueva_poblacion, nuevos_rivales)
print("2")
nueva_poblacion2, nuevos_rivales2, dict_vict_combinadas2 = algoritmo_genetico(corte_seleccion,lista_moves, pokemones, efectividad, nueva_poblacion1, nuevos_rivales1)
print("3")
nueva_poblacion3, nuevos_rivales3, dict_vict_combinadas3 = algoritmo_genetico(corte_seleccion,lista_moves, pokemones, efectividad, nueva_poblacion2, nuevos_rivales2)
nueva_poblacion4, nuevos_rivales4, dict_vict_combinadas4 = algoritmo_genetico(corte_seleccion,lista_moves, pokemones, efectividad, nueva_poblacion3, nuevos_rivales3)
nueva_poblacion5, nuevos_rivales5, dict_vict_combinadas5 = algoritmo_genetico(corte_seleccion,lista_moves, pokemones, efectividad, nueva_poblacion4, nuevos_rivales4)
print("6")
nueva_poblacion6, nuevos_rivales6, dict_vict_combinadas6 = algoritmo_genetico(corte_seleccion,lista_moves, pokemones, efectividad, nueva_poblacion5, nuevos_rivales5)
nueva_poblacion7, nuevos_rivales7, dict_vict_combinadas7 = algoritmo_genetico(corte_seleccion,lista_moves, pokemones, efectividad, nueva_poblacion6, nuevos_rivales6)
print("8")
nueva_poblacion8, nuevos_rivales8, dict_vict_combinadas8 = algoritmo_genetico(corte_seleccion,lista_moves, pokemones, efectividad, nueva_poblacion7, nuevos_rivales7)
print("9")
nueva_poblacion9, nuevos_rivales9, dict_vict_combinadas9 = algoritmo_genetico(corte_seleccion,lista_moves, pokemones, efectividad, nueva_poblacion8, nuevos_rivales8)
nueva_poblacion10, nuevos_rivales10, dict_vict_combinadas10 = algoritmo_genetico(corte_seleccion,lista_moves, pokemones, efectividad, nueva_poblacion9, nuevos_rivales9)

imprimir_dict_equipos(dict_vict_combinadas10)

'''