import sys
import os
import argparse
import theseus_utils

#NAME:DNA Rapid XP
#INPUTS:Genomic DNA
#COLOR:yellow
#yellow, red, green, +more in future


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
    type=list,
    help="input concentrations (list)")

options = parser.parse_args()
#options.i for input type, options.i2 for input concentrations

# making fragmentation buffer mixture
theseus_utils.aspirate(volume=10, height=25, column=0)
theseus_utils.dispense(volume=10, height=25, column=1)
theseus_utils.pipetteMix(volume=10, num_dispenses=10, aspirate_height=15, dispense_height=25, column=1)

# making fragmentation reaction
theseus_utils.aspirate(volume=39, height=25, column=1)
theseus_utils.dispense(volume=39, height=25, column=2)
theseus_utils.pipetteMix(volume=25, num_dispenses=10, aspirate_height=15, dispense_height=25, column=2)

# incubation fragmentation reaction
theseus_utils.aspirate(volume=50, height=0, column=2)
theseus_utils.moveVolumeToTEC()
theseus_utils.incubate(temp=4, seconds=60)
#   # using fragmentation table logic # assuming 200-300bp fragment size
minimum_input = min(options.i2)
if minimum_input < 10:
    theseus_utils..incubate(temp=35, seconds=theseus_utils.getSeconds(minutes=24))
elif minimum_input < 100:
    theseus_utils..incubate(temp=35, seconds=theseus_utils.getSeconds(minutes=18))
elif minimum_input < 1000:
    theseus_utils..incubate(temp=35, seconds=theseus_utils.getSeconds(minutes=15))
else:
    theseus_utils..incubate(temp=35, seconds=theseus_utils.getSeconds(minutes=14))
theseus_utils.incubate(temp=65, seconds=theseus_utils.getSeconds(minutes=30))
theseus_utils.incubate(temp=4, seconds=theseus_utils.getSeconds(minutes=5))

# adapter ligation

