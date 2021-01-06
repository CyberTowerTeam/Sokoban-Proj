import pygame
import pygame_gui


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
                    return self.pressed
        elif (event.type == pygame.MOUSEBUTTONUP and self._rect.collidepoint(event.pos)) or \
                (event.type == pygame.MOUSEMOTION and self._rect.collidepoint(event.pos)) and self.flag == 0:
            self.btn_event = 1
        else:
            self.btn_event = 0
            self.flag = 0


class Level():
    pass

def level1():
    print(111111111111111111111111)

def level2():
    print(222222222222222222222222)

def level3():
    print(333333333333333333333333)

def quit():
    pygame.quit()

def start_menu():
    START_BUTTON = Button(START_BUTTON_IMAGE_DEFAULT, START_BUTTON_IMAGE_ACTIVE, (10, 10), (200, 100), START_BUTTON_PRESSED)
    LEVEL_ONE_BUTTON = Button(LEVEL1_BUTTON_IMAGE_DEFAULT, LEVEL1_BUTTON_IMAGE_ACTIVE,
                          (50, SCREEN_HIGHT - 80), (190, 60), LEVEL1_BUTTON_PRESSED)
    LEVEL_TWO_BUTTON = Button(LEVEL2_BUTTON_IMAGE_DEFAULT, LEVEL2_BUTTON_IMAGE_ACTIVE,
                          (305, SCREEN_HIGHT - 80), (190, 60), LEVEL2_BUTTON_PRESSED)
    LEVEL_THREE_BUTTON = Button(LEVEL3_BUTTON_IMAGE_DEFAULT, LEVEL3_BUTTON_IMAGE_ACTIVE,
                            (SCREEN_WIDHT - 245, SCREEN_HIGHT - 80), (190, 60), LEVEL3_BUTTON_PRESSED)
    LEVEL1_SELECTED = pygame.image.load('LEVEL1_SELECTED_TEXT.png')
    LEVEL2_SELECTED = pygame.image.load('LEVEL2_SELECTED_TEXT.png')
    LEVEL3_SELECTED = pygame.image.load('LEVEL3_SELECTED_TEXT.png')
    running = True
    level_flag = 1
    while running:
        time_delta = clock.tick(60) / 1000
        screen.blit(SCREEN_BACKGROUND_IMAGE, (0, 0))
        screen.blit(GAME_NAME, pygame.Rect((SCREEN_WIDHT - 205, 5), (200, 150)))
        #цикл обработки событий
        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                confrimation_dialog = pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((50, 50), (300, 200)),
                    manager=manager,
                    window_title='Выход из игры',
                    action_long_desc='Вы уверены, что хотите выйти из игры?',
                    action_short_name='ок',
                    blocking=True
                )
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    running = False
                    quit()
            START_BUTTON.pressed_event(event)
            if START_BUTTON.pressed_event(event) == 0:
                if level_flag == 1:
                    level1()
                if level_flag == 2:
                    level2()
                elif level_flag == 3:
                    level3()
            LEVEL_ONE_BUTTON.pressed_event(event)
            if LEVEL_ONE_BUTTON.pressed_event(event) == 1:
                level_flag = 1
            LEVEL_TWO_BUTTON.pressed_event(event)
            if LEVEL_TWO_BUTTON.pressed_event(event) == 2:
                level_flag = 2
            LEVEL_THREE_BUTTON.pressed_event(event)
            if LEVEL_THREE_BUTTON.pressed_event(event) == 3:
                level_flag = 3
            if level_flag == 1:
                screen.blit(LEVEL1_SELECTED, pygame.Rect((250, 30), (200, 120)))
        #отрисовка изменений
        START_BUTTON.draw(screen)
        LEVEL_ONE_BUTTON.draw(screen)
        LEVEL_TWO_BUTTON.draw(screen)
        LEVEL_THREE_BUTTON.draw(screen)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HIGHT))
screen.blit(SCREEN_BACKGROUND_IMAGE, (800, 450))
manager = pygame_gui.UIManager((800, 450))
start_menu()
