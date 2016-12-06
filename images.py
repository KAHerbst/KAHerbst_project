import sys
import csv
import pandas as pd
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

def file_formatter(poverty_file, boundary_file):
    '''formats my poverty file to be in the same format as my boundary file, so they can read and mapped in unison'''
    f=pd.read_csv(poverty_file)
    keep_col = ['State / County Name' , 'All Ages in Poverty Percent']
    new_f = f[keep_col]
    new_f.to_csv('poverty_trimmed_initial.csv', index=False)
    with open('poverty_trimmed.csv', 'w') as fout:
        writer = csv.writer(fout)
        with open('poverty_trimmed_initial.csv', 'r') as fin:
            reader = csv.reader(fin)
            for rownum, entry in enumerate(reader):
                if rownum<1:continue
                writer.writerow(entry)
    poverty_dict = {}
    with open('poverty_trimmed.csv','r') as trim:
        trim_read = csv.reader(trim)
        for row in trim_read:
            lst = row[0].split()
            poverty_dict[lst[0]] = row
    with open('boundaries.csv', 'r') as bounds:
        boundaries = csv.reader(bounds)
        with open('poverty_formatted.csv', 'w') as pov_final:
            writer = csv.writer(pov_final)
            for row in boundaries:
                if row[0] not in poverty_dict:
                    poverty_dict[row[0]] = [row[0], '14.5']
                writer.writerow(poverty_dict[row[0]])



def main(poverty, boundaries, output, width, style,year):
    """
    Draws an image.
    This function creates an image object, constructs Region objects by reading
    in data from csv files, and draws polygons on the image based on those Regions

    Args:
        results (str): name of a csv file of poverty rates`
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
    region_plot.save('output_{}.png'.format(year))

def subplots(filename,year_cap):
    '''Creates two subplots graphing US overall poverty percentage and SNAP enrollment and saves them to a specified filename'''
    pov_lst = [11.3, 11.7, 12.1, 12.5, 12.7, 13.3, 13.3, 13.0, 13.2, 14.3, 15.3, 15.9, 15.9, 15.8, 15.5]
    SNAP_lst = [17.194000, 17.318000, 19.096000, 21.250000, 23.811000, 25.628000, 26.549000, 26.316000, 28.223000, 33.490000, 40.302000, 44.709000, 46.609000, 47.636000, 46.664000]
    pov_lst = pov_lst[:int(year_cap)-1999]
    SNAP_lst = SNAP_lst[:int(year_cap)-1999]
    years = [x for x in range(int(year_cap)-1999)]
    plt1 = plt.subplot2grid((2,6),(0,1), colspan = 5, rowspan = 1)
    plt1.axis([-1,15,0,20])
    plt1.scatter(years,pov_lst[:int(year_cap)-1999])


    plt2 = plt.subplot2grid((2,6),(1,1), colspan = 5, rowspan = 1)
    plt2.axis([-1,15,15,50])
    plt2.scatter(years,SNAP_lst[:int(year_cap)-1999])

    plt2.set_xlabel('Year (2000\'s)')
    plt1.set_ylabel('Poverty Percentage')
    plt2.set_ylabel('SNAP Enrollment (In Millions)')
    plt.tight_layout()
    plt.savefig(filename)

def stitch(pov_map, plots,year_cap):
    """Merges my plots and map into one image
    """
    map_img= Image.open(pov_map)
    plot_img= Image.open(plots)
    (width1, height1) = map_img.size
    (width2, height2) = plot_img.size
    result_width = width1 + width2
    result_height = max(height1, height2)
    result = Image.new('RGB', (result_width, result_height), 'white')
    result.paste(im=map_img, box=(0, 0))
    result.paste(im=plot_img, box=(width1, 0))
    result.save('stitches_{}.png'.format(year_cap))


if __name__ == '__main__':
    poverty_file = sys.argv[1]
    boundary_file = sys.argv[2]
    poverty_formatted= sys.argv[3]
    boundaries_formatted = sys.argv[4]
    output = sys.argv[5]
    width = int(sys.argv[6])
    style = sys.argv[7]
    year_cap = sys.argv[8]
    file_formatter(poverty_file, boundary_file)
    main(poverty_formatted, boundaries_formatted, output, width, style, year_cap)
    subplots('plots_{}.png'.format(year_cap),year_cap)
    stitch('output_{}.png'.format(year_cap),'plots_{}.png'.format(year_cap),year_cap)

# To run
# python poverty.py poverty_data.csv boundaries.csv poverty_formatted.csv boundaries_trimmed.csv output.png 1024 GRAD year_cap
