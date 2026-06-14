from robodk.robolink import *   
from robodk.robomath import *   

RDK = Robolink()
robot = RDK.Item('', ITEM_TYPE_ROBOT)

# All targets
HOME         = RDK.Item('Home')
T_SLOT0      = RDK.Item('T_slot0')                          # endcap pickup pose
T_SLOT1      = RDK.Item('T_slot1')                          # battery pickup at tray slot 1
T_SLOT2      = RDK.Item('T_slot2')                          # head pickup at tray slot 2
T_SLOT3      = RDK.Item('T_ped_place')                      # placement of endcap at tray slot 3
T_ROT_SAFE   = RDK.Item('T_rotate_safe')                    # safe pose to begin endcap rotation
T_ENDCAP_ROT = RDK.Item('T_endcap_rotated')                 # endcap rotation
T_CHUCK_APP  = RDK.Item('T_chuck_approach')                 # safe above chuck
T_HEAD_INS   = RDK.Item('T_head_chuck_insert')              # head seated in chuck
T_BATT_INS   = RDK.Item('T_batt_insert')                    # battery aligned above head opening
T_PED_PICK   = RDK.Item('T_ped_pick')                       # pickup the endcap from pedestal
T_ENDCAP_THREAD_PRESS = RDK.Item('T_endcap_thread_press')   # endcap on the head
T_ENDCAP_TWIST_1   = RDK.Item('T_endcap_twist_1')           # endcap rotation
T_FINAL_APP = RDK.Item('T_final_approach')                  # approach slot 2
T_FINAL = RDK.Item('T_final')                               # final pose


# Tunables
CLEAR_Z = 100   # mm for leaving the poses
SPEED   = 600    # mm/s
ACCEL   = 700   # mm/s^2


robot.setSpeed(SPEED)
robot.setAcceleration(ACCEL)

def set_default_speed():
    robot.setSpeedJoints(80)
    robot.setAccelerationJoints(150)  


INSTR = INSTRUCTION_CALL_PROGRAM # for gripper
AUX_INSTR = INSTRUCTION_INSERT_CODE # for chuck

# Gripper functions

def gripper_open():
    robot.RunCodeCustom('rq_set_speed_norm(50)', INSTR)
    robot.RunCodeCustom('rq_open_and_wait()', INSTR)

def gripper_close():
    robot.RunCodeCustom('rq_set_force(50)', INSTR)
    robot.RunCodeCustom('rq_close_and_wait()', INSTR)

#  Leave target using Linear Movement

def moveL_Leave(target_item, dz_clear=CLEAR_Z):
    base = target_item.Pose()
    robot.MoveL(base * transl(0, 0, -dz_clear))

#  Leave target using Joint Movement 

def moveJ_Leave(target_item, dz_clear=CLEAR_Z):
    base = target_item.Pose()
    robot.MoveJ(base * transl(0, 0, -dz_clear))

# Ensures not touching the objects during the movement

def moveJ_drop_leave_approach(target_item, dz_clear=CLEAR_Z):
    base = target_item.Pose()
    robot.MoveJ(base * transl(0, dz_clear, 0))

# Pick part from the target

def goto_pick(target_item):
    robot.MoveJ(target_item)
    gripper_close()
    moveL_Leave(target_item)

#place part to the target

def goto_place(target_item):
    robot.MoveJ(target_item)
    gripper_open()
    moveJ_drop_leave_approach(target_item)

#  Chuck functions

def clamp():
    robot.RunCodeCustom('clamp()', AUX_INSTR)

def unclamp():
    robot.RunCodeCustom('unclamp()', AUX_INSTR)

# Performs action of putting head of battery in the chuck

def put_head_in_chuck():
    moveJ_drop_leave_approach(T_SLOT3,300) # move safely from pedestal
    goto_pick(T_SLOT2)              # pick head from slot 2
    robot.MoveJ(T_CHUCK_APP)        # move above chuck
    moveJ_Leave(T_HEAD_INS, dz_clear = -5) 
    gripper_open()                  # release head
    clamp()
    robot.MoveJ(T_CHUCK_APP)        # back out

# Performs action of putting battery in the flashlight head

def put_battery_in_head():
    goto_pick(T_SLOT1)              # pick battery from slot 1
    robot.MoveJ(T_CHUCK_APP)
    robot.MoveL(T_BATT_INS)         # align above opening
    gripper_open()
    robot.MoveJ(T_CHUCK_APP)

# Putting endcap on the flashlight head to begin the threading

def put_endcap_in_head():
    goto_pick(T_PED_PICK)
    robot.MoveJ(T_CHUCK_APP)
    robot.MoveJ(T_ENDCAP_THREAD_PRESS)

# Function for threading

def prethread_4_strokes():
    for _ in range(4):
        robot.setSpeedJoints(110)
        robot.setAccelerationJoints(170)  
        gripper_close() # clamp endcap in gripper
        robot.MoveJ(T_ENDCAP_TWIST_1) # tightening stroke
        robot.RunCodeCustom('rq_move_and_wait_norm(50)', INSTRUCTION_INSERT_CODE) # slight open (regrip)
        robot.MoveJ(T_ENDCAP_THREAD_PRESS) # reset back to start pose

# Built in function

def final_tighten():
    robot.RunCodeCustom('tighten_torque(2, 0, 1.57, 2, 2, 1, 100, 100, 50)',INSTRUCTION_INSERT_CODE)

# action of placing the final assembly

def unload_and_return_to_slot2():
    gripper_open()
    gripper_close()
    unclamp()
    robot.MoveJ(T_CHUCK_APP)
    robot.MoveJ(T_FINAL_APP)
    robot.setSpeed(30)
    robot.setAcceleration(70)  
    robot.MoveL(T_FINAL)
    gripper_open()
    robot.MoveL(T_FINAL_APP)
    

# Step 1 (Endcap)

robot.MoveJ(HOME)      # Start Home
set_default_speed()
gripper_open()

goto_pick(T_SLOT0)     # Pick endcap from slot 0
robot.MoveJ(T_ROT_SAFE)
robot.MoveJ(T_ENDCAP_ROT)
goto_place(T_SLOT3)    # Place on pedestal slot 3

# STEP 2 (head + battery) 
put_head_in_chuck()
put_battery_in_head()

# STEP 3 (Endcap threading)
put_endcap_in_head()
robot.setRounding(-1) # ensures that it won't find the fastest approach to the T_ENDCAP_TWIST_1
prethread_4_strokes()
final_tighten()
set_default_speed()
unload_and_return_to_slot2()

robot.MoveJ(HOME)      # End Home
