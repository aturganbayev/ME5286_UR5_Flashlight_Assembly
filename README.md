# ME5286 Lab 4 - UR5 Flashlight Assembly

**Course:** ME5286 Robotics Labs, Spring 2026
**Authors:** Azamat Turganbayev and Aiden Wang

Automated flashlight assembly using a UR5 robot arm and pneumatic chuck, programmed via the RoboDK Python API and executed on a physical robot.

## Demo



https://github.com/user-attachments/assets/83b83660-67c0-4574-9d0e-76f7a3543dea



## Objective

Use the UR5 robot and a pneumatic chuck to fully assemble a flashlight (endcap, battery, and head) autonomously without human intervention.

## Hardware Setup

- **UR5 robot arm** with Robotiq gripper (force/torque sensor, TCP offset: 211.5 mm Z, 1.25 kg)
- **Pneumatic chuck** - holds the flashlight head during threading, controlled via solenoid valves at 80 psi
- **Optical sensor** (C5D-AP-2A photoelectric) - prevents the chuck from closing when empty
- **Flashlight tray** - machined aluminum tray with 3 part slots and a 3D-printed pedestal:
  - Slot 0: endcap
  - Slot 1: battery
  - Slot 2: flashlight head
  - Slot 3 / pedestal: endcap staging area after rotation

## Assembly Steps

1. **Endcap pickup and reorientation** - picks the endcap from slot 0, rotates it to the correct orientation, and places it on the pedestal (required first step).
2. **Head insertion** - picks the flashlight head from slot 2 and seats it in the chuck, which clamps it in place.
3. **Battery insertion** - picks the battery from slot 1 and drops it into the flashlight head opening with correct polarity.
4. **Endcap threading** - picks the endcap from the pedestal, presses it onto the head, runs 4 regrip threading strokes, then finishes with `tighten_torque()` at 2 Nm.
5. **Unload** - unclamps the chuck, removes the finished flashlight, places it in the head slot, and returns to home.

## Files

| File | Description |
|------|-------------|
| `ME5286_Lab4_Azamat_Turganbayev.py` | Main RoboDK Python script |
| `ME5286_Lab4_Azamat_Turganbayev.rdk` | RoboDK station file (robot, targets, fixtures) |
| `Azamat_Turganbayev_assembly_video.mp4` | Real robot assembly video recording |
| `Turganbayev_Azamat_Lab4_report.pdf` | Lab report |

## Requirements

- [RoboDK](https://robodk.com/) with the `robodk` Python package
- Post processor: `Universal_Robots_ME5286_Robot<X>.py` (required for chuck commands)
- Robotiq gripper activated on the pendant before running
- Chuck fixture with `clamp()` / `unclamp()` URScript functions

## Running

1. Open `ME5286_Lab4_Azamat_Turganbayev.rdk` in RoboDK.
2. Set the post processor to `Universal_Robots_ME5286_Robot<X>` matching your robot number.
3. Run `ME5286_Lab4_Azamat_Turganbayev.py` via the RoboDK Python editor or `Tools > Run Script`.
4. Generate and upload the robot program to the UR5 via flash drive.

## Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `SPEED` | 600 mm/s | Linear speed |
| `ACCEL` | 700 mm/s^2 | Linear acceleration |
| `CLEAR_Z` | 100 mm | Retract distance after pick/place |
| Threading strokes | 4 | Regrip cycles before final tighten |
| Final tighten torque | 2 Nm | Via `tighten_torque()` - called only when nearly fully threaded |
