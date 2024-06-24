import random 
from pokemon import Pokemon
from move import Move
from team import Team
from combat import*
from Archivo_funciones import*
from tqdm import tqdm


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

def crear_pokemon(indice,pokemones: list[str], lista_moves: list):
    while True:
        linea = pokemones[indice].rstrip()
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

def pokemon_por_nombre(nombre: str,pokemones,lista_moves):
    #Buscar indice
    indice = 0
    for i in range(len(pokemones)-1):
        if nombre == pokemones[i].split(",")[1]:
            indice = i
    return crear_pokemon(indice, pokemones, lista_moves)

def team_por_nombres(nombre_equipo:str, lista_nombre: list[str], pokemones, lista_moves):
    equipo = []
    for nombre in lista_nombre:
        pokemon = pokemon_por_nombre(nombre, pokemones, lista_moves)
        equipo.append(pokemon)
    return Team(nombre_equipo, equipo)


lista_moves = lista_movimientos()
pokemones = lista_pokemones()
efectividad = effectiveness_dic()

#Metagross,Houndoom,Morelull,Salamence,Krookodile,Slaking
#Team1
nombre1 = 'Metagross'
nombre2 = 'Houndoom'
nombre3 = 'Morelull'
nombre4 = 'Salamence'
nombre5 = 'Krookodile'
nombre6 = 'Slaking'
nombres_team1 = [nombre1, nombre2, nombre3, nombre4, nombre5, nombre6]
#Kangaskhan,Aerodactyl,Silvally,Palossand,Metagross,Snorlax
#team2
nombre7 = 'Kangaskhan'
nombre8 = 'Aerodactyl'
nombre9 = 'Silvally'
nombre10 = 'Palossand'
nombre11 = 'Metagross'
nombre12 = 'Snorlax'
nombres_team2 = [nombre7, nombre8, nombre9, nombre10, nombre11, nombre12]


team1 = team_por_nombres("team1",nombres_team1,pokemones,lista_moves)

team2 = team_por_nombres("team2",nombres_team2,pokemones,lista_moves)

ganador = get_winner(team1, team2, efectividad)

print(ganador.name)