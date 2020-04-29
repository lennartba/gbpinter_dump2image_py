import os
from PIL import Image

colors = [(0,0,0),(90,90,90),(180,180,180),(255,255,255)]

f = open('gbDump.out')

dump = []
for line in f:
	if (line[0] not in  ['!','#','{']) and (len(line)>1):
		dump.append(line[:-1])

for line in dump:
	print(line)

print(len(dump))

#img = Image.new('RGB', (8, 8), color = 'white')
img = Image.new('RGB', (20*8,18*8), color = 'green')
pixels = img.load()

#20 tiles width
#18 tiles hight
#tile = bytes.fromhex(dump[50])
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
					#farbcodierung: http://www.huderlem.com/demos/gameboy2bpp.html

	#img.show()
	#img.save('images/dump_{:03d}.png'.format(c))
	img_reszied = img.resize((640,576),resample=Image.NEAREST)
	img_reszied.save('images/4x/dump_{:03d}.png'.format(c))
