import rpyc
import curses

def rotate_servo(s, a):
    """Rotate servo drive by small angle a"""
    # s.wait_while('running')
    s.run_to_rel_pos(position_sp=a)

if __name__ == '__main__':
    conn = rpyc.classic.connect('10.42.0.3')
    ev3 = conn.modules['ev3dev.ev3']
    servo = ev3.MediumMotor('outB')

    sp = 2
    # get the curses screen window
    screen = curses.initscr()
     
    # turn off input echoing
    curses.noecho()
     
    # respond to keys immediately (don't wait for enter)
    curses.cbreak()
     
    # map arrow keys to special values
    screen.keypad(True)
    cur_pos = 'current position ---> '
    help_str = '\
| q - quit                         |\n\
| s - set current position as zero |\n\
| h - run to current zero          |\n'


    try:
        while True:
            screen.clear()
            screen.addstr(0, 0, help_str)
            screen.addstr(4, 0, cur_pos + str(servo.position))       

            char = screen.getch()
            if char == ord('q'):
                break
            elif char == curses.KEY_RIGHT:
                rotate_servo(servo, sp)
            elif char == curses.KEY_LEFT:
                rotate_servo(servo, -sp)
            elif char == ord('s'):
                servo.position = 0
            elif char == ord('h'):
                servo.run_to_abs_pos(position_sp=0, speed_sp=50)
                servo.wait_while('running')
    finally:
        # shut down cleanly
        curses.nocbreak(); screen.keypad(0); curses.echo()
        curses.endwin()
