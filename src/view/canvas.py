import random
import pygame
import src.common.constants as Constants
from src.listener.iobserver import IObserver
from src.listener.eventmanager import EventManagerWeak, InitializeEvent, QuitEvent, StateChangeEvent, TickEvent
from src.model.GameEngine import GameEngine


class Canvas(IObserver):
    def __init__(self, evManager: 'EventManagerWeak', model: 'GameEngine'):
        self.evManager = evManager
        evManager.register(self)
        self.model = model
        self.isinitialized = False
        self.screen = None
        # self.clock = None
        self.font = None

    def update(self, event):
        if isinstance(event, InitializeEvent):
            self.initialize()
        elif isinstance(event, QuitEvent):
            # shut down the pygame graphics
            self.isinitialized = False
            pygame.quit()
        elif isinstance(event, TickEvent):
            if not self.isinitialized:
                return
            currentstate = self.model.state.peek()
            if currentstate == Constants.STATE_MENU:
                self.rendermenu()
            elif currentstate == Constants.STATE_PLAY:
                self.rendergame()
            elif currentstate == Constants.STATE_END:
                self.renderGameOver()
            # limit the redraw speed to 30 frames per second
            self.model.clock.tick(30)

    def draw_text_middle(self, text, size, color):
        self.font = pygame.font.SysFont('comicsans', size, bold=True)
        label = self.font.render(text, 1, color)

        self.screen.blit(label, (Constants.TOP_LEFT_X + Constants.PLAY_WIDTH/2 - (label.get_width() / 2),
                                 Constants.TOP_LEFT_Y + Constants.PLAY_HEIGHT/2 - label.get_height()/2))

    def rendermenu(self):
        self.screen.fill((0, 0, 0))
        self.draw_text_middle('Press space key to begin.', 60, (255, 255, 255))
        pygame.display.flip()

    def rendergame(self):
        self.draw_window(self.model.grid)
        self.draw_next_shape(self.model.next_piece)
        pygame.display.update()

    def renderGameOver(self):
        self.draw_text_middle("You Lost", 40, (255, 255, 255))
        pygame.display.update()
    
    def initialize(self):
        _ = pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Tetris')
        self.screen = pygame.display.set_mode(
            (Constants.S_WIDTH, Constants.S_HEIGHT))
        # self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('comicsans', 60, bold=True)
        self.isinitialized = True


    def draw_grid(self, row, col):
        sx = Constants.TOP_LEFT_X
        sy = Constants.TOP_LEFT_Y
        for i in range(row):
            pygame.draw.line(self.screen, (128, 128, 128), (sx, sy + i*30),
                            (sx + Constants.PLAY_WIDTH, sy + i * 30))  # horizontal lines
            for j in range(col):
                pygame.draw.line(self.screen, (128, 128, 128), (sx + j * 30, sy),
                                (sx + j * 30, sy + Constants.PLAY_HEIGHT))  # vertical lines
            
    
    def draw_window(self, grid):
        self.screen.fill((0, 0, 0))
        # Tetris Title
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('TETRIS', 1, (255, 255, 255))

        self.screen.blit(label, (Constants.TOP_LEFT_X + Constants.PLAY_WIDTH /
                                 2 - (label.get_width() / 2), 30))

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(
                    self.screen, grid[i][j], (Constants.TOP_LEFT_X + j * 30, Constants.TOP_LEFT_Y + i * 30, 30, 30), 0)

        # draw grid and border
        self.draw_grid(20, 10)
        pygame.draw.rect(self.screen, (255, 0, 0), (Constants.TOP_LEFT_X,
                                                    Constants.TOP_LEFT_Y, Constants.PLAY_WIDTH, Constants.PLAY_HEIGHT), 5)

    def draw_next_shape(self, shape):
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Next Shape', 1, (255, 255, 255))

        sx = Constants.TOP_LEFT_X + Constants.PLAY_WIDTH + 50
        sy = Constants.TOP_LEFT_Y + Constants.PLAY_HEIGHT/2 - 100
        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(self.screen, shape.color,
                                     (sx + j*30, sy + i*30, 30, 30), 0)

        self.screen.blit(label, (sx + 10, sy - 30))