# gbpinter_dump2image_py
quick and dirty batch converting of raw gameboy camera image data to png

There are two scripts:
1. dump2img.py - Create scaled Gameboy Camera Pictures with 4 colours of your choice form your HEX dump file.
2. rgbDump2img.py - Create colored Game Boy Camera Pictures by combining red, green, blue and a black/white channels from four different images from your HEX file. The b/w part can be used to do basic Layer/Opacity operations like darken, lighten and multiply. 

- use Python 3
- install pillow python package (pip install pillow or pip3 install pillow when python 3 is not the default version)
- If you are on a mac where python 2.7 is the default you will need to install python3 from the python.org website. Then you can use "chmod +x runme.sh" in terminal to make the runme executable and from then on just doubleclick the runme.sh.
- the script expects “images” folder to be present
- copy paste the serial dump from your camera into gbDump.out or another file and run the script.
- the script will export files in the format "Image date - time nr.png" so it will not overwrite photos from an earlier export.



## Usage:
### dump2img.py
```
Arguments:
usage: dump2img.py [-h] [-s SCALE] [-c0 COLOR0 COLOR0 COLOR0] [-c1 COLOR1 COLOR1 COLOR1]
                   [-c2 COLOR2 COLOR2 COLOR2] [-c3 COLOR3 COLOR3 COLOR3] [-o OUT_FILENAME]
                   [-i IN_FILENAME] [-m] [-f]

optional arguments:
  -h, --help            show this help message and exit
  -s SCALE, --scale SCALE
                        scale factor for image resizing as int, default = 1
  -c0 COLOR0 COLOR0 COLOR0, --color0 COLOR0 COLOR0 COLOR0
                        substitute color for black in rgb, default = 0 0 0
  -c1 COLOR1 COLOR1 COLOR1, --color1 COLOR1 COLOR1 COLOR1
                        substitute color for gray in rgb, default = 90 90 90
  -c2 COLOR2 COLOR2 COLOR2, --color2 COLOR2 COLOR2 COLOR2
                        substitute color for light gray in rgb, default = 180 180 180
  -c3 COLOR3 COLOR3 COLOR3, --color3 COLOR3 COLOR3 COLOR3
                        substitute color for white in rgb, default = 255 255 255
  -o OUT_FILENAME, --out_filename OUT_FILENAME
                        output filename, default = 'Game Boy Photo'
  -i IN_FILENAME, --in_filename IN_FILENAME
                        input filename, default = 'gbDump.out'
  -m, --mute            mutes the scripts outputs, default = not muted
  -f, --cropframe       crops the frame, default = not cropped
```
Example: ``` python3 dump2img.py -i myDump.txt -o myGameBoyImages -s 4 -c0 255 0 0 -c1 0 255 0 -c2 0 0 255 -c3 0 0 0 ```

### rgbDump2img.py
```
usage: rgbDump2img.py [-h] [-s SCALE] [-o OUT_FILENAME] [-i IN_FILENAME] [-m] [-f]
                      [-d {0,...,100}]
                      [-dr]
                      [-l {0,...,100}]
                      [-lr]
                      [-mu {0,...,100}]
                      [-mr]

optional arguments:
  -h, --help            show this help message and exit
  -s SCALE, --scale SCALE
                        scale factor for image resizing as int, default = 1
  -o OUT_FILENAME, --out_filename OUT_FILENAME
                        output filename, default = 'Colorized Game Boy Photo'
  -i IN_FILENAME, --in_filename IN_FILENAME
                        input filename, default = 'gbDump.out'
  -m, --mute            mutes the scripts outputs, default = not muted
  -f, --cropframe       crops the frame, default = not cropped
  -d {0,...,100} ...]	darkens the image by appling the b/w image as layer with the set opacity, generates on image per given value
  -dr, --darkenrange    darkens the image by appling the b/w image as layer with opacity in 10% increments from 0-100%, resulting in 10 output images per RGB image
  -l {0,...,100} ...]	lightens the image by appling the b/w image as layer with the set opacity, generates on image per given value
  -lr, --lightenrange   lightens the image by appling the b/w image as layer with opacity in 10% increments from 0-100%, resulting in 10 output images per RGB image
  -mu {0,...,100} ...]	multiply layer operation by appling the b/w image as layer with the set opacity, generates on image per given value
  -mr, --multiplyrange  multiply layer operation by appling the b/w image as layer with opacity in 10% increments from 0-100%, resulting in 10 output images per RGB image
```

Example: ```python3 rgbDump2img.py -i myRGBdump.txt -mu 80 90 100 -s 4``` will create a basic RGB image and 3 different RGB images with multiplication layer effects, alls sized up by scale factor 4.

One great way to capture the image data:
https://github.com/mofosyne/arduino-gameboy-printer-emulator
