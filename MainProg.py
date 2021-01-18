import pygame
import sys
import pygame_gui
import queue
from game import Game
from constants import *

#класс создания кнопок, на вход принимаются изображения различных состояний,
# позиция, размер и номер события когда эта клавиша нажата
class Button():
    def __init__(self, image, active_image, position, size, pressed):
        #переобьявление полученных данных
        self.image = image
        self.btn_event = 0
        self.flag = 0
        self.active_image = active_image
        self.button_images = pygame.Surface(size)
        self._rect = pygame.Rect(position, size)
        self.pressed = pressed
    #метод отрисовки кнопки на экране
    def draw(self, screen):
        if self.btn_event == 0:
            screen.blit(self.image, self._rect)
        elif self.btn_event == 1:
            screen.blit(self.active_image, self._rect)
    #отработка логики нажатия и начала события
    def pressed_event(self, event):
        #если кнопка нажата
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.flag = 1
            if event.button == 1:
                if self._rect.collidepoint(event.pos):
                    self.btn_event = 0
                    #возвращение номера события при нажатии кнопки
                    return self.pressed
        #изменение состояния кнопки если мышка на ней но она не нажата
        elif (event.type == pygame.MOUSEBUTTONUP and self._rect.collidepoint(event.pos)) or \
                (event.type == pygame.MOUSEMOTION and self._rect.collidepoint(event.pos)) and self.flag == 0:
            self.btn_event = 1
        #сброс значений
        else:
            self.btn_event = 0
            self.flag = 0
#функция выхода из игры
def quit():
    pygame.quit()
#функция запуска главного меню
def start_menu():
    #обьявление стартовой кнопки и кнопки уровней
    START_BUTTON = Button(START_BUTTON_IMAGE_DEFAULT, START_BUTTON_IMAGE_ACTIVE, (300, 200), (160, 70), START_BUTTON_PRESSED)
    LEVEL_ONE_BUTTON = Button(LEVEL1_BUTTON_IMAGE_DEFAULT, LEVEL1_BUTTON_IMAGE_ACTIVE,
                          (530, SCREEN_HIGHT - 260), (150, 150), LEVEL1_BUTTON_PRESSED)
    LEVEL_TWO_BUTTON = Button(LEVEL2_BUTTON_IMAGE_DEFAULT, LEVEL2_BUTTON_IMAGE_ACTIVE,
                          (400, SCREEN_HIGHT - 150), (150, 150), LEVEL2_BUTTON_PRESSED)
    LEVEL_THREE_BUTTON = Button(LEVEL3_BUTTON_IMAGE_DEFAULT, LEVEL3_BUTTON_IMAGE_ACTIVE,
                            (SCREEN_WIDHT - 150, SCREEN_HIGHT - 150), (150, 150), LEVEL3_BUTTON_PRESSED)
    #запуск игрового цикла меню
    running = True
    level_flag = 1
    while running:
        time_delta = clock.tick(60) / 1000
        #заливка экрана изображением
        screen.blit(SCREEN_BACKGROUND_IMAGE, (0, 0))
        #цикл обработки событий
        for event in pygame.event.get():
            manager.process_events(event)
            #всплывающее окно если игрок захочет выйти
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
            #вызов функции старта уровня с различными данными на вход для запуска различных уровней
            START_BUTTON.pressed_event(event)
            if START_BUTTON.pressed_event(event) == 0:
                if level_flag == 1:
                    play_level(1)
                if level_flag == 2:
                    play_level(2)
                elif level_flag == 3:
                    play_level(3)
            LEVEL_ONE_BUTTON.pressed_event(event)
            if LEVEL_ONE_BUTTON.pressed_event(event) == 1:
                level_flag = 1
            LEVEL_TWO_BUTTON.pressed_event(event)
            if LEVEL_TWO_BUTTON.pressed_event(event) == 2:
                level_flag = 2
            LEVEL_ONE_BUTTON.pressed_event(event)
            if LEVEL_THREE_BUTTON.pressed_event(event) == 3:
                level_flag = 3

        #отрисовка изменений
        if level_flag == 1:
            screen.blit(LEVEL1_SELECTED, pygame.Rect((545, 330), (130, 110)))
        elif level_flag == 2:
            screen.blit(LEVEL2_SELECTED, pygame.Rect((545, 330), (130, 110)))
        elif level_flag == 3:
            screen.blit(LEVEL3_SELECTED, pygame.Rect((545, 330), (130, 110)))
        START_BUTTON.draw(screen)
        LEVEL_ONE_BUTTON.draw(screen)
        LEVEL_TWO_BUTTON.draw(screen)
        LEVEL_THREE_BUTTON.draw(screen)
        #обновление менеджера pygame ui и экрана
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()
#обьявление экземпляра класса с логикой уровней
#функция отрисовки победного экрана
def win_screen(screen):
    running = True
    while running:
        #отрисовка победного экрана с возможностью выхода в главное меню
        HOME_BUTTON = Button(HOME_BUTTON_DEFAULT, HOME_BUTTON_ACTIVE, (300, 200), (200, 100), 123)
        time_delta = clock.tick(60) / 1000
        screen.blit(pygame.Color((1, 200, 233)), (0, 0))
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
            HOME_BUTTON.pressed.event(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()
#функция отрисовки карты уровня
def print_game(matrix, screen):
    x = 0
    y = 0
    #проход по матрице из текстового файла и отрисовка клеток по 50 пикселей
    for row in matrix:
        for char in row:
            if char == ' ':  # floor
                screen.blit(FLOOR_IMAGE, (x, y))
            elif char == '#':  # wall
                screen.blit(WALL_IMAGE, (x, y))
            elif char == '@':  # worker on floor
                screen.blit(WORKER_IMAGE, (x, y))
            elif char == '.':  # dock
                screen.blit(DOCK_IMAGE, (x, y))
            elif char == '*':  # box on dock
                screen.blit(BOX_DOCKED_IMAGE, (x, y))
            elif char == '$':  # box
                screen.blit(BOX_IMAGE, (x, y))
            elif char == '+':  # worker on dock
                screen.blit(WORKER_ON_DOCK_IMAGE, (x, y))
            x = x + 50
        x = 0
        y = y + 50
#функция проигрывания уровня
def play_level(level):
    running = True
    game = Game('levels.txt', level)
    time_delta = clock.tick(60) / 1000
    while running:
        if game.is_completed():
            # отрисовка победного экрана
            win_screen(screen)
        #использование функции отрисовки уровня
        print_game(game.get_hell(), screen)
        #отработка события выхода из игры
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
            #принятие нажатых от игрока клавиш для изменения координат коробок и персонажа
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.move(0, -1, True)
                elif event.key == pygame.K_DOWN:
                    game.move(0, 1, True)
                elif event.key == pygame.K_LEFT:
                    game.move(-1, 0, True)
                elif event.key == pygame.K_RIGHT:
                    game.move(1, 0, True)
                elif event.key == pygame.K_q:
                    sys.exit(0)
                elif event.key == pygame.K_d:
                    game.unmove()
        #обновление менеджера и дисплея
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()

#инициализация инструментов pygame, задавание размеров окна и запуск меню
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HIGHT))
screen.blit(SCREEN_BACKGROUND_IMAGE, (800, 450))
manager = pygame_gui.UIManager((800, 450))
start_menu()
