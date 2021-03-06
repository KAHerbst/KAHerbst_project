import sys
import csv
import pandas as pd
import math
from region import Region
from plot import Plot
import matplotlib.pyplot as plt
from PIL import Image


def mercator(lat):
    """project latitude 'lat' according to Mercator"""
    lat_rad = (lat * math.pi) / 180
    projection = math.log(math.tan((math.pi / 4) + (lat_rad / 2)))
    return (180 * projection) / math.pi

def file_formatter(poverty_file, boundary_file,year):
    '''formats my poverty file to be in the same format as my boundary file, so they can be read and mapped in unison
    Handles the fact that the bondary file contains duplicates of counties in specific places by using a dicitionary and keys
    to duplicate these rows in my poverty file'''
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
    with open('region_data/boundaries_US', 'r') as bounds:
        boundaries = csv.reader(bounds)
        with open('poverty_formatted_{}.csv'.format(year), 'w') as pov_final:
            writer = csv.writer(pov_final)
            for row in boundaries:
                if row[0] not in poverty_dict:
                    poverty_dict[row[0]] = [row[0], '14.5']
                writer.writerow(poverty_dict[row[0]])



def main(poverty, boundaries, width, color ,year):
    """
    Draws an image.
    This function creates an image object, constructs Region objects by reading
    in data from csv files, and draws polygons on the image based on those Regions

    Args:
        results (str): name of a csv file of poverty rates`
        boundaries (str): name of a csv file of geographic information
        output (str): name of a file to save the image
        width (int): width of the image
        color (str): 'TURQUOISE', 'PURPLE', 'YELLOW' or 'GRAY' to determine the color of the regions
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
        region_plot.draw(region,color)
    region_plot.save('output_{}.png'.format(year))

def subplots(filename,color,year_cap):
    '''Creates two subplots graphing US overall poverty percentage and SNAP enrollment and saves them to a specified filename'''
    if color == "PURPLE":
        line_color = 'm'
    elif color == "TURQUOISE":
        line_color = 'c'
    elif color == "YELLOW":
        line_color = 'y'
    elif color == "GRAY":
        line_color = 'k'
    pov_lst = [11.3, 11.7, 12.1, 12.5, 12.7, 13.3, 13.3, 13.0, 13.2, 14.3, 15.3, 15.9, 15.9, 15.8, 15.5]
    SNAP_lst = [17.194000, 17.318000, 19.096000, 21.250000, 23.811000, 25.628000, 26.549000, 26.316000, 28.223000, 33.490000, 40.302000, 44.709000, 46.609000, 47.636000, 46.664000]
    pov_lst = pov_lst[:int(year_cap)-1999]
    SNAP_lst = SNAP_lst[:int(year_cap)-1999]
    years = [x for x in range(int(year_cap)-1999)]
    plt1 = plt.subplot2grid((2,6),(0,1), colspan = 5, rowspan = 1)
    plt1.axis([-1,15,0,20])
    plt1.plot(years, pov_lst[:int(year_cap)-1999], '.{}-'.format(line_color))


    plt2 = plt.subplot2grid((2,6),(1,1), colspan = 5, rowspan = 1)
    plt2.axis([-1,15,15,50])
    plt2.plot(years, SNAP_lst[:int(year_cap)-1999], '.{}-'.format(line_color))

    plt2.set_xlabel('Year (2000\'s)')
    plt1.set_ylabel('Poverty Percentage')
    plt2.set_ylabel('SNAP Enrollment (In Millions)')
    plt.tight_layout()
    plt.savefig(filename)

def stitch(pov_map, plots,year):
    """Merges my map and sub_plots into one image
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
    result.save('stitches_{}.png'.format(year))


if __name__ == '__main__':
    width = int(sys.argv[1])
    color = sys.argv[2]
    year_cap = sys.argv[3]
    for year in range(2000, int(year_cap) +1):
        file_formatter('region_data/US_Poverty_{}'.format(year), 'region_data/boundaries_US',year)
    for year in range(2000, int(year_cap) + 1):
        main("poverty_formatted_{}.csv".format(year), 'region_data/boundaries_US', width, color, year)
    for year in range(2000, int(year_cap) + 1):
        subplots('plots_{}.png'.format(year),color,year)
    for year in range(2000, int(year_cap) + 1):
        stitch('output_{}.png'.format(year),'plots_{}.png'.format(year),year)
