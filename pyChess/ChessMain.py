import os
import pygame as p
from ChessEngine import GameState, Move

# Initialize constants
WIDTH = HEIGHT = 512
DIMENSION = 8  # 8x8 chess board
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 30
IMAGES = {}
BEIGE = (219, 173, 114)
BROWN = (143, 75, 26)

def loadImages():
    """Load images for chess pieces."""
    pieces = ["wp", "bp", "wR", "bR", "wN", "bN", "wB", "bB", "wQ", "bQ", "wK", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))

def main():
    """Main driver for the chess game."""
    print(os.getcwd())
    p.init()
    p.font.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    gs = GameState()
    loadImages()
    font = p.font.Font("Roboto-Regular.ttf", SQ_SIZE // 4)

    piece_dragging = None
    start_row, start_col = None, None

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x, y) location of the mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if gs.board[row][col] is not None:  # Check if there's a piece to move
                    piece_dragging = True
                    start_pos = (row, col)
            elif e.type == p.MOUSEBUTTONUP:
                if piece_dragging:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    # Move the piece
                    gs.board[row][col] = gs.board[start_pos[0]][start_pos[1]]
                    gs.board[start_pos[0]][start_pos[1]] = None
                    piece_dragging = False

        drawGameState(screen, gs, font, piece_dragging)
        p.display.flip()
        clock.tick(MAX_FPS)

    p.quit()


def drawGameState(screen, gs, font, piece_dragging):
    """Draw the current game state."""
    drawBoard(screen, font)
    drawPieces(screen, gs.board)
    if piece_dragging is not None:
        drawDraggingPiece(screen, piece_dragging)

def drawBoard(screen, font):
    """Draw the chess board."""
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = BEIGE if (c + r) % 2 == 0 else BROWN
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            drawBoardLabels(screen, font, r, c)

def drawBoardLabels(screen, font, r, c):
    """Draw file letters and rank numbers on the board."""
    if r == DIMENSION - 1:
        label = chr(c + 97)
        text = font.render(label, True, (0, 0, 0))
        screen.blit(text, (c * SQ_SIZE + SQ_SIZE // 2 - text.get_width() // 2, HEIGHT - text.get_height()))
    if c == 0:
        label = str(8 - r)
        text = font.render(label, True, (0, 0, 0))
        screen.blit(text, (0, r * SQ_SIZE + SQ_SIZE // 2 - text.get_height() // 2))

def drawPieces(screen, board):
    """Draw the chess pieces on the board."""
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                if piece in IMAGES:
                    screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                else:
                    print(f"Missing image for piece: {piece}")

def drawDraggingPiece(screen, piece_dragging):
    """Draw the piece being dragged."""
    mouse_x, mouse_y = p.mouse.get_pos()
    screen.blit(IMAGES[piece_dragging], (mouse_x - SQ_SIZE // 2, mouse_y - SQ_SIZE // 2))

if __name__ == "__main__":
    main()
