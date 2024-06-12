import random

from pokemon import Pokemon

from move import Move

from team import Team

#Almaceno todas los pokemones en una lista 

def lectura_pokemones(archivo:str):
    with open(archivo, 'r') as file:
        pokemones = file.readlines()[1:]
    return pokemones

pokemones = lectura_pokemones('./data/pokemons.csv')

ataques = lectura_pokemones('./data/moves.csv')

efectividad = lectura_pokemones('./data/effectiveness_chart.csv')

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

    return Team('Team Rocket',equipo)

team = crear_equipo(pokemones)

for pokemon in team.pokemons:
    print(pokemon.name)
    

effectiveness_dict = {line.split(",")[0]: {efectividad[i].split(",")[0]: float(line.split(",")[i + 1]) for i in range(len(efectividad))} for line in efectividad}

