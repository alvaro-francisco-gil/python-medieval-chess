import medieval_chess as chess
import pygame
import os

IMAGE_PATH = r"C:\Users\alvar\Githubs\python-medieval-chess\images\JohnPablok Cburnett Chess Zip\JohnPablok Cburnett Chess set\\PNGs\No shadow\1024h"

# Initialize pygame
def initialize_pygame():
    pygame.init()
    return pygame.display.set_mode((WIDTH, HEIGHT))

# Screen dimensions
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8

# Colors
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)

# Load images for pieces
def load_piece_images(image_path):
    piece_images = {}
    for piece in ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']:
        piece_images[f'w_{piece}'] = pygame.image.load(os.path.join(image_path, f"w_{piece}_png_1024px.png"))
        piece_images[f'b_{piece}'] = pygame.image.load(os.path.join(image_path, f"b_{piece}_png_1024px.png"))
    
    for key in piece_images:
        piece_images[key] = pygame.transform.scale(piece_images[key], (SQUARE_SIZE, SQUARE_SIZE))
    
    return piece_images

# Mapping single-character piece symbols to full names
PIECE_NAME_MAP = {
    'p': 'pawn',
    'r': 'rook',
    'n': 'knight',
    'b': 'bishop',
    'q': 'queen',
    'k': 'king'
}

# Initialize the board with a custom position
def initialize_board(fen=None):
    return chess.Board(fen) if fen else chess.Board()

# Draw the chessboard
def draw_board(screen):
    for row in range(8):
        for col in range(8):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw the pieces on the board
def draw_pieces(screen, board, piece_images):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row = 7 - (square // 8)
            col = square % 8
            color = 'w' if piece.color else 'b'
            piece_name = PIECE_NAME_MAP[piece.symbol().lower()]
            image_key = f"{color}_{piece_name}"
            screen.blit(piece_images[image_key], (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Get the board square under the mouse position
def get_square_under_mouse(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return chess.square(col, 7 - row)

# Display a message at the center of the screen
def display_message(screen, message):
    font = pygame.font.SysFont("arial", 36)
    text = font.render(message, True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)

# Game loop for starting from a given FEN
def start_game_from_fen(fen=None, print_moves=False):
    screen = initialize_pygame()
    piece_images = load_piece_images(IMAGE_PATH)
    board = initialize_board(fen)
    pygame.display.set_caption("Chess Game")
    
    running = True
    selected_square = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                selected_square = get_square_under_mouse(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONUP:
                destination_square = get_square_under_mouse(pygame.mouse.get_pos())
                if selected_square is not None:  # Check if a piece was selected
                    move = chess.Move(selected_square, destination_square)

                    piece = board.piece_at(selected_square)
                    if piece and piece.piece_type == chess.PAWN and (
                        chess.square_rank(destination_square) == 0 or chess.square_rank(destination_square) == 7
                    ):
                        move = chess.Move(selected_square, destination_square, promotion=chess.QUEEN_GRACE_JUMP)

                    if move in list(board.legal_moves):
                        board.push(move)
                        if print_moves:
                            print(f"Move: {chess.square_name(selected_square)}{chess.square_name(destination_square)}")
                        if board.is_checkmate():
                            display_message(screen, "Checkmate! " + ("White wins!" if board.turn == chess.BLACK else "Black wins!"))
                            running = False
                        elif board.is_stalemate():
                            display_message(screen, "Stalemate! It's a draw!")
                            running = False
                        elif board.is_insufficient_material():
                            display_message(screen, "Draw due to insufficient material!")
                            running = False
                        elif board.is_seventyfive_moves():
                            display_message(screen, "Draw due to the 75-move rule!")
                            running = False
                        elif board.is_fivefold_repetition():
                            display_message(screen, "Draw due to fivefold repetition!")
                            running = False

                selected_square = None

            draw_board(screen)
            draw_pieces(screen, board, piece_images)

        if selected_square is not None and chess.SQUARES[0] <= selected_square <= chess.SQUARES[-1]:
            col = chess.square_file(selected_square)
            row = 7 - chess.square_rank(selected_square)
            pygame.draw.rect(screen, (0, 255, 0), (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), width=3)

        pygame.display.flip()

    pygame.quit()

# FEN = "rBB2qr1/n2pn3/1pp2k1p/4pPp1/4P3/2PbbNN1/P1QK4/R7 w - - 0 1"
# start_game_from_fen(FEN)

start_game_from_fen(print_moves=True)