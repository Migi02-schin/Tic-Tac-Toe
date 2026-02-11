import pygame
import sys

pygame.init()

WINDOW_SIZE = 300
HEIGHT = 360  
GRID_SIZE = 100
LINE_WIDTH = 5


PINK = (255, 182, 193)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
BUTTON_COLOR = (255, 105, 180)
BUTTON_HOVER = (255, 20, 147)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WINDOW_SIZE, HEIGHT))
pygame.display.set_caption('Tic-Tac-Toe')

font = pygame.font.SysFont(None, 40)
button_font = pygame.font.SysFont(None, 30)

game_board = [['' for _ in range(3)] for _ in range(3)]
current_player = 'X'
game_over = False
winner_line = None


button_rect = pygame.Rect(75, 310, 150, 40)

def check_win(board, player):
    global winner_line

    for row in range(3):
        if all(board[row][col] == player for col in range(3)):
            winner_line = ("row", row)
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            winner_line = ("col", col)
            return True

    if all(board[i][i] == player for i in range(3)):
        winner_line = ("diag", 0)
        return True

    if all(board[i][2-i] == player for i in range(3)):
        winner_line = ("diag", 1)
        return True

    return False

def draw_lines():
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK, (i * GRID_SIZE, 0),
                         (i * GRID_SIZE, WINDOW_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (0, i * GRID_SIZE),
                         (WINDOW_SIZE, i * GRID_SIZE), LINE_WIDTH)

def draw_x(row, col):
    offset = GRID_SIZE // 4
    pygame.draw.line(screen, RED,
                     (col * GRID_SIZE + offset, row * GRID_SIZE + offset),
                     ((col + 1) * GRID_SIZE - offset, (row + 1) * GRID_SIZE - offset),
                     LINE_WIDTH)
    pygame.draw.line(screen, RED,
                     ((col + 1) * GRID_SIZE - offset, row * GRID_SIZE + offset),
                     (col * GRID_SIZE + offset, (row + 1) * GRID_SIZE - offset),
                     LINE_WIDTH)

def draw_o(row, col):
    offset = GRID_SIZE // 4
    pygame.draw.circle(screen, GREEN,
                       (col * GRID_SIZE + GRID_SIZE // 2,
                        row * GRID_SIZE + GRID_SIZE // 2),
                       GRID_SIZE // 2 - offset,
                       LINE_WIDTH)

def draw_winner_line():
    if winner_line:
        if winner_line[0] == "row":
            y = winner_line[1] * GRID_SIZE + GRID_SIZE // 2
            pygame.draw.line(screen, BLUE, (0, y),
                             (WINDOW_SIZE, y), 6)

        elif winner_line[0] == "col":
            x = winner_line[1] * GRID_SIZE + GRID_SIZE // 2
            pygame.draw.line(screen, BLUE, (x, 0),
                             (x, WINDOW_SIZE), 6)

        elif winner_line[0] == "diag":
            if winner_line[1] == 0:
                pygame.draw.line(screen, BLUE,
                                 (0, 0), (WINDOW_SIZE, WINDOW_SIZE), 6)
            else:
                pygame.draw.line(screen, BLUE,
                                 (WINDOW_SIZE, 0), (0, WINDOW_SIZE), 6)
def draw_button():
    mouse_pos = pygame.mouse.get_pos()

    
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER, button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)

   
    pygame.draw.rect(screen, BLACK, button_rect, 3)

   
    text = button_font.render("RESET", True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)


def reset_game():
    global game_board, current_player, game_over, winner_line
    game_board = [['' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    game_over = False
    winner_line = None

running = True

while running:
    screen.fill(PINK)
    draw_lines()
    draw_button()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                reset_game()

            elif not game_over:
                x, y = event.pos
                if y < WINDOW_SIZE:
                    row, col = y // GRID_SIZE, x // GRID_SIZE

                    if game_board[row][col] == '':
                        game_board[row][col] = current_player

                        if check_win(game_board, current_player):
                            print(f"Player {current_player} wins!")
                            game_over = True
                        else:
                            current_player = 'O' if current_player == 'X' else 'X'

    for row in range(3):
        for col in range(3):
            if game_board[row][col] == 'X':
                draw_x(row, col)
            elif game_board[row][col] == 'O':
                draw_o(row, col)

    if game_over:
        draw_winner_line()

    pygame.display.flip()

pygame.quit()
sys.exit()
