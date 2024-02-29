import pygame
import random

pygame.init()  # инициализация pygame

# цветовая палитра для удобства в коде
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
BLUE = (0, 0, 245)
RED = (255, 78, 21)
GREEN = (77, 255, 77)
PURPLE = (220, 200, 240)
DARK_PURPLE = (180, 160, 200)
DEEP_PURPLE = (120, 100, 140)


class MainWindow:
    def __init__(self):
        self.main_window = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Сапёр")
        self.background_image = pygame.image.load("images/background.jpg").convert()

    def display_menu(self):
        running = True
        while running:  # открытие одного из 3-ёх уровней через нажатие клавиш
            self.main_window.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        GameWindow1().run()
                    elif event.key == pygame.K_2:
                        GameWindow2().run()
                    elif event.key == pygame.K_3:
                        GameWindow3().run()

            self.main_window.blit(self.background_image, (0, 0))  # менюшка с выбором сложности игры
            pygame.draw.rect(self.main_window, BLACK, (100, 430, 600, 250))
            font = pygame.font.Font(None, 36)

            text = font.render("1. Легкий ( Поле 9x9, 10 мин )", True, WHITE)
            self.main_window.blit(text, (150, 450))

            text = font.render("2. Средний ( Поле 15x15, 20 мин )", True, WHITE)
            self.main_window.blit(text, (150, 500))

            text = font.render("3. Сложный ( Поле 25x25, 100 мин )", True, WHITE)
            self.main_window.blit(text, (150, 550))

            pygame.display.flip()


class GameWindow:
    def __init__(self, level_name, width, height):
        self.game_window = pygame.display.set_mode((800, 600))
        pygame.display.set_caption(f"Сапёр - {level_name} уровень сложности")
        self.button_image = pygame.image.load("images/red_flag.jpg").convert()
        self.button_image = pygame.transform.scale(self.button_image, (50, 50))  # Изменение размера изображения кнопки
        self.flag_position = (500, 200)
        self.text_flag = ''
        font = pygame.font.Font(None, 36)
        self.text_flag_position = (self.flag_position[0], self.flag_position[1] + 50)
        self.button_clicked = False
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.cells = [[False] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.mine_positions = self.generate_mine_positions(level_name)
        self.data_kletki = []
        self.data_flags = []
        #self.data_free = []

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size


    def render(self, screen):
        self.screen = screen
        for y in range(self.height):
            for x in range(self.width):
                #if not self.cells[y][x]:
                #else:
                #   color = PURPLE
                #color = DARK_PURPLE if not self.cells[y][x] else PURPLE  # мягкие оттенки фиолетового
                rect = pygame.Rect(x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                   self.cell_size)
                pygame.draw.rect(self.screen, DARK_PURPLE, rect)
                pygame.draw.rect(self.screen, DEEP_PURPLE, rect, 1)  # тонкие линии для разделения клеток

                if isinstance(self.cells[y][x], pygame.Surface):  # проверяем, что в ячейке есть изображение
                    self.screen.blit(self.cells[y][x], (x * self.cell_size + self.left, y * self.cell_size + self.top))

        if self.button_clicked:
            self.text_for_flag = 'активен'
        else:
            self.text_for_flag = 'не активен'

        # self.text_flag = font.render(f'Статус флага: {self.text_for_flag}', True, RED)
        # screen.blit(self.text_flag, (150, 450))
        self.screen.blit(self.button_image, self.flag_position)
        # screen.blit(self.text_flag, self.text_flag_position)

    def on_click(self, cell):
        print('screeen:', self.screen)
        x, y = cell
        a = [x, y]
        cell_surface = pygame.Surface((self.cell_size, self.cell_size))
        free_image = pygame.image.load('images/noth.png').convert()
        free_image = pygame.transform.scale(free_image, (self.cell_size, self.cell_size))
        flag_image = pygame.image.load('images/red_flag.jpg').convert()
        if not self.button_clicked:  # если флаг не активен
            if [x, y] in self.mine_positions:  # если нажатие на мину
                if self.cells[y][x] != flag_image:  # проверка на наличие флага при нажатии на мину
                    print("Игра окончена")
                    mine_image = pygame.image.load('images/mine.png').convert()
                    mine_image = pygame.transform.scale(mine_image, (self.cell_size, self.cell_size))
                    self.cells[y][x] = mine_image
                elif self.cells[y][x] == flag_image:
                    print('NOU !!!!!!!')
            else:  # если не нажатие на мину
                self.cells[y][x] = free_image
                pygame.display.flip()
                self.screen.blit(free_image, (x * self.cell_size + self.left, y * self.cell_size + self.top))
                contains = False
                for i in range(len(self.data_kletki)):
                    if a == self.data_kletki[i]:  # проверка на повторное нажатие для корректного списка
                        contains = True
                        break
                if not contains:
                    self.data_kletki.append(a)
                else:
                    print('СОДЕРЖИТ УЖЕ')
        else:  # если флаг активен
            flag_image = pygame.transform.scale(flag_image, (self.cell_size, self.cell_size))
            self.cells[y][x] = flag_image
            self.button_clicked = False
            contains = False
            for i in range(len(self.data_flags)):
                if a == self.data_flags[i]:  # проверка на повторное нажатие для корректного списка
                    contains = True
                    break
            if not contains:

                self.data_flags.append(a)
            else:
                print('СОДЕРЖИТ УЖЕ')
            print('Флажок поставлен', self.data_flags)

        print(x, y, self.data_kletki)  # отображение координат клетки и списка нажатых
        self.open_free(a)
        pygame.display.flip()

    def open_free(self, a):
        print('Работа функции open_free:')
        print(a[0], a[1])
        x_analog = a[1] * self.rasm_x + a[0]
        y_analog = a[0] * self.rasm_y + a[1]
        #if x_analog - self.rasm_x > 0 and x_analog + self.rasm_x < self.rasm_x * self.rasm_x:
         #   if y_analog - self.rasm_y > 0 and y_analog + self.rasm_y < self.rasm_y * self.rasm_y:
        kletka_1 = [(x_analog - self.rasm_x) // self.rasm_x, (y_analog - self.rasm_y) // self.rasm_y]
        kletka_2 = [(x_analog - self.rasm_x) // self.rasm_x + 1, (y_analog - self.rasm_y) // self.rasm_y]
        kletka_3 = [(x_analog - self.rasm_x) // self.rasm_x + 2, (y_analog - self.rasm_y) // self.rasm_y]
        kletka_4 = [(x_analog - self.rasm_x) // self.rasm_x, a[1]]
        kletka_6 = [(x_analog - self.rasm_x) // self.rasm_x + 2, a[1]]
        kletka_7 = [(x_analog - self.rasm_x) // self.rasm_x, (y_analog - self.rasm_y) // self.rasm_y + 2]
        kletka_8 = [(x_analog - self.rasm_x) // self.rasm_x + 1, (y_analog - self.rasm_y) // self.rasm_y + 2]
        kletka_9 = [(x_analog - self.rasm_x) // self.rasm_x + 2, (y_analog - self.rasm_y) // self.rasm_y + 2]
        around_kletka = [kletka_1, kletka_2, kletka_3, kletka_4, kletka_6, kletka_7, kletka_8, kletka_9]
        count = 0
        for i in range(len(around_kletka)):
            if around_kletka[i] in self.mine_positions:
                count += 1
        print('ЧИСЛО МИН ВОКРУГ КЛЕТКИ',count)

        # координаты клеток вокруг клетки
        print(kletka_1, kletka_2, kletka_3)
        print(kletka_4, 0, kletka_6)
        print(kletka_7, kletka_8, kletka_9)
        #else:


    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        flag_x = self.flag_position[0]
        flag_y = self.flag_position[1]
        if flag_x < mouse_pos[0] < flag_x + 50:
            if flag_y < mouse_pos[1] < flag_y + 50:
                print("flag y = ", flag_y)
                print('flag x = ', flag_x)
                print(flag_x + 50)
                print(flag_y + 50)
                if not self.button_clicked:
                    self.button_clicked = True
                else:
                    self.button_clicked = False
                print(mouse_pos)
                print('флаг:', self.button_clicked)

        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            print('нажатие мимо клетки поля')
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            # if self.button_rect.collidepoint(mouse_pos):
            #    self.button_clicked = not self.button_clicked
            #    print(f"Значение флажка: {self.button_clicked}")
            # else:
            self.on_click(cell)

    def generate_mine_positions(self, level_name):
        # Генерация случайных позиций мин в зависимости от уровня сложности
        if level_name == "1":
            num_mines = 10
            self.rasm_x, self.rasm_y = 9, 9
        elif level_name == "2":
            num_mines = 20
            self.rasm_x, self.rasm_y = 15, 15
        else:
            num_mines = 100
            self.rasm_x, self.rasm_y = 25, 25

        mine_positions = random.sample([([self.rasm_x, self.rasm_y]) for self.rasm_x in range(self.width) for self.rasm_y in range(self.height)], num_mines)
        print(mine_positions)
        self.data_free = []
        for i in range(self.rasm_x):
            for j in range(self.rasm_y):
                a = [i, j]
                self.data_free.append(a)
        for pos in mine_positions:
            if pos in self.data_free:
                self.data_free.remove(pos)
        print(self.data_free)

        return mine_positions

    def run(self):
        running = True
        clock = pygame.time.Clock()
        timer_started = False
        self.current_time = 0
        while running:
            self.game_window.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not timer_started:
                        pygame.time.set_timer(pygame.USEREVENT, 1000)  # запуск таймера с интервалом в 1 секунду
                        timer_started = True
                    self.get_click(event.pos)  # обработка клика мыши
                elif event.type == pygame.USEREVENT:
                    self.current_time += 1

            self.render(self.game_window)  # отрисовка игрового поля
            pygame.display.flip()
            clock.tick(60)


class GameWindow1(GameWindow):
    def __init__(self):
        super().__init__("1", 9, 9)
        self.game_window = pygame.display.set_mode((800, 300))
        self.flag_position = (550, 60)
        self.font = pygame.font.Font(None, 36)
        self.text_position = (500, 20)
        self.current_time = 0
        self.text_flag = ''

    def run(self):
        font = pygame.font.Font(None, 36)
        running = True
        clock = pygame.time.Clock()
        timer_started = False

        while running:
            self.game_window.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.set_mode((800, 600))
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not timer_started:
                        pygame.time.set_timer(pygame.USEREVENT, 1000)
                        timer_started = True
                    self.get_click(event.pos)

                elif event.type == pygame.USEREVENT:
                    self.current_time += 1

            text_surface = self.font.render(f"Time: {self.current_time} sec", True, BLACK)
            self.game_window.blit(text_surface, self.text_position)

            if self.button_clicked == True:
                self.text_for_flag = 'активен'
            else:
                self.text_for_flag = 'не активен'
            self.text_flag = font.render(f'Статус флага: {self.text_for_flag}', True, RED)
            self.game_window.blit(self.text_flag, (425,125))


            self.render(self.game_window)

            pygame.display.flip()
            clock.tick(30)

            if not pygame.display.get_init():  # проверка, что окно не закрыто
                pygame.display.init()  # Переинициализация окна


class GameWindow2(GameWindow):
    def __init__(self):
        super().__init__("2", 15, 15)
        self.game_window = pygame.display.set_mode((850, 550))
        font = pygame.font.Font(None, 36)
        self.flag_position = (650, 70)
        self.text_position = (590, 20)  # новые координаты для отображения текста времени
        self.current_time = 0

    def run(self):

        font = pygame.font.Font(None, 36)
        clock = pygame.time.Clock()
        timer_started = False
        while True:
            self.game_window.fill(WHITE)  # очистка окна
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.set_mode((800, 600))  # установка стандартного размера окна для меню
                    return  # Возврат в меню
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not timer_started:
                        pygame.time.set_timer(pygame.USEREVENT, 1000)  # запуск таймера с интервалом в 1 секунду
                        timer_started = True
                    self.get_click(event.pos)  # обработка клика мыши
                elif event.type == pygame.USEREVENT:
                    self.current_time += 1

            if self.button_clicked == True:
                self.text_for_flag = 'активен'
            else:
                self.text_for_flag = 'не активен'
            self.text_flag = font.render(f'Статус флага: {self.text_for_flag}', True, RED)
            self.game_window.blit(self.text_flag, (510, 125))
            text_surface = font.render(f"Время: {self.current_time} сек", True, BLACK)
            self.game_window.blit(text_surface, self.text_position)  # отображение текста времени
            super().render(self.game_window)  # отрисовка игрового поля
            pygame.display.flip()
            clock.tick(60)

            if not pygame.display.get_init():  # проверка, что окно не закрыто
                pygame.display.init()  # Переинициализация окна


class GameWindow3(GameWindow):
    def __init__(self):
        super().__init__("3", 25, 25)
        self.game_window = pygame.display.set_mode((1200, 800))
        font = pygame.font.Font(None, 36)
        self.flag_position = (1000, 70)
        self.text_flag_position = (1, 1)
        self.text_position = (950, 20)  # н33овые координаты для отображения текста времени
        self.current_time = 0
        self.text_for_flag = ''
        self.button_clicked = False

    def run(self):
        font = pygame.font.Font(None, 36)
        clock = pygame.time.Clock()
        timer_started = False
        while True:
            self.game_window.fill(WHITE)  # очистка окна
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.set_mode((800, 600))  # установка стандартного размера окна для меню
                    return  # Возврат в меню
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not timer_started:
                        pygame.time.set_timer(pygame.USEREVENT, 1000)  # запуск таймера с интервалом в 1 секунду
                        timer_started = True
                    self.get_click(event.pos)  # обработка клика мыши
                elif event.type == pygame.USEREVENT:
                    self.current_time += 1

            text_surface = font.render(f"Время: {self.current_time} сек", True, BLACK)
            self.game_window.blit(text_surface, self.text_position)  # отображение текста о времени

            if self.button_clicked == True:
                self.text_for_flag = 'активен'
            else:
                self.text_for_flag = 'не активен'
            self.text_flag = font.render(f'Статус флага: {self.text_for_flag}', True, RED)
            self.game_window.blit(self.text_flag, (850,150))

            super().render(self.game_window)  # отрисовка игрового поля
            pygame.display.flip()
            clock.tick(60)

            if not pygame.display.get_init():  # проверка, что окно не закрыто
                pygame.display.init()  # переинициализация окна


if __name__ == "__main__":
    main_window = MainWindow()
    main_window.display_menu()
