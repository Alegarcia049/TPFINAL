import random

from tqdm import tqdm

from pokemon import Pokemon

from move import Move

from team import Team

from combat import *

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

def imprimir_equipos(poblacion): #Auxiliar
    for i, equipo in enumerate(poblacion, start=1):
        print(f'Equipo {i}:')
        for pokemon in equipo.pokemons:
            print(pokemon.name)

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

    for equipo, victorias in victorias_ordenadas.items():
        print(f'El equipo {equipo.name} ha ganado {victorias} veces.')
        print('Pokémon en este equipo:')
        for pokemon in equipo.pokemons:  
            print(pokemon.name)

    return victorias_ordenadas

def actualizar_poblacion(poblacion: list[Team], victorias_ordenadas: dict[Team, int]):
    # Seleccionar los 20 mejores equipos
    mejores_equipos = list(victorias_ordenadas.keys())[:20]
    # Generar 30 equipos randoms
    nuevos_equipos = crear_teams(30, pokemones)
    # Actualizar la poblacion
    poblacion = mejores_equipos + nuevos_equipos

    return poblacion, mejores_equipos

def mezclar_equipos(poblacion):
    
    nueva_poblacion = []

    while len(poblacion) >= 2:

        equipo1, equipo2 = random.sample(poblacion, 2)

        if random.random() < 0.7:
            
            equipo_unido = list(equipo1) + list(equipo2)

            nuevo_equipo1 = []
            nuevo_equipo2 = []

            for pokemon in equipo_unido:
                if len(nuevo_equipo1) < 6 and pokemon not in nuevo_equipo1:
                    nuevo_equipo1.append(pokemon)
                elif len(nuevo_equipo2) < 6 and pokemon not in nuevo_equipo2:
                    nuevo_equipo2.append(pokemon)

            # Agregar los nuevos equipos a la nueva población
            nueva_poblacion.append(nuevo_equipo1)
            nueva_poblacion.append(nuevo_equipo2)
        else:
            # Si no se mezclan, agregar los equipos originales a la nueva población
            nueva_poblacion.append(equipo1)
            nueva_poblacion.append(equipo2)

        # Remover los equipos seleccionados de la población
        poblacion.remove(equipo1)
        poblacion.remove(equipo2)

    return nueva_poblacion

def mutar(equipo):
    prob = random.random()

    if prob <= 0.03:
        tipo_mutacion = random.randint(1, 3)

        if tipo_mutacion == 1:
            # Cambiar el Pokémon inicial por un Pokémon aleatorio
            nuevo_pokemon = crear_pokemon(pokemones[random.randint(0, len(pokemones) - 1)])
            # Verifico que no haya pokemones repetidos
            while nuevo_pokemon in equipo: 
                nuevo_pokemon = crear_pokemon(pokemones[random.randint(0, len(pokemones) - 1)])
            equipo[0] = nuevo_pokemon
        elif tipo_mutacion == 2:
            # Cambiar el Pokémon inicial por otro Pokémon del equipo
            indice = random.randint(1, len(equipo) - 1)
            equipo[0], equipo[indice] = equipo[indice], equipo[0]
        else:
            # Seleccionar un Pokémon aleatorio del equipo y cambiarlo por un Pokémon aleatorio
            indice = random.randint(0, len(equipo) - 1)
            nuevo_pokemon = crear_pokemon(pokemones[random.randint(0, len(pokemones) - 1)])
            while nuevo_pokemon in equipo:
                nuevo_pokemon = crear_pokemon(pokemones[random.randint(0, len(pokemones) - 1)])
            equipo[indice] = nuevo_pokemon

    return equipo

def mutar_poblacion(poblacion):
    
    for i in range(len(poblacion)):
        
        poblacion[i] = mutar(poblacion[i])
    
    return poblacion

def imprimir_dict_equipos(victorias_combinadas_ordenadas, poblacion_seleccionada):
    contador = 0
    for equipo, victorias in victorias_combinadas_ordenadas.items():
        print(f"Equipo: {equipo}, Victorias: {victorias}")
        for pokemon in poblacion_seleccionada[equipo]:
            print(f"Pokémon: {pokemon}")
        contador += 1
        if contador == 50:
            break

#-------------------------------------------------------------------------------------------------------
#LECTURA DE DATOS
#-------------------------------------------------------------------------------------------------------
pokemones = lectura_pokemones('./data/pokemons.csv')

ataques = lectura_pokemones('./data/moves.csv')

efectividad = lectura_pokemones('./data/effectiveness_chart.csv')
#-------------------------------------------------------------------------------------------------------
#CREACION DE POBLACION Y RIVALES
#-------------------------------------------------------------------------------------------------------
poblacion = crear_teams(50, pokemones)

rivales = crear_teams(100, pokemones)
#-------------------------------------------------------------------------------------------------------
#CREACION DE DICCIONARIO DE EFECTIVIDAD
#-------------------------------------------------------------------------------------------------------
dicc_efectividad = crear_dict_efectividad(efectividad)
#-------------------------------------------------------------------------------------------------------
def algoritmo_genetico(poblacion, rivales, dicc_efectividad):
    pbar = tqdm(total=7, desc="Algoritmo genético", ncols=100)
    #-------------------------------------------------------------------------------------------------------
    #APTITUDES de cada TEAM (PADRES) (PELEAS Y PUNTOS)
    #-------------------------------------------------------------------------------------------------------
    victorias_ordenadas= peleas_y_puntos(poblacion, rivales, dicc_efectividad)
    pbar.update()
    #-------------------------------------------------------------------------------------------------------
    #SELECCION (SELECCIONA LOS MEJORES 20 EQUIPOS Y CREA 30 EQUIPOS RANDOMS) (ALMACENA LOS MEJORES 20)
    #-------------------------------------------------------------------------------------------------------
    poblacion_actualizada, futuros_rivales = actualizar_poblacion(poblacion, victorias_ordenadas)
    pbar.update()
    #-------------------------------------------------------------------------------------------------------
    #CRUZA (MEZCLA LOS EQUIPOS CON UNA PROBABILIDAD DE 70%)
    #-------------------------------------------------------------------------------------------------------
    poblacion_criada = mezclar_equipos(poblacion_actualizada)
    pbar.update()
    #-------------------------------------------------------------------------------------------------------
    #MUTACION
    #-------------------------------------------------------------------------------------------------------
    poblacion_mutada = mutar_poblacion(poblacion_criada)
    pbar.update()
    #-------------------------------------------------------------------------------------------------------
    #MEJORA DEL ALGORITMO GENETICO
    #-------------------------------------------------------------------------------------------------------
    #APTITUDES de cada TEAM (HIJOS) (PELEAS Y PUNTOS)
    #-------------------------------------------------------------------------------------------------------
    victorias_hijos_ordenada = peleas_y_puntos(poblacion_mutada, rivales, dicc_efectividad)
    pbar.update()
    #-------------------------------------------------------------------------------------------------------
    # COMBINO LOS EQUIPOS PADRES Y HIJOS Y ORDENO DE MAYOR A MENOR
    #-------------------------------------------------------------------------------------------------------
    victorias_combinadas = {**victorias_ordenadas, **victorias_hijos_ordenada}

    victorias_combinadas_ordenadas = dict(sorted(victorias_combinadas.items(), key=lambda item: item[1], reverse=True))
    pbar.update()
    #-------------------------------------------------------------------------------------------------------
    #SELECCION DE POBLACION Y RIVALES QUE CONTINUAN A LA PROXIMA GENERACION
    #-------------------------------------------------------------------------------------------------------
    poblacion_seleccionada = list(victorias_combinadas_ordenadas.keys())[:50] #ELIJO LOS MEJORES 50 EQUIPOS

    rivales_prox_gen = rivales[20:] + futuros_rivales #MEJORO LOS RIVALES CON BUENOS EQUIPOS 
    pbar.update()
    pbar.close()
    return poblacion_seleccionada, rivales_prox_gen, victorias_combinadas_ordenadas
    
nueva_poblacion, nuevos_rivales, dict_vict_combinadas = algoritmo_genetico(poblacion, rivales, dicc_efectividad)

imprimir_dict_equipos(dict_vict_combinadas, nueva_poblacion)







