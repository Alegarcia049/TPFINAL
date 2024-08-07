import random 
from pokemon import Pokemon
from move import Move
from team import Team
from combat import*
from tqdm import tqdm
import csv

def lista_pokemones():
    """ 
    Lee el archivo pokemons.csv y devuelve una lista con los datos de los pokemones

    Returns:
    list[str]: Lista de strings con los datos de los pokemones

    """
    with open("./data/pokemons.csv",mode="r") as arch:
        lines = [line.rstrip() for line in arch]
        lines.pop(0)
        return lines

def lista_movimientos():
    """
    Lee el archivo moves.csv y devuelve una lista con los datos de los movimientos

    Returns:
    list[str]: Lista de strings con los datos de los movimientos

    """

    with open("./data/moves.csv",mode="r") as arch:
        lines = [line.rstrip().split(",") for line in arch]
        lines.pop(0)
        return lines
    
def effectiveness_dic():
    """
    Lee el archivo effectiveness_chart.csv y devuelve un diccionario con la efectividad de los tipos de pokemones

    Returns:
    dict[str, dict[str, float]]: Diccionario con la efectividad de los tipos de pokemones

    """
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
    """
    Crea una lista de objetos de la clase Move a partir de una lista de nombres de movimientos y una lista de datos de movimientos

    Parameters:
    moves (list[str]): Lista de nombres de movimientos
    lista_moves (list): Lista de datos de movimientos

    Returns:
    list[Move]: Lista de objetos de la clase Move

    """
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
    """
    Crea un objeto de la clase Pokemon a partir de una lista de datos de pokemones y una lista de datos de movimientos
    
    Parameters:
    pokemones (list[str]): Lista de datos de pokemones
    lista_moves (list): Lista de datos de movimientos

    Returns:
    Pokemon: Objeto de la clase Pokemon

    """
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
        
        poke =  Pokemon(pokedex_number, name, type1, type2, hp, attack, deffense, sp_attack, sp_defense, speed, generation, height, weight, is_legendary, obj_moves, level)

        if not poke.is_legendary:
            return poke

  
def crear_equipo(pokemones: list[str], lista_moves):
    """
    Crea un equipo de 6 pokemones no legendarios y sin repetidos

    Parameters:
    pokemones (list[str]): Lista de datos de pokemones
    lista_moves (list): Lista de datos de movimientos
    
    Returns:
    Team: Objeto de la clase Team
    
    """
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
    """
    Crea una población de equipos de pokemones

    Parameters:
    cant_equipos (int): Cantidad de equipos a crear
    pokemones (list[str]): Lista de datos de pokemones
    lista_moves (list): Lista de datos de movimientos
    
    Returns:
    list[Team]: Lista de objetos de la clase Team

    """
    poblacion = []
    for i in range(cant_equipos):
        equipo = crear_equipo(pokemones, lista_moves)
        equipo.name = f'Equipo {i+1}'
        poblacion.append(equipo)
    return poblacion

def simu_batallas(poblacion, rivales, efectividad):
    """
    Simula las batallas entre los equipos de la población y los rivales

    Parameters:
    poblacion (list[Team]): Lista de equipos de pokemones
    rivales (list[Team]): Lista de equipos de pokemones rivales
    efectividad (dict[str, dict[str, float]]): Diccionario con la efectividad de los tipos de pokemones

    Returns:
    dict[Team, int]: Diccionario con la cantidad de victorias de cada equipo ordenadas de mayor a menor
    
    """
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
    '''
    Selecciona los "X" mejores equipos de la poblacion y completa la poblacion con nuevos equipos randoms
    Parameters:
    corte_seleccion (int): Cantidad de equipos a seleccionar
    poblacion (list[Team]): Lista de equipos de pokemones
    victorias (dict[int]): Diccionario con la cantidad de victorias de cada equipo
    pokemones (list[str]): Lista de datos de pokemones
    lista_moves (list): Lista de datos de movimientos

    Returns:
    list[Team]: Lista de equipos de pokemones
    list[Team]: Lista de los "X" mejores equipos
    '''

    # Seleccionar los "X" mejores equipos
    mejores_equipos = list(victorias.keys())[:corte_seleccion]

    # Generar "X" equipos randoms (rellenar hasta armar una poblacion de 50)
    nuevos_equipos = crear_poblaciones(50 - corte_seleccion, pokemones,lista_moves)

    # Actualizar la poblacion
    poblacion = mejores_equipos + nuevos_equipos
    

    return poblacion, mejores_equipos

def asegurar_unicos(nuevo_team, pokemones, lista_moves):
    '''
    Asegura que el equipo tenga 6 pokemones unicos
    Parameters:
    nuevo_team (list[Pokemon]): Lista de pokemones
    pokemones (list[str]): Lista de datos de pokemones
    lista_moves (list): Lista de datos de movimientos

    Returns:
    list[Pokemon]: Lista de pokemones unicos
    '''
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
    '''
    Cruza los pokemones de los equipos de la poblacion con una probabilidad del 70%
    Parameters:
    poblacion (list[Team]): Lista de equipos de pokemones
    pokemones (list[str]): Lista de datos de pokemones
    lista_moves (list): Lista de datos de movimientos

    Returns:
    list[Team]: Lista de equipos de pokemones cruzados
    '''
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
    '''
    Funcion auxiliar para el desarrollo del TP
    Imprime los equipos y sus victorias
    Parameters:
    dict_victorias (dict[Team, int]): Diccionario con la cantidad de victorias de cada equipo
    '''
    for equipo, victorias in dict_victorias.items():
        print(f"Equipo: {equipo.name}, Victorias: {victorias}")
        print("Pokémon en el equipo:")
        for pokemon in equipo.pokemons: 
            print(f"- {pokemon.name}")

def mutar(equipo, pokemones,lista_moves):
    '''
    Muta un equipo de pokemones con una probabilidad del 3%
    Parameters:
    equipo (Team): Equipo de pokemones
    pokemones (list[str]): Lista de datos de pokemones
    lista_moves (list): Lista de datos de movimientos

    Returns:
    Team: Equipo de pokemones mutado
    '''
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
    '''
    Muta la poblacion de equipos de pokemones
    Parameters:
    poblacion (list[Team]): Lista de equipos de pokemones
    pokemones (list[str]): Lista de datos de pokemones
    lista_moves (list): Lista de datos de movimientos
    
    Returns:
    list[Team]: Lista de equipos de pokemones mutados
    '''
    
    for i in range(len(poblacion)):
        
        poblacion[i] = mutar(poblacion[i], pokemones,lista_moves)
    
    return poblacion

def algoritmo_genetico(corte_seleccion, lista_moves, pokemones, efectividad, poblacion, rivales):
    '''
    Implementa el algoritmo genético para la evolución de los equipos de pokemones
    Parameters:
    corte_seleccion (int): Cantidad de equipos a seleccionar
    lista_moves (list): Lista de datos de movimientos
    pokemones (list[str]): Lista de datos de pokemones
    efectividad (dict[str, dict[str, float]]): Diccionario con la efectividad de los tipos de pokemones
    poblacion (list[Team]): Lista de equipos de pokemones
    rivales (list[Team]): Lista de equipos de pokemones rivales

    Returns:
    list[Team]: Lista de equipos de pokemones
    list[Team]: Lista de equipos de pokemones rivales
    dict[Team, int]: Diccionario con la cantidad de victorias de cada equipo ordenadas de mayor a menor
    '''
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
    '''
    Crea un archivo CSV con el nombre de los equipos y sus pokemones
    Parameters:
    name_archivo (str): Nombre del archivo
    '''
    with open(name_archivo, mode = 'w',newline='') as archivo:
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerow(['Generacion','Aptitud','Team Name','Starter','Pokemon1','Pokemon2','Pokemon3','Pokemon4','Pokemon5'])

def escritura_best_teams(best_teams:list[Team],best_points:list[int],name_archivo:str,gen:int):
    '''
    Escribe en un archivo CSV los mejores equipos de la generacion
    Parameters:
    best_teams (list[Team]): Lista de equipos de pokemones
    best_points (list[int]): Lista de puntos de los equipos
    name_archivo (str): Nombre del archivo
    gen (int): Numero de la generacion
    '''
    with open(name_archivo, mode ='a',newline='') as arch:
        escritor_csv = csv.writer(arch)
        for equipo, wins in zip(best_teams,best_points):
            pokes_str = [poke.name for poke in equipo.pokemons]
            escritor_csv.writerow([gen+1,wins,equipo.name]+ pokes_str)

def crear_archivo_cant_pokemons(name_archivo:str):
    '''
    Crea un archivo CSV con la cantidad de pokemones de cada generacion
    Parameters:
    name_archivo (str): Nombre del archivo
    '''
    with open(name_archivo, mode = 'w',newline='') as archivo:
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerow(['Generacion','Cantidad','Pokemon'])

def contar_cantidad_apariciones(poblacion:list[Team], cantidad_pokemons:dict,archivo:str, generacion:int):
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
    
    with open(archivo, mode='a', newline='') as arch:
        writer = csv.writer(arch)
        
        fila = [generacion+1]
        for pokemon, cantidad in cantidad_pokemons.items():
            fila.extend([cantidad, pokemon])
        
        writer.writerow(fila)  

def crear_archivo_tipos(name_archivo:str):
    '''
    Crea un archivo CSV con la cantidad de pokemones de cada tipo de la ultima generacion
    Parameters:
    name_archivo (str): Nombre del archivo
    '''

    with open(name_archivo, mode = 'w',newline='') as archivo:
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerow(['Tipo','Cantidad'])

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

def cargar_tipos_en_csv(diccionario_tipos: dict, name_archivo: str):
    """
    Carga los tipos de pokemones y su cantidad en un archivo CSV
    Parameters:
    diccionario_tipos (dict): Diccionario con la cantidad de pokemones de cada tipo
    name_archivo (str): Nombre del archivo
    """
    with open(name_archivo, mode='a', newline='') as archivo:  
        escritor_csv = csv.writer(archivo)
        for tipo, cantidad in diccionario_tipos.items():
            escritor_csv.writerow([tipo, cantidad])
    
def escritura_mejor_team(name_archivo: str, dict_vict: dict):
    """
    Escribe en un archivo CSV el mejor equipo de la ultima generacion
    Parameters:
    name_archivo (str): Nombre del archivo
    dict_vict (dict): Diccionario con la cantidad de victorias de cada equipo
    """

    with open(name_archivo, mode = 'w',newline='') as archivo:
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerow(['starter','pokemon1','pokemon2', 'pokemon2', 'pokemon3', 'pokemon4', 'pokemon5'])
        best_team = list(dict_vict.keys())[0]
        lista_pok = []
        for pokemon in best_team.pokemons:
            lista_pok.append(pokemon.name)
        escritor_csv.writerow(lista_pok)
    return best_team

def algoritmo_completo(corte_seleccion: int, generaciones: int, lista_moves, pokemones, efectividad, poblacion, rivales):
    '''
    Implementa el algoritmo genético para la evolución de los equipos de pokemones
    Parameters:
    corte_seleccion (int): Cantidad de equipos a seleccionar
    generaciones (int): Cantidad de generaciones
    lista_moves (list): Lista de datos de movimientos
    pokemones (list[str]): Lista de datos de pokemones
    efectividad (dict[str, dict[str, float]]): Diccionario con la efectividad de los tipos de pokemones
    poblacion (list[Team]): Lista de equipos de pokemones
    rivales (list[Team]): Lista de equipos de pokemones rivales

    Returns:
    list[Team]: Lista de equipos de pokemones
    list[Team]: Lista de equipos de pokemones rivales
    dict[Team, int]: Diccionario con la cantidad de victorias de cada equipo ordenadas de mayor a menor
    '''
    for gen in tqdm(range(generaciones), desc="Procesando generaciones"):

        nueva_poblacion, nuevos_rivales, dict_vict_combinadas = algoritmo_genetico(corte_seleccion, lista_moves, pokemones, efectividad, poblacion, rivales)
        poblacion = nueva_poblacion
        rivales = nuevos_rivales
        mejores_10_nombres = list(dict_vict_combinadas.keys())[:10]
        mejores_10_puntos = [dict_vict_combinadas[nombre] for nombre in mejores_10_nombres]
        escritura_best_teams(mejores_10_nombres,mejores_10_puntos,"Best_teams_x_generation.csv",gen)
        dict_poke_cantidad = {}
        contar_cantidad_apariciones(poblacion,dict_poke_cantidad,"Cantidad_pokemones_x_gen.csv", gen)
        
        print(f'Generación {gen+1}')

    return nueva_poblacion, nuevos_rivales, dict_vict_combinadas

def escritura_stats_best_team(best_team: Team, name_archivo: str):
    """
    Escribe en un archivo CSV las estadísticas del mejor equipo de la última generación
    Parameters:
    best_team (Team): Mejor equipo de la última generación
    name_archivo (str): Nombre del archivo
    """

    with open(name_archivo, mode='w', newline='') as archivo:
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerow(['Name','Max Hp', 'Attack', 'Defense', 'Sp.Attack', 'Sp.Defense', 'Speed'])
        for pokemon in best_team.pokemons:
            stats = [pokemon.name,pokemon.max_hp, pokemon.attack, pokemon.defense, pokemon.sp_attack, pokemon.sp_defense, pokemon.speed]
            escritor_csv.writerow(stats)

#------------------------------------------------------------------------------------------------------------------------------------#
#                                               FUNCIONES CON MULTIPROCESSING
#------------------------------------------------------------------------------------------------------------------------------------#
import multiprocessing

# Mismas funciones pero con multiprocessing para acelerar la ejecucion del codigo

""" Si se desea correr el codigo con multiprocessing, se debe unicamente cambiar en el main la funcion "agortimo_completo" por 
"algorimo_completoMulti" y agregar al final como parametro de entrada de la funcion "num_procesos" """

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
    '''
    Implementa el algoritmo genético para la evolución de los equipos de pokemones
    Parameters:
    corte_seleccion (int): Cantidad de equipos a seleccionar
    generaciones (int): Cantidad de generaciones
    lista_moves (list): Lista de datos de movimientos
    pokemones (list[str]): Lista de datos de pokemones
    efectividad (dict[str, dict[str, float]]): Diccionario con la efectividad de los tipos de pokemones
    poblacion (list[Team]): Lista de equipos de pokemones
    rivales (list[Team]): Lista de equipos de pokemones rivales

    Returns:
    list[Team]: Lista de equipos de pokemones
    list[Team]: Lista de equipos de pokemones rivales
    dict[Team, int]: Diccionario con la cantidad de victorias de cada equipo ordenadas de mayor a menor
    '''
    for gen in tqdm(range(generaciones), desc="Procesando generaciones"):

        nueva_poblacion, nuevos_rivales, dict_vict_combinadas = algoritmo_geneticoMulti(corte_seleccion, lista_moves, pokemones, efectividad, poblacion, rivales,num_procesos)
        poblacion = nueva_poblacion
        rivales = nuevos_rivales
        mejores_10_nombres = list(dict_vict_combinadas.keys())[:10]
        mejores_10_puntos = [dict_vict_combinadas[nombre] for nombre in mejores_10_nombres]
        escritura_best_teams(mejores_10_nombres,mejores_10_puntos,"Best_teams_x_generation.csv",gen)
        dict_poke_cantidad = {}
        contar_cantidad_apariciones(poblacion,dict_poke_cantidad,"Cantidad_pokemones_x_gen.csv", gen)
        print(f'Generación {gen+1}')

    return nueva_poblacion, nuevos_rivales, dict_vict_combinadas