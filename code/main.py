import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# --------------------
# PIN SETUP
# --------------------
GREEN_LED = 17
YELLOW_LED = 27
RED_LED = 22

PED_BUTTON = 5
EMERGENCY_BUTTON = 6
NIGHT_BUTTON = 13

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
state_start_time = time.time()
night_button_last = 0

def set_lights(green, yellow, red):
    GPIO.output(GREEN_LED, green)
    GPIO.output(YELLOW_LED, yellow)
    GPIO.output(RED_LED, red)

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

def countdown(seconds, label):
    for remaining in range(seconds, 0, -1):
        if GPIO.input(EMERGENCY_BUTTON) == GPIO.HIGH:
            return "EMERGENCY"
        print(f"{label}: {remaining} seconds")
        time.sleep(1)
    return "DONE"

def wait_for_button_press():
    while True:
        if GPIO.input(PED_BUTTON) == GPIO.HIGH:
            time.sleep(0.2)
            return True
        if GPIO.input(EMERGENCY_BUTTON) == GPIO.HIGH:
            return False
        if GPIO.input(NIGHT_BUTTON) == GPIO.HIGH:
            time.sleep(0.2)
            return "NIGHT"
        time.sleep(0.05)

def toggle_night_mode():
    global night_mode, night_button_last
    now = time.time()
    if GPIO.input(NIGHT_BUTTON) == GPIO.HIGH and (now - night_button_last) > 0.5:
        night_mode = not night_mode
        night_button_last = now
        print(f"Night mode is now {'ON' if night_mode else 'OFF'}")
        time.sleep(0.3)

def run_normal_mode():
    global state, state_start_time

    print("\nNORMAL MODE ACTIVE")

    while not night_mode:
        show_state(state)

        if GPIO.input(EMERGENCY_BUTTON) == GPIO.HIGH:
            state = GREEN
            state_start_time = time.time()
            print("EMERGENCY: forcing GREEN")
            continue

        if GPIO.input(NIGHT_BUTTON) == GPIO.HIGH:
            toggle_night_mode()
            if night_mode:
                state = GREEN
                state_start_time = time.time()
                continue

        if state == GREEN:
            print("Green light active. Press pedestrian button to start cycle.")
            result = wait_for_button_press()
            if result == True:
                state = YELLOW
                state_start_time = time.time()
            elif result == "NIGHT":
                toggle_night_mode()
                continue

        elif state == YELLOW:
            result = countdown(5, "YELLOW countdown")
            if result == "EMERGENCY":
                state = GREEN
                state_start_time = time.time()
            else:
                state = RED
                state_start_time = time.time()

        elif state == RED:
            result = countdown(15, "RED countdown")
            if result == "EMERGENCY":
                state = GREEN
                state_start_time = time.time()
            else:
                state = GREEN
                state_start_time = time.time()

def run_night_mode():
    global state, state_start_time

    print("\nNIGHT MODE ACTIVE")

    while night_mode:
        show_state(state)

        if GPIO.input(NIGHT_BUTTON) == GPIO.HIGH:
            toggle_night_mode()
            if not night_mode:
                state = GREEN
                state_start_time = time.time()
                break

        if GPIO.input(EMERGENCY_BUTTON) == GPIO.HIGH:
            state = GREEN
            state_start_time = time.time()
            print("EMERGENCY: forcing GREEN")
            continue

        if state == GREEN:
            print("Green light active. Press pedestrian button to start night cycle.")
            result = wait_for_button_press()
            if result == True:
                state = YELLOW
                state_start_time = time.time()
            elif result == "NIGHT":
                toggle_night_mode()

        elif state == YELLOW:
            result = countdown(3, "YELLOW countdown")
            if result == "EMERGENCY":
                state = GREEN
                state_start_time = time.time()
            else:
                state = RED
                state_start_time = time.time()

        elif state == RED:
            result = countdown(7, "RED countdown")
            if result == "EMERGENCY":
                state = GREEN
                state_start_time = time.time()
            else:
                state = GREEN
                state_start_time = time.time()

try:
    print("Starting traffic light state machine...")
    print("GREEN = cars go, pedestrians don't walk")
    print("YELLOW = cars go, pedestrians don't walk")
    print("RED = cars don't go, pedestrians can walk")
    print("Press NIGHT button to toggle night mode.")
    print("Press EMERGENCY button anytime during red to force green.")

    while True:
        if night_mode:
            run_night_mode()
        else:
            run_normal_mode()

except KeyboardInterrupt:
    print("\nProgram stopped by user.")

finally:
    GPIO.output(GREEN_LED, GPIO.LOW)
    GPIO.output(YELLOW_LED, GPIO.LOW)
    GPIO.output(RED_LED, GPIO.LOW)
    GPIO.cleanup()
