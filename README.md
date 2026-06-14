# ME5286 Lab 4 — UR5 Flashlight Assembly

Automated flashlight assembly simulation using a UR5 robot arm in RoboDK, developed for the ME5286 course by Azamat Turganbayev.

## Overview

The robot performs a full flashlight assembly sequence:

1. **Endcap pickup & reorientation** — picks the endcap from slot 0, rotates it to the correct orientation, and places it on a pedestal.
2. **Head insertion** — picks the flashlight head from slot 2 and seats it in the chuck fixture, which clamps it in place.
3. **Battery insertion** — picks the battery from slot 1 and drops it into the flashlight head opening.
4. **Endcap threading** — picks the endcap from the pedestal, presses it onto the head, and runs 4 regrip threading strokes followed by a final torque-controlled tighten.
5. **Unload** — releases the finished assembly into the output slot and returns the robot to home.

## Files

| File | Description |
|------|-------------|
| `ME5286_Lab4_Azamat_Turganbayev.py` | Main RoboDK Python script |
| `ME5286_Lab4_Azamat_Turganbayev.rdk` | RoboDK station file (robot, targets, fixtures) |
| `Azamat_Turganbayev_assembly_video.mp4` | Real robot assembly video recording |
| `Turganbayev_Azamat_Lab4_report.pdf` | Lab report |

## Requirements

- [RoboDK](https://robodk.com/) with the `robodk` Python package
- UR5 robot model loaded in the RoboDK station (`.rdk` file)
- Robotiq gripper driver (`rq_*` calls)
- Chuck fixture with `clamp()` / `unclamp()` auxiliary code

## Running the Simulation

1. Open `ME5286_Lab4_Azamat_Turganbayev.rdk` in RoboDK.
2. Run `ME5286_Lab4_Azamat_Turganbayev.py` via the RoboDK Python editor or `Tools > Run Script`.

## Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `SPEED` | 600 mm/s | Linear speed |
| `ACCEL` | 700 mm/s² | Linear acceleration |
| `CLEAR_Z` | 100 mm | Retract distance after pick/place |
| Threading strokes | 4 | Regrip cycles before final tighten |
| Final tighten torque | 2 Nm | Via `tighten_torque()` call |
