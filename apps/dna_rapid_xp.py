import argparse
from theseus_utils import *

#NAME:DNA Rapid XP
#INPUTS:Genomic DNA
#COLOR:yellow
#white, blue, purple, teal, green, wine, red, orange, yellow
parser = argparse.ArgumentParser(description='DNA Rapid XP')
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






# making fragmentation buffer mixture
aspirate(volume=10, height=25, column=LEFT1)
dispense(volume=10, height=25, column=LEFT2)
pipetteMix(volume=10, mix_cycles=10, aspirate_height=15, dispense_height=25, column=LEFT2)

# making fragmentation reaction
aspirate(volume=39, height=25, column=LEFT2)
dispense(volume=39, height=25, column=LEFT3)
pipetteMix(volume=25, mix_cycles=10, aspirate_height=15, dispense_height=25, column=LEFT3)

# incubation fragmentation reaction
aspirate(volume=50, height=1, column=LEFT3)
incubate(temp=4, seconds=60, end_open_valves=False)
#   # using fragmentation table logic # assuming 200-300bp fragment size
minimum_input = min(options.i2)
if minimum_input < 10:
    incubate(temp=35, seconds=getSeconds(minutes=24), end_open_valves=False)
elif minimum_input < 100:
    incubate(temp=35, seconds=getSeconds(minutes=18), end_open_valves=False)
elif minimum_input < 1000:
    incubate(temp=35, seconds=getSeconds(minutes=15), end_open_valves=False)
else:
    incubate(temp=35, seconds=getSeconds(minutes=14), end_open_valves=False)
incubate(temp=65, seconds=getSeconds(minutes=30), end_open_valves=False)
incubate(temp=4, seconds=getSeconds(minutes=5))
dispense(volume=50, height=1, column=LEFT3)

# adapter ligation mixing
aspirate(volume=50, height=25, column=LEFT3)
dispense(volume=50, height=25, column=LEFT7)
aspirate(volume=2.5, height=25, column=LEFT5)
dispense(volume=2.5, height=25, column=LEFT7)
aspirate(volume=3, height=25, column=RIGHT9)
dispense(volume=3, height=25, column=RIGHT7)
pipetteMix(volume=44.5, mix_cycles=10, aspirate_height=15, dispense_height=25, column=LEFT7)

# adapter ligation incubation
aspirate(volume=100, height=1, column=LEFT7)
incubate(temp=20, seconds=getSeconds(minutes=15), end_open_valves=False)
incubate(temp=4, seconds=getSeconds(minutes=5))
dispense(volume=100, height=25, column=LEFT7)

# bead cleanup
addCommand("print",["Bean cleanup not built yet*********"])
addCommand("print",["Bean cleanup not built yet*********"])
addCommand("print",["Bean cleanup not built yet*********"])
addCommand("add_block",[])

# pcr amplification mix
aspirate(volume=23, height=1, column=LEFT15)
dispense(volume=23, height=10, column=LEFT16)
aspirate(volume=2, height=1, column=LEFT18)
dispense(volume=2, height=10, column=LEFT16)
pipetteMix(volume=25, mix_cycles=10, aspirate_height=15, dispense_height=25, column=LEFT16)

# pcr
aspirate(volume=50, height=1, column=LEFT16)
incubate(temp=98, seconds=30, end_open_valves=False)
thermalCycle(cycles=8, temps=[98,65,72], times=[15,30,30], end_open_valves=False)
incubate(temp=72, seconds=120)
dispense(volume=50, height=10, column=LEFT16)

# bead cleanup
addCommand("print",["Bean cleanup not built yet*********"])
addCommand("print",["Bean cleanup not built yet*********"])
addCommand("print",["Bean cleanup not built yet*********"])
addCommand("add_block",[])


