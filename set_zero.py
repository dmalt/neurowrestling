"""Setup servo's zero position"""

import curses
from setup_brick import servo


if __name__ == '__main__':

    sp = 2  # rotation step

    # get the curses screen window
    screen = curses.initscr()

    # turn off input echoing
    curses.noecho()

    # respond to keys immediately (don't wait for enter)
    curses.cbreak()

    # map arrow keys to special values
    screen.keypad(True)
    cur_pos = '  =============  '
    help_str = '\
| q - quit                         |\n\
| s - set current position as zero |\n\
| h - run to current zero          |\n'

    try:
        while True:
            screen.clear()
            screen.addstr(0, 0, help_str)
            screen.addstr(4, 0, cur_pos + str(servo.position) + cur_pos)

            char = screen.getch()
            if char == ord('q'):
                break
            elif char == curses.KEY_RIGHT:
                servo.run_to_rel_pos(position_sp=sp)
            elif char == curses.KEY_LEFT:
                servo.run_to_rel_pos(position_sp=-sp)
            elif char == ord('s'):
                servo.position = 0
            elif char == ord('h'):
                servo.run_to_abs_pos(position_sp=0, speed_sp=150)
                servo.wait_while('running')
            elif char == ord('k'):
                servo.run_to_rel_pos(position_sp=sp * 20, speed_sp=150)
                servo.wait_while('running')
            elif char == ord('j'):
                servo.run_to_rel_pos(position_sp=- sp * 20, speed_sp=150)
                servo.wait_while('running')
    finally:
        # shut down cleanly
        curses.nocbreak()
        screen.keypad(0)
        curses.echo()
        curses.endwin()
