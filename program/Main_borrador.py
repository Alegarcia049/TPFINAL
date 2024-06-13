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

def crear_movimientos(moves: list[str], lista_moves: list[str]):
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

def crear_pokemon(pokemones: list[str]):
    while True:
        random_index = random.randint(0, len(pokemones)-1)
        linea = pokemones[random_index].rstrip()
        linea = linea.split(",")
        if int(linea[-2]) == 0: 
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
            
            return Pokemon(pokedex_number, name, type1, type2, hp, attack, deffense, sp_attack, sp_defense, speed, generation, height, weight, is_legendary, obj_moves, level)
            
def crear_equipo(pokemones: list[str]):
    equipo = []
    while True:
        if len(equipo) == 6:
            break
        pokemon = crear_pokemon(pokemones)
        if not (pokemon.name in set(pokemon.name for pokemon in equipo)):
            equipo.append(pokemon)
        else:
            continue
    return Team("Name",equipo)

def crear_poblaciones(cant_equipos: int,pokemones:list[str]):
    poblacion = []
    for i in range(cant_equipos):
        equipo = crear_equipo(pokemones)
        equipo.name = f'Equipo {i+1}'
        poblacion.append(equipo)
    return poblacion

def lectura_pokemones(archivo:str):
    with open(archivo, 'r') as file:
        pokemones = file.readlines()[1:]
    return pokemones
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

def seleccion_mejores(corte_seleccion : int,victorias : dict[int], pokemones):
    #Extraigo los mejores "X" equipos del diccionario de victorias
    mejores_equipos = {key:value for i,(key,value) in enumerate(victorias.items()) if i < corte_seleccion}
    #Creo una nueva poblacion y agregos estos mejores equipos
    nueva_poblacion = [key for key in mejores_equipos.keys()]
    #Completamos la poblacion a 50
    relleno = crear_poblaciones(50-corte_seleccion , pokemones)
    for equipo in relleno:
        nueva_poblacion.append(equipo)
    return nueva_poblacion

def cruza_equipos(poblacion):
    poblacion_mutada = []
    while True:
        if len(poblacion) == 0: 
            break

        #Extraigo dos equipos randoms de la poblacion
        indice1 = random.randint(0, len(poblacion)-1)
        team1 = poblacion.pop(indice1)

        
        indice2 = random.randint(0,len(poblacion)-1)
        team2 = poblacion.pop(indice2)

        #Creo un corte random de la cantidad de pokemones
        cut = random.randint(0,5)

        nuevo_team1 = team1.pokemons[0:cut+1] + team2.pokemons[cut+1:]
        nuevo_team2 = team1.pokemons[cut+1:] + team2.pokemons[:cut+1]

        #Chequeo repetidos
        if len(set(pokemon.name for pokemon in nuevo_team1)) < 6 or len(set(pokemon.name for pokemon in nuevo_team2)) < 6:
            joined_teams = nuevo_team1 + nuevo_team2
            random.shuffle(joined_teams)

            nuevo_team1 = []
            nuevo_team2 = []

            for pokemon in joined_teams:
                if pokemon not in nuevo_team1 and len(nuevo_team1) < 6:
                    nuevo_team1.append(pokemon)
                elif pokemon not in nuevo_team2 and len(nuevo_team2) < 6:
                    nuevo_team2.append(pokemon)
        
        poblacion_mutada.append(Team("name",nuevo_team1))
        poblacion_mutada.append(Team("name",nuevo_team2))

    return poblacion_mutada




#Extraigo la lista de pokemos y movimientos del arhivo CSV. Y la tabla de efectividad    
pokemones = lista_pokemones()
lista_moves = lista_movimientos()
efectividad = create_effectiveness_dict()
      
#Creo pokemon, equipo y poblacion
poblacion_inicial = 50
cant_rivales  = 100
poblacion = crear_poblaciones(poblacion_inicial , pokemones)
rivales = crear_poblaciones(cant_rivales , pokemones)

#Batallas
victorias = simu_batallas(poblacion,rivales,efectividad)

#Selecciono los "X" mejores equipos
corte_seleccion = 25
nueva_poblacion = seleccion_mejores(corte_seleccion, victorias, pokemones)
    

mutacion = cruza_equipos(nueva_poblacion)
print(mutacion)
for team in mutacion:
    for pokemon in team.pokemons:
        print(pokemon.name)
