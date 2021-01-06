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
                    if self.pressed == 1:#здесь добавлять события к кнопкам
                        pass
        elif (event.type == pygame.MOUSEBUTTONUP and self._rect.collidepoint(event.pos)) or \
                (event.type == pygame.MOUSEMOTION and self._rect.collidepoint(event.pos)) and self.flag == 0:
            self.btn_event = 1
        else:
            self.btn_event = 0
            self.flag = 0


pygame.init()
screen = pygame.display.set_mode((800, 450))

START_BUTTON = Button(START_BUTTON_IMAGE_DEFAULT, START_BUTTON_IMAGE_ACTIVE, (10, 10), (200, 100), START_BUTTON_PRESSED)


running = True

while running:
    screen.blit(SCREEN_BACKGROUND_IMAGE, (0, 0))
    #цикл обработки событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

        START_BUTTON.pressed_event(event)
    #отрисовка изменений
    START_BUTTON.draw(screen)
    pygame.display.update()


pygame.quit()