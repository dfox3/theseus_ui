import sys
import os
import time

#--------------------------------------------------------------
# GLOBALS
Z_SPEED = 0
'''
for motor indices:
"xaxis"  -> 1
"zaxis"  -> 0
"magnet  -> 3
"pump"   -> 2
"pinch1" -> 4
"pinch2" -> 5
"pinch3" -> 6
"pinch4" -> 7
'''

PLATE_Z_ALIGN = [
    5000,5010,5020,5030,5040,5050,5060,5070,
    5080,5090,5100,5110,5120,5130,5140,5150,
    5160,5170,5180,5190,5200,5210,5220,5230
]
MICRO_Z_ALIGN = 1000
MICRO_MAGNET_ALIGN = 5500
MAGNET_ACTIVE_ALIGN = 50
PIPETTE_MIN = 0
PIPETTE_WELL_MIN = 10
PIPETTE_WELL_MAX = 150
PIPETTE_MAX = 2000
TEC_SUC_ALIGN = 1000

START_VEL = 0
ACCEL_1 = 1
MAX_ACCEL = .5
MAX_DECEL = -.5
DECEL_1 = -1
STOP_VEL = 0

PLATES = {"plate":True,"chip":True}


CMDS = {
    "version": [],
    "motors_set_steps_per_unit": ["str","float"],
    "motors_set_max_current": ["str","float"],
    "motors_set_motion_params": ["str","float","float","float","float","float","float","float","float"],
    "motors_set_vel_simple": [],
    "motors_set_position": ["str","float"],
    "motors_home": ["str"],
    "tec_run": ["float"],
    "tec_setpoint": ["float"],
    "tec_params": ["float","float","float","float","float"],
    "hv": ["float"],
    "set_debug_level": ["int"],
    "set_diagnostics_period": ["float"]
}

OTHER_CMDS = set([
    "set_assert_block",
    "reboot",
    "heap_high_watermark",
    "state_dump",
    "motors_write_reg",
    "motors_read_reg",
    "dummy",
    "assert_fail"
])
    


#--------------------------------------------------------------
# UTILITIES
'''
From app script - import theseus_utils
To call a function, type theseus_utils.function
ex. theseus_utils.incubate(degrees=70,hours=1,minutes=5,seconds=30)

Additionally, a function can be imported directly to minimize verbosity.
ex. from theseus_utils import incubate
    incubate(degrees=70,hours=1,minutes=5,seconds=30)

For a deeper description of functions available, please see ******************
'''

def aspirate(volume=0, height=0, pre_aspirate_volume=0, column=0, plate_type="plate", z_speed=Z_SPEED):
    # may need to set directions
    # may need to track position

    try: 
        volume = float(volume)
        height = float(height)
        pre_aspirate_volume = float(pre_aspirate_volume)
        column = int(column)
        plate_type = str(plate_type)
        z_speed = float(z_speed)
    except ValueError:
        print("One or more parameters on an \"aspirate\" call is not type compatible. Please check call.")
        exit()
    
    #Align pipette to well
    moveToWell(column, plate_type)

    #Set zaxis velocity
    addCommand("motors_set_motion_params",["zaxis",START_VEL,ACCEL_1,z_speed/2.0,MAX_ACCEL,z_speed,MAX_DECEL,DECEL_1,STOP_VEL])

    #Check for pre_aspiration
    if pre_aspirate_volume > 0:
        airAspirate(pre_aspirate_volume)

    #Begin aspiration
    if mmToUnits(height) > PIPETTE_WELL_MIN:
        if volume > 0:
            addCommand("motors_set_position",["zaxis",mmToUnits(height)])
            addCommand("motors_set_position",["pump",volumeToPumpUnits(volume)])
        else:
            print("Warning: volume is set to empty.")
    else:
        print("The height is set too low on an \"aspirate\" call. Please check the call and make the height greater than the minimum value of " + str(PIPETTE_WELL_MIN) + ".")
        exit()

    #Remove tips from wells
    addCommand("motors_set_position",["zaxis",PIPETTE_WELL_MAX+200])
    return


def dispense(volume=0, height=0, post_aspirate_volume=0, column=0, plate_type="plate", z_speed=Z_SPEED):
    # may need to set directions
    # may need to track position

    try: 
        volume = float(volume)
        height = float(height)
        post_aspirate_volume = float(post_aspirate_volume)
        column = int(column)
        plate_type = str(plate_type)
        z_speed = float(z_speed)
    except ValueError:
        print("One or more parameters on an \"aspirate\" call is not type compatible. Please check call.")
        exit()
    
    #Align pipette to well
    moveToWell(column, plate_type)

    #Set zaxis velocity
    addCommand("motors_set_motion_params",["zaxis",START_VEL,ACCEL_1,z_speed/2.0,MAX_ACCEL,z_speed,MAX_DECEL,DECEL_1,STOP_VEL])

    #Begin aspiration
    if mmToUnits(height) > PIPETTE_WELL_MIN:
        if volume > 0:
            addCommand("motors_set_position",["zaxis",mmToUnits(height)])
            addCommand("motors_set_position",["pump",volumeToPumpUnits(volume)])
        else:
            print("Warning: volume is set to empty.")
    else:
        print("The height is set too low on an \"aspirate\" call. Please check the call and make the height greater than the minimum value of " + str(PIPETTE_WELL_MIN) + ".")
        exit()

    #Remove tips from wells
    addCommand("motors_set_position",["zaxis",PIPETTE_WELL_MAX+200])

    #Check for post_aspiration
    if post_aspirate_volume > 0:
        airAspirate(post_aspirate_volume)
    return    


def moveToWell(column, plate_type):
    try:
        test = PLATES[plate_type]
        if plate_type == "plate":
            try:
                addCommand("motors_set_position",["xaxis",PLATE_Z_ALIGN[column]])
            except KeyError:
                print("The column on a call is not type compatible. Please check call and only use an integer from 0 to 23 to specify 0-based column location.")
        else:
            addCommand("motors_set_position",["xaxis",MICRO_Z_ALIGN])
    except KeyError:
        print("The plate_type on a call is not type compatible. Please check call and only use \"plate\" or \"chip\" as a string value.")
        exit()
    return


def airAspirate(aspirate_volume):
    addCommand("motors_set_position",["zaxis",PIPETTE_WELL_MAX+200])
    addCommand("motors_set_position",["pump",volumeToPumpUnits(aspirate_volume)])
    return


def pipetteMix(volume=0,num_despenses=0,height=0,final_dispense_height=None,column=0,plate_type="plate",z_speed=Z_SPEED):
    print("not yet implemented")

def ejectTips():
    print("not yet implemented")

def newTips(column=0):
    print("not yet implemented")

def incubate(temp=0,seconds=0):
    print("not yet implemented")

def thermalCycle(cycles=0,step_temps=[],step_times=[]):
    print("not yet implemented")

def separateBeads():
    print("not yet implemented")

def wait(seconds=0):
    time.sleep(seconds)
    return

def getSeconds(hours=0,minutes=0,seconds=0):
    return (hours * 60 * 60) + (minutes * 60) + seconds
    
def volumeToPumpUnits(volume):
    print("not yet implemented")

def mmToUnits(mm):
    print("not yet implemented")

def clearCommands():
    print("not yet implemented")

def addCommand(cmd,args):
    print("not yet implemented")
    '''
    

    NOTE: There is an internal look-up table that maps a set of strings to integers, which can be substituted for any argument. E.g. instead of sending the command "motors_set_steps_per_unit: 3, 51200.0" you could send "motors_set_steps_per_unit: xaxis, 51200.0". The working list of substitutions is below:
    "xaxis"  -> 1
    "zaxis"  -> 0
    "magnet  -> 3
    "pump"   -> 2
    "pinch1" -> 4
    "pinch2" -> 5
    "pinch3" -> 6
    "pinch4" -> 7

    There are also some commands that I use for debugging that I will leave undocumented for now:
    set_assert_block
    reboot
    heap_high_watermark
    state_dump
    motors_write_reg
    motors_read_reg
    dummy
    assert_fail
    print("not yet implemented")
    '''
#-------------------------------------------------------------------------------------------
if __name__ == "__main__":
    aspirate()