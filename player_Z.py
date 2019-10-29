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
        self.initial_pos = {'x': paddle_pos['x'] + 1, 'y': paddle_pos['y']}

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

        #if the puck is in the right field, the paddle defends
        if is_puck_right(current_state):
            # get the target position for the paddle
            target = self.initial_pos

        else: 
            if  current_state['puck_speed']['x'] <= 0:
                enemy_pos = enemy_puck_pos(self.my_goal, current_state)

                if enemy_pos == 0:
                    target = utils.aim(current_state['puck_pos'], current_state['puck_speed'], {'x': 650, 'y': current_state['board_shape'][0]}, current_state['puck_radius'],
                                        current_state['paddle_radius']) 
                elif enemy_pos == 1:
                    target = utils.aim(current_state['puck_pos'], current_state['puck_speed'], {'x': 650, 'y': 0}, current_state['puck_radius'],
                                        current_state['paddle_radius']) 
            else:
                target = self.initial_pos

        
        # 
        if target['x'] < (current_state['board_shape'][1] / 2) - 10:
            self.my_paddle_pos = next_move_paddle(self.my_paddle_pos, target, current_state)

        return self.my_paddle_pos

def enemy_puck_pos(my_goal, current_state):
    """
        args:
            my_goal: if the paddle is on the left or right side
        return:
            0: if is in the first second of the field
            1: if is in the second second of the field
    """
    if my_goal == 'left':
        if current_state['paddle2_pos']['y'] < current_state['board_shape'][0]/2:
            return 0
        elif current_state['paddle2_pos']['y'] >= current_state['board_shape'][0]/2:
            return 1
    else: 
        if current_state['paddle1_pos']['y'] < current_state['board_shape'][0]/2:
            return 0
        elif current_state['paddle1_pos']['y'] >= current_state['board_shape'][0]/2:
            return 1
    return 1

def is_puck_top(current_state):
    """
        Args: 
            current_state, to obtain the position of the puck

        Return:
            true if the position of the puck is on the top side of the board
    """
    if current_state['puck_pos']['y'] < current_state['board_shape'][0]/2:
        return True
    return False

def is_puck_right(current_state):
    """
        Args: 
            current_state, to obtain the position of the puck

        Return:
            true if the position of the puck is on the right side of the board
    """
    if current_state['puck_pos']['x'] > current_state['board_shape'][1]/2:
        return True
    return False


def next_move_paddle(paddle_pos, target_pos, current_state):
    """
        Args:
            paddle_pos:
            target_pos:

        Return:
            the next movement of the paddle of 1 frame x and y
            next_move
    """
    if target_pos != paddle_pos:
        direction_vector = {'x': target_pos['x'] - paddle_pos['x'],
                            'y': target_pos['y'] - paddle_pos['y']}
        direction_vector = {k: v / utils.vector_l2norm(direction_vector)
                            for k, v in direction_vector.items()}

        movement_dist = min(current_state['paddle_max_speed'] * current_state['delta_t'],
                            utils.distance_between_points(target_pos, paddle_pos))
        direction_vector = {k: v * movement_dist
                            for k, v in direction_vector.items()}
        next_move = {'x': paddle_pos['x'] + direction_vector['x'],
                            'y': paddle_pos['y'] + direction_vector['y']}

    # check if computed new position in not inside goal area
    # check if computed new position in inside board limits
    if utils.is_inside_goal_area_paddle(next_move, current_state) is False and \
            utils.is_out_of_boundaries_paddle(next_move, current_state) is None:
        return next_move
        
    return paddle_pos
    
    
    """
    if paddle_pos[]
    next_move = {'x':paddle_pos['x'] + 5, 'y':paddle_pos['y'] + 5}
    return next_move
    """