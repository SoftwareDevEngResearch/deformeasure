#!/bin/python3
import argparse
import sys
sys.path.append('../Lib/')
from dic import DIC_NR
from visualization import Visualization
from output import Output

def main():
    parser = argparse.ArgumentParser(
        description="Measure deformation between two images, given a subset size and optional initial guess.")

    parser.add_argument("-ri", "--ref_image", metavar="ref_image", type=str,
                        help="The reference image to calculate deformations to")

    parser.add_argument("-di", "--def_image", metavar="def_image", type=str,required=False,
                        help="The deformed image to calculate deformations from")

    parser.add_argument("-dv", "--def_video", metavar="def_video", type=str,required=False,
                        help="The deformed video to calculate deformations from")

    parser.add_argument("-s", "--subset_size", metavar="N", type=int,
                        nargs="?", default=11, required=False,
                        help="The subset size to use. Default=11")

    parser.add_argument("-i", "--initial_guess", metavar="N", type=float,
                        nargs=2, default=[0.0, 0.0], required=False,
                        action="store", dest="ini_guess",
                        help="""Set the initial guess to work from. 
                        Defaults to [0.0, 0.0].
                        Example: -i 1.0 1.0""")

    parser.add_argument("-d", "--debug", dest="debug_mode", action="store_true",
                        help="Use debug print mode.")

    parser.add_argument("-o", "--output", dest="output",
                        type=str, required=False,
                        help="File to write formatted csv output.")

    parser.add_argument("-v", "--visualize", dest="visualize", action="store_true",
                        help="Use debug print mode.")

    args = parser.parse_args()


    if args.def_video != None:
        dic = DIC_NR(args.debug_mode)
        results = dic.calculate_from_video(args.ref_image, args.def_video, args.subset_size, args.ini_guess)
        x = []
        y = []

        for frames in range(len(results)):
            r_f = results[frames]
            x.append(r_f[:, :, 0])
            y.append(r_f[:, :, 1])

        if args.output != None:
            Output(mode='video', x=x, y=y, filename=args.output)

        if args.visualize != None:
            Visualization(mode='video', def_video=args.def_video, x=x, y=y)



    elif args.def_image !=None:
        dic = DIC_NR(args.debug_mode)
        results = dic.calculate_from_image(args.ref_image, args.def_image, args.subset_size, args.ini_guess)

        x = results[:, :, 0]
        y = results[:, :, 1]

        if args.output != None:
            Output(mode='video', x=x, y=y, filename=args.output)

        if args.visualize != None:
            Visualization(mode='image', def_image=args.def_image, x=x, y=y)

    else:
        print('Input either deformation video or image')
        x = 0
        y = 0



if __name__ == '__main__':
    main()
