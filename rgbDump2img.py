import os
import argparse
from PIL import Image
from PIL import ImageChops
import time
timestr = time.strftime("%Y%m%d - %H%M%S")

#get arguments and set default values
parser = argparse.ArgumentParser()
parser.add_argument("-s","--scale", type=int,help="scale factor for image resizing as int, default = 1")
parser.add_argument("-o","--out_filename",help="output filename, default = 'Colorized Game Boy Photo'")
parser.add_argument("-i","--in_filename",help="input filename, default = 'gbDump.out'")
parser.add_argument("-m","--mute",action = 'store_true', help="mutes the scripts outputs, default = not muted")
parser.add_argument("-f","--cropframe",action = 'store_true', help="crops the frame, default = not cropped")
parser.add_argument("-d","--darken",type=int, nargs='+', choices=range(0, 101), help="darkens the image by appling the b/w image as layer with the set opacity, generates on image per given value")
parser.add_argument("-dr","--darkenrange", action = 'store_true', help="darkens the image by appling the b/w image as layer with opacity in 10% increments from 0-100%, resulting in 10 output images per RGB image")
parser.add_argument("-l","--lighten",type=int, nargs='+', choices=range(0, 101), help="lightens the image by appling the b/w image as layer with the set opacity, generates on image per given value")
parser.add_argument("-lr","--lightenrange", action = 'store_true', help="lightens the image by appling the b/w image as layer with opacity in 10% increments from 0-100%, resulting in 10 output images per RGB image")
parser.add_argument("-mu","--multiply",type=int, nargs='+', choices=range(0, 101), help="multiply layer operation by appling the b/w image as layer with the set opacity, generates on image per given value")
parser.add_argument("-mr","--multiplyrange",action = 'store_true', help="multiply layer operation by appling the b/w image as layer with opacity in 10% increments from 0-100%, resulting in 10 output images per RGB image")
args = parser.parse_args()

# "color" values per channel
colors = [0,90,180,255] #back -> white


# this is your dump file
in_filename = 'gbDump.out'
if args.in_filename: in_filename = args.in_filename
f = open(in_filename)

# set output filename
out_filename = 'Colorized Game Boy Photo'
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

# for every 4 b/w images we create one RGB image
for c in range(0,int(len(dump)/360),4):
	# we create our canvas here
	channelR = Image.new('L', (20*8,18*8))
	channelG = Image.new('L', (20*8,18*8))
	channelB = Image.new('L', (20*8,18*8))
	channelDarken = Image.new('LA', (20*8,18*8))
	#img = Image.new('RGB', (20*8,18*8), color = 'green')
	channels = [channelDarken,channelR,channelG,channelB]
	for channel in range(0,4):			
		channelImg = channels[channel]
		pixels = channelImg.load()
		for h in range(0,18):
			for w in range(0,20):
				tile = bytes.fromhex(dump[((c+channel)*360)+(h*20)+w])
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
	
	
	#the number of saved images depends on the parameters for enhancements
	#create list of operations
	enhanceOpacityList = [.0] #image with no additional opperations
	enhanceModeList = ['n'] #image with no additional opperations
	
	#range of darken images
	if args.darkenrange:
		enhanceOpacityList.extend([1.0,.9,.8,.7,.6,.5,.4,.3,.2,.1])
		enhanceModeList.extend(['d','d','d','d','d','d','d','d','d','d'])#
		
	#single darken image with specified value
	if args.darken:
		for arg in args.darken:
			enhanceOpacityList.append(arg/100)
			enhanceModeList.append('d')
		
	#range of lighten images
	if args.lightenrange:
		enhanceOpacityList.extend([1.0,.9,.8,.7,.6,.5,.4,.3,.2,.1])
		enhanceModeList.extend(['l','l','l','l','l','l','l','l','l','l'])#
		
	#single lighten image with specified value
	if args.lighten:
		for arg in args.lighten:
			enhanceOpacityList.append(arg/100)
			enhanceModeList.append('l')
	
	#range of multiply images
	if args.multiplyrange:
		enhanceOpacityList.extend([1.0,.9,.8,.7,.6,.5,.4,.3,.2,.1])
		enhanceModeList.extend(['m','m','m','m','m','m','m','m','m','m'])#
	
	#single multiply image with specified value
	if args.multiply:
		for arg in args.multiply:
			enhanceOpacityList.append(arg/100)
			enhanceModeList.append('m')
		
	#image creation and enhancement
	for f,m in zip(enhanceOpacityList,enhanceModeList):
		#create single image from RGB channels
		RGBimage = Image.merge('RGB', channels[1:])
		RGBimage.putalpha(255)	
		RGBimage = RGBimage.convert('RGBA')
	
		#opacity of the b/W layer
		bwLayer = channels[0]
		bwLayer.putalpha(int(255*f))
		bwLayer = bwLayer.convert('RGBA')
		
		#apply opacity layer to helper image
		helperImg = RGBimage.copy()
		helperImg.alpha_composite(bwLayer)
		
		if m != 'n': #skip is there are no layer operations
			if m == 'd': #darken
				RGBimage = ImageChops.darker(RGBimage,helperImg)
			if m == 'm': #multiply
				RGBimage = ImageChops.multiply(RGBimage,helperImg)
			if m == 'l': #lighten
				RGBimage = ImageChops.lighter(RGBimage,helperImg)	
	
		#cropping
		if args.cropframe:
			RGBimage = RGBimage.crop((16,16,(18*8),(16*8)))
		
		# resizing
		RGBimage = RGBimage.resize((RGBimage.width*scale,RGBimage.height*scale),resample=Image.NEAREST)

		#saving
		RGBimage.save('images/{} {} {:03d} {} {}.png'.format(out_filename,timestr,c,m,int(100*f)))
		
	

