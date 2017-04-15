# opencv-Image-Segmentation
OpenCV - Image Segmentation using grabcut algorithm and edge detection using canny algorithm

This code is refactored to include OOP principles in python. The concepts of encapsulation, data abstraction and modularity have been implemented.

There are two classes in the code, namely, Image and GUI. The Image class deals with all functions related to image processing. The GUI class deals with the windows and user interaction using the mouse. The objects of the above two classes have been declared in the main function and all the other functions are accessed through these objects.

The repository contains the following:
1) run.py - the code to be run
2) Sample input files (from the Berkeley dataset)
3) Two sample output files
4) grabcut.py - the original implementation of the GrabCut algorithm
5) edge.py - the origincal implementation of the Canny edge detection algorithm

The main code snippet has been taken from the OpenCV 3.2.0 documentation. The link is as follows:
http://docs.opencv.org/3.2.0/d8/d83/tutorial_py_grabcut.html

This code is compatible with Python 2 and Python 3.
Written according to PEP8 Guidelines.
Written and modified by: Shruti Singala, CSE, NITK


Interactive Image Segmentation and conversion to black and white image so that it looks similar to a whiteboard image.

This program uses the GrabCut image segmentation algorithm and the Canny edge detection algorithm.

USAGE:
python run.py <filename>

README FIRST:
Two windows will show up, one for input and one for grabcut output. After pressing 's', two more windows show up, one with edged output and another one for inverted edged output.

At first, in the input window, draw a rectangle around the object or the entire image using right mouse button. Then press 'n' to segment the object (once or a few times). For any finer touch-ups, you can press any of the keys below and draw lines on the areas you want. The foreground lines will be white in color and the background lines in black. Then press 'n' again for updating the output. Once the segmentation of the image is done, press 's' to display the whiteboard version of the image and to save the file.

Key '0'   - To select areas of sure background
Key '1'   - To select areas of sure foreground
Key 'n'   - To update the segmentation
Key 's'   - To display and save the results
Key 'esc' - To exit

p.s. Some of the above attached images are from the Berkeley Segmentation Dataset and Benchmark.

To test the code with other images from this set, please visit: 
http://docs.opencv.org/3.0-beta/modules/datasets/doc/datasets/is_bsds.html
