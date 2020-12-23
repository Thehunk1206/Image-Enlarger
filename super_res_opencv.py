import cv2
from cv2 import dnn_superres
import numpy as np
import matplotlib.pyplot as plt

import argparse
import time
import os
import sys

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
    


def plot_results(image_list: list,title_list:list = ["original","Bicubic","SRx8"]):
    _, axs = plt.subplots(1, len(image_list))
    axs = axs.flatten()
    for img, ax, title in zip(image_list, axs,title_list):
        ax.set_title(title)
        ax.imshow(img)
    plt.tight_layout()
    plt.show()


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

    upscaled_bicubic = cv2.cvtColor(upscaled_bicubic, cv2.COLOR_RGB2BGR)
    cv2.imwrite("output/Bicubic_"+out_image, upscaled_bicubic)
    upscaled_bicubic = cv2.cvtColor(upscaled_bicubic, cv2.COLOR_BGR2RGB)
    return upscaled_bicubic


def super_res(input_image, out_image):
    print("[info] w: {}, h: {}".format(
        input_image.shape[1], input_image.shape[0]))

    start = time.time()
    upscaled = sr.upsample(input_image)
    end = time.time()

    print("[info] super resolution took {:.6f} seconds".format(
        end - start))
    print("[info] w: {}, h: {}".format(upscaled.shape[1],
                                       upscaled.shape[0]))

    upscaled = cv2.cvtColor(upscaled, cv2.COLOR_RGB2BGR)
    cv2.imwrite("output/"+out_image, upscaled)
    print("Upscaled")
    upscaled = cv2.cvtColor(upscaled, cv2.COLOR_BGR2RGB)
    return upscaled


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--model", required=True,
                    help="path to super resolution model")
    ap.add_argument("-i", "--image", required=True,
                    help="path to input image we want to increase resolution of")
    ap.add_argument("-B", "--Bicubic", required=False, type=bool, default=False,
                    help="Set to true if you want to upscale the image using Bicubic interpolation.")

    args = vars(ap.parse_args())

    out_images_list = []
    title_list = []

    
    model_path = args["model"]
    if not os.path.exists(model_path):
        print("File does not exist")
        sys.exit()
    else:pass
        
        
    image_name = args["image"].split(os.path.sep)[-1].split(".")[0]

    init_super_res(model_path)
    
    try:
        image = cv2.imread(args["image"])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if args["Bicubic"] == True:
            bicubic_image = bicubic_upsample(image, image_name+".jpg")
            out_images_list.append(bicubic_image)
            title_list.append("Bicubic"+"_x"+str(modelscale))

        out_images_list.append(image)
        title_list.append("Original")
        upscaled_SR = super_res(image, image_name+"_"+modelname + "_x" +
                            str(modelscale)+".jpg")
        out_images_list.append(upscaled_SR)
        title_list.append("SR "+modelname+"_x"+str(modelscale))
        plot_results(out_images_list,title_list)
    except:
        print("Image file does not exist or not in the right format")

    
    

    
