# gbpinter_dump2image_py
quick and dirty batch converting of raw gameboy camera image data to png

- use Python 3
- install pillow python package (pip install pillow or pip3 install pillow when python 3 is not the default version)
- If you are on a mac where python 2.7 is the default you will need to install python3 from the python.org website. Then you can use "chmod +x runme.sh" in terminal to make the runme executable and from then on just doubleclick the runme.sh.
- the script expects “gbDump.out” file and “images” folder to be present
- copy paste the serial dump from your camera into gbDump.out and run the script.
- the script will export files in the format "Image date - time nr.png" so it will not overwrite photos from an earlier export.


One great way to capture the image data:
https://github.com/mofosyne/arduino-gameboy-printer-emulator
