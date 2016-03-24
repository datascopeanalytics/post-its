"""Takes as input the `notes` directory of the zipfile export from the
Post-it Plus app, and creates one picture per group with the images in
a nice grid.

"""
import collections
import json
import math
import os
import random
import sys

from slugify import slugify

import imagehash
import ssim
from PIL import Image

X = 7
MAX_Y = 9
SIZE = 150
PAD = 5


def make_filename(key, extension):
    """Make a friendly filename for the image using the group key."""
    key = unicode(key.strip())
    return '{}.{}'.format(slugify(key), extension)


def read_duplicates(filename):
    to_remove = set()
    with open(filename) as infile:
        duplicate_groups = json.load(infile)
    total = 0
    for group in duplicate_groups:
        total += len(group)
        for path in group[1:]:
            to_remove.add(path)
    return to_remove


def group_by_board(directory, dupes=set()):
    duplicates_removed = 0
    grouped_by_board = collections.defaultdict(list)
    grouped_counter = collections.Counter()
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if path not in dupes:
            key = filename.split('[')[1].split(']')[0]
            if grouped_counter[key]:
                key_with_counter = '%s-%i' % (key, grouped_counter[key])
            else:
                key_with_counter = '%s' % key
            grouped_by_board[key_with_counter].append(path)
            if len(grouped_by_board[key_with_counter]) >= X * MAX_Y:
                grouped_counter[key] += 1
        else:
            duplicates_removed += 1
    print >> sys.stderr, 'Removed %i duplicates' % duplicates_removed
    return sorted(grouped_by_board.items())

# `notes` directory inside of zipfile export from post-it plus
notes_directory = sys.argv[1]

# if you've used the GUI to find duplicates, this is the filename of
# the JSON output
try:
    duplicates_filename = sys.argv[2]
except IndexError:
    dupes = set()
else:
    dupes = read_duplicates(duplicates_filename)

for key, filename_list in group_by_board(notes_directory, dupes):

    # TODO: how should we order these?
    random.shuffle(filename_list)

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
