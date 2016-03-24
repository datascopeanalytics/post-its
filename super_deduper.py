"""Creates an HTML file that can be used to deduplicate post-it notes.

"""
import collections
import os
import sys

from PIL import Image
import imagehash


HASH_SIZE = 6


def hexdistance(one, two):
    total = 0
    for a, b in zip(one, two):
        if int(a, 16) != int(b, 16):
            total += 1
        # total += abs(int(a, 16) - int(b, 16))
    return total


def most_frequent_color(image):

    width, height = image.size
    pixels = image.getcolors(width * height)

    pixels.sort(reverse=True)

    r, g, b = (int(i / (16.0 * 8)) * 8 for i in pixels[0][1])
    result = '%01x%01x%01x' % (r, g, b)
    return result

directory = sys.argv[1]

# group full file paths by board key
grouped = collections.defaultdict(list)
filename_list = [
    os.path.join(directory, filename) for filename in os.listdir(directory)
]
base_color = '000'
for path in filename_list:
    image = Image.open(path)
    color = most_frequent_color(image)
    image_hash = imagehash.dhash(image, hash_size=HASH_SIZE)
    distance = hexdistance(color, base_color)
    grouped[(distance, color, str(image_hash))].append(path)

print '<html>'
print '<head>'
print '<link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">'
print '<link rel="stylesheet" type="text/css" href="css/bunga.css">'
print '<script src="https://code.jquery.com/jquery-2.2.2.min.js"></script>'
print '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>'
print '<script src="js/clipboard.js"></script>'
print '<script src="js/json2.js"></script>'
print '<script src="js/bunga.js"></script>'
print '</head>'
print '<body>'
for (distance, color, image_hash), path_list in sorted(grouped.iteritems()):
    # print '<div class="row">'
    # print '<div class="swatch" style="background:#%s"></div>' % color
    # print '<h4 class="hash">%s %s</h4>' % (color, hash)
    for path in path_list:
        name = os.path.basename(path)
        print '<div class="col-md-1 holder">'
        print '<img class="post-it" src="%s" />' % path
        print '<div class="checkbox">'
        print '<label><input type="checkbox" value=""><span class="basename">%s</span></label>' % path
        print '</div>'
        print '</div>'
    # print '</div>'
print '</body>'
print '</html>'
