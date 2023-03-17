import copy
import pygame
import sys
import os
import numpy as np

from constants import  *

#PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe UNBEATABLE AI')
screen.fill(BG_COLOUR)

class Board:

    def __init__(self):
        self.squares = BOARD
        #self.mark_sqr(1, 1, AI)
        print(self.squares)
        self.emptySquares = self.squares
        self.usedSquares = 0
    
    def endGame(self):
        '''
        return 0 if there is no winner.
        return 1 if player 1 wins
        return 2 if player 2 wins
        '''
        #column wins
        for col in range(COLS) :
            if (self.squares[0][col] == self.squares[1][col] and self.squares[1][col] == self.squares[2][col] and self.squares[2][col] != ' ') :
                return self.squares[0][col]
        
        #row wins
        for row in range(ROWS) :    
            if (self.squares[row][0] == self.squares[row][1] and self.squares[row][1] == self.squares[row][2]) :       
                return self.squares[row][0]
        
        #diagonal wins
        if self.squares[0][0] == self.squares[1][1] and self.squares[1][1] == self.squares[2][2] and self.squares[0][0] != ' ':
            return self.squares[0][0]
        if self.squares[0][2] == self.squares[1][1] and self.squares[1][1] == self.squares[2][0] and self.squares[0][0] != ' ':
            return self.squares[0][0]
        
        return 'n'
            
    def addToSquare(self, row, col, player):
        self.squares[row][col] = player
        self.usedSquares += 1

    def emptySquare(self, row, col):
        return self.squares[row][col] == ' '
    
    def full(self):
        return self.usedSquares == 9
    
    def empty(self):
        return self.usedSquares == 0
    
    def getListOfEmptySqrs(self):
        emptySqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.emptySquare(row, col): #if check square is empty method returns true
                    emptySqrs.append((row, col))
        return emptySqrs

class UnbeatableAI:
    
    def __init__(self):
        self.player = AI

    def minimax(self, board, maximizer):
        
        scenario = board.endGame()
        
        #human wins
        if scenario == HUMAN:
            return 1
        
        #ai wins
        if scenario == AI:
            return -1
        #draw
        elif board.full():
            return 0
        
        if maximizer: #if ai 
            pass

        elif not maximizer: #if minimizer (human)
            bestScore = 9999999
            bestMove = None
            emptySqs = board.getListOfEmptySqrs()

            for (row, col) in emptySqs:
                tempBoard = copy.deepcopy(board)
                tempBoard.addToSquares(row, col, HUMAN)
                score = self.minimax(tempBoard, True)
                bestScore = min(score, bestScore) 
                bestMove = (row, col)
            return bestScore, bestMove

        
    pass
class Game:

    def __init__(self): #called each time a new game object is created
        self.gridLines()
        self.ai = UnbeatableAI()
        self.board = Board()
        self.ongoing = True
        self.player = FIRST_PLAYER

    def gridLines(self):
        #Vertical
        pygame.draw.line(screen, LINE_COLOUR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)
        
        #Horizontal
        pygame.draw.line(screen, LINE_COLOUR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (0, HEIGHT- SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def nextPlayer(self):
        if self.player == AI:
            self.player = HUMAN
        else:
            self.player = AI
    
    def dispImage(self, row, col):
        if row == 0:
            y = HEIGHT/6 - (IMG_SCALE_Y/2)
        if row == 1:
            y = HEIGHT/6 *3 -(IMG_SCALE_Y/2)
        if row == 2:
            y = HEIGHT/6 * 5-(IMG_SCALE_Y/2)
        
        if col == 0:
            x = WIDTH/6 -(IMG_SCALE_X/2)
        if col == 1:
            x = WIDTH/6 * 3-(IMG_SCALE_X/2)
        if col == 2:
            x = WIDTH/6 *5-(IMG_SCALE_X/2)

        if self.player == 'X':
            #draw cross
            ximg = pygame.image.load(os.path.join('images', 'Xgame.png'))
            ximg = pygame.transform.scale(ximg, (IMG_SCALE_X, IMG_SCALE_Y))
            screen.blit(ximg, (x, y))
            
        elif self.player == 'O':
            oimg = pygame.image.load(os.path.join('images', 'O.png'))
            oimg = pygame.transform.scale(oimg, (IMG_SCALE_X, IMG_SCALE_Y))
            screen.blit(oimg, (x, y))




def main():
    
    #obj
    game = Game()
    board = game.board
    ai = game.ai

    #big loop
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos) #for testing reveals mouse x and y coordinates
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                print(row, col)
               
                if board.emptySquare(row, col):
                    board.addToSquare(row, col, game.player)
                    game.dispImage(row, col)
                    game.nextPlayer()
                    print(board.squares)

        pygame.display.update()

main()