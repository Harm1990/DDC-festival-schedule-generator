# Script to generate festival-schedule from input
from logging import raiseExceptions
from multiprocessing.managers import Value

# Reads the input from a predefined file in the form of
# show_name hour_start hour_stop [space separated]
# and tries to put these shows onto different stages as efficiently as possible
# Output is either a list of shows per stage with their starting time or a tabular overview depending on which output flags are set (verboseOutput and imageOutput)

# The sorting idea is to loop across the available stages and plan the act on the stage where the previous act is most adjacent

# Variables
# Input is fixed for now
inputFile = "randomLineup.txt"

# Output
verboseOutput = True
imageOutput = False

# Function Variables
# Create class for shows
class Show:
    def __init__(self, name, start, stop):
        self.name = name
        self.start = int(start)
        self.stop = int(stop)

# Use check occupation to see where show might fit and plan show at closest existing fit
def planShow(localStagePlan, showNumber, showStart, showStop):
    showDuration = showStop - showStart
    # If stagePlan is too short, increase length of stagePlan
    if showStop > len(localStagePlan[0]):
        for stage in localStagePlan:
            targetExtension = showStop - len(stage)
            stage += [0] * targetExtension

    # Now check if stage is occupied and if not, check closest show
    stageClearance = []
    for stage in localStagePlan:
        if sum(stage[showStart:showStop]) == 0:
            # No occupation, check for closest
            ii = showStart
            while stage[ii] == 0 and ii > 0:
                ii -= 1 # Descend into list
            stageClearance.append(showStart - ii)
        else:
            stageClearance.append(0)

    # If no stages available, create new stage
    if sum(stageClearance) == 0:
        localStagePlan.append([0] * len(localStagePlan[0])) # Create new stage
        localStagePlan[-1][showStart:showStop] = [showNumber] * showDuration # Plan stage
    else:
        # Plan the show in the non-occupied, stage with least clearance
        local_minimum = max(stageClearance)
        best_stage = -1
        for ii, clearance in enumerate(stageClearance):
            if clearance != 0 and clearance < local_minimum:
                local_minimum = clearance
                best_stage = ii
        localStagePlan[best_stage][showStart:showStop] = [showNumber] * showDuration  # Plan stage

    return localStagePlan


def main():
    # Create list that contains all found shows in input file
    # Ensure that number 0 is not linked to a show, to allow 0 to indicate no show is given on that stage, see Stage.occupationHours
    listShows = [Show('noShow', 0, 0)]

    # Initial idea was to also use a Stage Class, but since all Stages should have the same event length,
    # decided to go for a nested loop
    stagePlan = [[0]]  # Start with only 1 hour, nothing planned


    # Read all shows into list
    with open(inputFile, 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                name, start, stop = line.split()
                if int(start) > int(stop):
                    raise ValueError
                listShows.append(Show(name,start,stop))
            except ValueError:
                print("Error reading line: %s" % line.replace("\r\n", "").replace("\n", ""))
                print("Skipped over line and continued")

    # For every show, plan show in Stage plan
    for showInt, show in enumerate(listShows):
        if showInt != 0: # Skip show 0
            print(showInt)
            stagePlan = planShow(stagePlan,showInt,show.start,show.stop)

    for stage in stagePlan:
        print(stage)





if __name__ == "__main__":
    main()