# Script to generate festival-schedule from list of shows

# Reads the input from a predefined file in the form of
# show_name hour_start hour_stop [space separated]
# and tries to put these shows onto different stages as efficiently as possible
# Output is either a list of shows per stage with their allocation or a tabular overview depending
# on which output flags are set (verboseOutput and imageOutput)

# The sorting idea is to loop across the available stages and plan the act on the stage where the previous act is most adjacent

# Variables
# Input is fixed for now
inputFile = "randomLineup.txt"

# Output
verboseOutput = True
imageOutput = True

# Function Variables
# Create class for shows
class Show:
    def __init__(self, name, start, stop, line_number):
        self.name = name
        self.start = int(start) # Starting hour
        self.stop = int(stop) # Stopping hour (excluding), e.g. if stop = 10, it stops at 9:59
        self.line_number = int(line_number)

# Use check occupation to see where show might fit and plan show at closest existing fit
def plan_show(local_stage_plan, show_number, show_start, show_stop):
    show_duration = show_stop - show_start
    # If stagePlan is too short, increase length of stagePlan
    if show_stop > len(local_stage_plan[0]):
        additional_show_length = show_stop - len(local_stage_plan[0])
        for stage in local_stage_plan:
            stage += [0] * additional_show_length

    # Now check if stage is occupied and if not, check closest show
    stage_clearance = []
    for stage in local_stage_plan:
        if sum(stage[show_start:show_stop]) == 0:
            # No occupation, check for closest
            ii = show_start
            while stage[ii] == 0 and ii > 0:
                ii -= 1 # Descend into list
            stage_clearance.append(show_start - ii)
        else:
            stage_clearance.append(-1) # Indicate no clearance

    # If no stages available, create new stage
    if sum(stage_clearance) == (-1 * len(stage_clearance)):
        local_stage_plan.append([0] * len(local_stage_plan[0])) # Create new stage
        local_stage_plan[-1][show_start:show_stop] = [show_number] * show_duration # Plan stage
    else:
        # Plan the show in the non-occupied, stage with the least clearance
        local_minimum = max(stage_clearance)+1
        best_stage = 0 # By default, use first stage in case all are equal
        for ii, clearance in enumerate(stage_clearance):
            if -1 < clearance < local_minimum:
                local_minimum = clearance
                best_stage = ii
        local_stage_plan[best_stage][show_start:show_stop] = [show_number] * show_duration  # Plan stage

    return local_stage_plan


def main():
    # Create list that contains all found shows in input file
    # Ensure that number 0 is not linked to a show, to allow 0 to indicate no show is given on that stage, see Stage.occupationHours
    list_shows = [Show('noShow', 0, 0, 0)]

    # Initial idea was to also use a Stage Class, but since all Stages should have the same event length,
    # decided to go for a nested loop
    stage_plan = [[0]]  # Start with only 1 hour, nothing planned


    # Read all shows into list
    with open(inputFile, 'r') as f:
        lines = f.readlines()
        for line_number, line in enumerate(lines, start=1):
            try:
                name, start, stop = line.split() # Extract values from line
                if int(start) > int(stop):
                    raise ValueError
                # The description indicates the stop is included, whilst the script is based on stop being excluded
                stop = int(stop) + 1
                list_shows.append(Show(name,start,stop,line_number))
            except ValueError:
                print("Error reading line %i: %s" %(line_number,line.replace("\r\n", "").replace("\n", "")) )
                print("Line is excluded, but script will process rest of file")

    # For every show, plan show into Stage plan
    for show in list_shows:
        if show.line_number != 0: # Skip show 0
            stage_plan = plan_show(stage_plan,show.line_number,show.start,show.stop)

    # Now create output
    if verboseOutput:
        if list_shows[-1].line_number > 99:
            # Do not use separating '|', since it screws up formatting
            print("Hours: \t\t" + "\t".join(map(str, range(len(stage_plan[0])))))
            for stageInt, stage in enumerate(stage_plan):
                print("Stage %i: \t" % (stageInt+1) + "\t".join(map(str, stage)))
        else:
            print("Hours: \t\t" + "\t|".join(map(str, range(len(stage_plan[0])))))
            for stageInt, stage in enumerate(stage_plan):
                print("Stage %i: \t" % (stageInt+1) + "\t|".join(map(str, stage)))

    if imageOutput:
        # Move to exterior function
        pass



if __name__ == "__main__":
    main()