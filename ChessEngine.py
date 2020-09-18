class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.moveFunctions = {
            'P': self.getPawnMoves,
            'R': self.getRookMoves,
            'N': self.getKnightMoves,
            'B': self.getBishopMoves,
            'Q': self.getQueenMoves,
            'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False

    def makeMove(self, move):
        self.board[move.startRow][move.startColumn] = "--"
        self.board[move.endRow][move.endColumn] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endColumn)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endColumn)

        # pawnpromotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endColumn] = move.pieceMoved[0] + 'Q'

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startColumn] = move.pieceMoved
            self.board[move.endRow][move.endColumn] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startColumn)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startColumn)

    def getValidMoves(self):
        moves = self.getAllPossibleMoves()
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        # else:
        #     self.checkMate = False
        #     self.staleMate = False
        return moves

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(
                self.whiteKingLocation[0], self.whiteKingLocation[1]
                )
        else:
            return self.squareUnderAttack(
                self.blackKingLocation[0], self.blackKingLocation[1]
                )

    def squareUnderAttack(self, row, column):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == row and move.endColumn == column:
                return True
        return False

    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                turn = self.board[row][column][0]
                if (
                    (turn == 'w' and self.whiteToMove)
                        or (turn == 'b' and not self.whiteToMove)):
                    piece = self.board[row][column][1]
                    self.moveFunctions[piece](row, column, moves)
        return moves

    def getPawnMoves(self, row, column, moves):
        if self.whiteToMove:
            if self.board[row - 1][column] == "--":
                moves.append(Move((row, column), (row-1, column), self.board))
                if row == 6 and self.board[row - 2][column] == "--":
                    moves.append(
                        Move((row, column), (row-2, column), self.board)
                        )
            if column - 1 >= 0:
                if self.board[row-1][column-1][0] == 'b':
                    moves.append(
                        Move((row, column), (row-1, column - 1), self.board)
                        )
            if column + 1 <= 7:
                if self.board[row-1][column+1][0] == 'b':
                    moves.append(
                        Move((row, column), (row-1, column+1), self.board)
                        )
        else:
            if self.board[row + 1][column] == "--":
                moves.append(Move((row, column), (row+1, column), self.board))
                if row == 1 and self.board[row + 2][column] == "--":
                    moves.append(
                        Move((row, column), (row+2, column), self.board)
                        )
            if column - 1 >= 0:
                if self.board[row + 1][column - 1][0] == 'w':
                    moves.append(
                        Move((row, column), (row+1, column - 1), self.board)
                        )
            if column + 1 <= 7:
                if self.board[row + 1][column + 1][0] == 'w':
                    moves.append(
                        Move((row, column), (row+1, column+1), self.board)
                        )

    def getRookMoves(self, row, column, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endColumn = column + d[1] * i
                if 0 <= endRow < 8 and 0 <= endColumn < 8:
                    endPiece = self.board[endRow][endColumn]
                    if endPiece == "--":
                        moves.append(
                            Move(
                                (row, column), (endRow, endColumn), self.board
                                )
                            )
                    elif endPiece[0] == enemyColor:
                        moves.append(
                            Move(
                                (row, column), (endRow, endColumn), self.board
                                )
                            )
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, row, column, moves):
        knightMoves = (
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
            )
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = row + m[0]
            endColumn = column + m[1]
            if 0 <= endRow < 8 and 0 <= endColumn < 8:
                endPiece = self.board[endRow][endColumn]
                if endPiece[0] != allyColor:
                    moves.append(
                        Move((row, column), (endRow, endColumn), self.board)
                        )

    def getBishopMoves(self, row, column, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endColumn = column + d[1] * i
                if 0 <= endRow < 8 and 0 <= endColumn < 8:
                    endPiece = self.board[endRow][endColumn]
                    if endPiece == "--":
                        moves.append(
                            Move(
                                (row, column), (endRow, endColumn), self.board
                                ))
                    elif endPiece[0] == enemyColor:
                        moves.append(
                            Move(
                                (row, column), (endRow, endColumn), self.board)
                                )
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, row, column, moves):
        self.getRookMoves(row, column, moves)
        self.getBishopMoves(row, column, moves)

    def getKingMoves(self, row, column, moves):
        kingMoves = (
            (-1, -1), (-1, 0), (-1, 1), (0, -1),
            (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = row + kingMoves[i][0]
            endColumn = column + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endColumn < 8:
                endPiece = self.board[endRow][endColumn]
                if endPiece[0] != allyColor:
                    moves.append(Move(
                        (row, column), (endRow, endColumn), self.board))


class Move():
    ranksToRows = {
        "1": 7, "2": 6, "3": 5, "4": 4,
        "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToColumns = {
        "a": 0, "b": 1, "c": 2, "d": 3,
        "e": 4, "f": 5, "g": 6, "h": 7}
    columnsToFiles = {v: k for k, v in filesToColumns.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startColumn = startSq[1]
        self.endRow = endSq[0]
        self.endColumn = endSq[1]
        self.pieceMoved = board[self.startRow][self.startColumn]
        self.pieceCaptured = board[self.endRow][self.endColumn]
        self.isPawnPromotion = False
        if (
            (self.pieceMoved == 'wP' and self.endRow == 0) or (
                self.pieceMoved == 'bP' and self.endRow == 7)):
            self.isPawnPromotion = True

        self.moveID = ((self.startRow * 1000) + (self.startColumn * 100)
                       + (self.endRow * 10) + self.endColumn)

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return (self.getRankFile(self.startRow, self.startColumn)
                + self.getRankFile(self.endRow, self.endColumn))

    def getRankFile(self, row, column):
        return self.columnsToFiles[column] + self.rowsToRanks[row]
