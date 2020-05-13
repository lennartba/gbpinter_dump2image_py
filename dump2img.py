import os
import argparse
from PIL import Image
import time
timestr = time.strftime("%Y%m%d - %H%M%S")

#get arguments and set default values
parser = argparse.ArgumentParser()
parser.add_argument("-s","--scale", type=int,help="scale factor for image resizing as int, default = 1")
parser.add_argument("-c0","--color0",nargs=3,type=int,help="substitute color for black in rgb, default = 0 0 0")
parser.add_argument("-c1","--color1",nargs=3,type=int,help="substitute color for gray in rgb, default = 90 90 90")
parser.add_argument("-c2","--color2",nargs=3,type=int,help="substitute color for light gray in rgb, default = 180 180 180")
parser.add_argument("-c3","--color3",nargs=3,type=int,help="substitute color for white in rgb, default = 255 255 255")
parser.add_argument("-o","--out_filename",help="output filename, default = 'Game Boy Photo'")
parser.add_argument("-i","--in_filename",help="input filename, default = 'gbDump.out'")
parser.add_argument("-m","--mute",action = 'store_true', help="mutes the scripts outputs, default = not muted")
parser.add_argument("-f","--cropframe",action = 'store_true', help="crops the frame, default = not cropped")
#parser.add_argument("-h","--help",help="show this message")

args = parser.parse_args()

# color values
colors = [(0,0,0),(90,90,90),(180,180,180),(255,255,255)] #default values
if args.color0: colors[0]=tuple(args.color0)
if args.color1: colors[1]=tuple(args.color1)
if args.color2: colors[2]=tuple(args.color2)
if args.color3: colors[3]=tuple(args.color3)

# this is your dump file
in_filename = 'gbDump.out'
if args.in_filename: in_filename = args.in_filename
f = open('gbDump.out')

# set output filename
out_filename = 'Game Boy Photo'
if args.out_filename: out_filename = args.out_filename

# set scale multiplyer
if args.scale:
	scale = args.scale
else:
	scale = 1

# here we remove comments, errors and empty lines from the input
dump = []
for line in f:
	if (line[0] not in  ['!','#','{']) and (len(line)>1):
		dump.append(line[:-1])

# some outputs
if not args.mute:
	for line in dump:
		print(line)

	print(len(dump))

# we create our canvas here
img = Image.new('RGB', (20*8,18*8), color = 'green')
pixels = img.load()

#20 tiles width
#18 tiles hight
# gb image format: https://www.huderlem.com/demos/gameboy2bpp.html
# conversion happens here
for c in range(int(len(dump)/360)):
	for h in range(0,18):
		for w in range(0,20):
			tile = bytes.fromhex(dump[(c*360)+(h*20)+w])
			for i in range(0,8):
				for j in range(0,8):
					col = (255,0,0)
					hi = (tile[i*2] >> (7-j)) &1
					lo = (tile[i*2+1] >> (7-j)) &1
					#print(hi,' ',lo)
					if hi == 0 and lo == 0:
						col = colors[3]
					if hi == 1 and lo == 0:
						col = colors[2]
					if hi == 0 and lo == 1:
						col = colors[1]
					if hi == 1 and lo == 1:
						col = colors[0]
					pixels[(w*8)+j,(h*8)+i] = col

	#img.show()

	#cropping
	if args.cropframe:
		img = img.crop((16,16,(18*8),(16*8)))
	
	# resizing
	img = img.resize((img.width*scale,img.height*scale),resample=Image.NEAREST)

	#saving
	img.save('images/{} {} {:03d}.png'.format(out_filename,timestr,c))
