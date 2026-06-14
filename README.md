# ME5286 Lab 4 - UR5 Flashlight Assembly

**University:** University of Minnesota
**Course:** ME 5286 - Robotics, Spring 2026
**Authors:** Azamat Turganbayev (MS Robotics) and Aiden Wang (BS Mechanical Engineering)
**Instructors:** Prof. Rachel G. Humann and Prof. Tim Kowalewski

## Demo

https://github.com/user-attachments/assets/83b83660-67c0-4574-9d0e-76f7a3543dea

## Abstract

Development and implementation of an automated robotic assembly process using a UR5 manipulator and integrated peripheral systems. The robot autonomously assembles a flashlight composed of three parts - the head, the battery, and the endcap - using a pneumatic clamp with an optical sensor to securely hold the flashlight head during threading operations. Accurate localization, trajectory planning, and coordinated control of the gripper and clamp were required. The full assembly sequence was completed in **1 minute and 39 seconds**, within the required 110-second time limit.

## Hardware Setup

- **UR5 robot arm** with Robotiq gripper and force/torque sensor (TCP offset: 211.5 mm Z, 1.25 kg)
- **Pneumatic chuck** - holds the flashlight head during threading, controlled via solenoid valves at 80 psi
- **Optical sensor** (C5D-AP-2A photoelectric) - prevents the chuck from closing when empty
- **Flashlight tray** - machined aluminum tray with 3 part slots and a 3D-printed pedestal:
  - Slot 0 (`T_SLOT0`): endcap pickup pose
  - Slot 1 (`T_SLOT1`): battery pickup pose
  - Slot 2 (`T_SLOT2`): flashlight head pickup pose
  - Slot 3 / pedestal (`T_SLOT3`): endcap staging area after rotation

## Assembly Steps

15 targets were predefined in RoboDK. Cartesian motions (`MoveL`) were used near contact points for precision; joint motions (`MoveJ`) were used for faster transitions between waypoints.

**Step 1 - Endcap preparation**
1. Pick endcap from `T_SLOT0`
2. Move to safe rotation pose `T_ROT_SAFE`, then rotate to `T_ENDCAP_ROT`
3. Place endcap on pedestal `T_SLOT3`

**Step 2 - Head and battery**
4. Pick head from `T_SLOT2`, approach chuck via `T_CHUCK_APP`
5. Insert head into chuck at `T_HEAD_INS`, clamp
6. Pick battery from `T_SLOT1`, insert into head at `T_BATT_INS`

**Step 3 - Endcap assembly**
7. Pick endcap from pedestal at `T_PED_PICK`
8. Press endcap onto head at `T_ENDCAP_THREAD_PRESS`
9. Run 4 regrip pre-threading strokes using `T_ENDCAP_TWIST_1`
10. Finish with `tighten_torque()` at 2 Nm

**Step 4 - Unload**
11. Unclamp chuck, approach via `T_FINAL_APP`
12. Place assembled flashlight at `T_FINAL`, return to `HOME`

> Note: a separate `T_FINAL` target was required for unloading because slight misalignment introduced during threading prevented reuse of `T_SLOT2`.

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
| Assembly time | 1 min 39 sec | Within the 110-second requirement |
| Total targets | 15 | Predefined 6-DOF poses in robot base frame |
