import sys
import numpy as np
from PIL import Image
from math import *
import math
import os
import cairo
import time
import imageio
# Requires pycairo & pkg-config
# Refer here: https://pycairo.readthedocs.io/en/latest/getting_started.html

# These functions allow for the generation of speckle images.
# Images are generated via the use of a vector graphics library pycairo.
# This allows for image transformations without the need for interpolation or resampling error consideration.
# Precision necessary when measuring accuracy of DIC algorithm to sub-pixel level.
# The x and y displacements can then be calculated precisely according to the transformation.

# Matrix transforms used for deformations
# [a1, c3, e5,
# b2, d4, f6,
# 0, 0, 1] these numbers relate to the .Matrix(1,2,3,4,5,6) variables

# x' = a1*x + c3*y + e5
# y' = d4*y + b2*x + f6

# (a1&d4):provide scale
# (c3&b2):provide shear
# (e5+f6):provide translation



# Function will generate reference image, deformed image and provide x&y translation arrays
def generate(image_size, seed, a1, b2, c3, d4, e5, f6, filename,mode):
    if mode == 'video':
        gen_ref(image_size, seed, filename, mode)
        gen_video(image_size, seed, a1, b2, c3, d4, e5, f6, filename)
        calc_translations(image_size, seed, a1, b2, c3, d4, e5, f6, filename, mode)
    elif mode == 'image':
        gen_ref(image_size, seed, filename, mode)
        gen_img(image_size, seed, a1, b2, c3, d4, e5, f6, filename)
        calc_translations(image_size, seed, a1, b2, c3, d4, e5, f6, filename, mode)
    else:
        print("Enter mode video or image")


def gen_video(image_size, seed, a1, b2, c3, d4, e5, f6, filename):
    original_dir = os.path.dirname(os.path.realpath(__file__))
    save_dir = original_dir + "/generated/video/def"

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    gif = []
    video_name = "def_" + filename + ".gif"
    os.chdir(save_dir)
    for i in range(1, 11):
        frame = gen_def(image_size, seed, a1, b2/10 * i, c3/10 * i, d4, e5/10 * i , f6/10 * i)
        gif.append(frame)
    imageio.mimsave(video_name, gif, 'GIF')
    os.chdir(original_dir)

def gen_img(image_size, seed, a1, b2, c3, d4, e5, f6, filename):
    original_dir = os.path.dirname(os.path.realpath(__file__))
    save_dir = original_dir + "/generated/image/def"

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file_name = "def_" + filename + ".bmp"
    os.chdir(save_dir)
    out = gen_def(image_size, seed, a1, b2, c3, d4, e5, f6)
    out.save(save_dir + "/" + file_name)
    os.chdir(original_dir)


# Will draw speckles using uniform random distribution, change seed for different speckle pattern
def draw_speckles(context, seed):
    # Create white background
    context.set_source_rgb(1, 1, 1)
    context.rectangle(0, 0, 1, 1)  # Rectangle(x0, y0, x1, y1)
    context.fill()

    # Change colour to black
    context.set_source_rgb(0, 0, 0)
    context.move_to(0, 0)

    size = 3000  # The number of speckles

    # To make the images the same each time (matching ref & def)
    np.random.seed(seed=seed)
    min = 0
    max = 1

    # Use a uniform random distribution
    initial_x = np.random.uniform(min, max, size)
    initial_y = np.random.uniform(min, max, size)

    for i in range(size):
        # circle (xc, yc, radius, start_angle, end_angle)
        context.arc(initial_x[i], initial_y[i], 0.01, 0, 2 * math.pi)
        context.fill()


# Calculates x and y displacements between reference image and deformed image, according to transformation matrix
def calc_translations(image_size, seed, a1, b2, c3, d4, e5, f6, filename, mode):
    # create transformation matrix
    trans_matrix = [[a1, c3], [b2, d4]]

    # original x and y coordinates
    orig_y, orig_x = np.mgrid[1:image_size + 1, 1:image_size + 1]

    # x,y pairs to be transformed
    xy_points = np.mgrid[1:image_size + 1, 1:image_size + 1].reshape((2, image_size * image_size))
    xy_points[[1, 0]] = xy_points[[0, 1]]

    # transformed x,y pairs
    new_points = np.dot(trans_matrix, xy_points)
    x, y = new_points.reshape((2, image_size, image_size))

    # add translation element of matrix
    x = np.add(x, e5).reshape((image_size, image_size))
    y = np.add(y, f6).reshape((image_size, image_size))

    # calculate the x and y displacements
    xd = (x - orig_x)
    yd = (y - orig_y)



    x_name = "x_" + filename

    y_name = "y_" + filename

    savetxt_compact(x_name, xd, mode)

    savetxt_compact(y_name, yd, mode)


# Generate reference images
def gen_ref(image_size, seed, filename, mode):
    WIDTH, HEIGHT = image_size, image_size

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    context = cairo.Context(surface)

    context.scale(WIDTH, HEIGHT)  # Normalizing the canvas

    draw_speckles(context, seed)

    context.close_path()

    img_name = "ref_" + filename + ".bmp"

    write_image(surface, image_size, img_name, mode)


# Generate deformed images
def gen_def(image_size, seed, a1, b2, c3, d4, e5, f6):
    WIDTH, HEIGHT = image_size, image_size

    format = cairo.FORMAT_ARGB32

    surface = cairo.ImageSurface(format, WIDTH, HEIGHT)
    context = cairo.Context(surface)

    # Normalizing the canvas
    context.scale(WIDTH, HEIGHT)

    # Matrix transform
    # [a1, c3, e5,
    # b2, d4, f6,
    # 0, 0, 1] these numbers relate to the .Matrix(1,2,3,4,5,6) variables

    # x' = a1*x + c3*y + e5
    # y' = d4*y + b2*x + f6

    # (a1&d4):provide scale
    # (c3&b2):provide shear
    # (e5+f6):provide translation

    mtx = cairo.Matrix(a1, b2, c3, d4, e5, f6)
    context.transform(mtx)

    draw_speckles(context, seed)

    context.close_path()

    buf = surface.get_data()
    data = np.ndarray(shape=(image_size, image_size), dtype=np.uint32, buffer=buf)
    out = Image.fromarray(data, 'RGBA')
    return out



# Writes image to /img_gen directory in format as specified by filename (currently works for .bmp)
def write_image(surface, image_size, file_name,mode):
    save_dir = os.path.dirname(os.path.realpath(__file__)) + f"/generated/{mode}/ref"

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    buf = surface.get_data()
    data = np.ndarray(shape=(image_size, image_size), dtype=np.uint32, buffer=buf)

    out = Image.fromarray(data, 'RGBA')
    out.save(save_dir + "/" + file_name)


def savetxt_compact(fname, x, mode, fmt="%.6g", delimiter=','):
    with open(f"generated/{mode}/def/def_{fname}.csv", 'w+') as fh:
        for row in x:
            line = delimiter.join("0" if value == 0 else fmt % value for value in row)
            fh.write(line + '\n')




def main():
    if (len(sys.argv) == 1):
        generate(50, 19, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 'sample', 'image')

    elif (len(sys.argv) == 11):
        try:
            generate(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7]), float(sys.argv[8]), sys.argv[9], sys.argv[10])
        except TypeError:
            print(
                "Type Error, input parameters are : int image_size, int seed, float a1, float b2, float c3, float d4, float e5, float f6, string filename, string mode. See documentation for specification of matrix elements.")


    else:
        print(
            "Requires parameters: image_size, seed, a1, b2, c3, d4, e5, f6, filename. Default generation is: 50,19,1.0,0.0,0.0,1.0,0.0,0.0,sample,image")


if __name__ == "__main__":
    main()