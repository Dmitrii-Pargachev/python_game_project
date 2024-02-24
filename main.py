import pygame


pygame.init()

# цветовая палитра для удобства в коде
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
BLUE = (0, 0, 245)
RED = (255, 78, 21)
GREEN = (77, 255, 77)


class MainWindow:
    def __init__(self):
        self.main_window = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Сапёр")
        self.background_image = pygame.image.load("images/background.jpg").convert()

    def display_menu(self):
        running = True
        while running: # открытие одного из 3-её уровней через нажатие клавиш
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

            text = font.render("1. Легкий ( Поле 10x10, 10 мин )", True, WHITE)
            self.main_window.blit(text, (150, 450))

            text = font.render("2. Средний ( Поле 15x15, 20 мин )", True, WHITE)
            self.main_window.blit(text, (150, 500))

            text = font.render("3. Сложный ( Поле 30x30, 100 мин )", True, WHITE)
            self.main_window.blit(text, (150, 550))

            pygame.display.flip()


class GameWindow:
    def __init__(self, level_name):
        self.game_window = pygame.display.set_mode((800, 600))
        pygame.display.set_caption(f"Сапёр - {level_name} уровень сложности")

    def run(self):
        running = True
        while running:
            self.game_window.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # код игры
            pygame.display.flip()


class GameWindow1(GameWindow):
    def __init__(self):
        super().__init__("1")


class GameWindow2(GameWindow):
    def __init__(self):
        super().__init__("2")


class GameWindow3(GameWindow):
    def __init__(self):
        super().__init__("3")


if __name__ == "__main__":
    main_window = MainWindow()
    main_window.display_menu()
