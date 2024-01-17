import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
from machine import Pin, PWM
from micropython_motor import MOTOR
from machine import Pin, PWM

#update with local area wifi details
ssid = '******'
password = '******'

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


def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(temperature, state):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
                <body>
                    <form action="./lighton" style="width: 80%" >
                        <div><input type="submit" value="Light on" style="width: 80%" /></div>
                    </form>
                    <form action="./lightoff" style="width: 80%" >
                        <div><input type="submit" value="Light off" style="width: 80%" /></div>
                    </form>
                    <form action="./forward" style="width: 80%" >
                        <div><input type="submit" value="forward" style="width: 80%" /></div>
                    </form>
                    <form action="./backward" style="width: 80%" >
                        <div><input type="submit" value="backward" style="width: 80%" /></div>
                    </form>
                    <form action="./left" style="width: 80%" >
                        <div><input type="submit" value="left" style="width: 80%" /></div>
                    </form>
                    <form action="./right" style="width: 80%" >
                        <div><input type="submit" value="right" style="width: 80%" /></div>
                    </form>
                    <form action="./stop" style="width: 80%" >
                        <div><input type="submit" value="stop" style="width: 80%" /></div>
                    </form>
                    <p>{state}</p>
                    <p>Temperature is {temperature}</p>
                </body>
            </html>
            """
    return str(html)

    
def serve(connection):
    #Start a web server
    state = 'OFF'
    pico_led.off()
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            pico_led.on()
            state = 'LED is ON'
            
        elif request =='/lightoff?':
            pico_led.off()
            state = 'LED is OFF'
            
        elif request =='/forward?':
            pico_led.on()
            state = 'going forward'
            # go forward for 2 seconds at 50% speed and stop
            stop()
            move_forward(50)
            
        elif request =='/backward?':
            pico_led.on()
            state = 'going backward'
            # go backward for 2 seconds at 50% speed and stop
            stop()
            move_backward(50)
            
        elif request =='/left?':
            pico_led.on()
            state = 'going left'
            # go left for 2 seconds at 70% speed and stop
            stop()
            move_left(50)
            
        elif request =='/right?':
            pico_led.on()
            state = 'going right'
            # go right for 2 seconds at 30% speed and stop
            stop()
            move_right(50)
            
        elif request =='/stop?':
            pico_led.off()
            state = 'Stopped'
            stop()
            
        temperature = pico_temp_sensor.temp
        html = webpage(temperature, state)
        client.send(html)
        client.close()


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
try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()

