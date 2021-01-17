class Game:
    def is_valid_value(self, char):
        if (char == ' ' or  # floor
                char == '#' or  # wall
                char == '@' or  # ghost on floor
                char == '.' or  # dock
                char == '*' or  # box on dock
                char == '$' or  # box
                char == '+'):  # ghost on dock
            return True
        else:
            return False

    def __init__(self, filename, level):
        self.queue = queue.LifoQueue() # очередь хранящая список наших действий в хронологическом порядке
        self.hell = [] #создаём поле
        #Проверка корректности введённого уровня
        if level < 1:
            print("Ошибка: уровень" + str(level) + "не существует")
            sys.exit(1)
        else:
            #открытие файла с уровнями
            file = open(filename, 'r')
            level_found = False
            #цикл прохождения по файлу
            for line in file:
                if not level_found:
                    #если название введенного уровня совпадает с текущей строкой-итератором, то переходить к считыванию уровня
                    if "Level " + str(level) == line.strip():
                        level_found = True
                else:
                    if line.strip() != "":
                        row = []
                        for c in line:
                            if c != '\n' and self.is_valid_value(c):
                                row.append(c)
                            elif c == '\n':
                                continue
                            else:
                                print("Ошибка: уровень" + str(level) + "не существует" + c)
                                sys.exit(1)
                        self.hell.append(row)
                    else:
                        break

    def load_size(self):
        #задаём размеры экрана относительно размеров игрового поля
        x = 0
        y = len(self.hell)
        for row in self.hell:
            if len(row) > x:
                x = len(row)
        return (x * 50, y * 50) #умножаем на сторону одного элемента в пикселях

    def get_hell(self):
        #задаём поле
        return self.hell

    def print_hell(self):
        #вывод поля
        for row in self.hell:
            for char in row:
                sys.stdout.write(char)
                sys.stdout.flush()
            sys.stdout.write('\n')

    def get_content(self, x, y):
        #изменяем текущую координату на новую
        return self.hell[y][x]

    def set_content(self, x, y, content):
        #добавляем элементы в наше поле, проевряя, чтобы они были в списке допустимых символов
        if self.is_valid_value(content):
            self.hell[y][x] = content
        else:
            print("Ошибка: символ'" + content + "'не может быть добавлен")

    def ghost(self):
        #изменение координаты персонажа
        x = 0
        y = 0
        for row in self.hell:
            for pos in row:
                if pos == '@' or pos == '+': #если положение на которое желает переместится игрок пол или доска, то не позволяем координате увеличиваться
                    return (x, y, pos)
                else:
                    x = x + 1
            y = y + 1
            x = 0

    def can_move(self, x, y):
        #проверяем, есть ли у персонажа возможность двигаться. Т.е. следующий элемент не стена или дьяволёнок в любом из его положений
        return self.get_content(self.ghost()[0] + x, self.ghost()[1] + y) not in ['#', '*', '$']

    def next(self, x, y):
        #получаем текущее положение нашего персонажа и к соответсвующим координатам прибавляем изменённые х и у
        return self.get_content(self.ghost()[0] + x, self.ghost()[1] + y)

    def can_push(self, x, y):
        #проверяем, возможно ли движение
        return (self.next(x, y) in ['*', '$'] and self.next(x + x, y + y) in [' ', '.'])

    def is_completed(self):
        #проверяем, что все дьяволята поставлены на требуемую позицию
        for row in self.hell:
            for cell in row:
                if cell == '$':
                    return False
        return True

    def move_box(self, x, y, a, b):
        #(x,y) - положение персонажа
        #(a,b) - положение коробки
        current_box = self.get_content(x, y) #положение коробки
        future_box = self.get_content(x + a, y + b) #положение коробки после изменения
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

    def unmove(self):
        #отмена последнего дейсвия при помощи перемещения в очереди
        if not self.queue.empty():
            movement = self.queue.get()
            if movement[2]:
                current = self.ghost()
                self.move(movement[0] * -1, movement[1] * -1, False)
                self.move_box(current[0] + movement[0], current[1] + movement[1], movement[0] * -1, movement[1] * -1)
            else:
                self.move(movement[0] * -1, movement[1] * -1, False)

    def move(self, x, y, save):
        if self.can_move(x, y):
            current = self.ghost() #переменная, хранящая координаты персонажа и его положение на доске
            future = self.next(x, y) #переменная, хранящая следующее, изменённое, положение персонажа
            if current[2] == '@' and future == ' ': #если призрак на полу и  следующая клетка пол
                self.set_content(current[0] + x, current[1] + y, '@')
                self.set_content(current[0], current[1], ' ')
                if save: self.queue.put((x, y, False))
            elif current[2] == '@' and future == '.': #если призрак на полу и следующая клетка пол
                self.set_content(current[0] + x, current[1] + y, '+')
                self.set_content(current[0], current[1], ' ')
                if save: self.queue.put((x, y, False))
            elif current[2] == '+' and future == ' ': #если призрак на доске и следующая клетка пол
                self.set_content(current[0] + x, current[1] + y, '@')
                self.set_content(current[0], current[1], '.')
                if save: self.queue.put((x, y, False))
            elif current[2] == '+' and future == '.': #если призрак на доске и следующая клетка пол
                self.set_content(current[0] + x, current[1] + y, '+')
                self.set_content(current[0], current[1], '.')
                if save: self.queue.put((x, y, False))
        elif self.can_push(x, y):
            current = self.ghost()
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