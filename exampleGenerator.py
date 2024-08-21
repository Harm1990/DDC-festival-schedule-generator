# Command line script to generate random lineup

# Input - script will ask for the following input:
## Amount of shows: int
## Duration of festival: int
## Typical length of show: int

# Output
## File with the name "randomLineup.txt"

import random

# Variables
outputFile = "randomLineup.txt"

### Part 1 - collect input
shows = input("How many shows are there? (1-999)")
if not shows.isdigit() or (int(shows) < 1) or (int(shows) > 999):
    print("Step 1: Unable to parse amount of shows, please run script again")
    exit(1)
shows = int(shows) # Convert to int

duration = input("How many hours does the festival take? (1-999)")
if not duration.isdigit() or (int(duration) < 1) or (int(duration) > 999):
    print("Step 2: Unable to parse duration, please run script again")
    exit(2)
duration = int(duration) # Convert to int

meanDurationShow = input("How many hours is the typical show (used as mean in normal dist)? (1-10)")
if not meanDurationShow.isdigit() or (int(meanDurationShow) < 1) or (int(meanDurationShow) > 10):
    print("Step 3: Unable to parse mean show duration, please run script again")
    exit(3)
meanDurationShow = int(meanDurationShow) # Convert to int

### Part 2 - generate show list and output it to file
print("Will generate show list with %d shows for %d hours with typical duration of %d hours" %(shows, duration, meanDurationShow))

with open(outputFile, 'w', encoding="utf-8") as f:
    for showNumber in range(shows):
        showName = "show_" + str(showNumber + 1)
        showStart = random.randrange(0,duration)
        showDuration = int(random.normalvariate(meanDurationShow,2))
        if showDuration < 1:
            showDuration = 1
        elif (showDuration + showStart) > duration:
            showDuration = duration - showStart
        print("%s %s %s" %(showName, showStart, showStart + showDuration))
        f.write("%s %s %s \n" %(showName, showStart, showStart + showDuration))

print("Output is saved to %s" % outputFile)