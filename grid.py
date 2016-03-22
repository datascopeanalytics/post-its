"""Takes as input the `notes` directory of the zipfile export from the
Post-it Plus app, and creates one picture per group with the images in
a nice grid.

"""
import collections
import os
import sys

from slugify import slugify
from PIL import Image


def make_filename(key, extension):
    """Make a friendly filename for the image using the group key."""
    key = unicode(key.strip())
    return '{}.{}'.format(slugify(key), extension)

# parameters
X = 7
SIZE = 150
PAD = 5

directory = sys.argv[1]

# group full file paths by board key
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

        # resize to square of SIZE x SIZE
        resized = image.resize((SIZE, SIZE), Image.BICUBIC)

        # place in the right grid position on new image
        x_index = image_index % X
        y_index = image_index / X
        size = SIZE + PAD
        new_image.paste(resized, (x_index * size, y_index * size))

    new_image.save(new_filename, 'PNG')
