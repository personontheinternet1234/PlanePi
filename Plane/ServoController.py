from gpiozero import AngularServo
from time import sleep
from PlaneUtil import zero, change_servo_wrapper_angle, ServoWrapper
import math
import threading
from datetime import datetime


class ServoController:

    def __init__(self):
        self.right_flap = ServoWrapper(AngularServo(18, min_pulse_width=0.0006, max_pulse_width=0.0023), 0)
        self.left_flap = ServoWrapper(AngularServo(17, min_pulse_width=0.0006, max_pulse_width=0.0023), 0)
        self.rudder = ServoWrapper(AngularServo(4, min_pulse_width=0.0006, max_pulse_width=0.0023), 0)

        self.servo_wrappers = [self.right_flap, self.left_flap, self.rudder]

        self.coefficient_product = 6

        self.recover_right_flap = True
        self.recover_left_flap = True
        self.recover_rudder = True
        self.right_flap_last_update = datetime.now()
        self.left_flap_last_update = datetime.now()
        self.rudder_last_update = datetime.now()

    def start_threads(self):
        threading.Thread(target=self.normalize_servo_angles).start()

    def setup_servos(self):
        for servo_wrapper in self.servo_wrappers:
            zero(servo_wrapper)

    def normalize_servo_angles(self):
        while True:

            if (self.recover_right_flap):
                if self.right_flap.angle > 0:
                    change_servo_wrapper_angle(self.right_flap, -2)
                elif self.right_flap.angle < 0:
                    change_servo_wrapper_angle(self.right_flap, 2)
            elif (datetime.now() - self.right_flap_last_update).total_seconds() > 0.15:
                self.recover_right_flap = True

            if (self.recover_left_flap):
                if self.left_flap.angle > 0:
                    change_servo_wrapper_angle(self.left_flap, -2)
                elif self.left_flap.angle < 0:
                    change_servo_wrapper_angle(self.left_flap, 2)
            elif (datetime.now() - self.left_flap_last_update).total_seconds() > 0.15:
                self.recover_left_flap = True

            if (self.recover_rudder):
                if self.rudder.angle > 0:
                    change_servo_wrapper_angle(self.rudder, -2)
                elif self.rudder.angle < 0:
                    change_servo_wrapper_angle(self.rudder, 2)
            elif (datetime.now() - self.rudder_last_update).total_seconds() > 0.15:
                self.recover_rudder = True

    def apply_motion_packet(self, delta_pitch, delta_yaw, delta_roll):
        right_flap_delta = delta_pitch + -1 * delta_roll
        left_flap_delta = -1 * delta_pitch + -1 * delta_roll
        rudder_delta = delta_yaw

        change_servo_wrapper_angle(self.right_flap, right_flap_delta)
        change_servo_wrapper_angle(self.left_flap, left_flap_delta)
        change_servo_wrapper_angle(self.rudder, rudder_delta)

        if (right_flap_delta == 0):
            self.recover_right_flap = True
        else:
            self.recover_right_flap = False
            self.right_flap_last_update = datetime.now()

        if (left_flap_delta == 0):
            self.recover_left_flap = True
        else:
            self.recover_left_flap = False
            self.left_flap_last_update = datetime.now()

        if (rudder_delta == 0):
            self.recover_rudder = True
        else:
            self.recover_rudder = False
            self.rudder_last_update = datetime.now()

    def dance(self):
        for i in range(3):
            for servo_wrapper in self.servo_wrappers:
                zero(servo_wrapper)
            sleep(1)
            for servo_wrapper in self.servo_wrappers:
                change_servo_wrapper_angle(servo_wrapper, 50)
            sleep(1)
            for servo_wrapper in self.servo_wrappers:
                zero(servo_wrapper)
            sleep(1)
            for servo_wrapper in self.servo_wrappers:
                change_servo_wrapper_angle(servo_wrapper, -50)
            sleep(1)
        for servo_wrapper in self.servo_wrappers:
            zero(servo_wrapper)
