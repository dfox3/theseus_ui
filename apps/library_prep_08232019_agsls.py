import argparse
from theseus_utils import *

#NAME:Library Prep 08232019 AGSLS
#INPUTS:Genomic DNA
#COLOR:purple
#white, blue, purple, teal, green, wine, red, orange, yellow
parser = argparse.ArgumentParser(description='Library Prep 08232019 AGSLS')
parser.add_argument('-i',  
    action='store', 
    dest='i',
    required=True,
    type=str,
    help="input type - Genomic DNA or 10 uL Blood")
parser.add_argument('-i2',  
    action='store', 
    dest='i2',
    required=True,
    nargs='+',
    type=float,
    help="input concentrations (list)")

options = parser.parse_args()
options.i2 = [ float(i) for i in options.i2 ]
#options.i for input type, options.i2 for input concentrations
initCommands()
#--------------------------------------------------------------

comment("Cann1 handles clean reagents, Cann2 handles contaminated reagents")
addBlock()

comment("Step 1: End Repair\t#DNA sample is mixed into ERA well before starting")
addCommand("motors_move",["pump",1.5]) # could probably replace with airAspirate(1.5) but I used commands to be more aligned with original code
addCommand("motors_move",["xaxis",15.1])
toPrint("End Repair Beginning, 30 minutes")
wait(getSeconds(minutes=30))
addBlock()

comment("Step 2: Adenylation")
closeCannula(LEFT)
addCommand("motors_move",["zaxis",23.5]) # could probably replace with an aspirate() call 
addCommand("motors_move",["pump",20.5])
# we should talk about pressurizing and if there are standard events
addCommand("motors_move",["valve2",10])
wait(seconds=3)
addCommand("motors_move",["pump",5])
addCommand("motors_move",["valve4",10])
wait(seconds=3)
toPrint("Adenylation Beginning, 30 minutes")
addCommand("tec",[65,getSeconds(minutes=30)])
