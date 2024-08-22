# DDC-festival-schedule-generator
 Decode Demcon Challenge - festival schedule generator

## How to use
_Optional:   Generate a random list of shows using "exampleGenerator.py". Run this script from your favorite Python editor 
or in PowerShell using "python exampleGenerator.py". Answer the three questions in the terminal. This will generate a
file called randomLineup.txt that can be used as input for main.py_

To run the script:
1) In main.py, adjust the required variables to suit your needs
   1) In line 13, adjust inputFile to indicate which file contains the show list 
   2) Set the flags verboseOutput and imageOutput (line 16 and 17) to True or False depending on what kind of output you wish
2) Run the script (e.g. using your favorite editor or use "python main.py" in PowerShell)
3) Appreciate the output
   1) If verboseOutput was True, the output is given in the terminal in the form of a table separated by tabs. 
The top row indicates the festival hours, the following rows indicate which show (in the form of line number) are at which stage
   2) If imageOutput was True, "planningProgram.png" will be generated with a column per stage

## Development environment
Project developed with PyCharm 2024.2 and Python 3.12.5