import time

GREEN = "GL"
YELLOW = "YL"
RED = "RL"

crosswalk_button = False
emergency_vehicle = False
night_mode = False

state = GREEN
state_start_time = time.time()

def read_inputs():
    global crosswalk_button, emergency_vehicle, night_mode

    print("\nPress:")
    print("  c = crosswalk button")
    print("  e = emergency vehicle")
    print("  n = toggle night mode")
    print("  Enter = no input")
    choice = input("Input: ").strip().lower()

    crosswalk_button = (choice == "c")
    emergency_vehicle = (choice == "e")
    if choice == "n":
        night_mode = not night_mode

def set_outputs(current_state):
    if current_state == GREEN:
        print("Cars: GREEN | Pedestrians: DON'T WALK")
    elif current_state == YELLOW:
        print("Cars: YELLOW | Pedestrians: DON'T WALK")
    elif current_state == RED:
        print("Cars: RED | Pedestrians: WALK")

def update_state():
    global state, state_start_time
    elapsed = time.time() - state_start_time

    if emergency_vehicle:
        state = GREEN
        state_start_time = time.time()
        return

    if state == GREEN:
        if crosswalk_button and not night_mode:
            state = YELLOW
            state_start_time = time.time()
    elif state == YELLOW:
        if elapsed >= 3:
            state = RED
            state_start_time = time.time()
    elif state == RED:
        if elapsed >= 5:
            state = GREEN
            state_start_time = time.time()

def main():
    print("Custom State Machine System: Pedestrian Crosswalk and Traffic Light")
    print("Starting in GREEN state")

    while True:
        print("\n-----------------------------------")
        print("Current state:", state, "| Night mode:", night_mode)
        read_inputs()
        update_state()
        set_outputs(state)
        time.sleep(1)

if __name__ == "__main__":
    main()
