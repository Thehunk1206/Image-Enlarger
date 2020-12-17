import cv2
import argparse
import sys
import numpy as np
import os


def downsample_img(image_path: str, factor: float = 0.5):
    if factor > 1 or factor < 0:
        print("factor should be in between 0 and 1")
        sys.exit()
    else:
        down_image = cv2.imread(image_path)
        h = int(down_image.shape[0]*factor)
        w = int(down_image.shape[1]*factor)
        print(h, w)
        down_image = cv2.resize(
            down_image, (w, h), interpolation=cv2.INTER_CUBIC)
        return down_image


def save_image(image: np.ndarray, base_path: str = "samples/"):
    save = cv2.imwrite(
        base_path+"downsampled_"+str(factor)+args["image"].split(os.path.sep)[-1], image)
    return save


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--factor", required=True, default=0.5,
                    help="Factor by which you want to downsample image.")
    ap.add_argument("-i", "--image", required=True,
                    help="path to input image we want to downsample")
    global args
    args = vars(ap.parse_args())

    global factor
    factor = args["factor"]
    factor = float(factor)
    dwnImg = downsample_img(args["image"], factor)
    saved = save_image(dwnImg)
    if saved: print(f"[info] Downsampled by {factor} and saved") 
    else: print("something went wrong") 
