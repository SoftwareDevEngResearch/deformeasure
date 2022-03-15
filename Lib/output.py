import numpy
import os

class Output():

    def __init__(self, mode=None, x=None, y=None, filename='default'):
        """Output class stores the output of deformations in output directory in a csv file

        Parameters
        ----------
        mode : string
            Flag whether the output is from deformation of image or video
        x : float
            Deformations in x
        y : float
            Deformations in y
        filename : string
            Name of the output file
        """
        self.save_dir = os.path.dirname(os.path.realpath(__file__)) + "/../output/"
        self.file_name = filename
        if x is not None:
            self.x = x
        else:
            print("Input deformations in X")
        if y is not None:
            self.y = y
        else:
            print("Input deformations in Y")

        if mode == 'image':
            self.output_image()
        elif mode == 'video':
            self.output_video()
        else:
            print("Enter mode either video or image")

    def output_video(self):
        """
        Deformations from a video are stored in a csv file
        """
        with open(self.save_dir + f"def_x_{self.file_name}.csv", "w") as f:
            f.write(f"Deformation for frame {0}")
            f.write("\n")
            numpy.savetxt(f, self.x[0], delimiter=',', fmt='%.2f')
            f.write("\n")

        with open(self.save_dir + f"def_y_{self.file_name}.csv", "w") as f:
            f.write(f"Deformation for frame {0}")
            f.write("\n")
            numpy.savetxt(f, self.y[0], delimiter=',', fmt='%.2f')
            f.write("\n")

        for i in range(1,len(self.x)):
            with open(self.save_dir + f"def_x_{self.file_name}.csv", "a") as f:
                f.write(f"Deformation for frame {i}")
                f.write("\n")
                numpy.savetxt(f, self.x[i], delimiter=',', fmt='%.2f')
                f.write("\n")

        for i in range(1,len(self.y)):
            with open(self.save_dir + f"def_y_{self.file_name}.csv", "a") as f:
                f.write(f"Deformation for frame {i}")
                f.write("\n")
                numpy.savetxt(f, self.y[i], delimiter=',', fmt='%.2f')
                f.write("\n")



    def output_image(self):
        """
        Deformations from an image are stored in a csv file
        """
        with open(self.save_dir + f"def_x_{self.file_name}.csv", "w") as f:
            numpy.savetxt(f, self.x, delimiter=',', fmt='%.2f')
        with open(self.save_dir + f"def_y_{self.file_name}.csv", "w") as f:
            numpy.savetxt(f, self.y, delimiter=',', fmt='%.2f')



