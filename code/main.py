# AI-assisted code:
# Used AI to help restructure this Raspberry Pi finite state machine so it starts in GREEN, stays GREEN when idle,
# and uses proper GPIO button handling, countdown timing, and emergency override behavior.

import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# --------------------
# GPIO PINS
# --------------------
GREEN_LED = 17
YELLOW_LED = 27
RED_LED = 22

PED_BUTTON = 5
EMERGENCY_BUTTON = 6
NIGHT_BUTTON = 13

# --------------------
# SETUP
# --------------------
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(YELLOW_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)

GPIO.setup(PED_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(EMERGENCY_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(NIGHT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# --------------------
# STATES
# --------------------
GREEN = "GREEN"
YELLOW = "YELLOW"
RED = "RED"

state = GREEN
night_mode = False

NORMAL_PRE_YELLOW = 5
NORMAL_YELLOW_TO_RED = 10
NORMAL_RED_TO_GREEN = 10

NIGHT_PRE_YELLOW = 3
NIGHT_YELLOW_TO_RED = 7
NIGHT_RED_TO_GREEN = 7

def set_lights(g, y, r):
    GPIO.output(GREEN_LED, g)
    GPIO.output(YELLOW_LED, y)
    GPIO.output(RED_LED, r)

def show_state(current_state):
    if current_state == GREEN:
        set_lights(GPIO.HIGH, GPIO.LOW, GPIO.LOW)
        print("Cars GO | Pedestrians DON'T WALK")
    elif current_state == YELLOW:
        set_lights(GPIO.LOW, GPIO.HIGH, GPIO.LOW)
        print("Cars GO | Pedestrians DON'T WALK")
    elif current_state == RED:
        set_lights(GPIO.LOW, GPIO.LOW, GPIO.HIGH)
        print("Cars DON'T GO | Pedestrians CAN WALK")

def emergency_pressed():
    return GPIO.input(EMERGENCY_BUTTON) == GPIO.HIGH

def night_pressed():
    return GPIO.input(NIGHT_BUTTON) == GPIO.HIGH

def ped_pressed():
    return GPIO.input(PED_BUTTON) == GPIO.HIGH

def wait_for_release(pin):
    while GPIO.input(pin) == GPIO.HIGH:
        time.sleep(0.05)

def print_countdown(seconds):
    for remaining in range(seconds, 0, -1):
        print(f"{remaining}s")
        time.sleep(1)

        if emergency_pressed():
            return "EMERGENCY"

        if night_pressed():
            wait_for_release(NIGHT_BUTTON)
            return "NIGHT"

    return "DONE"

def toggle_night_mode():
    global night_mode
    night_mode = not night_mode
    print(f"Night mode {'ON' if night_mode else 'OFF'}")
    time.sleep(0.3)

def normal_mode():
    global state

    while not night_mode:
        show_state(state)

        if emergency_pressed():
            state = GREEN
            print("EMERGENCY -> GREEN")
            time.sleep(0.2)
            continue

        if night_pressed():
            wait_for_release(NIGHT_BUTTON)
            toggle_night_mode()
            state = GREEN
            continue

        if state == GREEN:
            if ped_pressed():
                wait_for_release(PED_BUTTON)
                print("Pedestrian button pressed. Waiting 5 seconds before YELLOW.")
                result = print_countdown(NORMAL_PRE_YELLOW)
                if result == "EMERGENCY":
                    state = GREEN
                    continue
                if result == "NIGHT":
                    toggle_night_mode()
                    state = GREEN
                    continue
                state = YELLOW
            else:
                time.sleep(0.05)

        elif state == YELLOW:
            print("YELLOW for 10 seconds")
            result = print_countdown(NORMAL_YELLOW_TO_RED)
            if result == "EMERGENCY":
                state = GREEN
            elif result == "NIGHT":
                toggle_night_mode()
                state = GREEN
            else:
                state = RED

        elif state == RED:
            print("RED for 10 seconds")
            result = print_countdown(NORMAL_RED_TO_GREEN)
            if result == "EMERGENCY":
                state = GREEN
            elif result == "NIGHT":
                toggle_night_mode()
                state = GREEN
            else:
                state = GREEN

def night_mode_cycle():
    global state

    while night_mode:
        show_state(state)

        if emergency_pressed():
            state = GREEN
            print("EMERGENCY -> GREEN")
            time.sleep(0.2)
            continue

        if night_pressed():
            wait_for_release(NIGHT_BUTTON)
            toggle_night_mode()
            state = GREEN
            continue

        if state == GREEN:
            if ped_pressed():
                wait_for_release(PED_BUTTON)
                print("Pedestrian button pressed. Waiting 3 seconds before YELLOW.")
                result = print_countdown(NIGHT_PRE_YELLOW)
                if result == "EMERGENCY":
                    state = GREEN
                    continue
                if result == "NIGHT":
                    toggle_night_mode()
                    state = GREEN
                    continue
                state = YELLOW
            else:
                time.sleep(0.05)

        elif state == YELLOW:
            print("YELLOW for 7 seconds")
            result = print_countdown(NIGHT_YELLOW_TO_RED)
            if result == "EMERGENCY":
                state = GREEN
            elif result == "NIGHT":
                toggle_night_mode()
                state = GREEN
            else:
                state = RED

        elif state == RED:
            print("RED for 7 seconds")
            result = print_countdown(NIGHT_RED_TO_GREEN)
            if result == "EMERGENCY":
                state = GREEN
            elif result == "NIGHT":
                toggle_night_mode()
                state = GREEN
            else:
                state = GREEN

try:
    print("Traffic light system starting...")
    print("Normal mode: Green stays on until button press.")
    print("Night mode: Green stays on until button press.")
    print("Emergency button forces GREEN any time.")
    print("Night mode button toggles between modes.")

    while True:
        if night_mode:
            night_mode_cycle()
        else:
            normal_mode()

except KeyboardInterrupt:
    print("\nProgram stopped by user.")

finally:
    set_lights(GPIO.LOW, GPIO.LOW, GPIO.LOW)
    GPIO.cleanup()
