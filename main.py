import pygame
import ChessEngine

pygame.init()

WIDTH = HEIGHT = 512
DIMENSION = 8
SQUAR_SIZE = HEIGHT // DIMENSION
IMAGES = {}


pygame.display.set_caption("Chess")
icon = pygame.image.load('./image/chess.png')
pygame.display.set_icon(icon)


def loadImages():
    pieces = [
        "wR", "wN", "wB", "wQ", "wK", "wP",
        "bR", "bN", "bB", "bQ", "bK", "bP"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(
                        pygame.image.load("image/" + piece + ".png"),
                        (SQUAR_SIZE, SQUAR_SIZE))


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(pygame.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False

    loadImages()
    running = True
    sqselected = ()
    playerClicks = []

    while running:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                running = False
            elif event.type is pygame.MOUSEBUTTONDOWN:
                loction = pygame.mouse.get_pos()
                column = loction[0] // SQUAR_SIZE
                row = loction[1] // SQUAR_SIZE
                if sqselected is (row, column):
                    sqselected = ()
                    playerClicks = []
                else:
                    sqselected = (row, column)
                    playerClicks.append(sqselected)

                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0],
                                            playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            sqselected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqselected]
            # key handlers
            elif event.type is pygame.KEYDOWN:
                if event.key is pygame.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        pygame.display.flip()


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [pygame.Color("white"), pygame.Color("light blue")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            pygame.draw.rect(
                screen, color,
                pygame.Rect(column*SQUAR_SIZE, row*SQUAR_SIZE,
                            SQUAR_SIZE, SQUAR_SIZE))


def drawPieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece],
                            pygame.Rect(column*SQUAR_SIZE, row*SQUAR_SIZE,
                                        SQUAR_SIZE, SQUAR_SIZE))


if __name__ == "__main__":
    main()
