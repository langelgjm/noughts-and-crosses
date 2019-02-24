import logging
logging.basicConfig(level=logging.INFO)

import enum
import os
import uuid

import numpy as np

from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.space import SingleGrid


@enum.unique
class Endgame(enum.Enum):
    DRAW = 'draw'
    WIN_X = 1
    WIN_O = -1


class Player(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        if not self.model.endgame:
            logging.info(f"Player {self.unique_id}'s turn")

            # get and place a piece on the grid (at a random location that is not occupied)
            # this could be factored out into various placement strategies
            piece = Piece(uuid.uuid4(), self.model, player=self)

            logging.info('Trying to place a piece...')

            try:
                self.model.grid.position_agent(piece, x='random', y='random')
            except:
                logging.info('Game is a draw.')
                self.model.endgame = Endgame.DRAW

            logging.info('Checking grid...')

            # check to see if any winning conditions have been met
            if is_winning_game(get_game_grid(self.model)):
                logging.info(f'Player {self.unique_id} wins.')

                if self.unique_id == 1:
                    self.model.endgame = Endgame.WIN_X
                else:
                    self.model.endgame = Endgame.WIN_O
        else:
            pass


class Piece(Agent):
    def __init__(self, unique_id, model, player):
        super().__init__(unique_id, model)
        self.player = player


class TicTacToe(Model):
    def __init__(self):
        super().__init__()

        self.running = True
        self.endgame = None

        self.grid = SingleGrid(3, 3, False)
        self.schedule = BaseScheduler(self)

        playerX = Player(1, self)
        playerO = Player(-1, self)

        self.schedule.add(playerX)
        self.schedule.add(playerO)

    def step(self):
        if not self.endgame:
            self.schedule.step()
        else:
            self.running = False


def get_game_grid(model):
    counts = np.zeros((model.grid.width, model.grid.height))

    for contents, x, y in model.grid.coord_iter():
        if not (x, y) in model.grid.empties:
            counts[x][y] = contents.player.unique_id

    return counts


def is_winning_game(counts):
    logging.info(f'{os.linesep}{counts}')

    if any(abs(np.sum(counts, 0)) == 3) or any(abs(np.sum(counts, 1)) == 3) or abs(np.trace(counts)) == 3 or abs(np.trace(np.flipud(counts))) == 3:
        return True
    else:
        return False
