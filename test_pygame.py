import pygame
import pygame_gui
from constants import *


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HIGHT))
manager = pygame_gui.UIManager((800, 450))
running = True
clock = pygame.time.Clock()

while running:
    #цикл обработки событий
    time_delta = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(0)
            confrimation_dialog = pygame_gui.windows.UIConfirmationDialog(
                rect=pygame.Rect((0, 0), (50, 50)),
                manager=manager,
                window_title='ddd',
                action_long_desc='ss',
                action_short_name='ok',
                blocking=True
            )
        if event.type == pygame.USEREVENT:
            if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                running = False

    pygame.display.flip()

pygame.quit()
