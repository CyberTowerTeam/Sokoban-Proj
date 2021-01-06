import pygame, pygame_gui

from constants import *

class Button():
    def __init__(self, image, active_image, position, size, pressed):
        self.image = image
        self.btn_event = 0
        self.flag = 0
        self.active_image = active_image
        self.button_images = pygame.Surface(size)
        self._rect = pygame.Rect(position, size)
        self.pressed = pressed

    def draw(self, screen):
        if self.btn_event == 0:
            screen.blit(self.image, self._rect)
        elif self.btn_event == 1:
            screen.blit(self.active_image, self._rect)

    def pressed_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.flag = 1
            if event.button == 1: # is left button clicked
                if self._rect.collidepoint(event.pos): # is mouse over button
                    self.btn_event = 0
                    if self.pressed == 0:#здесь добавлять события к кнопкам
                        pass
        elif (event.type == pygame.MOUSEBUTTONUP and self._rect.collidepoint(event.pos)) or \
                (event.type == pygame.MOUSEMOTION and self._rect.collidepoint(event.pos)) and self.flag == 0:
            self.btn_event = 1
        else:
            self.btn_event = 0
            self.flag = 0


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HIGHT))
screen.blit(SCREEN_BACKGROUND_IMAGE, (800, 450))
manager = pygame_gui.UIManager((800, 450))

START_BUTTON = Button(START_BUTTON_IMAGE_DEFAULT, START_BUTTON_IMAGE_ACTIVE, (10, 10), (200, 100), START_BUTTON_PRESSED)
LEVEL_ONE_BUTTON = Button(LEVEL1_BUTTON_IMAGE_DEFAULT, LEVEL1_BUTTON_IMAGE_ACTIVE,
                          (50, SCREEN_HIGHT - 80), (190, 60), START_BUTTON_PRESSED)
LEVEL_TWO_BUTTON = Button(LEVEL2_BUTTON_IMAGE_DEFAULT, LEVEL2_BUTTON_IMAGE_ACTIVE,
                          (305, SCREEN_HIGHT - 80), (190, 60), START_BUTTON_PRESSED)
LEVEL_THREE_BUTTON = Button(LEVEL3_BUTTON_IMAGE_DEFAULT, LEVEL3_BUTTON_IMAGE_ACTIVE,
                            (SCREEN_WIDHT - 245, SCREEN_HIGHT - 80), (190, 60), START_BUTTON_PRESSED)
running = True

while running:
    screen.blit(SCREEN_BACKGROUND_IMAGE, (0, 0))
    screen.blit(GAME_NAME, pygame.Rect((SCREEN_WIDHT - 205, 5), (200, 150)))
    #цикл обработки событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            confrimation_dialog = pygame_gui.windows.UIConfirmationDialog(
                rect=pygame.Rect((50, 50), (300, 200)),
                manager=manager,
                window_title='ddd',
                action_long_desc='ss',
                action_short_name='ok',
                blocking=True
            )
        if event.type == pygame.USEREVENT:
            if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                running = False
        START_BUTTON.pressed_event(event)
        LEVEL_ONE_BUTTON.pressed_event(event)
        LEVEL_TWO_BUTTON.pressed_event(event)
        LEVEL_THREE_BUTTON.pressed_event(event)
    #отрисовка изменений
    START_BUTTON.draw(screen)
    LEVEL_ONE_BUTTON.draw(screen)
    LEVEL_TWO_BUTTON.draw(screen)
    LEVEL_THREE_BUTTON.draw(screen)
    pygame.display.update()


pygame.quit()
