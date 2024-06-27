import random

from tqdm import tqdm

from pokemon import Pokemon

from move import Move

from team import Team

from combat import *

import csv

def lectura_pokemones(archivo:str):
    with open(archivo, 'r') as file:
        pokemones = file.readlines()[1:]
    return pokemones

def crear_pokemon(pokemon:list[str]):
    number, name, type1, type2, hp, attack, defense, sp_attack, sp_defense, speed, generation, height, weight, is_legendary, moves = pokemon.strip().split(',')
    movimentazao = movs_pokemon(moves.split(';'), ataques)
    return Pokemon(int(number), name, type1, type2, int(hp), int(attack), int(defense), int(sp_attack), int(sp_defense), int(speed), int(generation), height, weight, bool(int(is_legendary)), movimentazao)
    
def movs_pokemon(movs: list[str], ataques:list[str]):
    lista_movs = []
    for ataque in ataques:
        if ataque.split(',')[0] in movs:
            name, type, category, pp, power, accuracy = ataque.strip().split(',')
            lista_movs.append(Move(name, type, category, int(pp), int(power), int(accuracy)))
    return lista_movs 
      
def crear_dict_efectividad(efectividad):
    effectiveness_dict = {}
    for line in efectividad:
        key = line.split(",")[0]
        dict_interno = {}
        for i in range(len(efectividad)):
            key_interna = efectividad[i].split(",")[0]
            valor_interno = float(line.split(",")[i + 1])
            dict_interno[key_interna] = valor_interno
        effectiveness_dict[key] = dict_interno
    return effectiveness_dict

def crear_equipo(pokemones: list[str]):
    equipo = []
    pokemones_elegidos = set()

    while len(equipo) < 6:
        poke_number = random.randint(0, len(pokemones)-1)
        if poke_number not in pokemones_elegidos:
            pokemon_elegido = pokemones[poke_number]
            pokemon_objeto = crear_pokemon(pokemon_elegido)
            if not pokemon_objeto.is_legendary:
                equipo.append(pokemon_objeto)
                pokemones_elegidos.add(poke_number)

    return Team('name',equipo)
    
def crear_teams(num_equipos:int, pokemones:list[str]):
    teams = []
    for i in range(num_equipos):
        equipo = crear_equipo(pokemones)
        equipo.name = f'Equipo {i+1}'
        teams.append(equipo)
    return teams

def imprimir_dict_equipos(dict_victorias):
    for equipo, victorias in dict_victorias.items():
        print(f"Equipo: {equipo.name}, Victorias: {victorias}")
        print("Pokémon en el equipo:")
        for pokemon in equipo.pokemons: 
            print(f"- {pokemon.name}")

def peleas_y_puntos(poblacion, rivales, effectiveness_dict):
    victorias = {}

    for equipo in poblacion:
        contador_victorias = 0
        for rival in rivales:
            ganador = get_winner(equipo, rival, effectiveness_dict)
            if ganador == equipo:
                contador_victorias += 1
        victorias[equipo] = contador_victorias
    
    victorias_ordenadas = dict(sorted(victorias.items(), key=lambda item: item[1], reverse=True))

    return victorias_ordenadas

def actualizar_poblacion(poblacion: list[Team], victorias_ordenadas: dict[Team, int]):
    # Seleccionar los 20 mejores equipos
    mejores_equipos = list(victorias_ordenadas.keys())[:25]
    # Generar 30 equipos randoms
    nuevos_equipos = crear_teams(25, pokemones)
    # Actualizar la poblacion
    poblacion = mejores_equipos + nuevos_equipos

    return poblacion, mejores_equipos

def asegurar_unicos(nuevo_team):
            nombres_vistos = set()
            equipo_unico = []
            for pokemon in nuevo_team:
                if pokemon.name not in nombres_vistos:
                    equipo_unico.append(pokemon)
                    nombres_vistos.add(pokemon.name)
            while len(equipo_unico) < 6:
                nuevo_pokemon = crear_pokemon(pokemones[random.randint(0, len(pokemones) - 1)])
                if nuevo_pokemon.name not in nombres_vistos and not nuevo_pokemon.is_legendary:
                    equipo_unico.append(nuevo_pokemon)
                    nombres_vistos.add(nuevo_pokemon.name)
            return equipo_unico

def cruza_equipos(poblacion):
    poblacion_cruzada = []
    while len(poblacion) > 1:
        # Extraigo dos equipos randoms de la poblacion
        indice1 = random.randint(0, len(poblacion)-1)
        team1 = poblacion.pop(indice1)

        indice2 = random.randint(0, len(poblacion)-1)
        team2 = poblacion.pop(indice2)

        # Creo un corte random de la cantidad de pokemones
        cut = random.randint(0, 5)

        nuevo_team1_pokemons = team1.pokemons[:cut] + team2.pokemons[cut:]
        nuevo_team2_pokemons = team2.pokemons[:cut] + team1.pokemons[cut:]

        # Asegurar que ambos equipos tengan 6 pokémones únicos
        nuevo_team1_pokemons = asegurar_unicos(nuevo_team1_pokemons)
        nuevo_team2_pokemons = asegurar_unicos(nuevo_team2_pokemons)

        poblacion_cruzada.append(Team(team1.name, nuevo_team1_pokemons))
        poblacion_cruzada.append(Team(team2.name, nuevo_team2_pokemons))

    return poblacion_cruzada

def mutar(equipo):
    prob = random.random()
    lista_equipo = [pokemon.name for pokemon in equipo.pokemons]  # Lista de nombres de Pokémon en el equipo
    if prob <= 0.03:
        tipo_mutacion = random.randint(1, 3)

        if tipo_mutacion == 1:
            # Cambiar el Pokémon inicial por un Pokémon aleatorio
            nuevo_pokemon = crear_pokemon(pokemones[random.randint(0, len(pokemones) - 1)])
    
            while nuevo_pokemon.name in lista_equipo:
                nuevo_pokemon = crear_pokemon(pokemones[random.randint(0, len(pokemones) - 1)])
            equipo.pokemons[0] = nuevo_pokemon
            lista_equipo[0] = nuevo_pokemon.name  # Actualizar la lista de nombres
        elif tipo_mutacion == 2:
            # Cambiar el Pokémon inicial por otro Pokémon del equipo
            indice = random.randint(1, 5)
            equipo.pokemons[0], equipo.pokemons[indice] = equipo.pokemons[indice], equipo.pokemons[0]
            lista_equipo[0], lista_equipo[indice] = lista_equipo[indice], lista_equipo[0]  
        else:
            # Seleccionar un Pokémon aleatorio del equipo y cambiarlo por un Pokémon aleatorio
            indice = random.randint(0, 5)
            nuevo_pokemon = crear_pokemon(pokemones[random.randint(0, len(pokemones) - 1)])
            
            while nuevo_pokemon.name in lista_equipo:
                nuevo_pokemon = crear_pokemon(pokemones[random.randint(0, len(pokemones) - 1)])
            equipo.pokemons[indice] = nuevo_pokemon
            lista_equipo[indice] = nuevo_pokemon.name  

    return equipo

def mutar_poblacion(poblacion):
    
    for i in range(len(poblacion)):
        
        poblacion[i] = mutar(poblacion[i])
    
    return poblacion

pokemones = lectura_pokemones('./data/pokemons.csv')

ataques = lectura_pokemones('./data/moves.csv')

efectividad = lectura_pokemones('./data/effectiveness_chart.csv')

poblacion = crear_teams(50, pokemones)

rivales = crear_teams(400, pokemones)

dicc_efectividad = crear_dict_efectividad(efectividad)
#-------------------------------------------------------------------------------------------------------
def algoritmo_genetico(poblacion, rivales, dicc_efectividad):
    #-------------------------------------------------------------------------------------------------------
    #APTITUDES de cada TEAM (PADRES) (PELEAS Y PUNTOS)
    #-------------------------------------------------------------------------------------------------------
    victorias_ordenadas= peleas_y_puntos(poblacion, rivales, dicc_efectividad)

    #-------------------------------------------------------------------------------------------------------
    #SELECCION (SELECCIONA LOS MEJORES 20 EQUIPOS Y CREA 30 EQUIPOS RANDOMS) (ALMACENA LOS MEJORES 20)
    #-------------------------------------------------------------------------------------------------------
    poblacion_actualizada, futuros_rivales = actualizar_poblacion(poblacion, victorias_ordenadas)
    
    #-------------------------------------------------------------------------------------------------------
    #CRUZA (MEZCLA LOS EQUIPOS CON UNA PROBABILIDAD DE 70%)
    #-------------------------------------------------------------------------------------------------------
    poblacion_criada = cruza_equipos(poblacion_actualizada)
    
    #-------------------------------------------------------------------------------------------------------
    #MUTACION
    #-------------------------------------------------------------------------------------------------------
    poblacion_cruzada = mutar_poblacion(poblacion_criada)
    
    #-------------------------------------------------------------------------------------------------------
    #APTITUDES de cada TEAM (HIJOS) (PELEAS Y PUNTOS)
    #-------------------------------------------------------------------------------------------------------
    victorias_hijos_ordenada = peleas_y_puntos(poblacion_cruzada, rivales, dicc_efectividad)
    
    #-------------------------------------------------------------------------------------------------------
    # COMBINO LOS EQUIPOS PADRES Y HIJOS Y ORDENO DE MAYOR A MENOR
    #-------------------------------------------------------------------------------------------------------
    victorias_combinadas = {**victorias_ordenadas, **victorias_hijos_ordenada}

    victorias_combinadas_ordenadas = dict(sorted(victorias_combinadas.items(), key=lambda item: item[1], reverse=True))
    
    #-------------------------------------------------------------------------------------------------------
    #SELECCION DE POBLACION Y RIVALES QUE CONTINUAN A LA PROXIMA GENERACION
    #-------------------------------------------------------------------------------------------------------
    poblacion_seleccionada = list(victorias_combinadas_ordenadas.keys())[:50] #ELIJO LOS MEJORES 50 EQUIPOS

    rivales_prox_gen = rivales[15:] + futuros_rivales[:15] #MEJORO LOS RIVALES CON BUENOS EQUIPOS 
    
    return poblacion_seleccionada, rivales_prox_gen, victorias_combinadas_ordenadas

def crear_archivo_best_teams(name_archivo:str):  
    with open(name_archivo, mode = 'w',newline='') as archivo:
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerow(['Generacion','Aptitud','Team Name','Starter','Pokemon1','Pokemon2','Pokemon3','Pokemon4','Pokemon5'])

def crear_archivo_cant_pokemons(name_archivo:str):
    with open(name_archivo, mode = 'w',newline='') as archivo:
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerow(['Generacion','Cantidad','Pokemon'])

def contar_cantidad_apariciones(poblacion:list[Team], cantidad_pokemons:dict):
    for equipo in poblacion:
        for pokemon in equipo.pokemons:
            if pokemon.name in cantidad_pokemons:
                cantidad_pokemons[pokemon.name] += 1
            else:
                cantidad_pokemons[pokemon.name] = 1
    return cantidad_pokemons

def cargar_csv_apariciones(cantidad_pokemones: dict[str, int], archivo: str, generacion: int):
    with open(archivo, mode='a', newline='') as arch:
        writer = csv.writer(arch)
        
        fila = [generacion+1]
        for pokemon, cantidad in cantidad_pokemones.items():
            fila.extend([cantidad, pokemon])
        
        writer.writerow(fila)

def crear_archivo_tipos(name_archivo:str):
    with open(name_archivo, mode = 'w',newline='') as archivo:
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerow(['Tipo','Cantidad'])

def contar_frecuencia_tipos(poblacion):
    frecuencia_tipos = {}
    for equipo in poblacion:
        for pokemon in equipo.pokemons:
            # Verificar y contar type1 si no es None
            if pokemon.type1 is not None:
                if pokemon.type1 in frecuencia_tipos:
                    frecuencia_tipos[pokemon.type1] += 1
                else:
                    frecuencia_tipos[pokemon.type1] = 1
            # Verificar y contar type2 si no es None
            if pokemon.type2 is not None:
                if pokemon.type2 in frecuencia_tipos:
                    frecuencia_tipos[pokemon.type2] += 1
                else:
                    frecuencia_tipos[pokemon.type2] = 1
    
    return frecuencia_tipos

def cargar_tipos_en_csv(diccionario_tipos: dict, name_archivo: str):
    with open(name_archivo, mode='a', newline='') as archivo:  
        escritor_csv = csv.writer(archivo)
        for tipo, cantidad in diccionario_tipos.items():
            escritor_csv.writerow([tipo, cantidad])
    
def escritura_best_teams(best_teams:list[Team],best_points:list[int],name_archivo:str,gen:int):
    with open(name_archivo, mode ='a',newline='') as arch:
        escritor_csv = csv.writer(arch)
        for equipo, wins in zip(best_teams,best_points):
            pokes_str = [poke.name for poke in equipo.pokemons]
            escritor_csv.writerow([gen+1,wins,equipo.name]+ pokes_str)

def algo_completo(generaciones:int,poblacion:list[Team],rivales:list[Team], dict_efectividad:dict[dict]):
    for gen in tqdm(range(generaciones), desc="Procesando generaciones"):

        nueva_poblacion, nuevos_rivales, dict_vict_combinadas = algoritmo_genetico(poblacion, rivales, dicc_efectividad)
        poblacion = nueva_poblacion
        rivales = nuevos_rivales
        mejores_10_nombres = list(dict_vict_combinadas.keys())[:10]
        mejores_10_puntos = [dict_vict_combinadas[nombre] for nombre in mejores_10_nombres]
        escritura_best_teams(mejores_10_nombres,mejores_10_puntos,"Best_teams_x_generation2.csv",gen)
        dict_poke_cantidad = {}
        dict_poke_cantidad = contar_cantidad_apariciones(poblacion,dict_poke_cantidad)
        cargar_csv_apariciones(dict_poke_cantidad,"Cantidad_pokemones_x_gen2.csv",gen)
        print(f'Generación {gen+1}')

    return nueva_poblacion, nuevos_rivales, dict_vict_combinadas

crear_archivo_best_teams("Best_teams_x_generation2.csv")  
crear_archivo_cant_pokemons("Cantidad_pokemones_x_gen2.csv")
crear_archivo_tipos("Cantidad_tipo_ult_gen2.csv")
ultima_poblacion, ultimos_rivales, dict_vict_finales = algo_completo(25,poblacion,rivales,dicc_efectividad)
dict_tipos = contar_frecuencia_tipos(ultima_poblacion)
dict_tipos_ordenado = dict(sorted(dict_tipos.items(), key=lambda item: item[1], reverse=True))
cargar_tipos_en_csv(dict_tipos_ordenado,"Cantidad_tipo_ult_gen2.csv")








