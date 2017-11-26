"""
Definition of functions which control
robot's rotation speed

"""


def count_nums(array, code_l, code_r):
    """
    Count occurencies of left and right
    commands in array

    """

    count_l = 0
    count_r = 0
    for i in array:
        # if i == code_l:
        #     count_l += 1
        # elif i == code_r:
        #     count_r += 1
        if i >= 0.00001:
            count_l += 1
        elif i < 0.00001:
            count_r += 1
    return count_l, count_r


def get_speed_2_players(pl1_inlet, pl2_inlet):
    """
    Generate speed value from two lsl protocols

    """

    from collections import deque
    from game_params import PL1_L_CODE, PL2_L_CODE, PL1_R_CODE, PL2_R_CODE
    from game_params import WIN_LEN, THRESH
    from numpy import sign

    pl1_deque = deque(maxlen=WIN_LEN)
    pl2_deque = deque(maxlen=WIN_LEN)

    pl1_chunk = pl1_inlet.pull_chunk()[0]
    pl2_chunk = pl2_inlet.pull_chunk()[0]
    # screen.clear()

    pl1_flat = [i for sublist in pl1_chunk for i in sublist]
    pl2_flat = [i for sublist in pl2_chunk for i in sublist]

    for i, j in zip(pl1_flat, pl2_flat):
        pl1_deque.append(i)
        pl2_deque.append(j)

    if len(pl1_deque) >= WIN_LEN and len(pl2_deque) >= WIN_LEN:

        pl1_lefts, pl1_rights = count_nums(pl1_deque, PL1_L_CODE, PL1_R_CODE)
        pl2_lefts, pl2_rights = count_nums(pl2_deque, PL2_L_CODE, PL2_R_CODE)

        lefts = pl1_lefts + pl2_lefts
        rights = pl1_rights + pl2_rights

        delta = rights - lefts
        rel_delta = abs(delta) / WIN_LEN

        if rel_delta > THRESH:
            speed = (50 + 20 * abs(delta) / WIN_LEN) * sign(delta)
            # screen.addstr(1,0,'speed = {}'.format(speed))
        else:
            speed = 0
        return speed, rel_delta


def random_speed(prev_speed):
    """
    Generate random speed

    """

    from random import randint

    speed_inc = randint(-20, 50)
    return prev_speed + speed_inc
