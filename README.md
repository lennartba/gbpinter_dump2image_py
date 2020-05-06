# gbpinter_dump2image_py
quick and dirty batch converting of raw gameboy camera image data to png

- use Python 3
- install pillow python package (pip install pillow or pip3 install pillow when python 3 is not the default version)
- If you are on a mac where python 2.7 is the default you will need to install python3 from the python.org website. Then you can use "chmod +x runme.sh" in terminal to make the runme executable and from then on just doubleclick the runme.sh.
- the script expects “images” folder to be present
- copy paste the serial dump from your camera into gbDump.out or another file and run the script.
- the script will export files in the format "Image date - time nr.png" so it will not overwrite photos from an earlier export.

```
Arguments:
usage: dump2img.py [-h] [-s SCALE] [-c0 COLOR0 COLOR0 COLOR0]
                   [-c1 COLOR1 COLOR1 COLOR1] [-c2 COLOR2 COLOR2 COLOR2]
                   [-c3 COLOR3 COLOR3 COLOR3] [-o OUT_FILENAME]
                   [-i IN_FILENAME]

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
                        substitute color for white in rgb, default = 255 255 55
  -o OUT_FILENAME, --out_filename OUT_FILENAME
                        output filename, default = 'Game Boy Photo'
  -i IN_FILENAME, --in_filename IN_FILENAME
                        input filename, default = 'gbDump.out'
```
Example: ``` python3 dump2img.py -i myDump.txt -o myGameBoyImages -s 4 -o test -c0 255 0 0 -c1 0 255 0 -c2 0 0 255 -c3 0 0 0 ```

One great way to capture the image data:
https://github.com/mofosyne/arduino-gameboy-printer-emulator
