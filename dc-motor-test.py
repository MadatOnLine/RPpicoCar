from machine import PWM, Pin
from time import sleep

# Motor drive area
MOTOR_PWM_PINS = [7, 6, 9, 8, 18, 19, 21, 20]
MOTOR_SPEED_MIN = -100
MOTOR_SPEED_MAX = 100

def motor_setup():
    return [PWM(Pin(pin)) for pin in MOTOR_PWM_PINS]

def motor_move_init(motors, m1_speed, m2_speed, m3_speed, m4_speed):
    speeds = [m1_speed, -m1_speed, m2_speed, -m2_speed, m3_speed, -m3_speed, m4_speed, -m4_speed]
    for motor, speed in zip(motors, speeds):
        speed = int(min(MOTOR_SPEED_MAX, max(MOTOR_SPEED_MIN, speed)))
        motor.duty_u16(speed)
        motor.freq(500)
        print(motor)
        

def motor_move(motors, left_speed, right_speed):
    lf, lb, rf, rb = left_speed, left_speed, right_speed, right_speed
    motor_move_init(motors, lf, lb, rf, rb)

def loop(motors):
    print('-----------------------')
    motor_move(motors, 50, 50)  # go forward
    sleep(2)
    motor_move(motors, 0, 0)  # stop
    sleep(2)

    motor_move(motors, -50, 50)  # turn left
    sleep(2)
    motor_move(motors, 0, 0)  # stop
    sleep(2)

# Main code
motors = motor_setup()

while True:
    loop(motors)
    #print(motors)
