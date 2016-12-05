import sys
import csv
import math
from region import Region
from plot import Plot
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def mercator(lat):
    """project latitude 'lat' according to Mercator"""
    lat_rad = (lat * math.pi) / 180
    projection = math.log(math.tan((math.pi / 4) + (lat_rad / 2)))
    return (180 * projection) / math.pi

def main(poverty, boundaries, output, width, style):
    """
    Draws an image.
    This function creates an image object, constructs Region objects by reading
    in data from csv files, and draws polygons on the image based on those Regions

    Args:
        results (str): name of a csv file of election results
        boundaries (str): name of a csv file of geographic information
        output (str): name of a file to save the image
        width (int): width of the image
        style (str): either 'GRAD' or 'SOLID'
    """
    def to_point(coords):
        new_coords=[]
        for index in range(2,len(coords)):
            if index%2 == 0:
                new_coords.append((float(coords[index]),mercator(float(coords[index+1]))))
        return new_coords

    with open(boundaries, 'r') as f1, open (poverty, 'r') as f2:
        region_list = [Region(to_point(bounds),float(pov_percent[1])) for bounds,pov_percent in zip(csv.reader(f1),csv.reader(f2))]
    regionminlat = min([region.min_lat() for region in region_list])
    regionmaxlat = max([region.max_lat() for region in region_list])
    regionminlong = min([region.min_long() for region in region_list])
    regionmaxlong = max([region.max_long() for region in region_list])


    region_plot = Plot(width,regionminlong,regionminlat,regionmaxlong,regionmaxlat)
    for region in region_list:
        region_plot.draw(region,style)
    region_plot.save(output)

def subplots(filename,year_cap):
    '''Creates two subplots graphing US overall poverty percentage and SNAP enrollment and saves them to a specified filename'''

    pov_lst = [11.3, 11.7, 12.1, 12.5, 12.7, 13.3, 13.3, 13.0, 13.2, 14.3, 15.3, 15.9, 15.9, 15.8, 15.5]

    SNAP_lst = [17.194000, 17.318000, 19.096000, 21.250000, 23.811000, 25.628000, 26.549000, 26.316000, 28.223000, 33.490000, 40.302000, 44.709000, 46.609000, 47.636000, 46.664000]
    years = [x for x in range(int(year_cap)-2000)]

    plt1 = plt.subplot2grid((2,6),(0,1), colspan = 5, rowspan = 1)
    for x in years:
        plt1.scatter(x,pov_lst[x])

    plt2 = plt.subplot2grid((2,6),(1,1), colspan = 5, rowspan = 1)
    for x in years:
        plt2.scatter(x,SNAP_lst[x])

    plt2.set_xlabel('Year')
    plt1.set_ylabel('Poverty Percentage')
    plt2.set_ylabel('SNAP Enrollment (In Millions)')
    plt.tight_layout()
    plt.savefig(filename)

def stitch(pov_map, plots):
    """Merges my plots and map into one image
    """
    image1 = Image.open(pov_map)
    image2 = Image.open(plots)

    (width1, height1) = image1.size
    (width2, height2) = image2.size

    result_width = width1 + width2
    result_height = max(height1, height2)

    result = Image.new('RGB', (result_width, result_height), 'white')
    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(width1, 0))
    result.save('stitched.png')


if __name__ == '__main__':
    poverty = sys.argv[1]
    boundaries = sys.argv[2]
    output = sys.argv[3]
    width = int(sys.argv[4])
    style = sys.argv[5]
    year_cap = sys.argv[6]
    main(poverty, boundaries, output, width, style)
    subplots('plots.png',year_cap)
    stitch('output.png','plots.png')

# To run
# python poverty.py poverty_formatted.csv boundaries_trimmed.csv output.png 1024 GRAD 2014
