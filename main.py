import pygame
import sys

pygame.init()

# размеры окна
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# цветовая палитра для удобства в написании кода
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
BLUE = (0, 0, 245)
RED = (255, 78, 21)
GREEN = (77, 255, 77)


# основное окно
main_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Сапёр")


def main_menu():
    running = True
    background_image = pygame.image.load("images/background.jpg").convert()
    # Размеры и позиция прямоугольника
    rect_width = 600
    rect_height = 300
    while running: # открытие одного из 3-её уровней через нажатие клавиш
        main_window.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game1()
                elif event.key == pygame.K_2:
                    game2()
                elif event.key == pygame.K_3:
                    game3()

        main_window.blit(background_image, (0, 0))
        pygame.draw.rect(main_window, BLACK, (100, 150, rect_width, rect_height))
        font = pygame.font.Font(None, 36) # менюшка с выбором сложности игры
        text = font.render("1. Легко ( Поле 10x10, 10 мин )", True, WHITE)
        main_window.blit(text, (150, 200))

        text = font.render("2. Средне ( Поле 15x15, 20 мин )", True, WHITE)
        main_window.blit(text, (150, 250))

        text = font.render("3. Сложный уровень ( Поле 30x30, 100 мин )", True, WHITE)
        main_window.blit(text, (150, 300))


        pygame.display.flip()


def game1():
    game1_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Сапёр - 1 уровень сложности")

    running = True

    while running:
        game1_window.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # код
        pygame.display.flip()


def game2():
    game2_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Сапёр - 2 уровень сложности")

    running = True

    while running:
        game2_window.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # код
        pygame.display.flip()


def game3():
    game2_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Сапёр - 3 уровень сложности")

    running = True

    while running:
        game2_window.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # код
        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
