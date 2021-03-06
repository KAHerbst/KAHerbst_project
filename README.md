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
- ImageMagick command line tools

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
I have really learned quite a bit of debugging techniques and patience for bugs. Further I have gotten a better grasp on objects and their use as well as formatting data uniformly. As for my original plans, they fell quite short, but I was able to use the skeleton of the Purple America lab and a similar mapping technique to achieve my gif in the end. I mainly learned that I might have a plan, but there is no real way to see if it will wokr until I try it. This time my original plan failed and I had to take an alternative route, but it all worked out in the end.
*What open questions remain*
I was not able to do it for Hawaii and Alaska so I am still curious as to how they changed. Also, I still have no idea how to use VEGA and I would definitely like to figure that out eventually (it would've made this project much easier if I could only figure out how).
## Instructions to run the code (From the Terminal)
To run the code it is pretty simple

1) activate and enter your virtual environment (pyvenv venv, .venv/bin/activate)
2) clone my repo
3) ls into my repo (KAHerbst-project)
4) pip install all required modules
4) choose a color from the following 'TURQUOISE', 'PURPLE', 'YELLOW' and 'GRAY'
5) Go to the terminal and type 'python images.py 1024 COLOR 2014' substitutiing your chosen color for COLOR
5) wait for what seems like an eternity
6) go back to the terminal and paste(convert -delay 50 -loop 0 stitches_*.png US_poverty.gif)
7) wait again
8) paste (open -a safari US_poverty.gif) to see the gif!

(You can also pick a year and just do a gif for the year up to that year)

# Feedback
- **Functionality**: 10/10
 * Your description to run the code wasn't well formatted (github markdown is fairly intuitive and extremely well documented), but it had clear descriptions of the exact commands to type to run your code.
- **Challenge and Endurance**: 10/10
 * There were moments when you struggled, which is completely normal, but I was impressed with your perserverence.
 * Stitching together multiple data sources with different formats is a challenge, and your dictionary approach was a good one.
 * You also figured out how to make a .gif using outside documentation from non-Python sources, which is great.
- **Code Quality**: 8/10
 * This is the one area where I think you could have improved. You had several places with hard-coded strings, filenames, and integers. The power of functions is your ability to use parameters to really customize their behaviors. If you want to use hard-coded values to completely control your output, there are two reasonable approaces:
  1. Use variable constants, or
  2. Hard code the values *outside* the functions (perhaps in `__main__` or in a specialized `generate_specific_graph()` function), and pass the hard-coded values as parameters. That way you can reuse the function for arbitrary values while still having tight control over a particular set of outputs.
- **Final Product**: 10/10
 * In general, your visualization shows a lot of data in a compact and interesting way. I was excited by what you produced, your explanation, and your insights.
 * Your map could have used a legend, but your image stitching and plots were excellent.

