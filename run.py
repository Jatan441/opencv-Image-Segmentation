# The main code snippet has been taken from the OpenCV 3.2.0
# documentation. The link is as follows:
# http://docs.opencv.org/3.2.0/d8/d83/tutorial_py_grabcut.html
#
# This code is compatible with Python 2 and Python 3.
# Written according to PEP8 Guidelines.
# Written and modified by: Shruti Singala, CSE, NITK
'''
=======================================================================
Interactive Image Segmentation and conversion to black and white image
so that it looks similar to a whiteboard image.

This program uses the GrabCut image segmentation algorithm and the
Canny edge detection algorithm.

USAGE:
    python run.py <filename>

README FIRST:
    Two windows will show up, one for input and one for output.

    At first, in the input window, draw a rectangle around the object
or the entire image using right mouse button. Then press 'n' to segment
the object (once or a few times). For any finer touch-ups, you can
press any of the keys below and draw lines on the areas you want. The
foreground lines will be white in color and the background lines in
black. Then press 'n' again for updating the output.

    Once the segmentation of the image is done, press 's' to display
the whiteboard version of the image and to save the file.

Key '0'   - To select areas of sure background
Key '1'   - To select areas of sure foreground
Key 'n'   - To update the segmentation
Key 's'   - To display and save the results
Key 'esc' - To exit
=======================================================================
'''


from __future__ import print_function

import numpy as np
import cv2
import sys

# This class deals with all functions related to image processing.


class Image(object):

    def __init__(self, filename):
        # Initialises all the attributes of the object.
        self.filename = filename
        self.img = cv2.imread(filename)
        self.temp_img = None
        self.mask = None
        self.temp_mask = None
        self.output = None
        # Setting up flags
        self.rect = (0, 0, 1, 1)     # Flag for drawing rectangle
        self.drawing = False         # Flag for drawing curves
        self.rect_or_mask = 100      # Flag for selecting rect or mask mode

    def is_valid_image(self):
        # Validates if file exists or not.
        while cv2.imread(self.filename) is None:
            print('\nFile does not exist!\nEnter Valid filename: ')
            self.filename = raw_input()
        # if file exists, initialises remaining attributes.
        self.img = cv2.imread(self.filename)
        self.temp_img = self.img.copy()
        self.mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
        self.temp_mask = self.mask.copy()
        self.output = np.zeros(self.img.shape, np.uint8)

    def invert_image(self, edged_output):
        # Inverts the given image and returns it.
        inverted_edged_output = (255 - edged_output)
        return inverted_edged_output

    def update_image(self):
        # Updates temp_mask and output
        self.temp_mask = np.where(
            (self.mask == 1) + (self.mask == 3), 255, 0).astype('uint8')
        self.output = cv2.bitwise_and(
            self.temp_img, self.temp_img, mask=self.temp_mask)

    def segment_image(self):
        '''
        This function segments the image using the GrabCut algorithm.
        It selects rect or mask mode and applies the algorithm.
        '''
        bgdmodel = np.zeros((1, 65), np.float64)
        fgdmodel = np.zeros((1, 65), np.float64)

        # grabcut with rect mode
        if (self.rect_or_mask == 0):
            cv2.grabCut(self.temp_img, self.mask, self.rect, bgdmodel,
                        fgdmodel, 1, cv2.GC_INIT_WITH_RECT)
            self.rect_or_mask = 1

        # grabcut with mask mode
        elif self.rect_or_mask == 1:
            cv2.grabCut(self.temp_img, self.mask, self.rect, bgdmodel,
                        fgdmodel, 1, cv2.GC_INIT_WITH_MASK)

    def display_image(self):
        '''
        This function converts the segmented image to edged image.
        It further inverts the edged image.
        It displays the edged and whiteboard outputs.
        Returns:  an inverted edged output
        '''
        # converts to and shows an edge detected image
        edged_output = cv2.Canny(self.output, 10, 250)
        cv2.imshow('Edged Output', edged_output)
        # inverts the Canny output
        inverted_edged_output = self.invert_image(edged_output)
        cv2.imshow('Whiteboard', inverted_edged_output)
        return inverted_edged_output

    def save_image(self, edged_output):
        # Save the output as Whiteboard.png
        cv2.imwrite('Whiteboard.png', edged_output)


class GUI(object):
    def __init__(self, image):
        # Initialises all the attributes of the object
        self.image = image
        self.value = {'color': None, 'val': 100}  # Drawing initialized to FG
        self.thickness = 2                        # Brush thickness
        self.rect_over = False                    # Flag to check if rect drawn
        self.rectangle = False                    # Flag for drawing rect
        self.ix = 0
        self.iy = 0
        self.BLUE = [255, 0, 0]        # Rectangle color
        self.BLACK = [0, 0, 0]         # Sure BG
        self.WHITE = [255, 255, 255]   # Sure FG
        self.DRAW_BG = {
            'color': self.BLACK,
            'val': 0
        }
        self.DRAW_FG = {
            'color': self.WHITE,
            'val': 1
        }

        # Initialises the windows and mouse for GUI.
        cv2.namedWindow('Output')
        cv2.namedWindow('Input')
        cv2.setMouseCallback('Input', self.onmouse)
        cv2.moveWindow('Input', self.image.img.shape[1] + 10, 90)

    def onmouse(self, event, x, y, flags, param):
        '''
        This function takes mouse input and executes the respective functions.
        '''

        # Draw Rectangle
        #
        # When the right button is pressed
        if event == cv2.EVENT_RBUTTONDOWN:
            self.rectangle = True
            self.ix, self.iy = x, y
        # When the mouse is moved
        elif event == cv2.EVENT_MOUSEMOVE:
            # if right button is still pressed
            if self.rectangle:
                self.image.img = self.image.temp_img.copy()
                cv2.rectangle(self.image.img, (self.ix, self.iy),
                              (x, y), self.BLUE, 2)
                self.image.rect = (min(self.ix, x), min(
                    self.iy, y), abs(self.ix - x), abs(self.iy - y))
                self.image.rect_or_mask = 0
        # When the right button is NOT pressed
        elif event == cv2.EVENT_RBUTTONUP:
            self.rectangle = False
            self.rect_over = True
            cv2.rectangle(self.image.img, (self.ix, self.iy),
                          (x, y), self.BLUE, 2)
            self.image.rect = (min(self.ix, x), min(
                self.iy, y), abs(self.ix - x), abs(self.iy - y))
            self.image.rect_or_mask = 0
            print('Now press the key (n) a few times till required\n')

        # Draw touchup curves
        #
        # When the left button is pressed
        if event == cv2.EVENT_LBUTTONDOWN:
            # if rectangle is not drawn
            if not self.rect_over:
                print('First, draw rectangle \n')
            else:
                self.image.drawing = True
                self.draw_dot(x, y)
        # When the mouse is moved
        elif event == cv2.EVENT_MOUSEMOVE:
            # if left button is still pressed
            if self.image.drawing:
                self.draw_dot(x, y)
        # When the left button is NOT pressed
        elif event == cv2.EVENT_LBUTTONUP:
            # if left button is still pressed
            if self.image.drawing:
                self.image.drawing = False
                self.draw_dot(x, y)

    def draw_dot(self, x, y):
        # This function marks the points of sure FG or BG
        cv2.circle(self.image.img, (x, y), self.thickness,
                   self.value['color'], -1)
        cv2.circle(self.image.mask, (x, y),
                   self.thickness, self.value['val'], -1)

    def assign_value(self, flag):
        # This function decides whether the marked points
        # are FG or BG
        if flag == 0:
            self.value = self.DRAW_BG
        elif flag == 1:
            self.value = self.DRAW_FG


# main function

def main(argv):

    # Print documentation
    print(__doc__)

    # Load image
    if len(sys.argv) == 2:
        filename = sys.argv[1]  # for drawing purposes
    else:
        print('\nUSAGE: python run.py <filename>\n')
        exit()

    # Create an object for the class Image.
    image = Image(filename)

    # Check if image provided is valid.
    image.is_valid_image()

    # Create an object for the class GUI
    gui = GUI(image)

    print('\nInstructions: \n')
    print('Draw a rectangle around the object using right mouse button \n')

    while True:
        # Display input and output windows
        cv2.imshow('Output', image.output)
        cv2.imshow('Input', image.img)

        # Wait for a key to be pressed
        key = cv2.waitKey(1)

        # Key bindings

        # if 'esc' is pressed, exit the code
        if key == 27:
            break
        # if '0' is pressed, draw background
        elif key == ord('0'):
            print('Use left mouse button for BG \n')
            gui.assign_value(0)
        # if '1' is pressed, draw foreground
        elif key == ord('1'):
            print("Use left mouse button for FG \n")
            gui.assign_value(1)
        # if 'n' is pressed, segment the image
        elif key == ord('n'):
            print('Mark foreground and background and press (n) again\n')
            image.segment_image()
        # if 's' is pressed, display the output and save it
        elif key == ord('s'):
            inverted_edged_output = image.display_image()
            print('Result saved as image \n')
            image.save_image(inverted_edged_output)

        # update the image.tmep_mask and image.output
        image.update_image()

    # Close all windows before exiting
    cv2.destroyAllWindows()


# control starts here
if __name__ == '__main__':
    main(sys.argv)
