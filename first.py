# импорт необходимых библиотек
import pygame
import random

# основные данные
pygame.init()
width = 400
height = 500
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 30
font = pygame.font.Font('freesansbold.ttf', 24)

# список цветов, взято из интернета
colors = {0: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 139, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}

# инициализация плиток
board_values = [[0 for _ in range(4)] for _ in range(4)]


# задний фон
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
    pass


# плитки
def draw_pieces():
    for i in range(4):
        for j in range(4):
            value = board_values[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75])


# основной код
run = True
while run:
    timer.tick(fps)
    screen.fill('gray')
    draw_board()
    draw_pieces()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()
