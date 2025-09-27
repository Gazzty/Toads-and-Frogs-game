import pygame
import sys

# --- Configuración ---
BOARD_SIZE = 9
SQUARE_SIZE = 100
WIDTH = BOARD_SIZE * SQUARE_SIZE
HEIGHT = SQUARE_SIZE + 100  # espacio extra para el botón

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Representación lógica
# +1 = Toad, -1 = Frog, 0 = vacío
def initial_board():
    return [1, 1, 1, 0, 0, 0, -1, -1, -1]


board = initial_board()
turn = 1  # 1 = toads, -1 = frogs

# Inicialización pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Toads and Frogs")

# Carga imágenes con tus paths
toad_img = pygame.image.load("./media/toad-svgrepo-com.svg")
frog_img = pygame.image.load("./media/frog-svgrepo-com.svg")

# Escalar imágenes al tamaño de la casilla
toad_img = pygame.transform.scale(toad_img, (SQUARE_SIZE, SQUARE_SIZE))
frog_img = pygame.transform.scale(frog_img, (SQUARE_SIZE, SQUARE_SIZE))

# Estado de selección
selected = None
valid_moves = []
game_over = False
winner = None

button_width = 200
button_height = 60
spacing = 20  # espacio entre botones

button_rect = pygame.Rect(WIDTH // 2 - button_width - spacing//2,
                          HEIGHT - 80,
                          button_width,
                          button_height)

quit_button = pygame.Rect(WIDTH // 2 + spacing//2,
                          HEIGHT - 80,
                          button_width,
                          button_height)


def draw_board():
    screen.fill(WHITE)

    # Mostrar turno
    font_turn = pygame.font.SysFont(None, 50)
    if not game_over:
        turn_text = "Toads turn" if turn == 1 else "Frogs turn"
        text_surface = font_turn.render(turn_text, True, BLACK)
        screen.blit(text_surface, (10, HEIGHT - 90))  # Arriba del área de botones

    # Dibujar tablero
    for i in range(BOARD_SIZE):
        rect = pygame.Rect(i * SQUARE_SIZE, 0, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(screen, BLACK, rect, 2)

        # Resaltado si es un movimiento válido
        if i in valid_moves:
            pygame.draw.rect(screen, GREEN, rect, 5)

        # Dibujar piezas
        if board[i] == 1:
            screen.blit(toad_img, rect.topleft)
        elif board[i] == -1:
            screen.blit(frog_img, rect.topleft)

    # Mensaje de ganador
    if game_over:
        font = pygame.font.SysFont(None, 72)
        if winner == 1:
            text = font.render("Toads win!", True, (0, 128, 0))
        else:
            text = font.render("Frogs win!", True, (0, 0, 128))
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, rect)

    # Botón Restart
    pygame.draw.rect(screen, GRAY, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 2)
    font = pygame.font.SysFont(None, 40)
    text = font.render("Restart", True, BLACK)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

    # Botón Quit
    pygame.draw.rect(screen, GRAY, quit_button)
    pygame.draw.rect(screen, BLACK, quit_button, 2)
    text = font.render("Quit", True, BLACK)
    text_rect = text.get_rect(center=quit_button.center)
    screen.blit(text, text_rect)


def get_valid_moves(index):
    piece = board[index]
    moves = []
    if piece == 1:  # Toad
        if index + 1 < BOARD_SIZE and board[index + 1] == 0:
            moves.append(index + 1)
        if index + 2 < BOARD_SIZE and board[index + 1] == -1 and board[index + 2] == 0:
            moves.append(index + 2)
    elif piece == -1:  # Frog
        if index - 1 >= 0 and board[index - 1] == 0:
            moves.append(index - 1)
        if index - 2 >= 0 and board[index - 1] == 1 and board[index - 2] == 0:
            moves.append(index - 2)
    return moves


def handle_click(pos):
    global selected, valid_moves, turn, game_over, winner, board

    # Click en botón Restart
    if button_rect.collidepoint(pos):
        restart_game()
        return
    
    if quit_button.collidepoint(pos):
        quit_game()
        return

    if game_over:
        return


    index = pos[0] // SQUARE_SIZE
    if index >= BOARD_SIZE:
        return

    if selected is None:
        if board[index] == turn:
            moves = get_valid_moves(index)
            if moves:
                selected = index
                valid_moves = moves
    else:
        if index in valid_moves:
            board[index] = board[selected]
            board[selected] = 0
            turn *= -1
            if not has_moves(turn):
                game_over = True
                winner = -turn
        selected = None
        valid_moves = []


def has_moves(player):
    for i, piece in enumerate(board):
        if piece == player and get_valid_moves(i):
            return True
    return False


def restart_game():
    global board, turn, selected, valid_moves, game_over, winner
    board = initial_board()
    turn = 1
    selected = None
    valid_moves = []
    game_over = False
    winner = None

def quit_game():
	pygame.quit()

# --- Loop principal ---
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(pygame.mouse.get_pos())

    draw_board()
    pygame.display.flip()
    clock.tick(30)
