import pygame
import sys

# --- Configuración ---
BOARD_SIZE = 9
SQUARE_SIZE = 100
WIDTH = BOARD_SIZE * SQUARE_SIZE
HEIGHT = SQUARE_SIZE

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Representación lógica
# +1 = Toad, -1 = Frog, 0 = vacío
board = [1, 1, 1, 0, -1, -1, -1, 0, 0]  # puedes ajustar la disposición
turn = 1  # 1 = toads, -1 = frogs

# Inicialización pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Toads and Frogs")

# Carga imágenes (pon tus paths aquí)
toad_img = pygame.image.load("toad.png")
frog_img = pygame.image.load("frog.png")

# Escalar imágenes al tamaño de la casilla
toad_img = pygame.transform.scale(toad_img, (SQUARE_SIZE, SQUARE_SIZE))
frog_img = pygame.transform.scale(frog_img, (SQUARE_SIZE, SQUARE_SIZE))

# Estado de selección
selected = None
valid_moves = []


def draw_board():
    screen.fill(WHITE)
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


def get_valid_moves(index):
    piece = board[index]
    moves = []
    if piece == 1:  # Toad
        # Step
        if index + 1 < BOARD_SIZE and board[index + 1] == 0:
            moves.append(index + 1)
        # Hop
        if index + 2 < BOARD_SIZE and board[index + 1] == -1 and board[index + 2] == 0:
            moves.append(index + 2)
    elif piece == -1:  # Frog
        # Step
        if index - 1 >= 0 and board[index - 1] == 0:
            moves.append(index - 1)
        # Hop
        if index - 2 >= 0 and board[index - 1] == 1 and board[index - 2] == 0:
            moves.append(index - 2)
    return moves


def handle_click(pos):
    global selected, valid_moves, turn
    index = pos[0] // SQUARE_SIZE

    if selected is None:
        # Selección de pieza
        if board[index] == turn:
            moves = get_valid_moves(index)
            if moves:
                selected = index
                valid_moves = moves
    else:
        # Intentar mover
        if index in valid_moves:
            board[index] = board[selected]
            board[selected] = 0
            # Cambio de turno
            turn *= -1
        # Reset selección
        selected = None
        valid_moves = []


def has_moves(player):
    for i, piece in enumerate(board):
        if piece == player and get_valid_moves(i):
            return True
    return False


# --- Loop principal ---
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if has_moves(turn):  # solo si quedan movimientos
                handle_click(pygame.mouse.get_pos())

    draw_board()
    pygame.display.flip()
    clock.tick(30)
