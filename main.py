import pygame
import random


pygame.init() # инициализация pygame

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
        while running: # открытие одного из 3-ёх уровней через нажатие клавиш
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

            self.main_window.blit(self.background_image, (0, 0)) # менюшка с выбором сложности игры
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
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.cells = [[False] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.mine_positions = self.generate_mine_positions(level_name)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                color = (DARK_PURPLE) if not self.cells[y][x] else (PURPLE)  # мягкие оттенки фиолетового
                rect = pygame.Rect(x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                   self.cell_size)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (DEEP_PURPLE), rect, 1)  # тонкие линии для разделения клеток

                if isinstance(self.cells[y][x], pygame.Surface):  # Проверяем, что в ячейке есть изображение
                    screen.blit(self.cells[y][x], (x * self.cell_size + self.left, y * self.cell_size + self.top))

    def on_click(self, cell):
        x, y = cell
        if (x, y) in self.mine_positions:
            print("Игра окончена")
            mine_image = pygame.image.load('images/mine.png').convert()

            # Масштабирование изображения под размер клетки
            mine_image = pygame.transform.scale(mine_image, (self.cell_size, self.cell_size))

            # Вычисление координат для отображения изображения в центре клетки
            image_x = x * self.cell_size + self.left
            image_y = y * self.cell_size + self.top

            self.cells[y][x] = mine_image
        else:
            self.cells[y][x] = not self.cells[y][x]
        print(x, y)

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def generate_mine_positions(self, level_name):
        # Генерация случайных позиций мин в зависимости от уровня сложности
        if level_name == "1":
            num_mines = 10
        elif level_name == "2":
            num_mines = 20
        else:
            num_mines = 100

        mine_positions = random.sample([(x, y) for x in range(self.width) for y in range(self.height)], num_mines)
        print(mine_positions)
        return mine_positions

    def run(self):
        running = True
        font = pygame.font.Font(None, 36)
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
            self.text_surface = font.render(f"Время: {self.current_time} сек", True, BLACK)
            self.game_window.blit(self.text_surface, self.text_position)  # отображение текста времени
            self.game_window.blit(self.text_surface, (600, 20))
            pygame.display.flip()
            clock.tick(60)


class GameWindow1(GameWindow):
    def __init__(self):
        super().__init__("1", 9, 9)
        self.game_window = pygame.display.set_mode((800, 600))
        self.font = pygame.font.Font(None, 36)
        self.text_position = (500, 20)
        self.current_time = 0

    def run(self):
        running = True
        clock = pygame.time.Clock()
        timer_started = False

        while running:
            self.game_window.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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

            self.render(self.game_window)

            pygame.display.flip()
            clock.tick(30)


class GameWindow2(GameWindow):
    def __init__(self):
        super().__init__("2", 15, 15)
        self.game_window = pygame.display.set_mode((850, 550))
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
        self.text_position = (950, 20)  # новые координаты для отображения текста времени
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

            text_surface = font.render(f"Время: {self.current_time} сек", True, BLACK)
            self.game_window.blit(text_surface, self.text_position)  # отображение текста о времени
            super().render(self.game_window)  # отрисовка игрового поля
            pygame.display.flip()
            clock.tick(60)

            if not pygame.display.get_init():  # проверка, что окно не закрыто
                pygame.display.init()  # переинициализация окна



if __name__ == "__main__":
    main_window = MainWindow()
    main_window.display_menu()
