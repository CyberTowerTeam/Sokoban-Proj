import pygame
import sys
import pygame_gui
import queue
from game import Game
from constants import *
from random import choice
import random

# объявление необходимых библеотек

# инициализация инструментов для работы с частицами
pygame.init()
GRAVITY = 0.1
screen_rect = (0, 0, 800, 450)


# класс создания кнопок, на вход принимаются изображения различных состояний,
# позиция, размер и номер события когда эта клавиша  нажата
class Button():
    def __init__(self, image, active_image, position, size, pressed):
        # переобьявление полученных данных
        self.image = image
        self.btn_event = 0
        self.flag = 0
        self.active_image = active_image
        self.button_images = pygame.Surface(size)
        self._rect = pygame.Rect(position, size)
        self.pressed = pressed

    # метод отрисовки кнопки на экране
    def draw(self, screen):
        # если мышка находится не на кнопке, отрисовка дефолтного состояния
        if self.btn_event == 0:
            screen.blit(self.image, self._rect)
        # если мышка находится на кнопке, отрисовка активного состояния
        elif self.btn_event == 1:
            screen.blit(self.active_image, self._rect)

    # отработка логики нажатия и начала события
    def pressed_event(self, event):
        # если кнопка нажата
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.flag = 1
            if event.button == 1:
                if self._rect.collidepoint(event.pos):
                    self.btn_event = 0
                    # возвращение номера события при нажатии кнопки
                    return self.pressed
        # изменение состояния кнопки если мышка на ней но она не нажата
        elif (event.type == pygame.MOUSEBUTTONUP and self._rect.collidepoint(event.pos)) or \
                (event.type == pygame.MOUSEMOTION and self._rect.collidepoint(event.pos)) and self.flag == 0:
            self.btn_event = 1
        # сброс значений
        else:
            self.btn_event = 0
            self.flag = 0


# функция выхода из игры
def quit():
    pygame.quit()


# функция запуска главного меню
def start_menu():
    # инициализация музыки
    pygame.mixer.music.load('musiks/musik2.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(100)
    # инициализация pygame часов, экрана и менеджера работы с виджетами
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HIGHT))
    screen.blit(SCREEN_BACKGROUND_IMAGE, (800, 450))
    manager = pygame_gui.UIManager((800, 450))
    # обьявление стартовой кнопки и кнопки уровней
    START_BUTTON = Button(START_BUTTON_IMAGE_DEFAULT, START_BUTTON_IMAGE_ACTIVE, (300, 200), (160, 70),
                          START_BUTTON_PRESSED)
    LEVEL_ONE_BUTTON = Button(LEVEL1_BUTTON_IMAGE_DEFAULT, LEVEL1_BUTTON_IMAGE_ACTIVE,
                              (530, SCREEN_HIGHT - 260), (150, 150), LEVEL1_BUTTON_PRESSED)
    LEVEL_TWO_BUTTON = Button(LEVEL2_BUTTON_IMAGE_DEFAULT, LEVEL2_BUTTON_IMAGE_ACTIVE,
                              (400, SCREEN_HIGHT - 150), (150, 150), LEVEL2_BUTTON_PRESSED)
    LEVEL_THREE_BUTTON = Button(LEVEL3_BUTTON_IMAGE_DEFAULT, LEVEL3_BUTTON_IMAGE_ACTIVE,
                                (SCREEN_WIDHT - 150, SCREEN_HIGHT - 150), (150, 150), LEVEL3_BUTTON_PRESSED)
    # запуск игрового цикла меню
    running = True
    level_flag = 1
    flag_out = 0
    while running:
        time_delta = clock.tick(60) / 1000
        # заливка экрана изображением
        screen.blit(SCREEN_BACKGROUND_IMAGE, (0, 0))
        # цикл обработки событий
        for event in pygame.event.get():
            manager.process_events(event)
            # всплывающее окно если игрок захочет выйти
            if event.type == pygame.QUIT:
                confrimation_dialog = pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((50, 50), (300, 200)),
                    manager=manager,
                    window_title='Выход из игры',
                    action_long_desc='Вы уверены, что хотите выйти из игры?',
                    action_short_name='ок',
                    blocking=True
                )
            # выход если игрок подтвержает выход из игры
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    running = False
                    quit()
            # вызов функции старта уровня с различными данными на вход для запуска различных уровней
            START_BUTTON.pressed_event(event)
            if START_BUTTON.pressed_event(event) == 0:
                if level_flag == 1:
                    flag_out = 1
                    return level_flag
                if level_flag == 2:
                    flag_out = 1
                    return level_flag
                elif level_flag == 3:
                    flag_out = 1
                    return level_flag
            # изменение флага, отслеживающего запуск конкретного уровня при нажатии другой кнопки
            LEVEL_ONE_BUTTON.pressed_event(event)
            if LEVEL_ONE_BUTTON.pressed_event(event) == 1:
                level_flag = 1
            LEVEL_TWO_BUTTON.pressed_event(event)
            if LEVEL_TWO_BUTTON.pressed_event(event) == 2:
                level_flag = 2
            LEVEL_ONE_BUTTON.pressed_event(event)
            if LEVEL_THREE_BUTTON.pressed_event(event) == 3:
                level_flag = 3
        if flag_out == 1:
            running = False
        # отрисовка изменений, если выбран уровень, выводится изображение с соответствующей цифрой
        if level_flag == 1:
            screen.blit(LEVEL1_SELECTED, pygame.Rect((545, 330), (130, 110)))
        elif level_flag == 2:
            screen.blit(LEVEL2_SELECTED, pygame.Rect((545, 330), (130, 110)))
        elif level_flag == 3:
            screen.blit(LEVEL3_SELECTED, pygame.Rect((545, 330), (130, 110)))
        # отрисовка кнопок
        START_BUTTON.draw(screen)
        LEVEL_ONE_BUTTON.draw(screen)
        LEVEL_TWO_BUTTON.draw(screen)
        LEVEL_THREE_BUTTON.draw(screen)
        # обновление менеджера pygame ui и экрана
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()


# класс для вывода спрайтов на экран
all_sprites = pygame.sprite.Group()


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [pygame.image.load('images/STAR.png')]
    for scale in (10, 20, 30, 5, 35):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 10
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


# функция вызова победного экрана
def win_screen():
    # инициализация музыки
    pygame.mixer.music.load('musiks/musik3.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(100)
    # иницализация pygame, экрана, менеджера выхода и переменной для замедления частиц, а также текста
    time_counter = 0
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HIGHT))
    manager = pygame_gui.UIManager((800, 450))
    screen.fill(pygame.Color((1, 200, 233)))
    font = pygame.font.Font(None, 100)
    text = font.render(choice(['МОЛОДЕЦ!', 'ОТЛИЧНО!', 'ТАК ДЕРЖАТЬ!', 'НЕПЛОХО!',
                               'НЕВЕРОЯТНО!']), True, (255, 255, 255))

    running = True
    while running:
        # отрисовка победного экрана с возможностью выхода в главное меню
        HOME_BUTTON = Button(HOME_BUTTON_DEFAULT, HOME_BUTTON_ACTIVE, (300, 200), (200, 100), HOME_BUTTON_PRESSED)
        time_delta = clock.tick(60)
        # цикл обработки событий
        for event in pygame.event.get():
            manager.process_events(event)
            # всплывающее окно если игрок захочет выйти
            if event.type == pygame.QUIT:
                confrimation_dialog = pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((15, 100), (300, 200)),
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
            # выход в главное меню при нажатии кнопки
            HOME_BUTTON.pressed_event(event)
            if HOME_BUTTON.pressed_event(event) == 123:
                return 123
        # отрисовка частиц
        if time_counter == 10:
            create_particles((400, 30))
            create_particles((50, 30))
            create_particles((750, 30))
            create_particles((400, 400))
            create_particles((50, 400))
            create_particles((750, 400))
            time_counter = 0
        else:
            time_counter += 1
        all_sprites.update()
        screen.fill((1, 200, 233))
        all_sprites.draw(screen)
        clock.tick(60)
        # отрисовка кнопки и обновление экрана
        HOME_BUTTON.draw(screen)
        manager.update(time_delta)
        manager.draw_ui(screen)
        screen.blit(text, (225, 50))

        pygame.display.update()
        pygame.display.flip()


# функция отрисовки карты уровня
def print_game(hell, screen):
    x = 0
    y = 0
    # проход по матрице из текстового файла и отрисовка клеток по 50 пикселей
    for row in hell:
        for char in row:
            if char == ' ':  # пол
                screen.blit(FLOOR_IMAGE, (x, y))
            elif char == '#':  # стена
                screen.blit(WALL_IMAGE, (x, y))
            elif char == '@':  # призрак на полу
                screen.blit(WORKER_IMAGE, (x, y))
            elif char == '.':  # котел
                screen.blit(DOCK_IMAGE, (x, y))
            elif char == '*':  # черт в котле
                screen.blit(BOX_DOCKED_IMAGE, (x, y))
            elif char == '$':  # черт
                screen.blit(BOX_IMAGE, (x, y))
            elif char == '+':  # призрак над котлом
                screen.blit(WORKER_ON_DOCK_IMAGE, (x, y))
            x = x + 50
        x = 0
        y = y + 50


# функция проигрывания уровня
def play_level(level):
    # инициализация музыки, времени, экрана и менеджера виджетов
    pygame.mixer.music.load('musiks/musik1.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(100)
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HIGHT))
    manager = pygame_gui.UIManager((800, 450))
    running = True
    # создание экземпляра класса game
    game = Game('levels.txt', level)
    time_delta = clock.tick(60) / 1000
    while running:
        # отслеживание завершения уровня
        if game.is_completed():
            return 666
        # использование функции отрисовки уровня
        print_game(game.get_hell(), screen)
        # отработка события выхода из игры
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
            # принятие нажатых от игрока клавиш для изменения координат коробок и персонажа
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.move(0, -1, True)
                elif event.key == pygame.K_DOWN:
                    game.move(0, 1, True)
                elif event.key == pygame.K_LEFT:
                    game.move(-1, 0, True)
                elif event.key == pygame.K_RIGHT:
                    game.move(1, 0, True)
                elif event.key == pygame.K_b:
                    game.unmove()
        # обновление менеджера и дисплея
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()

# запуск бесконечного цикла отслеживания функцию окон
if __name__ == '__main__':
    while True:
        x = start_menu()
        y = play_level(x)
        if y == 666:
            z = win_screen()
            if z == 123:
                continue
