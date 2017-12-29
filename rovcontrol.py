#!/usr/bin/python2.7
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

import time, json
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import threading
from threading import Lock

LH_PIN = "P9_14"
RH_PIN = "P9_16"
LV_PIN = "P8_19"
RV_PIN = "P8_13"
LH_RELAYS = ["P8_7", "P8_8"]
RH_RELAYS = ["P8_9", "P8_10"]
LV_RELAYS = ["P8_11", "P8_12"]
RV_RELAYS = ["P8_14", "P8_16"]
GRABBER_PIN = "P9_42"
WRIST_PIN = "P9_28"

SPINDOWN = 2

MAX_WAIT = 0.5

LH = False
RH = False
LV = False
RV = False

SERVO_MIN = 3
SERVO_MAX = 14.5
DUTY_SPAN = SERVO_MAX - SERVO_MIN

MOTOR_MIN = 45 # 800
MOTOR_MAX = 90 # 2000
SEVEN_HUNDRED = 35 # 700

dontbreakdontbreak_horiz = Lock()
dontbreakdontbreak_vert = Lock()
def enable_servos(pin = "*"):
    if pin == "*":
        enable_servos("GR")
        #enable_servos("WR")
    if pin == "GR":
        PWM.start(GRABBER_PIN, (100-SERVO_MIN), 60.0)
    #if pin == "WR":
        #PWM.start(WRIST_PIN, (100-SERVO_MIN), 500)

def set_servo(angle, pin):
    duty = 100 - ((float(angle)/180) * DUTY_SPAN + SERVO_MIN)
    print(duty)
    if pin == "GR":
        PWM.set_duty_cycle(GRABBER_PIN, duty)
    #if pin == "WR":
        #PWM.set_duty_cycle(WRIST_PIN, duty)

def initialize_motors(pin = "*"):
    print "init pin " + pin
    if pin == "*":
        PWM.start(LH_PIN, 0, 500)
        PWM.start(RH_PIN, 0, 500)
        PWM.start(LV_PIN, 0, 500)
        PWM.start(RV_PIN, 0, 500)
        time.sleep(2)
        PWM.set_duty_cycle(LH_PIN, SEVEN_HUNDRED)
        PWM.set_duty_cycle(RH_PIN, SEVEN_HUNDRED)
        PWM.set_duty_cycle(LV_PIN, SEVEN_HUNDRED)
        PWM.set_duty_cycle(RV_PIN, SEVEN_HUNDRED)
        time.sleep(3)
        PWM.set_duty_cycle(LH_PIN, MOTOR_MIN)
        PWM.set_duty_cycle(RH_PIN, MOTOR_MIN)
        PWM.set_duty_cycle(LV_PIN, MOTOR_MIN)
        PWM.set_duty_cycle(RV_PIN, MOTOR_MIN)
        return
    if pin == "LH":
        floof = LH_PIN
    elif pin == "RH":
        floof = RH_PIN
    elif pin == "LV":
        floof = LV_PIN
    elif pin == "RV":
        floof = RV_PIN
    else:
        initialize_motors("*")
        return
    PWM.start(floof, 0, 500)
    time.sleep(2)
    PWM.set_duty_cycle(floof, SEVEN_HUNDRED)
    time.sleep(3)
    PWM.set_duty_cycle(floof, MOTOR_MAX)

def set_speed(percent, pin):
    global LH, LV, RH, RV
    if pin == "LH":
        floof = LH_PIN
        if percent < 0:
            if LH == True:
                PWM.set_duty_cycle(floof, SEVEN_HUNDRED)
                time.sleep(SPINDOWN)
            GPIO.output(LH_RELAYS[0], GPIO.LOW)
            GPIO.output(LH_RELAYS[1], GPIO.LOW)
            LH = False
        else:
            if LH == False:
                PWM.set_duty_cycle(floof, SEVEN_HUNDRED)
                time.sleep(SPINDOWN)
            GPIO.output(LH_RELAYS[1], GPIO.HIGH)
            GPIO.output(LH_RELAYS[0], GPIO.HIGH)
            LH = True
    elif pin == "RH":
        floof = RH_PIN
        if percent < 0:
            if RH == True:
                PWM.set_duty_cycle(floof, SEVEN_HUNDRED)
                time.sleep(SPINDOWN)
            GPIO.output(RH_RELAYS[0], GPIO.LOW)
            GPIO.output(RH_RELAYS[1], GPIO.LOW)
            RH = False
        else:
            if RH == False:
                PWM.set_duty_cycle(floof, SEVEN_HUNDRED)
                time.sleep(SPINDOWN)
            GPIO.output(RH_RELAYS[1], GPIO.HIGH)
            GPIO.output(RH_RELAYS[0], GPIO.HIGH)
            RH = True
    elif pin == "LV":
        floof = LV_PIN
        if percent < 0:
            if LV == True:
                PWM.set_duty_cycle(floof, SEVEN_HUNDRED)
                time.sleep(SPINDOWN)
            GPIO.output(LV_RELAYS[0], GPIO.LOW)
            GPIO.output(LV_RELAYS[1], GPIO.LOW)
            LV = False
        else:
            if LV == False:
                PWM.set_duty_cycle(floof, SEVEN_HUNDRED)
                time.sleep(SPINDOWN)
            GPIO.output(LV_RELAYS[1], GPIO.HIGH)
            GPIO.output(LV_RELAYS[0], GPIO.HIGH)
            LV = True
    elif pin == "RV":
        floof = RV_PIN
        if percent < 0:
            if RV == True:
                PWM.set_duty_cycle(floof, SEVEN_HUNDRED)
                time.sleep(SPINDOWN)
            GPIO.output(RV_RELAYS[0], GPIO.LOW)
            GPIO.output(RV_RELAYS[1], GPIO.LOW)
            RV = False
        else:
            if LV == False:
                PWM.set_duty_cycle(floof, SEVEN_HUNDRED)
                time.sleep(SPINDOWN)
            GPIO.output(RV_RELAYS[1], GPIO.HIGH)
            GPIO.output(RV_RELAYS[0], GPIO.HIGH)
            RV = True
    else:
        floof = LH_PIN
        if percent < 0:
            if LH == True:
                PWM.set_duty_cycle(floof, SEVEN_HUNDRED)
                time.sleep(SPINDOWN)
            GPIO.output(LH_RELAYS[0], GPIO.LOW)
            GPIO.output(LH_RELAYS[1], GPIO.LOW)
            LH = False
        else:
            if LH == False:
                PWM.set_duty_cycle(floof, SEVEN_HUNDRED)
                time.sleep(SPINDOWN)
            GPIO.output(LH_RELAYS[1], GPIO.HIGH)
            GPIO.output(LH_RELAYS[0], GPIO.HIGH)
            LH = True
    print (abs(float(percent)) / 100) *  (MOTOR_MAX - MOTOR_MIN) + MOTOR_MIN
    PWM.set_duty_cycle(floof, (abs(float(percent)) / 100) *  (MOTOR_MAX - MOTOR_MIN) + MOTOR_MIN)

def rotate(percent, pin1, pin2):
    t1 = threading.Thread(target=set_speed, args=(percent, pin1))
    t1.start()
    t2 = threading.Thread(target=set_speed, args=(-1 * percent, pin2))
    t2.start()
    t1.join()
    t2.join()

def forward(percent):
    t1 = threading.Thread(target=set_speed, args=(percent, "LH"))
    t1.start()
    t2 = threading.Thread(target=set_speed, args=(percent, "RH"))
    t2.start()
    t1.join()
    t2.join()

def up(percent):
    t1 = threading.Thread(target=set_speed, args=(percent, "LV"))
    t1.start()
    t2 = threading.Thread(target=set_speed, args=(percent, "RV"))
    t2.start()
    t1.join()
    t2.join()

def rovexec(floof):
    horiz = False
    vert = False
    stime = time.time()
    print floof
    fluff = json.loads(floof)
    if fluff["op"] == "forward" or fluff["op"] == "yaw" or fluff["op"] == "set" or fluff["op"] == "reset":
        dontbreakdontbreak_horiz.acquire()
        horiz = True
    if fluff["op"] == "up" or fluff["op"] == "roll" or fluff["op"] == "set" or fluff["op"] == "reset":
        dontbreakdontbreak_vert.acquire()
        vert = True
    if time.time() - stime > MAX_WAIT:
        if horiz:
            dontbreakdontbreak_horiz.release()
        if vert:
            dontbreakdontbreak_vert.release()
        print "THREAD EXPIRED! THIS IS A MESSAGE FROM YOU, ALED, NOT PYTHON"
        return
    print "acquired lock"
    if fluff["op"] == "forward":
        forward(int(fluff["arg1"]))
    elif fluff["op"] == "up":
        up(int(fluff["arg1"]))
    elif fluff["op"] == "reset":
        initialize_motors(fluff["arg1"])
    elif fluff["op"] == "reset_servos":
        enable_servos(fluff["arg1"])
    elif fluff["op"] == "set_servo":
        set_servo(int(fluff["arg1"]), fluff["arg2"])
    elif fluff["op"] == "yaw":
        rotate(int(fluff["arg1"]), "LH", "RH")
    elif fluff["op"] == "roll":
        rotate(int(fluff["arg1"]), "LV", "RV")
    elif fluff["op"] == "set":
        set_speed(int(fluff["arg1"]), fluff["arg2"])
    print "releasing locks"
    if horiz:
        dontbreakdontbreak_horiz.release()
    if vert:
        dontbreakdontbreak_vert.release()
    print "finished"

class MateSocket(WebSocket):
    def handleMessage(self):
        print self.data
        t = threading.Thread(target=rovexec, args=(self.data,))
        t.start()
        
    def handleConnected(self):
        print self.address, 'connected'

    def handleClose(self):
        print self.address, 'closed'

GPIO.setup(LH_RELAYS[0], GPIO.OUT)
GPIO.setup(LH_RELAYS[1], GPIO.OUT)
GPIO.output(LH_RELAYS[1], GPIO.LOW)
GPIO.output(LH_RELAYS[0], GPIO.LOW)
GPIO.setup(LV_RELAYS[0], GPIO.OUT)
GPIO.setup(LV_RELAYS[1], GPIO.OUT)
GPIO.output(LV_RELAYS[1], GPIO.LOW)
GPIO.output(LV_RELAYS[0], GPIO.LOW)
GPIO.setup(RH_RELAYS[0], GPIO.OUT)
GPIO.setup(RH_RELAYS[1], GPIO.OUT)
GPIO.output(RH_RELAYS[1], GPIO.LOW)
GPIO.output(RH_RELAYS[0], GPIO.LOW)
GPIO.setup(RV_RELAYS[0], GPIO.OUT)
GPIO.setup(RV_RELAYS[1], GPIO.OUT)
GPIO.output(RV_RELAYS[1], GPIO.LOW)
GPIO.output(RV_RELAYS[0], GPIO.LOW)
server = SimpleWebSocketServer('', 8000, MateSocket)
server.serveforever()
