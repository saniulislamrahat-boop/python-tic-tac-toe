
import pygame as pg
import os
import random
from sys import exit

# Pygame initialization
pg.init()

# Creating Window
width, height = 600, 600
win = pg.display.set_mode((width, height))
pg.display.set_caption("Tic-Tac-Toe")

# Auto-detect the folder where main.py lives (works on any drive / OS)
base_path = os.path.dirname(os.path.abspath(__file__))


def load_image(filename):
    """Load an image from the project folder with a clear error if missing."""
    path = os.path.join(base_path, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Missing image file: {path}\n"
            f"Make sure '{filename}' is in the same folder as main.py."
        )
    return pg.image.load(path).convert_alpha()


# Loading Images
board_img   = load_image("board.png")
cross_img   = load_image("cross.png")
circle_img  = load_image("circle.png")
button_img  = load_image("button.png")
button_img_rect = button_img.get_rect(center=(300, 550))

# Font
font = pg.font.Font(None, 24)

label_info = None
label_info_rect = None


def set_label(text):
    global label_info, label_info_rect
    label_info = font.render(text, True, (255, 255, 255))
    label_info_rect = label_info.get_rect(center=(300, 30))


# Menu buttons
mode_buttons = [
    {'text': 'Player vs Player', 'rect': pg.Rect(150, 250, 300, 60)},
    {'text': 'Player vs Bot',    'rect': pg.Rect(150, 340, 300, 60)},
]

difficulty_buttons = [
    {'text': 'Easy',   'rect': pg.Rect(200, 200, 200, 50)},
    {'text': 'Medium', 'rect': pg.Rect(200, 275, 200, 50)},
    {'text': 'Hard',   'rect': pg.Rect(200, 350, 200, 50)},
]

# State variables
screen = 'mode_select'     # 'mode_select' | 'difficulty_select' | 'game'
mode = None                # 'pvp' | 'pvb'
difficulty = None          # 'easy' | 'medium' | 'hard'

block_size = 120
is_player1_chance = True
game_over = False
pos = (0, 0)
pieces = []
temp = None

matrix = [
    ['-', '-', '-'],
    ['-', '-', '-'],
    ['-', '-', '-']
]

clock = pg.time.Clock()
set_label("Player 1's turn")  # placeholder, not shown on menu screens


# ---------- Helpers for dynamic labels ----------
def turn_label(player1):
    if mode == 'pvp':
        return "Player 1's turn" if player1 else "Player 2's turn"
    else:
        return "Your turn" if player1 else "Bot's turn"


def winner_label(symbol):
    if symbol == 'draw':
        return "It's a Draw!"
    if mode == 'pvp':
        return "Player 1 wins!" if symbol == 'x' else "Player 2 wins!"
    else:
        return "You win!" if symbol == 'x' else "Bot wins!"


# ---------- Game logic ----------
def checkClickedPosition(pos):
    for row in range(3):
        for col in range(3):
            if (120 + col * 120 < pos[0] < 240 + col * 120) and \
               (120 + row * 120 < pos[1] < 240 + row * 120):
                return (row + 1, col + 1)
    return None


def checkCompletion(matrix):
    """Returns (winner, line_start, line_end) or None.
       winner is 'x', 'o', or 'draw'."""
    for i in range(3):
        # Rows
        if matrix[i][0] == matrix[i][1] == matrix[i][2] and matrix[i][0] != "-":
            return (matrix[i][0],
                    (120, 120 * (i + 1) + 60),
                    (480, 120 * (i + 1) + 60))
        # Columns
        if matrix[0][i] == matrix[1][i] == matrix[2][i] and matrix[0][i] != "-":
            return (matrix[0][i],
                    (120 * (i + 1) + 60, 120),
                    (120 * (i + 1) + 60, 480))

    # Diagonals
    if matrix[0][0] == matrix[1][1] == matrix[2][2] and matrix[0][0] != "-":
        return (matrix[0][0], (120, 120), (480, 480))
    if matrix[0][2] == matrix[1][1] == matrix[2][0] and matrix[0][2] != "-":
        return (matrix[0][2], (480, 120), (120, 480))

    if all(cell != '-' for row in matrix for cell in row):
        return ('draw', (0, 0), (0, 0))

    return None


def minimax(matrix, depth, is_maximizing):
    result = checkCompletion(matrix)
    if result:
        winner = result[0]
        if winner == 'x':
            return -10 + depth, None
        elif winner == 'o':
            return 10 - depth, None
        elif winner == 'draw':
            return 0, None

    if is_maximizing:
        best_score = -float('inf')
        best_move = None
        for row in range(3):
            for col in range(3):
                if matrix[row][col] == '-':
                    matrix[row][col] = 'o'
                    score, _ = minimax(matrix, depth + 1, False)
                    matrix[row][col] = '-'
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = None
        for row in range(3):
            for col in range(3):
                if matrix[row][col] == '-':
                    matrix[row][col] = 'x'
                    score, _ = minimax(matrix, depth + 1, True)
                    matrix[row][col] = '-'
                    if score < best_score:
                        best_score = score
                        best_move = (row, col)
        return best_score, best_move


def get_random_move(matrix):
    available = [(r, c) for r in range(3) for c in range(3) if matrix[r][c] == '-']
    return random.choice(available) if available else None


def get_medium_move(matrix):
    # Winning move?
    for row in range(3):
        for col in range(3):
            if matrix[row][col] == '-':
                matrix[row][col] = 'o'
                res = checkCompletion(matrix)
                matrix[row][col] = '-'
                if res and res[0] == 'o':
                    return (row, col)
    # Blocking move?
    for row in range(3):
        for col in range(3):
            if matrix[row][col] == '-':
                matrix[row][col] = 'x'
                res = checkCompletion(matrix)
                matrix[row][col] = '-'
                if res and res[0] == 'x':
                    return (row, col)
    return get_random_move(matrix)


def restart():
    global is_player1_chance, game_over, pos, pieces, matrix, temp
    is_player1_chance = True
    game_over = False
    pos = (0, 0)
    pieces = []
    temp = None
    matrix = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
    if screen == 'game':
        set_label(turn_label(True))


def place_piece(row, col, symbol, img):
    """Place a piece, update the matrix, check for game over. Returns True if game ended."""
    global temp, game_over
    pieces.append([img, block_size * (col + 1) + 20, block_size * (row + 1) + 20])
    matrix[row][col] = symbol
    result = checkCompletion(matrix)
    if result:
        temp = result
        set_label(winner_label(result[0]))
        game_over = True
        return True
    return False


# ---------- Main loop ----------
ignore_up_event = False

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        # ESC on the difficulty screen goes back to mode select
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE and screen == 'difficulty_select':
                screen = 'mode_select'
                mode = None

        if event.type == pg.MOUSEBUTTONUP:
            if not ignore_up_event:
                pos = pg.mouse.get_pos()
            ignore_up_event = False

        if event.type == pg.MOUSEBUTTONDOWN:
            if screen == 'mode_select':
                for btn in mode_buttons:
                    if btn['rect'].collidepoint(event.pos):
                        if btn['text'] == 'Player vs Player':
                            mode = 'pvp'
                            difficulty = None
                            screen = 'game'
                            restart()
                        else:  # Player vs Bot
                            mode = 'pvb'
                            screen = 'difficulty_select'
                        ignore_up_event = True
                        break

            elif screen == 'difficulty_select':
                for btn in difficulty_buttons:
                    if btn['rect'].collidepoint(event.pos):
                        difficulty = btn['text'].lower()
                        screen = 'game'
                        restart()
                        ignore_up_event = True
                        break

            elif screen == 'game':
                if game_over and button_img_rect.collidepoint(event.pos):
                    screen = 'mode_select'
                    mode = None
                    difficulty = None
                    restart()
                    ignore_up_event = True

    win.fill((18, 18, 18))

    # ---------- Draw current screen ----------
    if screen == 'mode_select':
        title = font.render("Select Game Mode", True, (255, 255, 255))
        win.blit(title, title.get_rect(center=(300, 180)))
        for btn in mode_buttons:
            pg.draw.rect(win, (50, 50, 50), btn['rect'])
            text = font.render(btn['text'], True, (255, 255, 255))
            win.blit(text, text.get_rect(center=btn['rect'].center))

    elif screen == 'difficulty_select':
        title = font.render("Choose Difficulty Level", True, (255, 255, 255))
        win.blit(title, title.get_rect(center=(300, 150)))
        for btn in difficulty_buttons:
            pg.draw.rect(win, (50, 50, 50), btn['rect'])
            text = font.render(btn['text'], True, (255, 255, 255))
            win.blit(text, text.get_rect(center=btn['rect'].center))
        hint = font.render("Press ESC to go back", True, (150, 150, 150))
        win.blit(hint, hint.get_rect(center=(300, 450)))

    else:  # 'game'
        result = checkClickedPosition(pos)
        bot_playing = (mode == 'pvb' and not is_player1_chance)

        # Human turn
        if not game_over and not bot_playing and result:
            row, col = result[0] - 1, result[1] - 1
            if matrix[row][col] == '-':
                if is_player1_chance:
                    place_piece(row, col, 'x', cross_img)
                else:  # PvP: player 2 ('o')
                    place_piece(row, col, 'o', circle_img)

                if not game_over:
                    is_player1_chance = not is_player1_chance
                    set_label(turn_label(is_player1_chance))

        # Bot turn (PvBot only)
        if not game_over and bot_playing:
            move = None
            if difficulty == 'easy':
                move = get_random_move(matrix)
            elif difficulty == 'medium':
                move = get_medium_move(matrix)
            elif difficulty == 'hard':
                _, move = minimax(matrix, 0, True)

            if move:
                row, col = move
                place_piece(row, col, 'o', circle_img)
                if not game_over:
                    is_player1_chance = True
                    set_label(turn_label(True))

        pos = (0, 0)

        # Draw game elements
        win.blit(board_img, (120, 120))
        win.blit(label_info, label_info_rect)
        for piece in pieces:
            win.blit(piece[0], (piece[1], piece[2]))

        # Game-over UI
        if game_over:
            if temp and temp[1] != (0, 0):
                pg.draw.line(win, (255, 255, 255), temp[1], temp[2], 5)
            win.blit(button_img, button_img_rect)

    pg.display.update()
    clock.tick(60)