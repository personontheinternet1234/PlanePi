from gpiozero import AngularServo
from time import sleep
import Util

servo = AngularServo(18, min_pulse_width=0.0006, max_pulse_width=0.0023)

try:
    while True:
        servo.angle = 90
        sleep(1)
        servo.angle = 0
        sleep(1)
        servo.angle = -90
        sleep(1)
except KeyboardInterrupt:
    Util.zero(servo)
