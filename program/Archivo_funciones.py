import random 
from pokemon import Pokemon
from move import Move
from team import Team
from combat import*


def lista_pokemones():
    """ 
    Funcion que abre el archivo csv con toda la info sobre pokemos y crea una lista de listas con cada pokemon, 
    para podes trabajarlos comodamente en el resto del codigo.

    """
    with open("./data/pokemons.csv",mode="r") as arch:
        lines = [line.rstrip() for line in arch]
        lines.pop(0)
        return lines

def lista_movimientos():
    with open("./data/moves.csv",mode="r") as arch:
        lines = [line.rstrip().split(",") for line in arch]
        lines.pop(0)
        return lines
    
def create_effectiveness_dict()->dict[str, dict[str, float]]:
    effectiveness = {}
    with open('./data/effectiveness_chart.csv') as file:
        defenders = file.readline().strip('\n').split(',')
        defenders.pop(0)
        line = file.readline()
        while line != '':
            line = line.strip('\n').split(',')
            attacker = line.pop(0)
            for n in range(len(line)): line[n] = float(line[n])
            effectiveness[attacker] = {defender:dmg for defender, dmg in zip(defenders,line)}
            line = file.readline()
    return effectiveness

def crear_movimientos(moves: list[str], lista_moves: list):
    lista_obj_moves = []
    for move in moves:
        #Busqueda lineal
        for datos_mov in lista_moves:
            if datos_mov[0] == move:
                name = move
                type1 = str(datos_mov[1])
                category = str(datos_mov[2])
                pp = int(datos_mov[3])
                power = int(datos_mov[4])
                accuaracy = int(datos_mov[5])
                lista_obj_moves.append(Move(name, type1, category, pp, power, accuaracy))
    return lista_obj_moves

def crear_pokemon(pokemones: list[str], lista_moves: list):
    while True:
        random_index = random.randint(0, len(pokemones)-1)
        linea = pokemones[random_index].rstrip()
        linea = linea.split(",")
        
        pokedex_number = int(linea[0])
        name = linea[1]
        type1 = linea[2]
        type2 = linea[3]
        hp = int(linea[4])
        attack = int(linea[5])
        deffense = int(linea[6])
        sp_attack = int(linea[7])
        sp_defense = int(linea[8])
        speed = int(linea[9])
        generation = int(linea[10])
        height = float(linea[11]) if len(linea[11]) > 0 else 0
        weight = float(linea[12]) if len(linea[12]) > 0 else 0 
        is_legendary = bool(linea[13])
        moves = linea[14].split(";")
        obj_moves = crear_movimientos(moves,lista_moves)
        level = 50
        
        pokemon = Pokemon(pokedex_number, name, type1, type2, hp, attack, deffense, sp_attack, sp_defense, speed, generation, height, weight, is_legendary, obj_moves, level)

        if not pokemon.is_legendary:
            return pokemon
            
def crear_equipo(pokemones: list[str], lista_moves):
    equipo = []
    while True:
        if len(equipo) == 6:
            break
        pokemon = crear_pokemon(pokemones, lista_moves)
        if not (pokemon.name in set(pokemon.name for pokemon in equipo)):
            equipo.append(pokemon)
        else:
            continue
    return Team("Name",equipo)

def crear_poblaciones(cant_equipos: int, pokemones:list[str], lista_moves):
    poblacion = []
    for i in range(cant_equipos):
        equipo = crear_equipo(pokemones, lista_moves)
        equipo.name = f'Equipo {i+1}'
        poblacion.append(equipo)
    return poblacion

def simu_batallas(poblacion, rivales, efectividad):
    victorias = {}

    for equipo in poblacion:
        cant_victorias = 0
        for rival in rivales:
            ganador = get_winner(equipo, rival, efectividad)
            if ganador == equipo:
                cant_victorias += 1
        victorias[equipo] = cant_victorias

    victorias_ordenadas = dict(sorted(victorias.items(), key=lambda item: item[1], reverse=True))
    return victorias_ordenadas

def seleccion_mejores(corte_seleccion : int,victorias : dict[int], pokemones: list[str], lista_moves):
    #Extraigo los mejores "X" equipos del diccionario de victorias
    mejores_equipos = {key:value for i,(key,value) in enumerate(victorias.items()) if i < corte_seleccion}
    #Creo una nueva poblacion y agregos estos mejores equipos
    nueva_poblacion = [key for key in mejores_equipos.keys()]
    #Extraigo los 20 mejores para futuros rivales
    futuros_rivales = nueva_poblacion[:15]
    #Completamos la poblacion a 50
    relleno = crear_poblaciones(50-corte_seleccion , pokemones, lista_moves)
    for equipo in relleno:
        nueva_poblacion.append(equipo)
    return nueva_poblacion, futuros_rivales

def asegurar_unicos(nuevo_team, pokemones, lista_moves):
    nombres_vistos = set()
    equipo_unico = []
    for pokemon in nuevo_team:
        if pokemon.name not in nombres_vistos:
            equipo_unico.append(pokemon)
            nombres_vistos.add(pokemon.name)
    contador = 0
    while len(equipo_unico) < 6:
        contador += 1
        if contador > 15:
            print("bucle infito en repetidos")
        nuevo_pokemon = crear_pokemon(pokemones, lista_moves)
        if nuevo_pokemon.name not in nombres_vistos:
            equipo_unico.append(nuevo_pokemon)
            nombres_vistos.add(nuevo_pokemon.name)
    return equipo_unico

def cruza_equipos(poblacion, pokemones, lista_moves):
    poblacion_cruzada = []
    while True:
        if len(poblacion) == 0: 
            break

        #Extraigo dos equipos randoms de la poblacion
        indice1 = random.randint(0, len(poblacion)-1)
        team1 = poblacion.pop(indice1)

        
        indice2 = random.randint(0,len(poblacion)-1)
        team2 = poblacion.pop(indice2)

        #Mezclar con 70% de chance
        if random.random() < 0.7:
            #Creo un corte random de la cantidad de pokemones
            cut = random.randint(0,5)

            nuevo_team1 = team1.pokemons[0:cut+1] + team2.pokemons[cut+1:]
            nuevo_team2 = team1.pokemons[cut+1:] + team2.pokemons[:cut+1]
        #Caso, contrario, se mantienen iguales
        else:
            nuevo_team1 = team1
            nuevo_team2 = team2
            
        #Asegurar que ambos equipos tengan 6 pokémones únicos
        nuevo_team1 = asegurar_unicos(nuevo_team1,pokemones,lista_moves)
        nuevo_team2 = asegurar_unicos(nuevo_team2,pokemones,lista_moves)


    return poblacion_cruzada

def imprimir_dict_equipos(dict_victorias):
    for equipo, victorias in dict_victorias.items():
        print(f"Equipo: {equipo.name}, Victorias: {victorias}")
        print("Pokémon en el equipo:")
        for pokemon in equipo.pokemons: 
            print(f"- {pokemon.name}")


def mutar(equipo, pokemones):
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

def mutar_poblacion(poblacion, pokemones):
    
    for i in range(len(poblacion)):
        
        poblacion[i] = mutar(poblacion[i], pokemones)
    
    return poblacion
