# импорт необходимых библиотек
import pygame
import random


# основные данные
pygame.init()
pygame.mouse.set_visible(False)
width = 400
height = 560
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("2048-")
timer = pygame.time.Clock()
fps = 60
levell = 0
font = pygame.font.Font('freesansbold.ttf', 24)
music = pygame.mixer.music.load('song.mp3')
crash = pygame.mixer.Sound("soundeffect.mp3")
pygame.mixer.music.play(-1, 0.0)


# список цветов, взято из интернета
colors = {0: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
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
datab = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
new_spawn = True
cheats = False
init_count = 0
score = 0
with open('high_score', 'r') as file:
    init_high = int(file.readline())
with open('init_block', 'r') as file:
    init_block = int(file.readline())
directionn = ""
high_score = init_high
max_block = init_block


# задний фон
def draw_over():
    pygame.draw.rect(screen, "black", [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render("Game Over!", True, "white")
    game_over_text2 = font.render("Press Space to Restart", True, "white")
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))


# ход игрока
def turn(direct, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direct == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
                            and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    elif direct == 'DOWN':
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] \
                            and not merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True

    elif direct == 'LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direct == 'RIGHT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] \
                            and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True
    return board


# новые плитки
def pieces_new(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full


# текст снизу
def bg_text():
    pygame.draw.rect(screen, colors["bg"], [0, 0, 400, 400], 0, 10)
    score_text = font.render(f"Score: {score}", True, "black")
    high_score_text = font.render(f"High Score: {high_score}", True, "black")
    max_block_text = font.render(f"Max Block: {max_block}", True, "black")
    levell_text = font.render(f"Level: {levell}", True, "black")
    cheat_status = font.render(f"Cheats: {cheats}", True, "black")
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))
    screen.blit(max_block_text, (10, 490))
    screen.blit(levell_text, (10, 530))
    screen.blit(cheat_status, (210, 530))
    pass


# плитки
def pieces_draw(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors["light text"]
            else:
                value_color = colors["dark text"]
            if value <= 2048:
                color = colors[value]
            else:
                color = colors["other"]
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font("freesansbold.ttf", 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, "black", [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)


# основной код
run = True
do = True
while run:
    timer.tick(fps)
    screen.fill("gray")
    bg_text()
    pieces_draw(datab)
    if new_spawn or init_count < 2:
        datab, game_over = pieces_new(datab)
        new_spawn = False
        init_count += 1
    if directionn != "":
        datab = turn(directionn, datab)
        directionn = ""
        new_spawn = True
    if game_over:
        # запись рекордов
        draw_over()
        if high_score >= init_high and not cheats:
            file = open("high_score", "w")
            file.write(f'{high_score}')
            file.close()
            init_high = high_score
        if max_block >= init_block and not cheats:
            file = open("init_block", "w")
            file.write(f'{max_block}')
            file.close()
            init_block = max_block
    # инициализация хода
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                directionn = "UP"
            elif event.key == pygame.K_DOWN:
                directionn = "DOWN"
            elif event.key == pygame.K_LEFT:
                directionn = "LEFT"
            elif event.key == pygame.K_RIGHT:
                directionn = "RIGHT"
            elif event.key == pygame.K_SPACE:
                pygame.mixer.music.play(-1, 0.0)
                datab = [[0 for _ in range(4)] for _ in range(4)]
                new_spawn = True
                init_count = 0
                score = 0
                directionn = ""
                game_over = False
            if event.key == pygame.K_KP_ENTER:
                cheats = True
                high_score = 999999999
                max_block = 999999999
                pygame.mixer.music.play(-1, 0.0)
                datab = [[16777216 for _ in range(4)] for _ in range(4)]
                new_spawn = True
                init_count = 0
                score = 0
                directionn = ""
                game_over = False
            if event.key == pygame.K_1:
                cheats = True
                high_score = 999999999
                max_block = 999999999
                pygame.mixer.music.play(-1, 0.0)
                datab = [[2 for _ in range(4)] for _ in range(4)]
                new_spawn = True
                init_count = 0
                score = 0
                directionn = ""
                game_over = False
            if event.key == pygame.K_2:
                cheats = True
                high_score = 999999999
                max_block = 999999999
                pygame.mixer.music.play(-1, 0.0)
                datab = [[4 for _ in range(4)] for _ in range(4)]
                new_spawn = True
                init_count = 0
                score = 0
                directionn = ""
                game_over = False
            if event.key == pygame.K_3:
                cheats = True
                high_score = 999999999
                max_block = 999999999
                pygame.mixer.music.play(-1, 0.0)
                datab = [[8 for _ in range(4)] for _ in range(4)]
                new_spawn = True
                init_count = 0
                score = 0
                directionn = ""
                game_over = False
            if event.key == pygame.K_4:
                cheats = True
                high_score = 999999999
                max_block = 999999999
                pygame.mixer.music.play(-1, 0.0)
                datab = [[16 for _ in range(4)] for _ in range(4)]
                new_spawn = True
                init_count = 0
                score = 0
                directionn = ""
                game_over = False
            if event.key == pygame.K_5:
                cheats = True
                high_score = 999999999
                max_block = 999999999
                pygame.mixer.music.play(-1, 0.0)
                datab = [[32 for _ in range(4)] for _ in range(4)]
                new_spawn = True
                init_count = 0
                score = 0
                directionn = ""
                game_over = False
            if event.key == pygame.K_6:
                cheats = True
                high_score = 999999999
                max_block = 999999999
                pygame.mixer.music.play(-1, 0.0)
                datab = [[64 for _ in range(4)] for _ in range(4)]
                new_spawn = True
                init_count = 0
                score = 0
                directionn = ""
                game_over = False
            if event.key == pygame.K_7:
                cheats = True
                high_score = 999999999
                max_block = 999999999
                pygame.mixer.music.play(-1, 0.0)
                datab = [[128 for _ in range(4)] for _ in range(4)]
                new_spawn = True
                init_count = 0
                score = 0
                directionn = ""
                game_over = False
            if event.key == pygame.K_8:
                cheats = True
                high_score = 999999999
                max_block = 999999999
                pygame.mixer.music.play(-1, 0.0)
                datab = [[256 for _ in range(4)] for _ in range(4)]
                new_spawn = True
                init_count = 0
                score = 0
                directionn = ""
                game_over = False
            if event.key == pygame.K_9:
                cheats = True
                high_score = 999999999
                max_block = 999999999
                pygame.mixer.music.play(-1, 0.0)
                datab = [[512 for _ in range(4)] for _ in range(4)]
                new_spawn = True
                init_count = 0
                score = 0
                directionn = ""
                game_over = False
            if event.key == pygame.K_0:
                cheats = True
                high_score = 999999999
                max_block = 999999999
                pygame.mixer.music.play(-1, 0.0)
                datab = [[1024 for _ in range(4)] for _ in range(4)]
                new_spawn = True
                init_count = 0
                score = 0
                directionn = ""
                game_over = False
            if event.key == pygame.K_BACKSPACE:
                cheats = True
                high_score = 999999999
                max_block = 999999999
                pygame.mixer.music.play(-1, 0.0)
                datab = [[16777216 for _ in range(4)] for _ in range(4)]
                new_spawn = True
                init_count = 0
                score = 0
                directionn = ""
                game_over = False
            if game_over:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.play(-1, 0.0)
                    datab = [[0 for _ in range(4)] for _ in range(4)]
                    new_spawn = True
                    init_count = 0
                    score = 0
                    directionn = ""
                    game_over = False

    if score > high_score:
        high_score = score
    for i in range(4):
        for j in range(4):
            if datab[i][j] > max_block:
                max_block = datab[i][j]
                levell += 1
                pygame.mixer.music.play(-1, 0.0)
                datab = [[0 for _ in range(4)] for _ in range(4)]
                new_spawn = True
                init_count = 0
                score = 0
                directionn = ""
                game_over = False
                pygame.mixer.Sound.play(crash)
    pygame.display.flip()
pygame.quit()
