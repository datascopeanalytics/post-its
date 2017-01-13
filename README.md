# post-its
Some super duper scripts that process the proprietary Post-it file format into
images that we use in our post-workshop reports. 

# Pre-reqs
1. A board on the Post-it Plus iOS app that you want to prettify.
2. A non-zero amount of patience for navigating the UI of the Post-it Plus app

# Get the archive file from iPad to local machine
1. Open the Post-it Plus app and navigate to the board that you want to export.
2. If you want to make your life easier, you may want to name the groups on the
board something more useful than `Group A`. Your choice.
3. While viewing the board, tap the top-right area of the screen (just under the
iPad battery indicator). It's an invisible menu-option! Sneaky. Once you've
found it, choose the option to `Export Board`.
4. This repo is optimized to `3CSB` export format. Choose that one.
5. The iPad gives you many options. Easiest might be to just email the export to
yourself. Feel free to explore other options at your own peril.

# OK, you have the file locally. Now what?
1. Create a folder, perhaps called `my_postit_board`.
2. Unzip `my_postit_board.3csb` (yup, it's just a zip file) into `my_postit_board`.
3. Run `python grid.py my_postit_board` from the root of this repo. This script
will create .png files that map to each of the group names.

# De-dupeer-5000
1. Ask Mike? Let's fill in details on this at some point.
