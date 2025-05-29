import medieval_chess as chess
import pygame
import os
import sys
import tkinter as tk
from tkinter import simpledialog

# Determine if we're running as a script or frozen executable
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Update the image path to use the resource_path function
IMAGE_PATH = resource_path(r"images")

# Get screen dimensions
def get_screen_dimensions():
    pygame.init()
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    return screen_width, screen_height

# Calculate dynamic dimensions
def calculate_dimensions():
    screen_width, screen_height = get_screen_dimensions()
    
    # Calculate board size (80% of the smaller screen dimension)
    board_size = min(screen_width, screen_height) * 0.8
    
    # Ensure board size is divisible by 8 for clean squares
    board_size = (board_size // 8) * 8
    
    # Calculate menu height (5% of screen height, minimum 30px)
    menu_height = max(int(screen_height * 0.05), 30)
    
    # Calculate total window dimensions
    width = board_size
    height = board_size + menu_height
    
    # Calculate square size
    square_size = board_size // 8
    
    return {
        'width': width,
        'height': height,
        'board_size': board_size,
        'menu_height': menu_height,
        'square_size': square_size
    }

# Get dimensions
DIMENSIONS = calculate_dimensions()
WIDTH = DIMENSIONS['width']
MENU_HEIGHT = DIMENSIONS['menu_height']
BOARD_SIZE = DIMENSIONS['board_size']
HEIGHT = DIMENSIONS['height']
SQUARE_SIZE = DIMENSIONS['square_size']

# Colors
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
HIGHLIGHT_COLOR = (101, 67, 33, 128)  # Semi-transparent dark brown for possible moves
CAPTURE_COLOR = (140, 120, 100, 160)  # Lighter semi-transparent color for captures

# Add to the constants section
BOARD_OFFSET_Y = MENU_HEIGHT  # Offset the board to make room for the menu

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.is_hovered = False

    def draw(self, screen):
        color = (min(self.color[0] + 30, 255), min(self.color[1] + 30, 255), min(self.color[2] + 30, 255)) if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Scale font size based on button height
        font_size = int(self.rect.height * 0.5)  # Font size is 50% of button height
        font = pygame.font.SysFont("arial", font_size)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

# Example FEN position
EXAMPLE_FEN = "rBB2qr1/n2pn3/1pp2k1p/4pPp1/4P3/2PbbNN1/P1QK4/R7 w - - 0 1"

def get_fen_from_user():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    fen = simpledialog.askstring("Load FEN", "Enter FEN string:", initialvalue=EXAMPLE_FEN)
    if fen:
        try:
            # Validate FEN by attempting to create a board
            chess.Board(fen)
            return fen
        except ValueError:
            return None
    return None

def show_menu():
    pygame.init()
    pygame.font.init()  # Initialize the font system
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Medieval Chess")
    
    # Calculate button dimensions
    button_width = WIDTH * 0.6
    button_height = HEIGHT * 0.1
    button_spacing = HEIGHT * 0.05
    
    # Create buttons with dynamic positioning
    new_game_btn = Button(
        (WIDTH - button_width) // 2,
        HEIGHT * 0.3,
        button_width,
        button_height,
        "New Game",
        WHITE
    )
    load_fen_btn = Button(
        (WIDTH - button_width) // 2,
        HEIGHT * 0.3 + button_height + button_spacing,
        button_width,
        button_height,
        "Load Position (FEN)",
        WHITE
    )
    quit_btn = Button(
        (WIDTH - button_width) // 2,
        HEIGHT * 0.3 + 2 * (button_height + button_spacing),
        button_width,
        button_height,
        "Quit",
        WHITE
    )
    
    running = True
    while running:
        screen.fill(LIGHT_BROWN)
        
        # Draw title with dynamic font size
        font_size = int(HEIGHT * 0.06)  # Font size is 6% of screen height
        font = pygame.font.SysFont("arial", font_size)
        title = font.render("Medieval Chess", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH//2, HEIGHT * 0.15))
        screen.blit(title, title_rect)
        
        # Draw buttons
        new_game_btn.draw(screen)
        load_fen_btn.draw(screen)
        quit_btn.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if new_game_btn.handle_event(event):
                pygame.quit()
                return "new_game"
            elif load_fen_btn.handle_event(event):
                pygame.quit()
                return "load_fen"
            elif quit_btn.handle_event(event):
                pygame.quit()
                sys.exit()
        
        pygame.display.flip()

# Initialize pygame
def initialize_pygame():
    pygame.init()
    return pygame.display.set_mode((WIDTH, HEIGHT))

# Load images for pieces
def load_piece_images(image_path):
    piece_images = {}
    for piece in ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']:
        piece_images[f'w_{piece}'] = pygame.image.load(os.path.join(image_path, f"w_{piece}_png_1024px.png"))
        piece_images[f'b_{piece}'] = pygame.image.load(os.path.join(image_path, f"b_{piece}_png_1024px.png"))
    
    # Scale pieces to fit the square size
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
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE + BOARD_OFFSET_Y, SQUARE_SIZE, SQUARE_SIZE))

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
            screen.blit(piece_images[image_key], (col * SQUARE_SIZE, row * SQUARE_SIZE + BOARD_OFFSET_Y))

# Get the board square under the mouse position
def get_square_under_mouse(pos):
    x, y = pos
    y = y - BOARD_OFFSET_Y  # Adjust for menu
    if y < 0:  # Click was in the menu area
        return None
    col = int(x // SQUARE_SIZE)  # Ensure integer division
    row = int(y // SQUARE_SIZE)  # Ensure integer division
    if 0 <= row < 8 and 0 <= col < 8:  # Make sure click is within board
        return int(chess.square(col, 7 - row))  # Ensure integer return
    return None

# Display a message at the center of the screen
def display_message(screen, message, duration=3000):
    # Calculate font size based on screen height
    font_size = int(HEIGHT * 0.04)  # Font size is 4% of screen height
    font = pygame.font.SysFont("arial", font_size)
    text = font.render(message, True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    # Store the portion of the screen that will be covered
    background = screen.copy()
    
    # Draw message
    screen.blit(text, text_rect)
    pygame.display.flip()
    
    # Wait
    pygame.time.wait(duration)
    
    # Restore the background
    screen.blit(background, (0, 0))
    pygame.display.flip()

# Add new function for the in-game menu
def draw_game_menu(screen, board):
    # Draw menu background
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, MENU_HEIGHT))
    
    # Create menu buttons
    font = pygame.font.SysFont("arial", 16)
    
    # Export FEN button
    export_text = font.render("Export FEN", True, BLACK)
    export_rect = export_text.get_rect(topleft=(10, 10))
    pygame.draw.rect(screen, WHITE, (5, 5, 100, 30))
    screen.blit(export_text, export_rect)
    
    # Main Menu button
    menu_text = font.render("Main Menu", True, BLACK)
    menu_rect = menu_text.get_rect(topleft=(WIDTH - 110, 10))
    pygame.draw.rect(screen, WHITE, (WIDTH - 115, 5, 100, 30))
    screen.blit(menu_text, menu_rect)
    
    return pygame.Rect(5, 5, 100, 30), pygame.Rect(WIDTH - 115, 5, 100, 30)

def copy_to_clipboard(text):
    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()
    root.destroy()

def draw_possible_moves(screen, board, selected_square):
    """Draw circles on squares where the selected piece can move"""
    if selected_square is None:
        return
        
    piece = board.piece_at(selected_square)
    if piece is None:
        return
        
    # Create surfaces for the move indicators
    normal_indicator = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    capture_indicator = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    
    # Draw both indicators the same size
    circle_size = SQUARE_SIZE // 4  # Using the same size for both
    pygame.draw.circle(normal_indicator, HIGHLIGHT_COLOR, 
                      (SQUARE_SIZE // 2, SQUARE_SIZE // 2), 
                      circle_size)
    pygame.draw.circle(capture_indicator, CAPTURE_COLOR, 
                      (SQUARE_SIZE // 2, SQUARE_SIZE // 2), 
                      circle_size)
    
    # Show possible moves
    for move in board.legal_moves:
        if move.from_square == selected_square:
            dest_col = chess.square_file(move.to_square)
            dest_row = 7 - chess.square_rank(move.to_square)
            
            # Check if it's a capture move
            target_piece = board.piece_at(move.to_square)
            if target_piece is not None:
                screen.blit(capture_indicator, 
                          (dest_col * SQUARE_SIZE, 
                           dest_row * SQUARE_SIZE + BOARD_OFFSET_Y))
            else:
                screen.blit(normal_indicator, 
                          (dest_col * SQUARE_SIZE, 
                           dest_row * SQUARE_SIZE + BOARD_OFFSET_Y))

# Game loop for starting from a given FEN
def start_game_from_fen(fen=None, print_moves=False):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.font.init()  # Initialize the font system
    piece_images = load_piece_images(IMAGE_PATH)
    board = initialize_board(fen)
    pygame.display.set_caption("Medieval Chess")
    
    running = True
    selected_square = None
    possible_moves = []  # Store possible moves for the selected piece

    while running:
        screen.fill(GRAY)  # Fill background
        
        # Draw the menu and get button rectangles
        export_btn, menu_btn = draw_game_menu(screen, board)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check menu button clicks
                if export_btn.collidepoint(mouse_pos):
                    # Copy current FEN to clipboard
                    fen = board.fen()
                    copy_to_clipboard(fen)
                    # Show feedback
                    display_message(screen, "FEN copied to clipboard!", duration=1000)
                elif menu_btn.collidepoint(mouse_pos):
                    return "menu"  # Return to main menu
                else:
                    clicked_square = get_square_under_mouse(mouse_pos)
                    
                    if clicked_square is not None:
                        piece = board.piece_at(clicked_square)
                        
                        # If clicking on a piece of the current player's color
                        if piece and piece.color == board.turn:
                            # If clicking on a different piece, update selection
                            if clicked_square != selected_square:
                                selected_square = clicked_square
                                # Calculate possible moves for the selected piece
                                possible_moves = [move.to_square for move in board.legal_moves 
                                                if move.from_square == selected_square]
                        # If a piece is selected and clicking on a valid move
                        elif selected_square is not None and clicked_square in possible_moves:
                            # Make the move
                            move = chess.Move(selected_square, clicked_square)
                            
                            # Handle pawn promotion
                            piece = board.piece_at(selected_square)
                            if piece and piece.piece_type == chess.PAWN and (
                                chess.square_rank(clicked_square) == 0 or chess.square_rank(clicked_square) == 7
                            ):
                                move = chess.Move(selected_square, clicked_square, promotion=chess.QUEEN_GRACE_JUMP)
                            
                            board.push(move)
                            if print_moves:
                                print(f"Move: {chess.square_name(selected_square)}{chess.square_name(clicked_square)}")
                            
                            # Check game end conditions
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
                            
                            # Reset selection
                            selected_square = None
                            possible_moves = []
                        # If clicking on an invalid square, clear selection
                        else:
                            selected_square = None
                            possible_moves = []

        draw_board(screen)
        draw_pieces(screen, board, piece_images)

        # Draw the selected square highlight and possible moves
        if selected_square is not None:
            # Highlight selected square
            col = chess.square_file(selected_square)
            row = 7 - chess.square_rank(selected_square)
            pygame.draw.rect(screen, (0, 255, 0), 
                           (col * SQUARE_SIZE, row * SQUARE_SIZE + BOARD_OFFSET_Y, SQUARE_SIZE, SQUARE_SIZE), 
                           width=3)
            
            # Draw possible moves
            for move_square in possible_moves:
                dest_col = chess.square_file(move_square)
                dest_row = 7 - chess.square_rank(move_square)
                
                # Check if it's a capture move
                target_piece = board.piece_at(move_square)
                if target_piece is not None:
                    # Draw capture indicator
                    capture_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    pygame.draw.circle(capture_surface, CAPTURE_COLOR, 
                                    (SQUARE_SIZE // 2, SQUARE_SIZE // 2), 
                                    SQUARE_SIZE // 4)
                    screen.blit(capture_surface, 
                              (dest_col * SQUARE_SIZE, 
                               dest_row * SQUARE_SIZE + BOARD_OFFSET_Y))
                else:
                    # Draw normal move indicator
                    move_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    pygame.draw.circle(move_surface, HIGHLIGHT_COLOR, 
                                    (SQUARE_SIZE // 2, SQUARE_SIZE // 2), 
                                    SQUARE_SIZE // 4)
                    screen.blit(move_surface, 
                              (dest_col * SQUARE_SIZE, 
                               dest_row * SQUARE_SIZE + BOARD_OFFSET_Y))

        pygame.display.flip()

    pygame.quit()
    return None

def main():
    while True:
        choice = show_menu()
        if choice == "new_game":
            result = start_game_from_fen(print_moves=True)
            if result != "menu":  # If we didn't return to menu, exit
                break
        elif choice == "load_fen":
            fen = get_fen_from_user()
            if fen:
                result = start_game_from_fen(fen, print_moves=True)
                if result != "menu":  # If we didn't return to menu, exit
                    break

if __name__ == "__main__":
    main()