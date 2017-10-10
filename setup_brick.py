import rpyc
conn = rpyc.classic.connect('10.42.0.3')
ev3 = conn.modules['ev3dev.ev3']
servo = ev3.MediumMotor('outB')
