import Archivo_funciones as fun
import pygame as pg
import combat
import os
from pokemon import Pokemon
from team import Team
from move import Move

pg.init()
pg.display.set_caption('SIMU')

POKE_LIST = [line.rstrip().split(',') for line in fun.lista_pokemones()] ### csv pokemon list with all info separeted for each pokemon
EFFECTIVENESS = fun.create_effectiveness_dict()
MOVES = fun.lista_movimientos()

SIZE = (1060, 596)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
SCREEN = pg.display.set_mode(SIZE)
FONT = pg.font.SysFont(None, 55)        #sets fonts for text

KANTO_TEAMS = {
                "Will": ("Bronzong", "Jynx", "Grumpig", "Slowbro", "Gardevoir", "Xatu"),
                "Koga": ("Skunktank", "Toxicroak", "Swalot", "Venomoth", "Muk", "Crobat"),
                "Bruno": ("Hitmontop", "Hitmonlee", "Hariyama", "Machamp", "Lucario", "Hitmonchan"),
                "Karen": ("Weavile", "Spiritomb", "Honchkrow", "Umbreon", "Houndoom", "Absol"),
                "Lance": ("Salamence", "Garchomp", "Dragonite", "Charizard", "Altaria", "Gyarados")
                }

def create_self_team(file_name: str)->Team:
    with open(file_name, mode = 'r') as file:
        team_line = file.readlines()[1].rstrip().split(',')
    return team_por_nombre('YOU', team_line)

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
        linea = pokemones[indice]
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

def pokemon_por_nombre(nombre: str, pokemones: list[str] = POKE_LIST, lista_moves: list[list[str]]= MOVES)->Pokemon:
    #Buscar indice
    indice = 0
    for i in range(len(pokemones)-1):
        if nombre == pokemones[i][1]:
            indice = i
    return crear_pokemon(indice, pokemones, lista_moves)

def team_por_nombre(nombre_equipo:str, lista_nombre: list[str], pokemones: list[str] = POKE_LIST, lista_moves: list[list[str]]= MOVES)->Team:
    equipo = []
    for nombre in lista_nombre:
        pokemon = pokemon_por_nombre(nombre)
        equipo.append(pokemon)
    return Team(nombre_equipo, equipo)


def reset_screen()->None: 
    """Reffills screen with total black to clear scene and free up space on runtime"""
    SCREEN.fill(BLACK)
    pg.display.flip()

def wait_for_no_keys()->None:
    """
    It simply pause the program till every single key is not pressed.
    Only then continues running
    """
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
        if not any(pg.key.get_pressed()): break
    
def wait_for_key_pressed():
    """
    It simply pause the program till every single key is not pressed.
    Only then continues running
    """
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
        if any(pg.key.get_pressed()): return pg.key.get_pressed()

def check_quit()->None:
    """
    Checks if program is terminated
    """
    for event in pg.event.get():
        if event.type == pg.QUIT: pg.quit()

def display_message(msg:str, position: tuple[int, int], color: tuple[int, int, int], rescale: float | None = None)->None:
    message = FONT.render(msg, True, color)
    if rescale: message = pg.transform.scale_by(message, rescale)
    message_rect = message.get_rect(center = position)   
    SCREEN.blit(message, message_rect)
    pg.display.flip()

def rescale_image(image: pg.Surface, target_size: tuple[int, int])->None:
    image_width, image_height = image.get_size()
    image_ratio = image_width / image_height
    target_width, target_height = target_size
    target_ratio = target_width / target_height
    if target_ratio > image_ratio:
        new_height = target_height
        new_width = int(new_height * image_ratio)
    else:
        new_width = target_width
        new_height = int(new_width / image_ratio)
    return pg.transform.scale(image, (new_width, new_height))

def draw_bg(name: str)->None:
    reset_screen()
    bg = pg.image.load(os.path.join("data", "imgs", "simu", name))
    bg = rescale_image(bg, SIZE)
    bg_rect = bg.get_rect(center = (SIZE[0]//2, SIZE[1]//2))         
    SCREEN.blit(bg, bg_rect)
    pg.display.flip()

def draw_poke_img(name: str, position: tuple[int, int], rescale: float | None = None)->None:
    """
    ## Draws the image of a pokeom given:
    name (name of the file to open it)
    position (a set-like of coordinates to place the image)
    rescale (posible resizing scalar)
    """
    img = pg.image.load(os.path.join("data", "imgs", name))
    if rescale: img = img = pg.transform.scale(img, (int(img.get_width() * rescale), int(img.get_height() * rescale)))
    img_rect = img.get_rect(center = position)
    SCREEN.blit(img, img_rect)
    pg.display.flip()


def draw_pokemons_menu(team: Team)->None:
     for poknum, pokemon in enumerate(team.pokemons):
        for i in range(len(POKE_LIST)):
            if POKE_LIST[i][1]==pokemon.name: 
                img_index = int(POKE_LIST[i][0])
                break
        if img_index<10: img_index = f'00{str(img_index)}.png'
        elif img_index<100: img_index = f'0{str(img_index)}.png'
        else: img_index = f'{str(img_index)}.png'
        draw_poke_img(img_index, ((1+poknum)*SIZE[0]//7, SIZE[1]//2))
        display_message(pokemon.name, ((1+poknum)*SIZE[0]//7, SIZE[1]//2+100), WHITE, 0.5)
     
def draw_poketeam_battleground(team: Team, position_1: tuple[int, int])->None:
    for poknum, pokemon in enumerate(team.pokemons):
        for i in range(len(POKE_LIST)):
            if POKE_LIST[i][1]==pokemon.name: 
                img_index = int(POKE_LIST[i][0])
                break
        if img_index<10: img_index = f'00{str(img_index)}.png'
        elif img_index<100: img_index = f'0{str(img_index)}.png'
        else: img_index = f'{str(img_index)}.png'
        if team.current_pokemon_index != poknum:
            draw_poke_img(img_index, (position_1[0]+(1+poknum)*(SIZE[0]-position_1[0]*2)//6, position_1[1]), rescale=0.5)
            if team.name == 'YOU':
                draw_pokemons_health_bar(pokemon, (position_1[0]+(1+poknum)*(SIZE[0]-position_1[0]*2)//6,position_1[1]-50))
            else:
                draw_pokemons_health_bar(pokemon, (position_1[0]+(1+poknum)*(SIZE[0]-position_1[0]*2)//6,position_1[1]+50))
        else:
            draw_poke_img(img_index, position=(400,350) if team.name == 'YOU' else (650, 280))
            draw_pokemons_health_bar(pokemon, position=(400, 250) if team.name == 'YOU' else (650, 200))
    pg.display.flip()

def draw_move(team1: Team, team2: Team):
    wait_for_no_keys()
    next_action = team1.get_next_action(team2, EFFECTIVENESS)
    if next_action[0] == 'attack':
        move = next_action[1]
        damage = move.get_damage(team1.get_current_pokemon(), team2.get_current_pokemon(), EFFECTIVENESS)
        display_message(move.name.upper(), position=(SIZE[0]//2, SIZE[1]//2-130), color=WHITE)
        display_message(str(int(damage)), position=(SIZE[0]//2, SIZE[1]//2-80), color=WHITE)
        team1.do_action(next_action[0], next_action[1], team2, EFFECTIVENESS)
    elif next_action[0] == 'switch':
        display_message('SWITCHING', position=(SIZE[0]//2, SIZE[1]//2-130), color=WHITE)
        team1.do_action(next_action[0], next_action[1], team2, EFFECTIVENESS)
    elif next_action[0] == 'skip':
        display_message('SKIPPING', position=(SIZE[0]//2, SIZE[1]//2-130), color=WHITE)
        team1.do_action(next_action[0], next_action[1], team2, EFFECTIVENESS)
    pg.display.flip()

     
def draw_pokemons_health_bar(pokemon: Pokemon,  position: tuple[int, int])->None:
    max_hp = pokemon.max_hp
    current_hp = pokemon.current_hp
    bar_length = (max_hp / pokemon.max_hp) * 100
    fill = (current_hp / max_hp) * bar_length
    left_x = position[0] - bar_length // 2
    top_y = position[1] - 10 // 2
    outline_rect = pg.Rect(left_x, top_y, bar_length, 10)
    fill_rect = pg.Rect(left_x, top_y, fill, 10)
    empty_rect = pg.Rect(left_x + fill, top_y, bar_length - fill, 10)
    pg.draw.rect(SCREEN, (0, 0, 0), empty_rect)
    pg.draw.rect(SCREEN, (0, 255, 0), fill_rect)
    pg.draw.rect(SCREEN, (255, 255, 255), outline_rect, 2)
    pg.display.flip()

def menu()->None:
    reset_screen()
    draw_bg('menu_bg.jpg')
    while True:
        pg.display.update()
        display_message("PRESS ANY KEY TO CONTINUE", (SIZE[0]//2, SIZE[1]//2), color=WHITE)
        for event in pg.event.get():
                if event.type == pg.QUIT: pg.quit()
                if event.type == pg.KEYDOWN: return None

def select_kanto_champs()->str:
    reset_screen()
    draw_bg('kanto_champions.jpg')
    display_message("SELECT YOUR OPPONENT", (SIZE[0]//2, SIZE[1]//2), color=WHITE)
    wait_for_no_keys()
    selected = None
    while not selected:         #select kanto champion to fight against
        key_pressed = pg.key.get_pressed()
        if key_pressed[pg.K_1]: selected = 'Will'
        elif key_pressed[pg.K_2]: selected = 'Koga'
        elif key_pressed[pg.K_3]: selected = 'Lance'
        elif key_pressed[pg.K_4]: selected = 'Bruno'
        elif key_pressed[pg.K_5]: selected = 'Karen'
        check_quit()
    #design screen displaying which team has been choosen
    return selected


def select_starter(team: Team)->int:
    reset_screen()
    draw_bg('loading_bg.jpg')
    display_message("SELECT YOUR STARTER POKEMON", (SIZE[0]//2, SIZE[1]//2-150), color=WHITE)
    draw_pokemons_menu(team)
    wait_for_no_keys()
    selected = None
    while selected == None:
        key_pressed = pg.key.get_pressed()
        if key_pressed[pg.K_1]: selected = 0
        elif key_pressed[pg.K_2]: selected = 1
        elif key_pressed[pg.K_3]: selected = 2
        elif key_pressed[pg.K_4]: selected = 3
        elif key_pressed[pg.K_5]: selected = 4
        elif key_pressed[pg.K_6]: selected = 5
        check_quit()
    #blink the image of the selected pokemon
    return selected

def fight(team1: Team, team2: Team):
    winner = None
    team_turn = 0
    while not winner:
        team_turn+=1
        clock = pg.time.Clock()
        clock.tick(30)
        wait_for_key_pressed()
        draw_bg('battle_bg.jpg')
        draw_poketeam_battleground(team1,(200, SIZE[1]-50))
        draw_poketeam_battleground(team2,(200, 50))
        wait_for_no_keys()
        key_pressed = wait_for_key_pressed()
        if key_pressed[pg.K_ESCAPE]:
            winner = combat.get_winner(team1, team2, EFFECTIVENESS)
            wait_for_no_keys()
        else: 
            draw_move(team1 = team1 if team_turn%2==1 else team2, team2 = team2 if team_turn%2==1 else team1)
            wait_for_no_keys()
        check_quit()
        if any(pokemon.current_hp > 0 for pokemon in team1.pokemons) and not any(pokemon.current_hp > 0 for pokemon in team2.pokemons): winner = team1
        elif  any(pokemon.current_hp > 0 for pokemon in team2.pokemons) and not any(pokemon.current_hp > 0 for pokemon in team1.pokemons): winner = team2
    return winner


def display_winner(team: Team):
    draw_bg('loading_bg.jpg')
    wait_for_key_pressed()
    wait_for_no_keys()
    display_message("THE WINNER TEAM IS", (SIZE[0]//2, SIZE[1]//2), color=WHITE, rescale=2.5)
    wait_for_key_pressed()
    wait_for_no_keys()
    draw_bg('loading_bg.jpg')
    display_message(team.name, (SIZE[0]//2, SIZE[1]//2-150), color=WHITE, rescale=2)
    draw_pokemons_menu(team)
    wait_for_key_pressed()
    wait_for_no_keys()



def main():
    reset_screen()
    menu()
    selected_champ = select_kanto_champs()
    your_team = create_self_team('best_team.csv')
    op_team = team_por_nombre(selected_champ, KANTO_TEAMS[selected_champ])
    starter_index = select_starter(your_team)
    your_team.change_pokemon(starter_index)
    winner = fight(your_team, op_team)
    display_winner(winner)
    pg.quit()
            

if __name__ == '__main__':
    main()