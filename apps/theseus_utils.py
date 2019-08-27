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
    5160,5170,5180,5190,5200,
]
MICRO_Z_ALIGN = 1000
MICRO_MAGNET_ALIGN = 5500
MAGNET_ACTIVE_ALIGN = 50
PIPETTE_MIN = 0
PIPETTE_WELL_MIN = 1
PIPETTE_WELL_MAX = 100
PIPETTE_MAX = 2000
TEC_POSITION = 1000

START_VEL = 0.0
ACCEL_1 = 1.0
MAX_ACCEL = 0.5
MAX_DECEL = -0.5
DECEL_1 = -1.0
STOP_VEL = 0.0

Z_UP = 0
Z_DOWN = 1

X_LEFT = 0
X_RIGHT = 1

PUMP_OUT = 0
PUMP_IN = 1

VALVE_OFF = 0
VALVE_ON = 10

HOME = 0

PLATES = {"plate":True,"chip":True}


CMDS = {
    "version": [],
    "motors_set_steps_per_unit": ["str","float"],
    "motors_set_max_current": ["str","float"],
    "motors_set_motion_params": ["str","float","float","float","float","float","float","float","float"],
    "motors_set_vel_simple": [],
    "motors_set_position": ["str","float"],
    "motors_home": ["str"],
    "tec_run": ["float", "float"],
    "tec_params": ["float","float","float","float","float"],
    "hv": ["float"],
    "set_debug_level": ["int"],
    "set_diagnostics_period": ["float"],
    "set_leds": ["int","int","int"]
}

OTHER_CMDS = set([
    "set_assert_block",
    "reboot",
    "heap_high_watermark",
    "state_dump",
    "motors_write_reg",
    "motors_read_reg",
    "dummy",
    "assert_fail",
    "print",
    "delay",
    "add_block",
    "comment"
])
dir = os.path.dirname(os.path.realpath(__file__))
CMD_FILE = os.path.join(dir, "..", "cmd", "cmd.txt")

cmd_id = 0
current_volume = 0

#last_x_pos = 

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
    global current_volume
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
    
    #Adding comment
    
    toPrint("aspiration")

    #Align pipette to well
    moveToWell(column, plate_type)

    #Set zaxis velocity
    addCommand("motors_set_motion_params",["zaxis",START_VEL,ACCEL_1,z_speed/2.0,MAX_ACCEL,float(z_speed),MAX_DECEL,DECEL_1,STOP_VEL])

    #Check for pre_aspiration
    if pre_aspirate_volume > 0:
        airAspirate(pre_aspirate_volume)

    #Begin aspiration
    if mmToUnits(height) >= PIPETTE_WELL_MIN:
        if volume > 0:
            addCommand("motors_set_position",["zaxis",mmToUnits(height)])
            wait(seconds=5)
            addCommand("motors_set_position",["pump",volumeToPumpUnits(current_volume + volume)])
            current_volume += volume
            wait(seconds=5)
        else:
            print("Warning: volume is set to empty.")
    else:
        print("The height is set too low on an \"aspirate\" call. Please check the call and make the height greater than the minimum value of " + str(PIPETTE_WELL_MIN) + ".")
        exit()

    #Remove tips from wells
    addCommand("motors_set_position",["zaxis",PIPETTE_WELL_MAX+200])
    wait(seconds=5)

    #Adding block
    addBlock()
    return


def dispense(volume=0, height=0, post_aspirate_volume=0, column=0, plate_type="plate", z_speed=Z_SPEED):
    global current_volume
    try: 
        volume = float(volume)
        height = float(height)
        post_aspirate_volume = float(post_aspirate_volume)
        column = int(column)
        plate_type = str(plate_type)
        z_speed = float(z_speed)
    except ValueError:
        print("One or more parameters on an \"dispense\" call is not type compatible. Please check call.")
        exit()
    
    #Adding comment
    toPrint("dispense")

    #Align pipette to well
    moveToWell(column, plate_type)

    #Set zaxis velocity
    addCommand("motors_set_motion_params",["zaxis",START_VEL,ACCEL_1,z_speed/2.0,MAX_ACCEL,z_speed,MAX_DECEL,DECEL_1,STOP_VEL])
    
    #Begin dispense
    if mmToUnits(height) >= PIPETTE_WELL_MIN:
        if volume > 0:
            addCommand("motors_set_position",["zaxis",mmToUnits(height)])
            wait(seconds=5)
            addCommand("motors_set_position",["pump",volumeToPumpUnits(current_volume - volume)])
            current_volume -= volume
            wait(seconds=5)
        else:
            print("Warning: volume is set to empty.")
    else:
        print("The height is set too low on an \"dispense\" call. Please check the call and make the height greater than the minimum value of " + str(PIPETTE_WELL_MIN) + ".")
        exit()

    #Remove tips from wells
    addCommand("motors_set_position",["zaxis",PIPETTE_WELL_MAX+200])
    wait(seconds=5)

    #Check for post_aspiration
    if post_aspirate_volume > 0:
        airAspirate(post_aspirate_volume)

    #Adding block
    addBlock()
    return    


def moveToWell(column, plate_type):
    try:
        test = PLATES[plate_type]
        if plate_type == "plate":
            try:
                addCommand("motors_set_position",["xaxis",PLATE_Z_ALIGN[column]])
            except KeyError:
                print("The column on a call is not type compatible. Please check call and only use an integer from 0 to 20 to specify 0-based column location.")
        else:
            addCommand("motors_set_position",["xaxis",MICRO_Z_ALIGN])

        wait(seconds=10)
    except KeyError:
        print("The plate_type on a call is not type compatible. Please check call and only use \"plate\" or \"chip\" as a string value.")
        exit()
    return


def airAspirate(aspirate_volume):
    global current_volume
    addCommand("motors_set_position",["zaxis",PIPETTE_WELL_MAX+200])
    wait(seconds=5)
    addCommand("motors_set_position",["pump",volumeToPumpUnits(current_volume + aspirate_volume)])
    wait(seconds=5)
    current_volume += aspirate_volume
    return


def pipetteMix(volume=0, mix_cycles=0, pre_aspirate_volume=0, aspirate_height=0, dispense_height=0, final_dispense_height=-1, column=0, plate_type="plate", z_speed=Z_SPEED):
    global current_volume
    try: 
        volume = float(volume)
        mix_cycles = int(mix_cycles)
        pre_aspirate_volume = float(pre_aspirate_volume)
        aspirate_height = float(aspirate_height)
        dispense_height = float(dispense_height)
        final_dispense_height = float(final_dispense_height)
        column = int(column)
        plate_type = str(plate_type)
        z_speed = float(z_speed)
    except ValueError:
        print("One or more parameters on an \"pipetteMix\" call is not type compatible. Please check call.")
        exit()

    #Adding comment
    toPrint("pipetterMix")

    #Align pipette to well
    moveToWell(column, plate_type)

    #Set zaxis velocity
    addCommand("motors_set_motion_params",["zaxis",START_VEL,ACCEL_1,z_speed/2.0,MAX_ACCEL,float(z_speed),MAX_DECEL,DECEL_1,STOP_VEL])

    #Check for pre_aspiration
    if pre_aspirate_volume > 0:
        airAspirate(pre_aspirate_volume)

    #Loop dispenses
    for m in range(mix_cycles):
        #Aspirate
        if mmToUnits(aspirate_height) >= PIPETTE_WELL_MIN:
            if volume > 0:
                addCommand("motors_set_position",["zaxis",mmToUnits(aspirate_height)])
                wait(seconds=2)
                addCommand("motors_set_position",["pump",volumeToPumpUnits(current_volume + volume)])
                current_volume += volume
                wait(seconds=2)
            else:
                print("Warning: pipetteMix aspirate volume is set to empty.")
        else:
            print("The aspirate height is set too low on an \"pipetteMix\" call. Please check the call and make the aspirate height greater than the minimum value of " + str(PIPETTE_WELL_MIN) + ".")
            exit()
        #Dispense
        if m != mix_cycles - 1 or final_dispense_height == -1:
            if mmToUnits(dispense_height) >= PIPETTE_WELL_MIN:
                if volume > 0:
                    addCommand("motors_set_position",["zaxis",mmToUnits(dispense_height)])
                    wait(seconds=2)
                    addCommand("motors_set_position",["pump",volumeToPumpUnits(current_volume - volume)])
                    current_volume -= volume
                    wait(seconds=2)
                else:
                    print("Warning: pipetteMix volume is set to empty.")
            else:
                print("The dispense height is set too low on an \"pipetteMix\" call. Please check the call and make the dispense height greater than the minimum value of " + str(PIPETTE_WELL_MIN) + ".")
                exit()
        else:
            if mmToUnits(final_dispense_height) >= PIPETTE_WELL_MIN:
                if volume > 0:
                    addCommand("motors_set_position",["zaxis",mmToUnits(final_dispense_height)])
                    wait(seconds=2)
                    addCommand("motors_set_position",["pump",volumeToPumpUnits(current_volume - volume)])
                    current_volume -= volume
                    wait(seconds=2)
                else:
                    print("Warning: pipetteMix volume is set to empty.")
            else:
                print("The final dispense height is set too low on an \"pipetteMix\" call. Please check the call and make the final dispense height greater than the minimum value of " + str(PIPETTE_WELL_MIN) + ".")
                exit()
    #Remove tips from wells
    addCommand("motors_set_position",["zaxis",PIPETTE_WELL_MAX+200])
    wait(seconds=5)

    #Adding block
    addBlock()
    return 

def closeCannula(cannula):
    if cannula = LEFT:
        addCommand("motors_set_position":["valve1",VALVE_ON])
        wait(seconds=3)
        addCommand("motors_set_position":["valve3",VALVE_ON])
        wait(seconds=3)
    elif cannula = RIGHT:
        addCommand("motors_set_position":["valve2",VALVE_ON])
        wait(seconds=3)
        addCommand("motors_set_position":["valve4",VALVE_ON])
        wait(seconds=3)
    else:
        print("closeCannula input incorrect, please use LEFT or RIGHT as input")
        exit()




def incubate(temp=0, seconds=0, end_open_valves=True):
    global current_volume
    global pre_tec_volume

    try: 
        temp = float(temp)
        seconds = float(seconds)
    except ValueError:
        print("One or more parameters on an \"incubate\" call is not type compatible. Please check call.")
        exit()

    #Adding comment
    toPrint("incubate")

    if current_volume != TEC_POSITION:
        #Move to TEC
        addCommand("motors_set_position",["pump",volumeToPumpUnits(TEC_POSITION)])
        wait(seconds=10)

        #Close valves
        addCommand("motors_set_position",["valve1",VALVE_ON])
        addCommand("motors_set_position",["valve2",VALVE_ON])
        addCommand("motors_set_position",["valve3",VALVE_ON])
        addCommand("motors_set_position",["valve4",VALVE_ON])
        wait(seconds=10)
        pre_tec_volume = current_volume

    #TEC activate
    addCommand("tec_run",[temp,seconds])
    wait(seconds=seconds)

    if end_open_valves:
        #Open valves
        addCommand("motors_set_position",["valve1",VALVE_OFF])
        addCommand("motors_set_position",["valve2",VALVE_OFF])
        addCommand("motors_set_position",["valve3",VALVE_OFF])
        addCommand("motors_set_position",["valve4",VALVE_OFF])
        wait(seconds=10)

        #Move back to position
        addCommand("motors_set_position",["pump",volumeToPumpUnits(pre_tec_volume)])
        wait(seconds=10)
        current_volume = pre_tec_volume
    else:
        current_volume = TEC_POSITION

    #Adding block
    addBlock()
    return


def thermalCycle(cycles=0, temps=[], times=[], end_open_valves=True):
    global current_volume
    global pre_tec_volume

    try: 
        temps = list(temps)
        times = list(times)
    except ValueError:
        print("One or more parameters on an \"incubate\" call is not type compatible. Please check call.")
        exit()

    if len(temps) != len(times):
        print("temps and times on an \"incubate\" call are not the same length. Please ensure the same length.")
        exit()

    #Adding comment
    toPrint("thermalCycle")

    if current_volume != TEC_POSITION:
        #Move to TEC
        addCommand("motors_set_position",["pump",volumeToPumpUnits(TEC_POSITION)])
        wait(seconds=10)

        #Close valves
        addCommand("motors_set_position",["valve1",VALVE_ON])
        addCommand("motors_set_position",["valve2",VALVE_ON])
        addCommand("motors_set_position",["valve3",VALVE_ON])
        addCommand("motors_set_position",["valve4",VALVE_ON])
        wait(seconds=10)
        pre_tec_volume = current_volume
    
    #TEC activate
    for c in range(cycles):
        for i, t in enumerate(temps):
            addCommand("tec_run",[t,times[i]])
            wait(seconds=times[i])

    if end_open_valves:
        #Open valves
        addCommand("motors_set_position",["valve1",VALVE_OFF])
        addCommand("motors_set_position",["valve2",VALVE_OFF])
        addCommand("motors_set_position",["valve3",VALVE_OFF])
        addCommand("motors_set_position",["valve4",VALVE_OFF])
        wait(seconds=10)

        #Move back to position
        addCommand("motors_set_position",["pump",volumeToPumpUnits(pre_tec_volume)])
        wait(seconds=10)
        current_volume = pre_tec_volume
    else:
        current_volume = TEC_POSITION

    #Adding block
    addBlock()
    return


def separateBeads():
    print("not yet implemented")

def wait(seconds=0):
    addCommand("delay",[seconds]) 
    return


def getSeconds(hours=0, minutes=0, seconds=0):
    return (hours * 60 * 60) + (minutes * 60) + seconds
    
def volumeToPumpUnits(volume):
    return volume # change when actual conversion is known

def mmToUnits(mm):
    return mm # change when actual conversion is known

def comment(message):
    addCommand("comment",[str(message)]) 

def toPrint(message):
    addCommand("print",[str(message)]) 

def addBlock():
    addCommand("add_block",[]) 

def initCommands():
    print(dir)
    with open(CMD_FILE, 'w'): pass
    comment("Before assay") 
    addCommand("version",[]) 
    addCommand("motors_home",["zaxis"]) 
    addCommand("motors_home",["magnet"]) 
    addCommand("motors_home",["xaxis"]) 
    addCommand("motors_home",["pump"]) 
    addCommand("motors_home",["valve1"]) 
    addCommand("motors_home",["valve2"]) 
    addCommand("motors_home",["valve3"]) 
    addCommand("motors_home",["valve4"]) 
    toPrint("homing complete")
    addBlock()
    comment("input speed values for stages")
    addCommand("set_leds":[1,0,1])
    addBlock()

    return

def addCommand(cmd, args):
    # assertions for cmd and args being formatted correctly
    # asserting cmd exists
    global cmd_id
    if cmd not in CMDS and cmd not in OTHER_CMDS:
        print("Attempted to add cmd to cmd.txt via an \"addCommand\" call that does not exist.")
        print(cmd)
        exit()
    if cmd in CMDS and cmd not in OTHER_CMDS:
        # asserting number of args is correct with associated cmd
        expected_args = CMDS[cmd]
        if len(expected_args) != len(args):
            print("Number of arguments specified in an \"addCommand\" call not correct. Expected " + str(len(expected_args)) + " but recieved " + str(len(args)) +".")
            exit()
        # asserting args types are correct
        for b, a in enumerate(args):
            if expected_args[b] == 'float':
                if (isinstance(a, float) or isinstance(a, int)) == False:
                    print("cmd:\t" + str(cmd))
                    print("expected_args:\t" + str(expected_args))
                    print("An argument in an \"addCommand\" call is the wrong type. Expected float but recieved " + str(a) + " at args index " + str(b) + ".")
                    exit()
            elif expected_args[b] == 'int' == False:
                if isinstance(a, int):
                    print("An argument in an \"addCommand\" call is the wrong type. Expected int but recieved " + str(a) + " at args index " + str(b) + ".")
                    exit()
            elif expected_args[b] == 'str':
                if isinstance(a, str) == False:
                    print("An argument in an \"addCommand\" call is the wrong type. Expected str but recieved " + str(a) + " at args index " + str(b) + ".")
                    exit()


    # retrieving cmd_id
    cmd_id += 1

    # setting init 
    if cmd_id == 1:
        print("Initializing cmd.txt")
        cmd_id += 0 # change when you intialize the cmd.txt

    # appending new command to cmd.txt
    args = [ str(a) for a in args ]
    with open(CMD_FILE, 'a') as f:
        if cmd == "comment":
            f.write("# " + '\n#'.join(args) + "\n")
        elif cmd == "add_block":
            f.write("\n")
        else:
            #f.write(str(cmd_id) + ":\t" + str(cmd) + ":\t" + ', '.join(args) + "\n")
            if len(args) != 0:
                f.write(str(cmd) + ":\t" + ', '.join(args) + "\n")
            else:
                f.write(str(cmd) + "\n")

    return

LEFT = 1
RIGHT = 2

LEFT1 = 0
LEFT2 = 1
LEFT3 = 2
LEFT4 = 3
LEFT5 = 4
LEFT6 = 5
LEFT7 = 6
LEFT8 = 7
LEFT9 = 8
LEFT10 = 9
LEFT11 = 10
LEFT12 = 11
LEFT13 = 12
LEFT14 = 13
LEFT15 = 14
LEFT16 = 15
LEFT17 = 16
LEFT18 = 17
LEFT19 = 18
LEFT20 = 19
LEFT21 = 20

RIGHT4 = 0 
RIGHT5 = 1
RIGHT6 = 2
RIGHT7 = 3
RIGHT8 = 4
RIGHT9 = 5
RIGHT10 = 6
RIGHT11 = 7
RIGHT12 = 8
RIGHT13 = 9
RIGHT14 = 10
RIGHT15 = 11
RIGHT16 = 12
RIGHT17 = 13
RIGHT18 = 14
RIGHT19 = 15
RIGHT20 = 16
RIGHT21 = 17
RIGHT22 = 18
RIGHT23 = 19
RIGHT24 = 20

#-------------------------------------------------------------------------------------------
if __name__ == "__main__":
    aspirate()