# Image-Enlarger
Increasing spatial resolution of an image using Deep learining based super resolution model.



### Usage

- For image super resolution
```
usage: super_res_opencv.py [-h] -m MODEL -i IMAGE [-B BICUBIC]

optional arguments:
  -h, --help            show this help message and exit
  -m MODEL, --model MODEL
                        path to super resolution model
  -i IMAGE, --image IMAGE
                        path to input image we want to increase resolution of
  -B BICUBIC, --Bicubic BICUBIC
                        Set to true if you want to upscale the image using Bicubic interpolation.

```
#### Example
```
$ python super_res_opencv.py -m models/LapSRN_x8.pb -i samples/flower2.jpg -B True 
```

- Fow Downsampling image
```
python downsample.py --help                       
usage: downsample.py [-h] -f FACTOR -i IMAGE

optional arguments:
  -h, --help            show this help message and exit
  -f FACTOR, --factor FACTOR
                        Factor by which you want to downsample image. Example: 0.5 will downsample
                        the image by 1/2
  -i IMAGE, --image IMAGE
                        path to input image we want to downsample
```
#### Example
```
$ python downsample.py -i samples/bird.jpg -f 0.4
```


# Results
Resuls has been compared between classical Bicubic Interpolation method and Deep Learning Super Sampling methods


## EDSR model 
* SCale x3
![result1](https://github.com/Thehunk1206/Image-Enlarger/blob/master/output/EDSR_x3_2.png)

* scale x4
![result2](https://github.com/Thehunk1206/Image-Enlarger/blob/master/output/EDSR_x4_2.png)

## ESPCN model
* scale x3
![result3](https://github.com/Thehunk1206/Image-Enlarger/blob/master/output/ESPCN_x3_1.png)

* scale x4
![result4](https://github.com/Thehunk1206/Image-Enlarger/blob/master/output/ESPCN_x4_1.png)
![result5](https://github.com/Thehunk1206/Image-Enlarger/blob/master/output/ESPCN_x4_3.png)

## FSRCNN model
* scale x3
![result6](https://github.com/Thehunk1206/Image-Enlarger/blob/master/output/FSRCNN_x3_2.png)

* scale x4
![result7](https://github.com/Thehunk1206/Image-Enlarger/blob/master/output/FSRCNN_x4_2.png)
![result8](https://github.com/Thehunk1206/Image-Enlarger/blob/master/output/FSRCNN_x4_3.png)

## LapSRN model
* scale x4
![result9](https://github.com/Thehunk1206/Image-Enlarger/blob/master/output/LAPSRN_x4_3.png)

* scale x8
![result10](https://github.com/Thehunk1206/Image-Enlarger/blob/master/output/LAPSRN_x8_1.png)
![result11](https://github.com/Thehunk1206/Image-Enlarger/blob/master/output/LAPRN_x8_2.png)
