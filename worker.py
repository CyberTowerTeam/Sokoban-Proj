import pygame
import sys


class Game:

    def can_move(self, x, y):
        return self.get_content(self.worker()[0] + x, self.worker()[1] + y) not in ['#', '*', '$']

    def move(self, x, y, save):
        if self.can_move(x, y):
            current = self.worker()
            future = self.next(x, y)
            if current[2] == '@' and future == ' ':
                self.set_content(current[0] + x, current[1] + y, '@')
                self.set_content(current[0], current[1], ' ')
                if save: self.queue.put((x, y, False))
            elif current[2] == '@' and future == '.':
                self.set_content(current[0] + x, current[1] + y, '+')
                self.set_content(current[0], current[1], ' ')
                if save: self.queue.put((x, y, False))
            elif current[2] == '+' and future == ' ':
                self.set_content(current[0] + x, current[1] + y, '@')
                self.set_content(current[0], current[1], '.')
                if save: self.queue.put((x, y, False))
            elif current[2] == '+' and future == '.':
                self.set_content(current[0] + x, current[1] + y, '+')
                self.set_content(current[0], current[1], '.')
                if save: self.queue.put((x, y, False))
        elif self.can_push(x, y):
            current = self.worker()
            future = self.next(x, y)
            future_box = self.next(x + x, y + y)
            if current[2] == '@' and future == '$' and future_box == ' ':
                self.move_box(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], ' ')
                self.set_content(current[0] + x, current[1] + y, '@')
                if save: self.queue.put((x, y, True))
            elif current[2] == '@' and future == '$' and future_box == '.':
                self.move_box(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], ' ')
                self.set_content(current[0] + x, current[1] + y, '@')
                if save: self.queue.put((x, y, True))
            elif current[2] == '@' and future == '*' and future_box == ' ':
                self.move_box(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], ' ')
                self.set_content(current[0] + x, current[1] + y, '+')
                if save: self.queue.put((x, y, True))
            elif current[2] == '@' and future == '*' and future_box == '.':
                self.move_box(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], ' ')
                self.set_content(current[0] + x, current[1] + y, '+')
                if save: self.queue.put((x, y, True))
            if current[2] == '+' and future == '$' and future_box == ' ':
                self.move_box(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], '.')
                self.set_content(current[0] + x, current[1] + y, '@')
                if save: self.queue.put((x, y, True))
            elif current[2] == '+' and future == '$' and future_box == '.':
                self.move_box(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], '.')
                self.set_content(current[0] + x, current[1] + y, '+')
                if save: self.queue.put((x, y, True))
            elif current[2] == '+' and future == '*' and future_box == ' ':
                self.move_box(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], '.')
                self.set_content(current[0] + x, current[1] + y, '+')
                if save: self.queue.put((x, y, True))
            elif current[2] == '+' and future == '*' and future_box == '.':
                self.move_box(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], '.')
                self.set_content(current[0] + x, current[1] + y, '+')
                if save: self.queue.put((x, y, True))

    def next(self, x, y):
        return self.get_content(self.worker()[0] + x, self.worker()[1] + y)


    def can_push(self, x, y):
        return (self.next(x, y) in ['*', '$'] and self.next(x + x, y + y) in [' ', '.'])


    def worker(self):
        x = 0
        y = 0
        for row in self.matrix:
            for pos in row:
                if pos == '@' or pos == '+':
                    return (x, y, pos)
                else:
                    x = x + 1
            y = y + 1
            x = 0

    def unmove(self):
        if not self.queue.empty():
            movement = self.queue.get()
            if movement[2]:
                current = self.worker()
                self.move(movement[0] * -1, movement[1] * -1, False)
                self.move_box(current[0] + movement[0], current[1] + movement[1], movement[0] * -1, movement[1] * -1)
            else:
                self.move(movement[0] * -1, movement[1] * -1, False)


    def move_box(self, x, y, a, b):
        #        (x,y) -> move to do
        #        (a,b) -> box to move
        current_box = self.get_content(x, y)
        future_box = self.get_content(x + a, y + b)
        if current_box == '$' and future_box == ' ':
            self.set_content(x + a, y + b, '$')
            self.set_content(x, y, ' ')
        elif current_box == '$' and future_box == '.':
            self.set_content(x + a, y + b, '*')
            self.set_content(x, y, ' ')
        elif current_box == '*' and future_box == ' ':
            self.set_content(x + a, y + b, '$')
            self.set_content(x, y, '.')
        elif current_box == '*' and future_box == '.':
            self.set_content(x + a, y + b, '*')
            self.set_content(x, y, '.')



#size = Game.load_size()
#screen = pygame.display.set_mode((50, 60), (500, 600))
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                Game.move(0, -1, True)
            elif event.key == pygame.K_DOWN:
                Game.move(0, 1, True)
            elif event.key == pygame.K_LEFT:
                Game.move(-1, 0, True)
            elif event.key == pygame.K_RIGHT:
                Game.move(1, 0, True)
            elif event.key == pygame.K_q:
                sys.exit(0)
            elif event.key == pygame.K_d:
                Game.unmove()
    pygame.display.update()

