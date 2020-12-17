import cv2
from cv2 import dnn_superres
import numpy as np

import argparse
import time
import os

'''
TODO Exception handlling for the files.
TODO File naming properly
'''


def init_super_res(model_path: str):
    '''
    Make sure that model name in the path should be in following format: modelname_xScale.pb
    '''
    global sr, modelname, modelscale
    sr = dnn_superres.DnnSuperResImpl_create()

    modelname = model_path.split(os.path.sep)[-1].split("_")[0].lower()
    modelscale = model_path.split("_x")[-1]
    modelscale = int(modelscale[:modelscale.find(".")])

    print(f"[info] Loading super resolution model {modelname}...")
    print(f"[info] Model name {modelname}")
    print(f"[info] Model scale {modelscale}")
    sr.readModel(model_path)
    sr.setModel(modelname, modelscale)


def bicubic_upsample(input_image: np.ndarray, out_image: str):
    print("[info] Upscaling using bicubic interpolation...")
    print("[info] w: {}, h: {}".format(
        input_image.shape[1], input_image.shape[0]))
        
    start = time.time()
    upscaled_bicubic = cv2.resize(
        input_image, (input_image.shape[1]*modelscale, input_image.shape[0]*modelscale))
    end = time.time()

    print("[info] Bicubic upscaling took {:.6f} seconds".format(
        end - start))
    cv2.imwrite("output/Bicubic_"+out_image, upscaled_bicubic)


def super_res(input_image, out_image, do_bicubic: bool):
    if do_bicubic:
        bicubic_upsample(input_image, out_image)

    print("[info] w: {}, h: {}".format(
        input_image.shape[1], input_image.shape[0]))

    start = time.time()
    upscaled = sr.upsample(input_image)
    end = time.time()

    print("[info] super resolution took {:.6f} seconds".format(
        end - start))

    print("[info] w: {}, h: {}".format(upscaled.shape[1],
                                       upscaled.shape[0]))

    cv2.imwrite("output/"+out_image, upscaled)
    print("Upscaled")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--model", required=True,
                    help="path to super resolution model")
    ap.add_argument("-i", "--image", required=True,
                    help="path to input image we want to increase resolution of")
    ap.add_argument("-B", "--Bicubic", required=False, type=bool,
                    help="Set to true if you want to upscale the image using Bicubic interpolation.")

    args = vars(ap.parse_args())

    model_path = args["model"]
    image_name = args["image"].split(os.path.sep)[-1].split(".")[0]

    init_super_res(model_path)

    image = cv2.imread(args["image"])

    super_res(image, image_name+"_"+modelname + "_x" +
              str(modelscale)+".jpg", do_bicubic=args["Bicubic"])
