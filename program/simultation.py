import pygame
import os
import combat

pygame.init()
pygame.display.set_caption('SIMU')

SIZE = (1060, 596)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
SCREEN = pygame.display.set_mode(SIZE)
FONT = pygame.font.SysFont(None, 55)        #sets fonts for text

"""
    #### Events are handled one at a time by functions (menu, opponent select and starter select)
    every event defines:
    1) Background
    2) messages displayed
    3) 
    
"""

kanto_teams = {
                "Will": ("Bronzong", "Jynx", "Grumpig", "Slowbro", "Gardevoir", "Xatu"),
                "Koga": ("Skunktank", "Toxicroak", "Swalot", "Venomoth", "Muk", "Crobat"),
                "Bruno": ("Hitmontop", "Hitmonlee", "Hariyama", "Machamp", "Lucario", "Hitmonchan"),
                "Karen": ("Weavile", "Spiritomb", "Honchkrow", "Umbreon", "Houndoom", "Absol"),
                "Lance": ("Salamence", "Garchomp", "Dragonite", "Charizard", "Altaria", "Gyarados")
                }

def rescale_image(image, target_size: tuple[int, int]):
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
    return pygame.transform.scale(image, (new_width, new_height))

def display_message(msg:str, position: tuple[int, int], color, size: int=0):
    message = FONT.render(msg, True, color)
    message_rect = message.get_rect()
    message_rect.center = (position[0], position[1])     
    SCREEN.blit(message, message_rect)

def draw_bg(name: str):
    bg = pygame.image.load(os.path.join("data", "imgs", "simu", name))
    bg = rescale_image(bg, SIZE)
    bg_rect = bg.get_rect()
    bg_rect.center = (SIZE[0]//2, SIZE[1]//2)           
    SCREEN.blit(bg, bg_rect)
    pygame.display.update()



def menu():
    draw_bg('menu_bg.jpg')
    while True:
        pygame.display.update()
        display_message("PRESS ANY KEY TO CONTINUE", (SIZE[0]//2, SIZE[1]//2), color=WHITE)
        #resize bg image
        for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit()
                if event.type == pygame.KEYDOWN: return None

def select_kanto_champs()->str:
    draw_bg('kanto_champions.jpg')
    selected = False
    while selected == False:         #select kanto champion to fight against
        pygame.display.update()
        display_message("SELECT YOUR OPPONENT", (SIZE[0]//2, SIZE[1]//2), color=WHITE)
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_1]: selected = 'Will'
        elif key_pressed[pygame.K_2]: selected = 'Koga'
        elif key_pressed[pygame.K_3]: selected = 'Lance'
        elif key_pressed[pygame.K_4]: selected = 'Bruno'
        elif key_pressed[pygame.K_5]: selected = 'Karen'
        for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit()
    #design screen displaying which team has been choosen
    return selected

def select_starter():
    pass
def fight():
    draw_bg('battle_bg.jpg')
    while True:
        pygame.display.update()

    pass

def winner():
    pass
def check_quit():
    pass

def main():
    SCREEN.fill(BLACK)
    clock = pygame.time.Clock()
    clock.tick(60)
    menu()
    slected_champ = select_kanto_champs()
    your_team = 
    op_team = 

    pygame.quit()
            

if __name__ == '__main__':
    main()