import pygame as pg
import Poke_game_functions as fights
from pokemon import Pokemon
from team import Team
import combat
import os

pg.init()
pg.display.set_caption('SIMU')

SIZE = (1060, 596)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
SCREEN = pg.display.set_mode(SIZE)
FONT = pg.font.SysFont(None, 55)        #sets fonts for text

reset_screen = lambda : SCREEN.fill(BLACK)
"""Reffills screen with total black to clear scene and free up space on runtime"""


"""
    For combat logging:
    ## get_damage() calculates the damage that a pokemon would do to another
    ## combat.__faint_change__() when hp=0, changes the current pokemon
    ## team has everything needed to actually change the state of team and pokemons on get_next_action and do_action 
"""

"""
    #### Events are handled one at a time by functions (menu, opponent select and starter select)
    every event defines:
    1) Background
    2) messages displayed
    3) 
    
"""
def display_message(msg:str, position: tuple[int, int], color: tuple[int, int, int], rescale: float = 1)->None:
    message = FONT.render(msg, True, color)
    if rescale != 1: message = pg.transform.scale_by(message, rescale)
    message_rect = message.get_rect(center = position)   
    SCREEN.blit(message, message_rect)

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
    bg = pg.image.load(os.path.join("data", "imgs", "simu", name))
    bg = rescale_image(bg, SIZE)
    bg_rect = bg.get_rect(center = (SIZE[0]//2, SIZE[1]//2))         
    SCREEN.blit(bg, bg_rect)
    pg.display.update()

def draw_img(name: str, position: tuple[int, int], rescale: float = 1.0 )->None:
    """
    ## Draws an image onscreen given:
    name (name of the file to open it)
    position (a set-like of coordinates to place the image)
    rescale (posible resizing scalar)
    """
    img = pg.image.load(os.path.join("data", "imgs", "simu", name))
    if rescale != 1: img = pg.transform.scale_by(img, rescale)
    img_rect = img.get_rect(center = (position[0], position[1]))
    SCREEN.blit(img, img_rect)
    pg.display.update()

def draw_pokemons_menu(team: Team):
     for poknum, pokemon in enumerate(team.pokemons):
        img_index = fights.pokemones.index(pokemon.name)+1
        if img_index<10:
            img_index = "00".join(str(img_index))
        elif img_index<100: 
             img_index = "0".join(str(img_index))
        else:
             img_index = str(img_index)
        draw_img(img_index.join('.png'), ((1+poknum)*SIZE[0]//7, SIZE[1]//2))
        display_message(pokemon.name, ((1+poknum)*SIZE[0]//7, SIZE[1]//2+100), WHITE, 0.5)
     
def draw_pokemons_fight(team: Team, position_1: tuple[int, int], rescale: float = 1):
     for poknum, pokemon in enumerate(team.pokemons):
        img_index = fights.pokemones.index(pokemon.name)+1
        if img_index<10:
            img_index = "00".join(str(img_index))
        elif img_index<100: 
             img_index = "0".join(str(img_index))
        else:
             img_index = str(img_index)
        draw_img(img_index.join('.png'), ((1+poknum)*position_1[0]//7, position_1[1]//2))
        display_message(pokemon.name, ((1+poknum)*position_1[0]//7, position_1[1]//2+100), WHITE, 0.5)

def draw_move():
     pass
     
def draw_pokemons_health_bar(pokemon: Pokemon,  position: tuple[int, int])->None:
    BAR_LENGTH = 50
    BAR_HEIGHT = 5
    fill = (pokemon.current_hp / 100) * BAR_LENGTH
    outline_rect = pg.Rect(position[0], position[1], BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(position[0], position[1], fill, BAR_HEIGHT)
    pg.draw.rect(SCREEN, (255, 0, 0), fill_rect)
    pg.draw.rect(SCREEN, (255, 255, 255), outline_rect, 2)
    pg.display.update()

def menu()->None:
    reset_screen
    draw_bg('menu_bg.jpg')
    while True:
        pg.display.update()
        display_message("PRESS ANY KEY TO CONTINUE", (SIZE[0]//2, SIZE[1]//2), color=WHITE)
        #resize bg image
        for event in pg.event.get():
                if event.type == pg.QUIT: pg.quit()
                if event.type == pg.KEYDOWN: return None

def select_kanto_champs()->str:
    reset_screen
    draw_bg('kanto_champions.jpg')
    display_message("SELECT YOUR OPPONENT", (SIZE[0]//2, SIZE[1]//2), color=WHITE)
    pg.display.update()
    selected = False
    while selected == False:         #select kanto champion to fight against
        key_pressed = pg.key.get_pressed()
        if key_pressed[pg.K_1]: selected = 'Will'
        elif key_pressed[pg.K_2]: selected = 'Koga'
        elif key_pressed[pg.K_3]: selected = 'Lance'
        elif key_pressed[pg.K_4]: selected = 'Bruno'
        elif key_pressed[pg.K_5]: selected = 'Karen'
        for event in pg.event.get():
                if event.type == pg.QUIT: pg.quit()
    #design screen displaying which team has been choosen


    return selected


def select_starter(team: Team)->int:
    reset_screen
    draw_bg('loading_bg.jpg')
    display_message("SELECT YOUR STARTER POKEMON", (SIZE[0]//2, SIZE[1]//2-100), color=WHITE)
    draw_pokemons_menu(team)
    pg.display.update()
    selected = False
    while selected == False:
        key_pressed = pg.key.get_pressed()
        if key_pressed[pg.K_1]: selected = 1
        elif key_pressed[pg.K_2]: selected = 2
        elif key_pressed[pg.K_3]: selected = 3
        elif key_pressed[pg.K_4]: selected = 4
        elif key_pressed[pg.K_5]: selected = 5
        elif key_pressed[pg.K_6]: selected = 6
        for event in pg.event.get():
                if event.type == pg.QUIT: pg.quit()
    #blink the image of the selected pokemon
    return selected

def fight():
    reset_screen
    draw_bg('battle_bg.jpg')
    while True:
        pg.display.update()


def winner():
    pass


def main():
    reset_screen
    clock = pg.time.Clock()
    clock.tick(60)
    menu()
    selected_champ = select_kanto_champs()
    your_team = fights.team_por_nombre("Your Team", fights.self_team, fights.pokemones, fights.lista_moves)
    op_team = fights.team_por_nombre(selected_champ, fights.kanto_teams[selected_champ],fights.pokemones, fights.lista_moves)
    starter_index = select_starter(your_team)
    pg.quit()
            

if __name__ == '__main__':
    main()