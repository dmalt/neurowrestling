"""
Mind-controlled drinking game in python
Authors:
    kuznesashka, nikolai.sm, dmalt
Date:

Mon Jun 26 14:34:41 MSK 2017

"""

from time import sleep
import curses
import rpyc

from get_speed import get_speed_2_players, random_speed
from get_streams import get_streams_2_players


if __name__ == '__main__':
    from setup_brick import servo
    from game_params import AMP

    # ---------- init servo motor ---------------- #
    servo.run_to_abs_pos(position_sp=0, speed_sp=50)
    # servo.position_ssp = 0
    # servo.reset()
    # -------------------------------------------- #

    # ---------- init curses ------- #
    screen = curses.initscr()
    win = curses.newwin(5, 40, 20, 7)
    screen.clear()
    curses.noecho()
    curses.cbreak()
    # ------------------------------ #

    # screen.clear()

    # pl1_inlet, pl2_inlet = get_streams_2_players()
    INI_SPEED = 0

    speed = INI_SPEED
    while True:
        # speed, rel_delta = get_speed_2_players(pl1_inlet, pl2_inlet)
        speed = random_speed(speed)
        servo.run_forever(speed_sp=speed)

        screen.refresh()
        # screen.clear()
        screen.addstr(0, 0, 'position --- > {}        '.format(servo.position))
        screen.addstr(1, 0, 'speed --- > {}           '.format(round(speed, 4)))
        # screen.addstr(2, 0, 'rel_delta --- > {}'.format(rel_delta))

        if abs(servo.position) > AMP:
            servo.stop()
            sleep(3)
            servo.run_to_abs_pos(position_sp=0, speed_sp=300)
            print('break by position')
            break
    curses.endwin()
