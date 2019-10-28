""" Player module

This is a template/example class for your player.
This is the only file you should modify.

The logic of your hockey robot will be implemented in this class.
Please implement the interface next_move().

The only restrictions here are:
 - to implement a class constructor with the args: paddle_pos, goal_side
 - set self.my_display_name with your team's name, max. 15 characters
 - to implement the function next_move(self, current_state),
    returning the next position of your paddle
"""

import copy
import utils

class Player:
    def __init__(self, paddle_pos, goal_side):

        # set your team's name, max. 15 chars
        self.my_display_name = "LAS PERRAS"

        # these belong to my solution,
        # you may erase or change them in yours
        self.future_size = 30
        self.my_goal = goal_side
        self.my_goal_center = {}
        self.opponent_goal_center = {}
        self.my_paddle_pos = paddle_pos
        self.initial_pos = paddle_pos

    def next_move(self, current_state):
        """ Function that computes the next move of your paddle

        Implement your algorithm here. This will be the only function
        used by the GameCore. Be aware of abiding all the game rules.

        Returns:
            dict: coordinates of next position of your paddle.
        """

        # update my paddle pos
        # I need to do this because GameCore moves my paddle randomly
        self.my_paddle_pos = current_state['paddle1_pos'] if self.my_goal == 'left' \
                                                              else current_state['paddle2_pos']

        


        #if the puck is in our field
        if current_state['puck_pos']['x'] < current_state['board_shape'][1]/2:
            #if the puck overpass the vertical of the paddle
            if current_state['puck_pos']['x'] < self.my_paddle_pos['x']:
                self.my_paddle_pos['x'] = self.my_paddle_pos['x'] - 2
            else: 
                self.my_paddle_pos['x'] = self.my_paddle_pos['x'] + 1
            # boundaries for the paddle vertically
            if current_state['puck_pos']['y'] > self.my_paddle_pos['y'] and self.my_paddle_pos['y'] < current_state['board_shape'][0]/4*3:
                self.my_paddle_pos['y'] = self.my_paddle_pos['y'] + 5
            elif current_state['puck_pos']['y'] < self.my_paddle_pos['y'] and self.my_paddle_pos['y'] > current_state['board_shape'][0]/4 :
                self.my_paddle_pos['y'] = self.my_paddle_pos['y'] - 5
        else:
            if self.my_paddle_pos['x'] > self.initial_pos['x']:
                if self.my_paddle_pos['y'] > current_state['board_shape'][0]/2:
                    self.my_paddle_pos['x'] = self.my_paddle_pos['x'] - 5
                    self.my_paddle_pos['y'] = self.my_paddle_pos['y'] - 5
                elif self.my_paddle_pos['y'] < current_state['board_shape'][0]/2:
                    self.my_paddle_pos['x'] = self.my_paddle_pos['x'] - 5
                    self.my_paddle_pos['y'] = self.my_paddle_pos['y'] + 5
            if self.my_paddle_pos['x'] < (current_state['board_shape'][1]/8) + 5:
                self.my_paddle_pos['x'] = self.my_paddle_pos['x'] + 5

        

        


        return self.my_paddle_pos


def predictNextMove(self, buck_position):
    direction_vector = {k: v / utils.vector_l2norm(buck_position)
                        for k, v in direction_vector.items()}
