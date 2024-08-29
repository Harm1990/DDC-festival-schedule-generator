# File to generate image with stage planning
import matplotlib.pyplot as plt
# Input
# Stage plan with act names

# Output
# Image with filename festivalPlanning.png

outputFile = "festivalPlanning.png"


def generate_stage_overview(local_stage_plan,list_acts,plot_title,savefile=True):
    ## First generate rectangle with info of each show
    # Data for rectangles (x, y, width, height, and label)
    rectangles = []
    # Iterate over stage plan to deduct which show is where and how long
    for stage_number, stage_hour_plan in enumerate(local_stage_plan):
        # Initialize parameters
        active_act = stage_hour_plan[0]
        length = 0
        starting_hour = 0
        # Iterate over this stage to check if current act is still playing
        for hour, current_act in enumerate(stage_hour_plan):
            if active_act == current_act: # Current act is still active
                length += 1
            else: # Act is no longer playing
                # Create rectangle based on previous act
                if current_act != active_act and active_act != 0:
                    # Create rectangle at x,y coordinates with 1 width and height according to playing length
                    rectangles.append((stage_number + 0.5,starting_hour,1,length,list_acts[active_act]))
                # Prepare new set of parameters
                active_act = current_act
                starting_hour = hour
                length = 1
        # Append the latest act of this stage only if it was not "no act" aka 0
        if active_act != 0:
            rectangles.append((stage_number + 0.5, starting_hour, 1, length, list_acts[active_act]))

    ## Next plot those rectangles
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(16, 10))

    # Plot each rectangle with a label
    for x, y, width, height, label in rectangles:
        # Create a rectangle
        rect = plt.Rectangle((x, y), width, height, fill=True, edgecolor='black', facecolor='lightblue',zorder=3)
        # Add rectangle to the plot
        ax.add_patch(rect)
        # Place the label inside the rectangle (centered)
        plt.text(x + width / 2, y + height / 2, label, ha='center', va='center', fontsize=10, zorder=4)

    # Set the limits of the plot and add text
    ax.set_xlim(0.4, len(local_stage_plan)+0.6)
    ax.set_xlabel("Stage number")
    ax.set_ylim(-0.1, len(local_stage_plan[0])+0.1)
    ax.set_ylabel("Festival Hours")
    # Invert the Y-axis such that 0 is at the top
    ax.invert_yaxis()

    # Ensure all stages get a number by setting correct ticks
    ax.set_xticks(range(1, len(local_stage_plan)+1) )
    ax.set_yticks(range(0, len(local_stage_plan[0])+1) )

    # Add grid lines to make it more visually attractive
    ax.grid(True, which='both', axis='y', linestyle='--', color='gray', zorder=1)

    # Display the plot title
    plt.title(plot_title)

    # Save the plot to a PNG file
    if savefile:
        plt.savefig(outputFile, dpi=300, bbox_inches='tight')
        plt.close()
        return outputFile
    else:
        plt.show()
        return None



if __name__ == "__main__":
    # If running as main, use debug inputs
    # Create dummy inputs
    stage_plan = [[5, 5, 5, 0, 0, 2, 2, 1, 1, 1, 1], [0, 0, 7, 7, 3, 3, 3, 3, 3, 3, 0],
                  [0, 13, 13, 4, 4, 4, 4, 0, 12, 12, 12], [0, 15, 15, 0, 6, 6, 6, 0, 0, 0, 0],
                  [0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 9, 9, 10, 10, 10, 10, 10],
                  [0, 0, 0, 0, 0, 11, 11, 0, 0, 0, 0], [0, 0, 0, 14, 14, 14, 0, 0, 0, 0, 0]]
    act_names = [None, 'show_1', 'show_2', 'show_3', 'show_4', 'show_5', 'show_6', 'show_7', 'show_8', 'show_9', 'show_10', 'show_11', 'show_12', 'show_13', 'show_14', 'show_15']
    # Run function to test output
    generate_stage_overview(stage_plan,act_names,"TestOutput",savefile=False)
