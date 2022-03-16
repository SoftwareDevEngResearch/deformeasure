try:
    from c_first_order import CFirstOrder
except:
    pass
from math import floor
import numpy as np
from PIL import Image
from scipy.interpolate import RectBivariateSpline



class DIC_NR(object):
    def __init__(self, debug=False):
        """DIC class calculates the deformation from either an image or a video.

        Parameters
        ----------
        debug : bool
            Activate debug mode
        """
        self.debug = debug

    def set_parameters(self, ref_img, def_img, subset_size, ini_guess):
        """Initialize variables

        Parameters
        ----------
        ref_img : string
            Reference Image
        def_img : string
            Deformed Image
        subset_size : int
            Size of the subset
        ini_guess : list
            Initial guess of deformation
        """

        self.subset_size = subset_size
        self.spline_order = 5
        self.ini_guess = ini_guess

        # Make sure that the subset size specified is valid (not odd at this point)
        if (self.subset_size % 2 == 0):
            raise ValueError("Subset size must be odd")

        # Prepare for trouble (load images) (default directory is current working directory) https://stackoverflow.com/questions/12201577/how-can-i-convert-an-rgb-image-into-grayscale-in-python
        if type(ref_img) == type("s") or type(def_img) == type("s"):
            ref_img = np.array(Image.open(ref_img).convert('LA'))  # numpy.array
            def_img = np.array(Image.open(def_img).convert('LA'))  # numpy.array

        self.ref_image = ref_img
        self.def_image = def_img

        # Make it double
        self.ref_image = self.ref_image.astype('d')  # convert to double
        self.def_image = self.def_image.astype('d')  # convert to double

        # Obtain the size of the reference image
        self.X_size, self.Y_size, self._tmp = self.ref_image.shape

        # Termination condition for newton-raphson iteration
        self.Max_num_iter = 40  # maximum number of iterations
        self.TOL = [0, 0]
        self.TOL[0] = 10 ** (-8)  # change in correlation coefficient
        self.TOL[1] = 10 ** (-8) / 2  # change in sum of all gradients.


        #condition to check that point of interest is not close to edge. Point
        #must away from edge greater than half of subset adding 10 to it to have
        #range of initial guess accuracy.

        # +10 due to range of calc in initial_guess
        # border is number of places from edge required
        border = floor((self.subset_size / 2) + 10)
        # Due to 0 indexing, min position can be placed "at" border.
        self.Xmin = border
        self.Ymin = self.Xmin

        # Due to zero indexing, to get last position, subtract 1.
        self.Xmax = (self.X_size - 1) - border
        self.Ymax = (self.Y_size - 1) - border

        self.Xp = self.Xmin
        self.Yp = self.Ymin

        self.initial_guess()
        self.fit_spline()

        self.cfo = CFirstOrder()
        self.cfo.set_image(self.ref_image, self.subset_size)
        self.cfo.set_splines(self.def_interp, self.def_interp_x, self.def_interp_y)

    def initial_guess(self, ref_img=None, def_img=None):
        """Calculating initial deformation parameters from user's initial guess

        Parameters
        ----------
        ref_img : Image
            Reference Image
        def_img : Image
            Deformed Image

        """

        if type(ref_img) == type(None) or type(def_img) == type(None):
            ref_img = self.ref_image
            def_img = self.def_image
            if type(ref_img) == type(None):
                raise error("Tried to run initial_guess without supplying ref_img")

        # Automatic Initial Guess
        q_0 = np.zeros(6)
        q_0[0:2] = self.ini_guess

        if (q_0[0] < -15 or q_0[0] > 15 or q_0[1] < -15 or q_0[1] > 15):
            raise error("Initial guess outside of range, must be within +/- 15.")

        # check all values of u & v within +/- 10 range of initial guess
        range_ = 10
        u_check = np.arange((round(q_0[0]) - range_), (round(q_0[0]) + range_) + 1, 1, dtype=int)
        v_check = np.arange((round(q_0[1]) - range_), (round(q_0[1]) + range_) + 1, 1, dtype=int)

        half_subset = floor(self.subset_size / 2)

        # Define the intensities of the first reference subset
        y0 = self.Yp - half_subset
        y1 = self.Yp + half_subset

        x0 = self.Xp - half_subset
        x1 = self.Xp + half_subset

        subref = ref_img[y0:y1, x0:x1, 0]

        # Preallocate some matrix space
        sum_diff_sq = np.zeros((u_check.size, v_check.size))

        # Check every value of u and v and see where the best match occurs
        for iter1 in range(u_check.size):
            for iter2 in range(v_check.size):
                # Define intensities for deformed subset
                y0 = self.Yp - half_subset + v_check[iter2]
                y1 = self.Yp + half_subset + v_check[iter2]

                x0 = self.Xp - half_subset + u_check[iter1]
                x1 = self.Xp + half_subset + u_check[iter1]

                subdef = def_img[y0:y1, x0:x1, 0]

                sum_diff_sq[iter1, iter2] = np.sum(np.square(subref - subdef))

        # These indexes locate the u & v value(in the initial range we are checking through) which returned the smallest sum of differences squared.
        u_value_index = np.argmin(np.min(sum_diff_sq, axis=1))
        v_value_index = np.argmin(np.min(sum_diff_sq, axis=0))

        q_0[0] = u_check[u_value_index]
        q_0[1] = v_check[v_value_index]

        self.q_k = q_0[0:6]

    def fit_spline(self):
        """Fitting spline to deformed image data

        """
        if type(self.ref_image) == type(None):
            raise error("Tried to run fit_spline before supplying parameters")

        # Obtain the size of the reference image
        Y_size, X_size, tmp = self.ref_image.shape

        # Define the deformed image's coordinates
        X_defcoord = np.arange(0, X_size, dtype=int)
        Y_defcoord = np.arange(0, Y_size, dtype=int)

        # Fit spline
        self.def_interp = RectBivariateSpline(X_defcoord, Y_defcoord, self.def_image[:, :, 0],
                                              kx=self.spline_order, ky=self.spline_order)

        # Evaluate derivatives at coordinates
        self.def_interp_x = self.def_interp(X_defcoord, Y_defcoord, 0, 1)

        self.def_interp_y = self.def_interp(X_defcoord, Y_defcoord, 1, 0)

    def sequential_calculate(self):
        """Helper function to calculate deformation
        """
        for yy in range(self.Ymin, self.Ymax + 1):
            if yy > self.Ymin:
                self.q_k[0:6] = self.DEFORMATION_PARAMETERS[yy - 1, self.Xmin, 0:6]

            for xx in range(self.Xmin, self.Xmax + 1):
                # Points for correlation and initializing the q matrix
                self.Xp = xx
                self.Yp = yy

                # __________OPTIMIZATION ROUTINE: FIND BEST FIT____________________________
                # Initialize some values
                n = 0
                C_last, GRAD_last, HESS = self.cfo.calculate(self.q_k, self.Xp,
                                                             self.Yp)  # q_k was the result from last point or the user's guess
                optim_completed = False

                if np.isnan(abs(np.mean(np.mean(HESS)))):
                    optim_completed = True

                while not optim_completed:
                    # Compute the next guess and update the values
                    delta_q = np.linalg.lstsq(HESS, (-GRAD_last),
                                              rcond=None)  # Find the difference between q_k+1 and q_k
                    self.q_k = self.q_k + delta_q[0]  # q_k+1 = q_k + delta_q[0]
                    C, GRAD, HESS = self.cfo.calculate(self.q_k, self.Xp, self.Yp)  # Compute new values

                    # Add one to the iteration counter
                    n = n + 1  # Keep track of the number of iterations

                    # Check to see if the values have converged according to the stopping criteria
                    if n > self.Max_num_iter or (abs(C - C_last) < self.TOL[0] and all(
                            abs(delta_q[0]) < self.TOL[1])):  # needs to be tested...
                        optim_completed = True

                    C_last = C  # Save the C value for comparison in the next iteration
                    GRAD_last = GRAD  # Save the GRAD value for comparison in the next iteration
                # _________________________________________________________________________

                # _______STORE RESULTS AND PREPARE INDICES OF NEXT SUBSET__________________
                # Store the current displacements
                self.DEFORMATION_PARAMETERS[yy, xx, 0] = self.q_k[0]  # displacement x
                self.DEFORMATION_PARAMETERS[yy, xx, 1] = self.q_k[1]  # displacement y
                self.DEFORMATION_PARAMETERS[yy, xx, 2] = self.q_k[2]
                self.DEFORMATION_PARAMETERS[yy, xx, 3] = self.q_k[3]
                self.DEFORMATION_PARAMETERS[yy, xx, 4] = self.q_k[4]
                self.DEFORMATION_PARAMETERS[yy, xx, 5] = self.q_k[5]

            if self.debug:
                print(yy)
                print(xx)

    def calculate_from_image(self, ref_img: str, def_img: str, subset_size: int = 11, ini_guess: list = [0, 0]):
        """Calculates deformation from image

        Parameters
        ----------
        ref_img : string
            Name of the reference image
        def_img : string
            Name of the deformation image
        subset_size : int
            Size of the subset
        ini_guess : list
            Initial guess of deformation

        Returns
        -------
        3D array
            Deformations in x and y for each pixel
        """
        self.set_parameters(ref_img, def_img, subset_size, ini_guess)
        self.DEFORMATION_PARAMETERS = np.zeros((self.Y_size, self.X_size, 6), dtype=float)
        self.sequential_calculate()

        return self.DEFORMATION_PARAMETERS[:, :, 0:2]

    def calculate_from_video(self, ref_img: str, def_video: str, subset_size: int = 11, ini_guess: list = [0, 0]):
        """Calculates deformation from video

        Parameters
        ----------
        ref_img : string
            Name of the reference image
        def_img : string
            Name of the deformation image
        subset_size : int
            Size of the subset
        ini_guess : list
            Initial guess of deformation

        Returns
        -------
        list 3D array
            Deformations in x and y for each pixel for each frame
        """
        video = Image.open(def_video)
        list = []
        for i in range(video.n_frames):
            video.seek(i)
            video.save('temp.bmp')
            results = self.calculate_from_image(ref_img, 'temp.bmp', subset_size, ini_guess)
            ini_guess = results[self.Ymin, self.Xmin, 0:2]
            list.append(results)
        video.close()
        return list
