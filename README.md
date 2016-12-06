# Final Project Proposal
For my CSCI 135 final project I would like to do something similar to our earlier Purple America Lab. However, I would like to map census data detailing percentage of population in poverty in specific counties (And use a color gradeint to indicate this like in Purple America). I want to create separate images for all the years from 2000-2014 and use them each as a frame in a gif. I think this project is interesting because it allows me to easily visualize poverty rate in the US over time and helps to put into perspective where certain areas are worsening or getting better over time. I am really intersted in Economics and especially social welfare and this will be a gnarly project to not only feel empowered by computer science but to do something I think will have lasting value.

## Data Plan
My sources of data are as follows, I will pull all my county level poverty data and national poverty data in csv files from census.gov. I will pull all my SNAP enrollment from fns.gov and use each point at each year to map points onto each "frame" of my gif.
The formatting of the map for my county poverty data is trickier than the Purple America lab, I will use each county's ID to determine its coordinate value (for mapping) and then map all points to my map.

## Implementation Plan
I am starting from semi-existing code, I will use a similar structure to the Purple America lab, but also like the gif lab that Bill linked me when we spoke about the project (from an earlier version of the class). I will most likely use recursion to build up my gifs from previous 'frames', object oriented programming similar to Purple America and imaging (similar to Purple America.

### External Libraries
- sys
- csv
- pandas
- math
- matplotlib
- PIL

### Milestones
- file formatting
- mapping pov_pct to corresponding regions
- SNAP/overall poverty plot making
- stitching map and plots together
- figuring out how to run it
- gif creation


## Deliverables
- 15 maps of the US with color gradient depending on pov_pct there
- 15 subplots marking the progression of SNAP enrollment and pov_pct in the US
- 1 gif with all corresponding images stiched

# Final Project Report
*What you have achieved/learned*
I have really learned quite a bit of debugging techniques and patience for bugs. Further I have gotten a better grasp on objects and their use as well as formatting data uniformly.
*What open questions remain*
N/A
## Instructions to run the code (From the Terminal)
To run the code it is pretty simple

1) activate and enter your virtual environment (pyvenv venv, .venv/bin/activate)
2) clone my repo
3) ls into my repo (KAHerbst-project)
4) pip install all required modules
4) go to the terminal and paste (python images.py 1024 GRAD 2014)
5) wait for what seems like an eternity
6) go back to the terminal and paste(convert -delay 60 -loop 0 stitches_*.png US_poverty.gif
7) wait again
8) paste (open -a safari US_poverty.gif) to see the gif!

