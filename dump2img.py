import os
from PIL import Image
import time
timestr = time.strftime("%Y-%m-%d %H%M%S")

# you can set rgb color values here
colors = [(0,0,0),(90,90,90),(180,180,180),(255,255,255)]

# this is your dump file
f = open('gbDump.out')

# here we remove comments, errors and empty lines from the input
dump = []
for line in f:
	if (line[0] not in  ['!','#','{']) and (len(line)>1):
		dump.append(line[:-1])

# some outputs
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

	# resizing
	img_resized = img.resize((640,576),resample=Image.NEAREST)

	#saving
	img_resized.save('images/image '+ timestr +' {:03d}.png'.format(c))
