"""
Test domains for deep transfer
"""
import numpy as np
import random
from collections import deque

from params import game_params


class fire_fighter(object):
    """
    Taxi cab style domain
    """
    actions = ['Left', 'Right', 'Up', 'Down', 'Pick', 'Drop']

    def __init__(self, params):
        self.screen_size = params.img_size
        self.agent_color = params.agent_color
        self.water_color = params.water_color
        self.fire_color = params.fire_color
        self.agent_water_color = params.agent_water_color
        self.counter = 0
        possible_coordinates = [(x, y) for x in range(self.screen_size[0]) for y in range(self.screen_size[1])]
        coord_pool = random.sample(possible_coordinates, 3)
        self.agent = coord_pool[0]
        self.fire = coord_pool[1]
        self.water = coord_pool[2]
        self.has_water = False
        self.grid = self.grab_screen()


    def grab_screen(self):
        """current screen of the game
        returns: numpy nd-array of shape screen_size"""
        self.grid = self.counter*np.zeros(self.screen_size)
        self.grid[self.agent[0]][self.agent[1]] = self.agent_water_color if self.has_water else self.agent_color
        self.grid[self.water[0]][self.water[1]] = self.agent_water_color if self.has_water else self.water_color
        self.grid[self.fire[0]][self.fire[1]] = self.fire_color
        # print(self.grid)
        return self.grid

    def get_dims(self):
        """row and column of screen in pixels"""
        return self.screen_size

    def execute_action(self, a):
        """takes action a in the game and gives new screen, reward and terminal
        if the new state is terminal, then start a new game.
        a: index of action to be executed
        returns: numpy.ndarray, shape=self.screen_size: new game screen (from grab_screen)
                 float32: reward for executing given action
                 boolean: whether the new state is a terminal state or not
        """
        self.counter += 1
        reward = 0
        if a == 4 or a == 5: #same square

            if self.agent == self.water: #on water or has water

                if self.has_water: #can drop
                    if a == 5:
                        # print('Dropping Water')
                        self.has_water = False
                        if self.isAdjacent(self.fire, self.agent): #agent is adjacent to fire
                            # print('Dousing. Win.')
                            self.agent = self.fire
                            self.water = self.fire
                            reward = 1
                else: #can pick
                    if a == 4:
                        # print('Picking Water Up')
                        self.has_water = True #positive reward
        else:
            if a == 0:
                self.agent = (self.agent[0], self.agent[1] - 1) if self.agent[1] > 0 else self.agent
            elif a == 1:
                self.agent = (self.agent[0], self.agent[1] + 1) if self.agent[1] < self.screen_size[1] - 1 else self.agent
            elif a == 2:
                self.agent = (self.agent[0] - 1, self.agent[1]) if self.agent[0] > 0 else self.agent
            elif a == 3:
                self.agent = (self.agent[0] + 1, self.agent[1]) if self.agent[0] < self.screen_size[0] - 1 else self.agent


            if self.has_water:
                self.water = self.agent

            if self.agent == self.fire: #die
                # print('Death.')
                reward = -1 #negative reward

        return (self.grab_screen(), reward, self.isTerminal())

    def isTerminal(self):
        """
        Decides if terminal condition has been reached
        :return: True if water douses fire or agent walks into fire
        """
        return ((self.fire == self.water) and not self.has_water) or (self.agent == self.fire)

    def isAdjacent(self, coord, check_coord):
        # print("Fire: ", coord)
        # print("Agent: ", check_coord)
        adjCoords = [(coord[0] - 1, coord[1]), (coord[0] + 1, coord[1]), (coord[0], coord[1] - 1), (coord[0], coord[1] + 1)]
        adjCoords = [some_coord for some_coord in adjCoords if self.isLegal(coord)]
        # print("Fire: ", coord)
        # print("Agent: ", check_coord)
        # print("Adj to fire: ", adjCoords)
        return check_coord in adjCoords

    def isLegal(self, coord):
        x = coord[0]
        y = coord[1]
        return 0 <= x < self.screen_size[0] and 0 <= y < self.screen_size[1]
