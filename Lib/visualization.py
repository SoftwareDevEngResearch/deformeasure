import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def vis_plotter(x, y, img):


    ig, ax = plt.subplots()


    plt.subplot(1, 3, 1)
    plt.title("Deformation Image")
    imgplot = plt.imshow(img)


    plt.subplot(1, 3, 2)
    plt.title("X Deformations")
    imgplot = plt.imshow(x)
    imgplot.set_cmap('YlGnBu')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.colorbar()

    plt.subplot(1, 3, 3)
    plt.title("Y Deformations")
    imgplot = plt.imshow(y)
    imgplot.set_cmap('YlGnBu')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.colorbar()
    plt.tight_layout()
    plt.show()



class Visualization():
    def __init__(self, mode=None, def_video=None, def_image=None, x=None, y=None):
        if x is not None:
            self.x = x
        else:
            print("Input deformations in X")
        if y is not None:
            self.y = y
        else:
            print("Input deformations in Y")

        if mode == 'image':
            if def_image is not None:
                self.image = def_image
            else:
                print("Mode selected is image. Input deformed image")
            self.show_image()
        elif mode == 'video':
            if def_video is not None:
                self.video = def_video
            else:
                print("Mode selected is image. Input deformation video")
            self.show_video()
        else:
            print("Enter mode either video or image")

    def show_video(self):
        image = Image.open(self.video)
        # Display individual frames from the loaded animated GIF file
        for frame in range(image.n_frames):
            image.seek(frame)
            img = image.copy()
            vis_plotter(self.x[frame], self.y[frame], img)
        image.close()

    def show_image(self):
        image = Image.open(self.image)
        vis_plotter(self.x, self.y, image)
        image.close()



if __name__ == '__main__':
    Visualization(mode='video', def_video='generated/def_translate_x.gif', x='output/sample_x.npy', y='sample_y.npy')
