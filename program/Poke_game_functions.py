from pokemon import Pokemon
from move import Move
from team import Team
import csv
import combat
import Archivo_funciones as fun
from tqdm import tqdm


kanto_teams = {
                "Will": ("Bronzong", "Jynx", "Grumpig", "Slowbro", "Gardevoir", "Xatu"),
                "Koga": ("Skunktank", "Toxicroak", "Swalot", "Venomoth", "Muk", "Crobat"),
                "Bruno": ("Hitmontop", "Hitmonlee", "Hariyama", "Machamp", "Lucario", "Hitmonchan"),
                "Karen": ("Weavile", "Spiritomb", "Honchkrow", "Umbreon", "Houndoom", "Absol"),
                "Lance": ("Salamence", "Garchomp", "Dragonite", "Charizard", "Altaria", "Gyarados")
                }

lista_moves = fun.lista_movimientos()
pokemones = fun.lista_pokemones()
efectividad = fun.effectiveness_dic()

def create_self_team(file_name: str)->Team:
    with open(file_name, mode = 'r') as file:
        team_line = file.readlines()[1].rstrip().split(',')
    return team_por_nombre('Self', team_line)

def crear_movimientos(moves: list[str], lista_moves: list)->list[Move]:
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

def crear_pokemon(indice,pokemones: list[str], lista_moves: list)->Pokemon:
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

def pokemon_por_nombre(nombre: str, pokemones: list[str] = pokemones, lista_moves: list[list[str]]= lista_moves)->Pokemon:
    #Buscar indice
    indice = 0
    for i in range(len(pokemones)-1):
        if nombre == pokemones[i].split(",")[1]:
            indice = i
    return crear_pokemon(indice, pokemones, lista_moves)

def team_por_nombre(nombre_equipo:str, lista_nombre: list[str], pokemones: list[str] = pokemones, lista_moves: list[list[str]]= lista_moves)->Team:
    equipo = []
    for nombre in lista_nombre:
        pokemon = pokemon_por_nombre(nombre)
        equipo.append(pokemon)
    return Team(nombre_equipo, equipo)


