import argparse
import os
import time

from PIL import Image

BLACK = (0, 0, 0)
DARK_GREY = (90, 90, 90)
LIGHT_GREY = (180, 180, 180)
WHITE = (255, 255, 255)


def create_image(data, colors=(BLACK, DARK_GREY, LIGHT_GREY, WHITE), mute=False, scale=1, cropframe=False, file_prefix='Game Boy Photo', output_dir='images'):
    # here we remove comments, errors and empty lines from the input
    dump = []
    for line in data:
        if (line[0] not in ['!', '#', '{']) and (len(line) > 1):
            dump.append(line.strip())

    # some outputs
    if not mute:
        for line in dump:
            print(line)
        print(len(dump))

    # 20 tiles width
    # 18 tiles hight
    # gb image format: https://www.huderlem.com/demos/gameboy2bpp.html
    # conversion happens here
    for c in range(len(dump) // 360):
        # we create our canvas here
        img = Image.new('RGB', (20 * 8, 18 * 8), color='green')
        pixels = img.load()
        for h in range(18):
            for w in range(20):
                tile = bytes.fromhex(dump[(c * 360) + (h * 20) + w])
                for i in range(8):
                    for j in range(8):
                        col = (255, 0, 0)
                        hi = (tile[i * 2] >> (7 - j)) & 1
                        lo = (tile[i * 2 + 1] >> (7 - j)) & 1
                        if hi == 0 and lo == 0:
                            col = colors[3]
                        if hi == 1 and lo == 0:
                            col = colors[2]
                        if hi == 0 and lo == 1:
                            col = colors[1]
                        if hi == 1 and lo == 1:
                            col = colors[0]
                        pixels[(w * 8) + j, (h * 8) + i] = col
        # cropping
        if cropframe:
            img = img.crop((16, 16, (18 * 8), (16 * 8)))

        # resizing
        img = img.resize((img.width * scale, img.height * scale), resample=Image.NEAREST)

        # saving
        img.save(os.path.join(output_dir, f'{file_prefix} {time.strftime("%Y%m%d - %H%M%S")} {c:03d}.png'))


if __name__ == "__main__":
    # get arguments and set default values
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s", "--scale", default=1, type=int, help="scale factor for image resizing as int")
    parser.add_argument("-c0", "--color0", default=BLACK, nargs=3, type=int, help="substitute color for black in rgb")
    parser.add_argument("-c1", "--color1", default=DARK_GREY, nargs=3, type=int, help="substitute color for gray in rgb")
    parser.add_argument("-c2", "--color2", default=LIGHT_GREY, nargs=3, type=int, help="substitute color for light gray in rgb")
    parser.add_argument("-c3", "--color3", default=WHITE, nargs=3, type=int, help="substitute color for white in rgb")
    parser.add_argument("-o", "--out_filename", default='Game Boy Photo', help="output filename prefix")
    parser.add_argument("-d", "--output_dir", default='images', help="output directory")
    parser.add_argument("-i", "--in_filename", default='gbDump.out', help="input filename")
    parser.add_argument("-m", "--mute", action='store_true', help="mutes the scripts outputs")
    parser.add_argument("-f", "--cropframe", action='store_true', help="crops the frame")

    args = parser.parse_args()

    with open(args.in_filename) as input:
        create_image(data=input,
                     colors=[args.color0, args.color1, args.color2, args.color3],
                     mute=args.mute,
                     scale=args.scale,
                     cropframe=args.cropframe,
                     file_prefix=args.out_filename,
                     output_dir=args.output_dir
                     )
