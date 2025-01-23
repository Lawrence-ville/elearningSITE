import pygame
import time
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 800
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animation
IMAGES = {}

# Initialize a dictionary of images
def loadImages():
    pieces = ['wp', 'bp', 'wn', 'bn', 'wb', 'bb', 'wR', 'bR', 'wN', 'bN', 'wB',
              'bB', 'wQ', 'bQ']
    for piece in pieces:
        IMAGES[piece] = pygame.image.load('images/' + piece + '.png')

# Handle player input
def handleInput(screen, board, validMoves, selectedPiece, gameOver):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            location = pygame.mouse.get_pos()
            col = location[0] // SQ_SIZE
            row = location[1] // SQ_SIZE
            if selectedPiece == None:
                piece = board[row][col]
                if piece != '--':
                    validMoves = getValidMoves(board, piece)
                    if len(validMoves) > 0:
                        selectedPiece = piece
                        screen.blit(IMAGES[piece], (col * SQ_SIZE, row * SQ_SIZE))
            else:
                piece = board[row][col]
                if piece == selectedPiece:
                    selectedPiece = None
                elif piece != '--' and piece in validMoves:
                    selectedPiece = None
                    makeMove(board, validMoves, row, col)
                    time.sleep(0.5)
                    gameOver = isGameOver(board)
                    if gameOver:
                        print("Game Over")
                        pygame.quit()
                        sys.exit()
    return screen, board, validMoves, selectedPiece, gameOver

# Determine valid moves for a piece
def getValidMoves(board, piece):
    moves = []
    if piece != '--':
        if piece[1] == 'p':  # pawn
            if piece[0] == 'w':
                for i in range(1, 3):
                    if not onBoard((piece[2] - i, piece[3] - 1)) or board[(piece[2] - i)][piece[3] - 1] != '--':
                        break
                    moves.append((piece[2] - i, piece[3] - 1))
                if onBoard((piece[2] - 2, piece[3] - 1)) and board[(piece[2] - 2)][piece[3] - 1] == '--' and board[(piece[2] - 1)][piece[3] - 1] == '--':
                    moves.append((piece[2] - 2, piece[3] - 1))
            elif piece[0] == 'b':
                for i in range(1, 3):
                    if not onBoard((piece[2] + i, piece[3] - 1)) or board[(piece[2] + i)][piece[3] - 1] != '--':
                        break
                    moves.append((piece[2] + i, piece[3] - 1))
                if onBoard((piece[2] + 2, piece[3] - 1)) and board[(piece[2] + 2)][piece[3] - 1] == '--' and board[(piece[2] + 1)][piece[3] - 1] == '--':
                    moves.append((piece[2] + 2, piece[3] - 1))
        elif piece[1] == 'r':  # rook
            moves = rookMoves(board, piece)
        elif piece[1] == 'n':  # knight
            moves = knightMoves(board, piece)
        elif piece[1] == 'b':  # bishop
            moves = bishopMoves(board, piece)
        elif piece[1] == 'q':  # queen
            moves = queenMoves(board, piece)
        elif piece[1] == 'k':  # king
            moves = kingMoves(board, piece)
    return moves

# Make a move on the board
def makeMove(board, validMoves, row, col):
    board[row][col] = board[selectedPiece[2]][selectedPiece[3]]
    board[selectedPiece[2]][selectedPiece[3]] = '--'
    selectedPiece = None
    for i in range(len(validMoves)):
        if validMoves[i][0] == row and validMoves[i][1] == col:
            validMoves.pop(i)
            break

# Check if game is over
def isGameOver(board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            if board[row][col][0] == 'w' and kingAlive(board, row, col):
                return False
    return True

# Check if king is alive
def kingAlive(board, row, col):
    if board[row][col][1] == 'k':
        return True
    return False

# Check if a position is on the board
def onBoard(position):
    if position[0] > -1 and position[0] < 8 and position[1] > -1 and position[1] < 8:
        return True
    return False

# Main game loop
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    board = createBoard()
    validMoves = []
    selectedPiece = None
    gameOver = False
    loadImages()
    while not gameOver:
        for event in pygame.event.\