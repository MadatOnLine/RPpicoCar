from machine import Pin, PWM
from time import sleep

# Motor drive area
MOTOR_PWM_PINS = [7, 6, 9, 8, 18, 19, 21, 20]
MOTOR_SPEED_MIN = 0
MOTOR_SPEED_MAX = 100
FREQUENCY = 500

#Motor Pin map
rb = [7, 6]
rf = [9, 8]
lf = [18, 19]
lb = [21, 20]

def motor_setup(pins):
    return [PWM(Pin(pin)) for pin in pins]

def motor_move(motor, speed):
    speed = min(MOTOR_SPEED_MAX, max(MOTOR_SPEED_MIN, speed))
    duty = int(abs(speed/MOTOR_SPEED_MAX) * 65535)
    motor.freq(FREQUENCY)
    motor.duty_u16(duty)
    print(speed, ' -> ', duty)

def move_forward(speed):
    print('go forward')
    motor_move(PWM(Pin(rb[0])), speed)
    motor_move(PWM(Pin(lb[0])), speed)
    motor_move(PWM(Pin(rf[0])), speed)
    motor_move(PWM(Pin(lf[0])), speed)
    
def move_backward(speed):
    print('go back')
    motor_move(PWM(Pin(rb[1])), speed)
    motor_move(PWM(Pin(lb[1])), speed)
    motor_move(PWM(Pin(rf[1])), speed)
    motor_move(PWM(Pin(lf[1])), speed)
    
def move_left(speed):
    print('go left')
    motor_move(PWM(Pin(rb[0])), speed)
    motor_move(PWM(Pin(rf[0])), speed)
    
    motor_move(PWM(Pin(lb[1])), speed)
    motor_move(PWM(Pin(lf[1])), speed)    

def move_right(speed):
    print('go right')
    motor_move(PWM(Pin(rb[1])), speed)
    motor_move(PWM(Pin(rf[1])), speed)
    
    motor_move(PWM(Pin(lb[0])), speed)
    motor_move(PWM(Pin(lf[0])), speed)    

def stop():
    print('stop')
    motor_move(PWM(Pin(rb[0])), 0)
    motor_move(PWM(Pin(lb[0])), 0)
    motor_move(PWM(Pin(rf[0])), 0)
    motor_move(PWM(Pin(lf[0])), 0)
    
    motor_move(PWM(Pin(rb[1])), 0)
    motor_move(PWM(Pin(lb[1])), 0)
    motor_move(PWM(Pin(rf[1])), 0)
    motor_move(PWM(Pin(lf[1])), 0)
    

# Main code
motors = motor_setup(MOTOR_PWM_PINS)

#testing motor movements - make sure to stop after every move
# go forward for 2 seconds at 50% speed and stop
move_forward(50)
sleep(2)
stop()

# go backward for 2 seconds at 50% speed and stop
move_backward(50)
sleep(2)
stop()

# go left for 2 seconds at 70% speed and stop
move_left(70)
sleep(2)
stop()

# go right for 2 seconds at 30% speed and stop
move_right(100)
sleep(2)
stop()

        


