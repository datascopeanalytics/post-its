"""Takes as input the `notes` directory of the zipfile export from the
Post-it Plus app, and creates one picture per group with the images in
a nice grid.

"""
import collections
import os
import sys
import math

from slugify import slugify
from PIL import Image
import imagehash
import ssim

def make_filename(key, extension):
    """Make a friendly filename for the image using the group key."""
    key = unicode(key.strip())
    return '{}.{}'.format(slugify(key), extension)

# parameters
X = 7
SIZE = 150
PAD = 5
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

def hashmaster(image):
    color = most_frequent_color(image)
    image_hash = imagehash.dhash(image, hash_size=HASH_SIZE)
    return color

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
print '<link rel="stylesheet" type="text/css" href="bunga.css">'
print '<script src="https://code.jquery.com/jquery-2.2.2.min.js"></script>'
print '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>'
print '<script src="bunga.js"></script>'
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
raise 'TOP'

for h, dupes in sorted(grouped.items()):
    if len(dupes) > 1:
        print '<div class="row">'
        for i in dupes:
            print '<img src="%s" />' % i
        # print str(h), 'open', ' '.join('"%s"' % i for i in dupes)
        print '</div>'
    else:
        pass

raise 'STOP'
    
grouped_by_board = collections.defaultdict(list)
for filename in os.listdir(directory):
    path = os.path.join(directory, filename)
    key = filename.split('[')[1].split(']')[0]
    grouped_by_board[key].append(path)
    
for key, filename_list in grouped_by_board.iteritems():

    # make new filename from key
    new_filename = make_filename(key, 'png')
    print >> sys.stderr, 'generating %s...' % new_filename

    # calculate image sizes
    n_images = len(filename_list)
    rows = ((n_images - 1) / X) + 1
    new_width = X * SIZE + (X - 1) * PAD
    new_height = rows * SIZE + (rows - 1) * PAD

    # make a new image big enough to hold the grid
    new_image = Image.new(
        'RGB',
        (new_width, new_height),
        color=(255, 255, 255),
    )

    for image_index, filename in enumerate(filename_list):

        # open image
        image = Image.open(filename)
        import ipdb
        ipdb.set_trace()
        
        # resize to square of SIZE x SIZE
        resized = image.resize((SIZE, SIZE), Image.BICUBIC)

        # place in the right grid position on new image
        x_index = image_index % X
        y_index = image_index / X
        size = SIZE + PAD
        new_image.paste(resized, (x_index * size, y_index * size))

    new_image.save(new_filename, 'PNG')
