"""
Mind-controlled drinking game in python
Authors:
    kuznesashka, nikolai.sm, dmalt
Date:

Mon Jun 26 14:34:41 MSK 2017

"""

from time import sleep
from collections import deque
import rpyc
from pylsl import resolve_byprop, StreamInlet
from numpy import sign

LSL_TIMEPROP = 5

# ev3.Sound.speak('Sasha privet').wait()

def rotate_90(l, r, speed):
     l.run_timed(time_sp=10000, speed_sp=speed)
     r.run_timed(time_sp=10000, speed_sp=-speed)

def run(l, r, speed):
     l.run_timed(time_sp=1000, speed_sp=speed)
     r.run_timed(time_sp=1000, speed_sp=speed)

def pour(s):
     #    s.wait_while('running')
     s.run_timed(time_sp=500, speed_sp=-400)
 #    s.run_to_rel_pos(postion_sp=-90, speed_sp=100)
     s.wait_while('running')
     s.run_timed(time_sp=500, speed_sp=400)
 #    s.run_to_rel_pos(position_sp=90, speed_sp=100)

def rotate_servo(s, a):
    """Rotate servo drive by small angle a"""
    s.wait_while('running')
    s.run_to_rel_pos(position_sp=a)

def count_nums(array, code_l, code_r):
    count_l = 0;
    count_r = 0;
    for i in array:
        if i == code_l:
            count_l += 1
        elif i == code_r:
            count_r += 1
    return count_l, count_r

class CustomException(Exception):
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


if __name__ == '__main__':
    from setup_brick import servo
    from game_params import pl1, pl2, win_len, thresh, amp
    # ---------- init servo motor ---------------- #
    servo.run_to_abs_pos(position_sp=0, speed_sp=50)
    # servo.position_sp = 0
    # servo.reset()
    # -------------------------------------------- #

    pl1_l_code = 1.;
    pl1_r_code = 2.;

    pl2_l_code = 2.;
    pl2_r_code = 1.;

    pl1_deque = deque(maxlen=win_len)
    pl2_deque = deque(maxlen=win_len)

    # -------------------- connect to streams ------------------- #
    stream_pl1 = resolve_byprop('name', pl1, timeout=LSL_TIMEPROP)
    stream_pl2 = resolve_byprop('name', pl2, timeout=LSL_TIMEPROP)
    # ----------------------------------------------------------- #
    if not(stream_pl1):
        raise CustomException('STREAM1 CONNECTION ERROR')

    if not(stream_pl2):
        raise CustomException('STREAM2 CONNECTION ERROR')

    pl1_inlet = StreamInlet(stream_pl1[0])
    pl2_inlet = StreamInlet(stream_pl2[0])


    while(True):
        pl1_chunk = pl1_inlet.pull_chunk()[0]
        print('1-st players chunk')
        print(pl1_chunk)
        print('-------------------------')
        pl2_chunk = pl2_inlet.pull_chunk()[0]
        print('2-st players chunk')
        print(pl2_chunk)
        print('_________________________')

        pl1_flat = [i for sublist in pl1_chunk for i in sublist]
        pl2_flat = [i for sublist in pl2_chunk for i in sublist]

        for i,j in zip(pl1_flat, pl2_flat):
            pl1_deque.append(i)
            pl2_deque.append(j)


        if len(pl1_deque) >= win_len and len(pl2_deque) >= win_len:

            p1_lefts, p1_rights = count_nums(pl1_deque, pl1_l_code, pl1_r_code)
            p2_lefts, p2_rights = count_nums(pl2_deque, pl2_l_code, pl2_r_code)

            lefts = p1_lefts + p2_lefts
            rights = p1_rights + p2_rights

            delta = rights - lefts

            if abs(delta) / win_len > thresh:
                speed = (50 + 50 * abs(delta) / win_len) * sign(delta)
                print('speed = {}'.format(speed))
            else:
                speed = 0
            servo.run_forever(speed_sp=speed)

        print('position = {}'.format(servo.position))

        if abs(servo.position) > amp:
            servo.stop()
            sleep(3)
            servo.run_to_abs_pos(position_sp=0, speed_sp=300)
            print('break by position')
            break
