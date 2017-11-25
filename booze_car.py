"""
Mind-controlled drinking game in python
Authors:
    kuznesashka, nikolai.sm, dmalt
Date:

Mon Jun 26 14:34:41 MSK 2017

"""

from time import sleep
from collections import deque
import curses
import rpyc
from pylsl import resolve_byprop, StreamInlet
from numpy import sign

LSL_TIMEPROP = 5

# ev3.Sound.speak('Sasha privet').wait()

def count_nums(array, code_l, code_r):
    count_l = 0;
    count_r = 0;
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

class MyException(Exception):
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


if __name__ == '__main__':
    from setup_brick import servo
    from game_params import pl1, pl2, win_len, thresh, amp

    # ---------- init servo motor ---------------- #
    servo.run_to_abs_pos(position_sp=0, speed_sp=50)
    # servo.position_ssp = 0
    # servo.reset()
    # -------------------------------------------- #
    pl1_l_code = 1.;
    pl1_r_code = 2.;

    pl2_l_code = 2.;
    pl2_r_code = 1.;

    # pl2_l_code = 1.;
    # pl2_r_code = 2.;

    pl1_deque = deque(maxlen=win_len)
    pl2_deque = deque(maxlen=win_len)

    # ---------- init curses ------- #
    screen = curses.initscr()
    win = curses.newwin(5,40,20,7)
    screen.clear()
    curses.noecho()
    curses.cbreak()
    # ------------------------------ #

    # -------------------- connect to streams ------------------- #
    stream_pl1 = resolve_byprop('name', pl1, timeout=LSL_TIMEPROP)
    stream_pl2 = resolve_byprop('name', pl2, timeout=LSL_TIMEPROP)
    if not stream_pl1:
        raise MyException('STREAM {} CONNECTION ERROR'.format(pl1.upper()))

    if not stream_pl2:
        raise MyException('STREAM {} CONNECTION ERROR'.format(pl2.upper()))

    pl1_inlet = StreamInlet(stream_pl1[0])
    pl2_inlet = StreamInlet(stream_pl2[0])
    # ----------------------------------------------------------- #

    # screen.clear()


    speed = 0
    rel_delta = 0
    while(True):
        pl1_chunk = pl1_inlet.pull_chunk()[0]
        pl2_chunk = pl2_inlet.pull_chunk()[0]
        # screen.clear()

        pl1_flat = [i for sublist in pl1_chunk for i in sublist]
        pl2_flat = [i for sublist in pl2_chunk for i in sublist]

        for i,j in zip(pl1_flat, pl2_flat):
            pl1_deque.append(i)
            pl2_deque.append(j)


        if len(pl1_deque) >= win_len and len(pl2_deque) >= win_len:

            pl1_lefts, pl1_rights = count_nums(pl1_deque, pl1_l_code, pl1_r_code)
            pl2_lefts, pl2_rights = count_nums(pl2_deque, pl2_l_code, pl2_r_code)

            lefts = pl1_lefts + pl2_lefts
            rights = pl1_rights + pl2_rights

            delta = rights - lefts
            rel_delta = abs(delta) / win_len

            if rel_delta > thresh:
                speed = (50 + 20 * abs(delta) / win_len) * sign(delta)
                # screen.addstr(1,0,'speed = {}'.format(speed))
            else:
                speed = 0
            servo.run_forever(speed_sp=speed)

        screen.refresh()
        # screen.clear()
        screen.addstr(0, 0, 'position --- > {}               '.format(servo.position))
        screen.addstr(1, 0, 'speed --- > {}                  '.format(round(speed,4)))
        screen.addstr(2, 0, 'rel_delta --- > {}   '.format(rel_delta))
        


        if abs(servo.position) > amp:
            servo.stop()
            sleep(3)
            servo.run_to_abs_pos(position_sp=0, speed_sp=300)
            print('break by position')
            break
    curses.endwin()
