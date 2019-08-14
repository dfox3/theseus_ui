# theseus_ui

## Concept
These scripts and files make up the developmental Theseus UI. 


## Installation

Open a Unix terminal and type `git clone https://github.com/dfox3/theseus_ui.git`

Alternatively, you can download the zip from [the current repo](https://github.com/dfox3/theseus_ui) and unzip the directory.

## Requirements

These scripts are not packaged and are not standalone executable at this stage. 
Needed:
 - Windows cmd line
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

Navigate to the working "theseus_ui" directory via Windows cmd.
Execute python script.

```
python theseus_ui.py
```

## Status

### GUI related
This is the opening screen of the software when launched. There are 3 buttons to choose from.
![screen1](screenshots/20190813/screen1.png)

This screenshot shows the initial configuration of a Theseus run. User can choose from a dropdown a Library and Sample Type for the run. Dropdowns were used so newly developed App scripts can be more easily (automatically) incorporated into the UI. The user will also have a Reset button and a ? button that will abort and guide the user respectively via prompts.
![screen2](screenshots/20190813/screen2.png)

Here is an example of one of the dropdowns.
![screen3](screenshots/20190813/screen3.png)

After the Library and Sample Type is configured, the user can then ready the intrument with a 3 step process. These steps are currentlt clickable for testing purposes - the ideal system waits for system barcode triggers to check the buttons.
![screen4](screenshots/20190813/screen4.png)

![screen5](screenshots/20190813/screen5.png)

Click the timer and wait. Timer set for 5 secs for testing.
![screen6](screenshots/20190813/screen6.png)

![screen7](screenshots/20190813/screen7.png)

Plate displays preloaded wells w/ reagents colorized. This is currently a static image, but ideally these will be generated on a Library to Library basis. This currently moves to the next screen after all wells are clicked. I question the function of these clickable wells at the moment - needs clarification.
![screen8](screenshots/20190813/screen8.png)

Currently, when all wells are checked on the previous screen, a spreadsheet appears that allows the user to annotate samples with names and notes. The greyed-out columns are not mutable, but the white columns are. When the user is satisfied with the annotation, they can select "Run App" which executes the configured library prep application.
![screen9](screenshots/20190813/screen9.png)

![screen10](screenshots/20190813/screen10.png)



### Middle package for app scientists
Here are a tenative functions an app scientist could use to build app scripts. Aspirating and dispensing pipettes are tenatively developed, and we need calibration of global variables on a real Theseus. The most important method is "addCommand" which will writes commands to a text file that will be sent off to the embeded listener. 
![screen1](screenshots/20190814/screen1.png)



## Not yet developed:
### GUI related
 - ? button help prompt
 - dynamic plate diagram
 - run progress bar
 - view results screen
    - spreadsheet displayed w/ output concentrations
    - export to csv function
 - tools screen
 - connection to barcoded sample system
 - connection to library prep apps
    - send commands
    - interpret embedded commands
 - connection to Theseus
 - standalone executable

### Middle package for app scientists
 - get static, global variable for various motor units
 - pipetteMix
 - ejectTips
 - newTips
 - incubate
 - thermalCycle
 - separateBeads
 - volumeToPumpUnits
 - mmToUnits
 - clearCommands
 - addCommand


## Info:

**20190814**

**Dylan Fox**

**dylan.fox@perkinelmer.com**
