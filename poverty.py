import sys
import csv
import math
from region import Region
from plot import Plot

def mercator(lat):
    """project latitude 'lat' according to Mercator"""
    lat_rad = (lat * math.pi) / 180
    projection = math.log(math.tan((math.pi / 4) + (lat_rad / 2)))
    return (180 * projection) / math.pi

def main(results, boundaries, output, width):
    """
    Draws an image.
    This function creates an image object, constructs Region objects by reading
    in data from csv files, and draws polygons on the image based on those Regions

    Args:
        results (str): name of a csv file of election results
        boundaries (str): name of a csv file of geographic information
        output (str): name of a file to save the image
        width (int): width of the image
    """
    def to_point(coords):
        new_coords=[]
        for index in range(2,len(coords)):
            if index%2 == 0:
                new_coords.append((float(coords[index]),mercator(float(coords[index+1]))))
        return new_coords

    with open(boundaries, 'r') as f1, open (results, 'r') as f2:
        region_list = [Region(to_point(bounds),float(poverty_percent[10])) for bounds,poverty_percent in zip(csv.reader(f1),csv.reader(f2))]
    regionminlat = min([region.min_lat() for region in region_list])
    regionmaxlat = max([region.max_lat() for region in region_list])
    regionminlong = min([region.min_long() for region in region_list])
    regionmaxlong = max([region.max_long() for region in region_list])

    region_plot = Plot(width,regionminlong,regionminlat,regionmaxlong,regionmaxlat)
    for region in region_list:
        region_plot.draw(region)
    region_plot.save(output)


#I don't care about the style it will always be gradient

if __name__ == '__main__':
    poverty_data = sys.argv[1]
    boundaries = sys.argv[2]
    output = sys.argv[3]
    width = int(sys.argv[4])
    main(results, boundaries, output, width, style)
