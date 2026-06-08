# Interactive Pedestrian Crosswalk and Traffic Light

This project simulates a traffic light and pedestrian crosswalk system using a Raspberry Pi and a finite state machine.

## States

1. Green Light (GL)
2. Yellow Light (YL)
3. Red Light (RL)

## Inputs

* Pedestrian Button
* Emergency Vehicle Button
* Night Mode Button

## Outputs

* Green LED
* Yellow LED
* Red LED

## How it Works

The system starts in Green Light mode.

In Normal Mode:

* Green stays on until the pedestrian button is pressed.
* After 5 seconds the light changes to Yellow.
* After another 10 seconds it changes to Red.
* After another 10 seconds it returns to Green.

In Night Mode:

* Green stays on until the pedestrian button is pressed.
* After 3 seconds it changes to Yellow.
* After another 7 seconds it changes to Red.
* After another 7 seconds it returns to Green.

If the Emergency Vehicle button is pressed at any time, the system immediately returns to Green.

## State Diagram

![State Diagram](state_diagram.jpg)
