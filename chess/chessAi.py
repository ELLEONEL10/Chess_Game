import random
from multiprocessing import Pool, Manager


pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

queenScores = [[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1]]

rookScores = [[4, 3, 4, 4, 4, 4, 3, 4],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 1, 2, 2, 2, 2, 1, 1],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [4, 3, 2, 1, 1, 2, 3, 4]]

whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8]]


piecePositionScores = {"N": knightScores, "B": bishopScores, "Q": queenScores,
                       "R": rookScores, "wp": whitePawnScores, "bp": blackPawnScores}


CHECKMATE = 1000
STALEMATE = 0
DEPTH = 4
SET_WHITE_AS_BOT = -1


def findRandomMoves(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


def findBestMove(gs, validMoves, returnQueue):
    global nextMove, whitePawnScores, blackPawnScores
    nextMove = None
    random.shuffle(validMoves)

    if gs.playerWantsToPlayAsBlack:
        # Swap the variables
        whitePawnScores, blackPawnScores = blackPawnScores, whitePawnScores

    SET_WHITE_AS_BOT = 1 if gs.whiteToMove else -1

    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -
                             CHECKMATE, CHECKMATE,  SET_WHITE_AS_BOT)

    returnQueue.put(nextMove)


# with alpha beta pruning
'''
alpha is keeping track of maximum so far
beta is keeping track of minimum so far
'''


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    # (will add later) move ordering - like evaluate all the move first that results in check or evaluate all the move first that results in capturing opponent's queen

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()  # opponent validmoves

        score = - \
            findMoveNegaMaxAlphaBeta(
                gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(move, score)
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore  # alpha is the new max
        if alpha >= beta:  # if we find new max is greater than minimum so far in a branch then we stop iterating in that branch as we found a worse move in that branch
            break
    return maxScore


def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            gs.checkmate = False
            return -CHECKMATE  # black wins
        else:
            gs.checkmate = False
            return CHECKMATE  # white wins
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                piecePositionScore = 0
                # score positionally based on piece type
                if square[1] != "K":
                    # return score of the piece at that position
                    if square[1] == "p":
                        piecePositionScore = piecePositionScores[square][row][col]
                    else:
                        piecePositionScore = piecePositionScores[square[1]][row][col]
                if SET_WHITE_AS_BOT:
                    if square[0] == 'w':
                        score += pieceScore[square[1]] + \
                            piecePositionScore * .1
                    elif square[0] == 'b':
                        score -= pieceScore[square[1]] + \
                            piecePositionScore * .1
                else:
                    if square[0] == 'w':
                        score -= pieceScore[square[1]] + \
                            piecePositionScore * .1
                    elif square[0] == 'b':
                        score += pieceScore[square[1]] + \
                            piecePositionScore * .1

    return score
def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    """
    Optimized NegaMax with Alpha-Beta Pruning.
    """
    global nextMove, transpositionTable
    if depth == 0:
        return quiescenceSearch(gs, alpha, beta, turnMultiplier)

    # Use transposition table
    boardHash = hash(str(gs.board))
    if boardHash in transpositionTable:
        return transpositionTable[boardHash]

    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        gs.undoMove()
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        alpha = max(alpha, maxScore)
        if alpha >= beta:
            break

    # Cache result in transposition table
    transpositionTable[boardHash] = maxScore
    return maxScore

def getCaptureMoves(gs):
    """
    Returns a list of all capture or check moves for the current game state.
    """
    captureMoves = []
    for move in gs.getValidMoves():
        if move.isCapture or move.isCheck:  # Assuming isCheck is also a property of Move
            captureMoves.append(move)
    return captureMoves

def quiescenceSearch(gs, alpha, beta, turnMultiplier):
    """
    Extends search to evaluate only captures/checks to avoid horizon effects.
    """
    evaluation = turnMultiplier * scoreBoard(gs)
    if evaluation >= beta:
        return beta
    if evaluation > alpha:
        alpha = evaluation

    # Consider only captures
    for move in getCaptureMoves(gs):
        gs.makeMove(move)
        score = -quiescenceSearch(gs, -beta, -alpha, -turnMultiplier)
        gs.undoMove()
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    
    for move in getCaptureMoves(gs):
        gs.makeMove(move)
        score = -quiescenceSearch(gs, -beta, -alpha, -turnMultiplier)
        gs.undoMove()
        return alpha
    
def parallelFindBestMove(gs, validMoves):
    with Manager() as manager:
        returnQueue = manager.Queue()
        pool = Pool(processes=4)  # Adjust based on your system's cores
        for move in validMoves:
            pool.apply_async(evaluateMove, args=(gs, move, returnQueue))
        pool.close()
        pool.join()

        # Collect results
        bestMove = None
        maxScore = -CHECKMATE
        while not returnQueue.empty():
            move, score = returnQueue.get()
            if score > maxScore:
                bestMove = move
                maxScore = score
        return bestMove

def evaluateMove(gs, move, returnQueue):
    """
    Evaluates a single move in a separate process.
    """
    gs.makeMove(move)
    score = -findMoveNegaMaxAlphaBeta(gs, gs.getValidMoves(), DEPTH - 1, -CHECKMATE, CHECKMATE, -1)
    gs.undoMove()
    returnQueue.put((move, score))

# Precompute Zobrist keys
ZOBRIST_KEYS = [[[random.randint(0, 2**64) for _ in range(12)] for _ in range(8)] for _ in range(8)]

def zobristHash(board):
    """
    Generates a unique hash for the given board state.
    """
    hashValue = 0
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != "--":
                pieceIndex = pieceToIndex(piece)
                hashValue ^= ZOBRIST_KEYS[row][col][pieceIndex]
    return hashValue

def pieceToIndex(piece):
    """
    Converts a piece to a unique index for Zobrist hashing.
    """
    pieceOrder = "KQRBNP"
    return (0 if piece[0] == 'w' else 6) + pieceOrder.index(piece[1])
def findBestMove(gs, validMoves, returnQueue):
    """
    Entry point to find the best move using parallelized search.
    """
    bestMove = parallelFindBestMove(gs, validMoves)
    returnQueue.put(bestMove)
class Move:
    def __init__(self, pieceMoved, capturedPiece=None, isCapture=False, isCheck=False):
        self.pieceMoved = pieceMoved
        self.capturedPiece = capturedPiece
        self.isCapture = isCapture
        self.isCheck = isCheck
