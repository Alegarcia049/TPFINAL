import random 
from pokemon import Pokemon
from move import Move
from team import Team
from combat import*
from Archivo_funciones import*
from tqdm import tqdm
import multiprocessing

if __name__ == '__main__':
    
    #Parametros iniciales
    poblacion_inicial = 50
    cant_rivales  = 400
    corte_seleccion = 25
    generaciones = 50
    num_procesos = multiprocessing.cpu_count() #Si se desea ejecutar con multiprocessing ir a linea 584 del archivo funciones


    #Extraigo la lista de pokemos y movimientos del arhivo CSV. Y la tabla de efectividad    
    lista_moves = lista_movimientos()
    pokemones = lista_pokemones()
    efectividad = effectiveness_dic()


    #Creo poblacion inicial y rivales
    poblacion = crear_poblaciones(poblacion_inicial , pokemones, lista_moves)
    rivales = crear_poblaciones(cant_rivales , pokemones, lista_moves)

    #Creo los archivos de salida
    crear_archivo_best_teams("Best_teams_x_generation.csv")  
    crear_archivo_cant_pokemons("Cantidad_pokemones_x_gen.csv")
    crear_archivo_tipos("Cantidad_tipo_ult_gen.csv")

    #Ejecuto las generaciones del algoritmo genetico
    print("Comienza el algoritmo genetico")
    ultima_poblacion, ultimos_rivales, dict_vict_finales = algoritmo_completo(corte_seleccion,generaciones,lista_moves,pokemones,efectividad,poblacion,rivales)


    dict_tipos = contar_frecuencia_tipos(ultima_poblacion)
    dict_tipos_ordenado = dict(sorted(dict_tipos.items(), key=lambda item: item[1], reverse=True))
    cargar_tipos_en_csv(dict_tipos_ordenado,"Cantidad_tipo_ult_gen.csv")

    #Cargo el mejor equipo para pelear en el simulador
    best_team = escritura_mejor_team('best_team6.csv', dict_vict_finales)
    escritura_stats_best_team(best_team, 'mejor_equipo_stats.csv')





