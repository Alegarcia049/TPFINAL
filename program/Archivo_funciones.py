import random 
from pokemon import Pokemon
from move import Move
from team import Team
from combat import*
from tqdm import tqdm
import csv


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

def effectiveness_dic():
    with open('./data/effectiveness_chart.csv', 'r') as file:
        efectividad = file.readlines()[1:]
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
        is_legendary = bool(int(linea[13]))
        moves = linea[14].split(";")
        obj_moves = crear_movimientos(moves,lista_moves)
        level = 50
        
        return Pokemon(pokedex_number, name, type1, type2, hp, attack, deffense, sp_attack, sp_defense, speed, generation, height, weight, is_legendary, obj_moves, level)

        
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
               
def crear_equipo(pokemones: list[str], lista_moves):
    equipo = []
    while True:
        if len(equipo) == 6:
            break
        pokemon = crear_pokemon(pokemones, lista_moves)

        if not (pokemon.name in set(pokemon.name for pokemon in equipo)):
            if not pokemon.is_legendary:
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

def seleccion_mejores(corte_seleccion : int, poblacion : list[Team], victorias : dict[int], pokemones: list[str], lista_moves):
    # Seleccionar los "X" mejores equipos
    mejores_equipos = list(victorias.keys())[:corte_seleccion]

    # Generar "X" equipos randoms (rellenar hasta armar una poblacion de 50)
    nuevos_equipos = crear_poblaciones(50 - corte_seleccion, pokemones,lista_moves)

    # Actualizar la poblacion
    poblacion = mejores_equipos + nuevos_equipos
    

    return poblacion, mejores_equipos

'''
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
'''

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
    while len(poblacion) > 1:
        # Extraigo dos equipos randoms de la poblacion
        indice1 = random.randint(0, len(poblacion)-1)
        team1 = poblacion.pop(indice1)

        indice2 = random.randint(0, len(poblacion)-1)
        team2 = poblacion.pop(indice2)

        if random.random() <= 0.7:

            #Creo un corte random de la cantidad de pokemones
            cut = random.randint(0,5)

            nuevo_team1 = team1.pokemons[:cut] + team2.pokemons[cut:]
            nuevo_team2 = team2.pokemons[:cut] + team1.pokemons[cut:]
            
            #Asegurar que ambos equipos tengan 6 pokémones únicos
            nuevo_team1 = asegurar_unicos(nuevo_team1,pokemones,lista_moves)
            nuevo_team2 = asegurar_unicos(nuevo_team2,pokemones,lista_moves)

        else: 
            nuevo_team1 = team1.pokemons[:]
            nuevo_team2 = team2.pokemons[:]

        poblacion_cruzada.append(Team(team1.name,nuevo_team1))
        poblacion_cruzada.append(Team(team2.name,nuevo_team2))


    return poblacion_cruzada

def imprimir_dict_equipos(dict_victorias):
    for equipo, victorias in dict_victorias.items():
        print(f"Equipo: {equipo.name}, Victorias: {victorias}")
        print("Pokémon en el equipo:")
        for pokemon in equipo.pokemons: 
            print(f"- {pokemon.name}")


def mutar(equipo, pokemones,lista_moves):
    prob = random.random()
    lista_equipo = [pokemon.name for pokemon in equipo.pokemons]  # Lista de nombres de Pokémon en el equipo
    if prob <= 0.03:
        tipo_mutacion = random.randint(1, 3)

        if tipo_mutacion == 1:
            # Cambiar el Pokémon inicial por un Pokémon aleatorio
            nuevo_pokemon = crear_pokemon(pokemones,lista_moves)
    
            while nuevo_pokemon.name in lista_equipo:
                nuevo_pokemon = crear_pokemon(pokemones,lista_moves)
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
            nuevo_pokemon = crear_pokemon(pokemones,lista_moves)
            
            while nuevo_pokemon.name in lista_equipo:
                nuevo_pokemon = crear_pokemon(pokemones,lista_moves)
            equipo.pokemons[indice] = nuevo_pokemon
            lista_equipo[indice] = nuevo_pokemon.name  

    return equipo

def mutar_poblacion(poblacion, pokemones,lista_moves):
    
    for i in range(len(poblacion)):
        
        poblacion[i] = mutar(poblacion[i], pokemones,lista_moves)
    
    return poblacion


def algoritmo_genetico(corte_seleccion, lista_moves, pokemones, efectividad, poblacion, rivales):
    #Simulo las batallas y extraigo las estadisticas
    victorias = simu_batallas(poblacion,rivales,efectividad)
    # print("Primeras victorias",victorias)

    #Selecciono los "X" mejores equipos y completo la poblacion con nuevos equipos randoms
    nueva_poblacion, futuros_rivales = seleccion_mejores(corte_seleccion, poblacion, victorias, pokemones, lista_moves)

    #Cruzo los pokemones de los equipos
    poblacion_cruzada = cruza_equipos(nueva_poblacion, pokemones, lista_moves)

    #Muto la poblacion
    poblacion_mutada = mutar_poblacion(poblacion_cruzada, pokemones, lista_moves)

    #Simulo las batallas y extraigo estadisticas
    victorias_mutacion = simu_batallas(poblacion_mutada,rivales, efectividad)


    #Combino las victorias de la poblacion original y la mutada
    victorias_combinadas = {**victorias, **victorias_mutacion}
    victorias_combinadas_ordenadas = dict(sorted(victorias_combinadas.items(), key=lambda item: item[1], reverse=True))
    

    #Selecciono la mejor poblacion y proximos rivales
    poblacion_seleccionada = list(victorias_combinadas_ordenadas.keys())[:50]
    
    nuevos_rivales = crear_poblaciones(15,pokemones, lista_moves)
    rivales_prox_gen = rivales[30:] + futuros_rivales[:15] + nuevos_rivales


    return poblacion_seleccionada, rivales_prox_gen, victorias_combinadas_ordenadas

def crear_archivo_best_teams(name_archivo:str):
    with open(name_archivo, mode = 'w',newline='') as archivo:
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerow(['Generacion','Aptitud','Team Name','Starter','Pokemon1','Pokemon2','Pokemon3','Pokemon4','Pokemon5'])

def crear_archivo_cant_pokemons(name_archivo:str):
    with open(name_archivo, mode = 'w',newline='') as archivo:
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerow(['Generacion','Cantidad','Pokemon'])

def crear_archivo_tipos(name_archivo:str):
    with open(name_archivo, mode = 'w',newline='') as archivo:
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerow(['Tipo','Cantidad'])

def contar_cantidad_apariciones(poblacion:list[Team], cantidad_pokemons:dict):
    """ 
    Parametros: Recibe una poblacion de pokemones y un diccionario vacio
    Cuenta la cantidad de apareciciones de pokemones en la poblacion y los carga al diccionario
    Con el formato Key : Value tal que "Pokemon" : "cant"
    Se utiliza para contar la cant de apariciones de la poblacion de cada generacion
    """
    for equipo in poblacion:
        for pokemon in equipo.pokemons:
            if pokemon.name in cantidad_pokemons:
                cantidad_pokemons[pokemon.name] += 1
            else:
                cantidad_pokemons[pokemon.name] = 1
    return cantidad_pokemons

def contar_frecuencia_tipos(poblacion: list[Team]):
    """ 
    Parametros: Recibe una poblacion de pokemones
    Cuenta la cantidad de frecuencias de tipos de toda la poblacion
    y los almacena de un diccionario, que luego devuelve.
    Con el formato Key : value tal que "type1/2" : cant 
    Se utilza solamente para la poblacion de la ultima generacion
    """
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

def cargar_csv_apariciones(cantidad_pokemones: dict[str, int], archivo: str, generacion: int):
    with open(archivo, mode='a', newline='') as arch:
        writer = csv.writer(arch)
        
        fila = [generacion+1]
        for pokemon, cantidad in cantidad_pokemones.items():
            fila.extend([cantidad, pokemon])
        
        writer.writerow(fila)

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


def algoritmo_completo(corte_seleccion: int, generaciones: int, lista_moves, pokemones, efectividad, poblacion, rivales):
    for gen in tqdm(range(generaciones), desc="Procesando generaciones"):

        nueva_poblacion, nuevos_rivales, dict_vict_combinadas = algoritmo_genetico(corte_seleccion, lista_moves, pokemones, efectividad, poblacion, rivales)
        poblacion = nueva_poblacion
        rivales = nuevos_rivales
        mejores_10_nombres = list(dict_vict_combinadas.keys())[:10]
        mejores_10_puntos = [dict_vict_combinadas[nombre] for nombre in mejores_10_nombres]
        escritura_best_teams(mejores_10_nombres,mejores_10_puntos,"Best_teams_x_generation3.csv",gen)
        dict_poke_cantidad = {}
        dict_poke_cantidad = contar_cantidad_apariciones(poblacion,dict_poke_cantidad)
        cargar_csv_apariciones(dict_poke_cantidad,"Cantidad_pokemones_x_gen3.csv",gen)
        print(f'Generación {gen+1}')

    return nueva_poblacion, nuevos_rivales, dict_vict_combinadas


#------------------------------------------------------------------------------------------------------------------------------------#
#                                               FUNCIONES CON MULTIPROCESSING
#------------------------------------------------------------------------------------------------------------------------------------#
import multiprocessing

def simu_batallas_paralelo(poblacion, rivales, efectividad, num_procesos):
    with multiprocessing.Pool(processes=num_procesos) as pool:
        args = [(equipo, rivales, efectividad) for equipo in poblacion]
        resultados = pool.map(simu_batalla_individual, args)
    
    victorias = {equipo: cant_victorias for equipo, cant_victorias in resultados}
    victorias_ordenadas = dict(sorted(victorias.items(), key=lambda item: item[1], reverse=True))
    return victorias_ordenadas

def simu_batalla_individual(args):
    equipo, rivales, efectividad = args
    cant_victorias = 0
    for rival in rivales:
        ganador = get_winner(equipo, rival, efectividad)
        if ganador == equipo:
            cant_victorias += 1
    return equipo, cant_victorias

def algoritmo_geneticoMulti(corte_seleccion, lista_moves, pokemones, efectividad, poblacion, rivales, num_procesos):
    # Simulo las batallas y extraigo las estadísticas
    victorias = simu_batallas_paralelo(poblacion, rivales, efectividad, num_procesos)

    # Selecciono los "X" mejores equipos y completo la población con nuevos equipos aleatorios
    nueva_poblacion, futuros_rivales = seleccion_mejores(corte_seleccion, poblacion, victorias, pokemones, lista_moves)

    # Cruzo los pokemones de los equipos
    poblacion_cruzada = cruza_equipos(nueva_poblacion, pokemones, lista_moves)

    # Muto la población
    poblacion_mutada = mutar_poblacion(poblacion_cruzada, pokemones, lista_moves)

    # Simulo las batallas y extraigo estadísticas
    victorias_mutacion = simu_batallas_paralelo(poblacion_mutada, rivales, efectividad, num_procesos)

    # Combino las victorias de la población original y la mutada
    victorias_combinadas = {**victorias, **victorias_mutacion}
    victorias_combinadas_ordenadas = dict(sorted(victorias_combinadas.items(), key=lambda item: item[1], reverse=True))

    # Selecciono la mejor población y próximos rivales
    poblacion_seleccionada = list(victorias_combinadas_ordenadas.keys())[:50]

    nuevos_rivales = crear_poblaciones(15, pokemones, lista_moves)
    rivales_prox_gen = rivales[30:] + futuros_rivales[:15] + nuevos_rivales

    return poblacion_seleccionada, rivales_prox_gen, victorias_combinadas_ordenadas

def algoritmo_completoMulti(corte_seleccion: int, generaciones: int, lista_moves, pokemones, efectividad, poblacion, rivales,num_procesos):
    for gen in tqdm(range(generaciones), desc="Procesando generaciones"):

        nueva_poblacion, nuevos_rivales, dict_vict_combinadas = algoritmo_geneticoMulti(corte_seleccion, lista_moves, pokemones, efectividad, poblacion, rivales,num_procesos)
        poblacion = nueva_poblacion
        rivales = nuevos_rivales
        mejores_10_nombres = list(dict_vict_combinadas.keys())[:10]
        mejores_10_puntos = [dict_vict_combinadas[nombre] for nombre in mejores_10_nombres]
        escritura_best_teams(mejores_10_nombres,mejores_10_puntos,"Best_teams_x_generation3.csv",gen)
        dict_poke_cantidad = {}
        dict_poke_cantidad = contar_cantidad_apariciones(poblacion,dict_poke_cantidad)
        cargar_csv_apariciones(dict_poke_cantidad,"Cantidad_pokemones_x_gen3.csv",gen)
        print(f'Generación {gen+1}')

    return nueva_poblacion, nuevos_rivales, dict_vict_combinadas