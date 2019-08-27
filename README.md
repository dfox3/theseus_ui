# theseus_ui

## Concept
These scripts and files make up the developmental Theseus UI. 


## Installation

Open a Unix terminal and type `git clone https://dylando@bitbucket.org/thesepe/thesui.git`


## Requirements

*These scripts are not packaged and are not standalone executable at this stage. Requirements are needed for dev env.*

Needed:

 - Python 3.7.X (latest version)
     - pip installed with
         - [PyQt5](https://pypi.org/project/PyQt5/)
         - For more information on how to pip install, visit [this guide](https://packaging.python.org/tutorials/installing-packages/#ensure-you-can-run-pip-from-the-command-line) for more information.


     - other imports from [The Python Standard Library](https://docs.python.org/2/library/) (typically pre-installed):
        - [functools](https://docs.python.org/3/library/functools.html)
        - [datetime](https://docs.python.org/3/library/datetime.html)
        - [time](https://docs.python.org/3/library/time.html)
        - [csv](https://docs.python.org/3/library/csv.html)
        - [pickle](https://docs.python.org/3/library/pickle.html)

## Use:
### Standalone Executable
Double click on theseus_ui.exe

### cmd line
Navigate to the working "theseus_ui" directory via Windows cmd.
Execute python script.

```
python theseus_ui.py
```

## Status

### GUI related

**3. Make Libraries**

![gif1](screenshots/20190825/gif1.gif)

There are 3 buttons to choose from. I propose there should be a title launched on this screen to make use of the negative space. 

User can choose from a dropdown a Library and Sample Type for the run. Dropdowns were used so newly developed App scripts can be more easily (automatically) incorporated into the UI. The user will also have a Reset button and a ? button that will abort and guide the user respectively via prompts.

After the Library and Sample Type is configured, the user can then ready the intrument with a 3 step process. These steps are currently clickable for testing purposes - the ideal system waits for system barcode triggers to check the buttons.

Click the timer and wait. Timer set for 5 secs for testing.

Plate displays preloaded wells w/ reagents colorized. 

A spreadsheet appears that allows the user to annotate samples with names and notes. The greyed-out columns are not mutable, but the white columns are. When the user is satisfied with the annotation, they can select "Run App" which executes the configured library prep application.


**2. View Results**

![gif2](screenshots/20190825/gif2.gif)

The View Results screen automatically loads the most recent dataset upon software start-up. 

The user can only edit the sample names at this moment, and the other data fields are immutable. 

The user can load in other datasets with the Load button, which are automatically stored in .p serial pickle (python object) files in the software file structure.

If the user makes any changes to the spreadsheet, they can opt to overwrite the .p files with the Save button.

The Export button allows the user to convert the data to .csv if they need to use the data in downstream analysis.


**3. Tools**

Not yet implemented


### Support package for app scientists
Here are a tentative functions an app scientist could use to build app scripts. The most important method is "addCommand" which will writes commands to a text file that will be sent off to the embeded listener. 

```
def aspirate(volume=0, height=0, pre_aspirate_volume=0, column=0, plate_type="plate", z_speed=Z_SPEED):

def dispense(volume=0, height=0, post_aspirate_volume=0, column=0, plate_type="plate", z_speed=Z_SPEED):

def moveToWell(column, plate_type):

def airAspirate(aspirate_volume):

def pipetteMix(volume=0, mix_cycles=0, pre_aspirate_volume=0, aspirate_height=0, dispense_height=0, final_dispense_height=-1, column=0, plate_type="plate", z_speed=Z_SPEED):

def incubate(temp=0, seconds=0, end_open_valves=True):

def thermalCycle(cycles=0, temps=[], times=[], end_open_valves=True):

def separateBeads(): #  ***************not yet implemented

def wait(seconds=0):

def getSeconds(hours=0, minutes=0, seconds=0):

def volumeToPumpUnits(volume): # might not need

def mmToUnits(mm): # might not need

def clearCommands():

def addCommand(cmd, args):
```

Global variables need to be calibrated for the theseus_utils.py to work in practice. Currently by importing theseus_utils.py to write a script, an app developer can write cmd.txts that will be interpreted by thes_host, but the global variables used for positional reference are nonsense. 

The global variables that will need to be changed are located near the top of theseus_utils.py. They are as follows:

```
PLATE_Z_ALIGN = [
    5000,5010,5020,5030,5040,5050,5060,5070,
    5080,5090,5100,5110,5120,5130,5140,5150,
    5160,5170,5180,5190,5200,
]
```
PLATE_Z_ALIGN is a list that contains the positions that align the pipette tips to columns on the 384 well plate. There are 21 positions because the y-shaped pipette tips are 3 columns apart and there are 24 columns total. The left tip cannot clip to the left of column 1, so the right tip's left most column is column 4. Conversely, the left tip's right most column is column 21, and the right tip's right most column is column 24.

```
MICRO_Z_ALIGN = 1000
```
MICRO_Z_ALIGN is intended to align the pipettes to the microfluidic chips. I am not currently versed on the nature of the microfluidic chip - specifically how the pipettes can interact with the chip. This may become a list like PLATE_Z_ALIGN once the microfluidic chip functions are developed.

```
MICRO_MAGNET_ALIGN = 5500
```
This is the position that aligns the microfluidic chip to the magnet on the x axis.

```
MAGNET_ACTIVE_ALIGN = 50
```
This is the position that aligns the magnet veritically to the level of a microfluidic chip via the magnet motor.

```
PIPETTE_MIN = 0
PIPETTE_WELL_MIN = 1
PIPETTE_WELL_MAX = 100
PIPETTE_MICRO_MIN = 1
PIPETTE_MICRO_MAX = 100
PIPETTE_MAX = 2000
```
The PIPETTE values are all different positional calibrations for the z-axis. PIPETTE_MIN is the absolute lowest value that the pipettes can align. PIPETTE_WELL_MIN is the position that aligns the pipette to the bottom of a well on a 384 well plate. PIPETTE_WELL_MAX is the position that aligns the pipette to the top of a well on a 384 well plate. PIPETTE_MICRO_MIN is the position that aligns the pipette to the bottom of a well on a microfluidic chip. PIPETTE_MICRO_MAX is the position that aligns the pipette to the top of a well on a microfluidic chip. PIPETTE_MAX is the absolute highest value that pipettes can align.

```
TEC_POSITION = 1000
```
TEC_POSITION is the position that aligns volume to the TEC. Please calibrate this value by aspirating liquid when the pump motor is initialized at 0. This implies there is not an air aspiration prior to a liquid aspiration. 



### Writing apps
In the directory apps/, there are examples of how apps may be written. [dna_rapid_xp.py](apps/dna_rapid_xp.py) is the most developed app example at the moment. dna_rapid_xp.py is a pseudo-implementation of an app based on the library prep manual located [here](library_prep_manuals/5149-01 NEXTflex Rapid XP DNA-Seq Kit_v19.05_EDTA_v3.pdf). 

There are a few practices that need to be followed when building app scripts.


**1. Imports**
```
import argparse
from theseus_utils import *
```

Importing argparse is important for processing arguments sent from the UI. The theseus_utils import allows for all defs and global variable from theseus_utils.py to be used in the app script.


**2. Comment configurations**
```
#NAME:name
#INPUTS:Genomic DNA, 10 uL Blood
#COLOR:color
#colors - white, blue, purple, teal, grean, wine, red, orange, yellow
```

Adding #NAME:name as a comment allows for the UI know the name of the script. Adding #INPUTS:Genomic DNA, 10 uL Blood as a comments tells the UI which inputs are allowed for this library prep; however, this function is not fully implemented at the moment. Adding #COLOR:color as a comment lets the app scientist change the color associated to the dropdown element build from the app. replace "color" with the colors listed (white, blue, purple, etc.). If these comments are not syntaxial to the example, the UI may not incorporate the app correctly. 

**3. Arguments**
```
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
```

This adds arguments to the script. There are two arguments needed for an app script to connect correctly with the UI, -i and -i2. -i is the input type that was chosen in the UI. -i2 is a list of floats that have the different input values. This information can be used in conditionals that represent different paths in library prep protocols. Sometimes library prep manuals will give the user different options based on input concentrations and types. 

**4. Clear commands**
```
clearCommands()
```
Calling clearCommands(), which is imported from theseus_utils, will wipe the previous commands in cmd/cmd.txt. This is necessary to prevent appending to previously built cmd.txts. 

**Best practice**

All four of the practices listed above should always be included in an app script. It's easiest to copy-paste an example, or this code into your script prior to writing the protocol:
```
import argparse
from theseus_utils import *

#NAME:new kit
#INPUTS:Genomic DNA, 10 uL Blood
#COLOR:yellow
#white, blue, purple, teal, grean, wine, red, orange, yellow
parser = argparse.ArgumentParser(description='new kit')
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
clearCommands()
#--------------------------------------------------------------

```
The rest of the script should include calling functions from theseus_utils mixed with standard python code and practices. 


### Theseus host
The theseus host script, thes_host.py lives in thes_host/. This script communicates with the embedded scripts and serves as a middle-man for app scripts and theseus. It accepts txt commands found in this [documentation](https://bitbucket.org/thesepe/thesfw/src/master/fw/Documentation/html/group__thes__cmds.html). The script will run two ways. The first is with an input script, see here:

```
python thes_host.py -i cmd.txt
```

The second is "dev mode," which allows the users to manually input commands via terminal prompts. Remove the -i flag to enter dev mode. 

```
python thes_host.py
```

Similar to theseus_utils.py, thes_host.py needs an update to global variables. Currently, there is only one variable that needs to be changed.

```
WINPORT = "ELTIMA"
```
WINPORT should be changed to a string unique to the serial port identifier. When thes_host.py is executed, it will automatically try to connect to a serial port. If run on Windows, thes_host.py will first print all serial ports connected to the host computer to the console. Replace "ELTIMA" with the correct Theseus unique identifier.


## Not yet developed:
### GUI related
 - ? button help prompt
 - run progress bar
 - view results screen
    - spreadsheet displayed w/ output concentrations
    - export to csv function
 - tools screen
 - connection to barcoded sample system
 - connection to library prep apps
    - interpret embedded commands

### Support package for app scientists
 - get static, global variables for various motor units
 - separateBeads
 - volumeToPumpUnits
 - mmToUnits


## Info:

**20190821**

**Dylan Fox**

**dylan.fox@perkinelmer.com**
