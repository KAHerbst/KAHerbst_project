from PIL import Image, ImageDraw
from PIL.ImageColor import getrgb


class Plot:
    """
    Provides the ability to map, draw and color regions in a long/lat
    bounding box onto a proportionally scaled image.
    """
    @staticmethod
    def interpolate(x_1, x_2, x_3, newlength):
        """
        linearly interpolates x_2 <= x_1 <= x_3 into newlength
        x_2 and x_3 define a line segment, and x2 falls somewhere between them
        scale the width of the line segment to newlength, and return where
        x_1 falls on the scaled line.
        """
        return ((x_1 - x_2)/(x_3 - x_2))*(newlength)

    @staticmethod
    def proportional_height(new_width, width, height):
        """
        return a height for new_width that is
        proportional to height with respect to width
        Yields:
            int: a new height
        """
        return int((height/width)*new_width)


    @staticmethod
    def gradient(region):
        """
        a gradient color based on the poverty rate for a given region
        Args:
            region (Region): a region object
        Yields:
            (int, int, int): a triple with a gradient purple fill from a color picker
        """
        return (int(region.poverty_rate()*79),int(region.poverty_rate()*79),int(region.poverty_rate()*79))

    @staticmethod
    def fill(region):
        """Fills a given region with the poverty rate color gradient"""
        return Plot.gradient(region)

    def __init__(self, width, min_long, min_lat, max_long, max_lat):
        """
        Create a width x height image where height is proportional to width
        with respect to the long/lat coordinates.
        """
        self.min_long = min_long
        self.min_lat = min_lat
        self.max_long = max_long
        self.max_lat = max_lat
        self.height = Plot.proportional_height(width, max_long - min_long, max_lat - min_lat)
        self.width = width
        self.Image = Image.new("RGB",(width, self.height),(255,255,255))

    def save(self, filename):
        """save the current image to 'filename'"""
        self.Image.save(filename,"PNG")

    def draw(self, region):
        """
        Draws 'region' with color gradient at the correct position on the
        current image
        Args:
            region (Region): a Region object with a set of coordinates
        """
        def trans_longs():
            return[int(Plot.interpolate(lon,self.min_long, self.max_long, self.width)) for lon in region.longs()]

        def trans_lats():
            return[self.height - int(Plot.interpolate(lat, self.min_lat,self.max_lat,self.height)) for lat in region.lats()]

        coords = [(x,y) for x,y in zip(trans_longs(),trans_lats())]
        for lo,la in coords:
            if lo<0 or lo>self.max_long:
                print("BAD COORD")
            elif la<0 or la>self.max_lat:
                print("BAD COORD")

        ImageDraw.Draw(self.Image).polygon(coords,Plot.fill(region), outline = None)

