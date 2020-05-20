import argparse
import os
import time

from PIL import Image
from PIL import ImageChops

BLACK = 0
DARK_GREY = 90
LIGHT_GREY = 180
WHITE = 255

COLORS = [[WHITE, DARK_GREY],
          [LIGHT_GREY, BLACK]]

TILE_WIDTH = 20
TILE_HEIGHT = 18
TILE_SIZE = TILE_WIDTH * TILE_HEIGHT

DEFAULT_RANGE = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]


def create_image(data, mute, scale, cropframe, file_prefix, output_dir, darkenrange, lightenrange, multiplyrange, darken, lighten, multiply):
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

    # for every 4 b/w images we create one RGB image
    for c in range(0, len(dump) // TILE_SIZE, 4):
        # we create our canvas here
        channels = [Image.new('L', (TILE_WIDTH * 8, TILE_HEIGHT * 8)),
                    Image.new('L', (TILE_WIDTH * 8, TILE_HEIGHT * 8)),
                    Image.new('L', (TILE_WIDTH * 8, TILE_HEIGHT * 8)),
                    Image.new('L', (TILE_WIDTH * 8, TILE_HEIGHT * 8))]

        for idx, channel in enumerate(channels):
            pixels = channel.load()
            for h in range(TILE_HEIGHT):
                for w in range(TILE_WIDTH):
                    tile = bytes.fromhex(dump[((c + idx) * TILE_SIZE) + (h * TILE_WIDTH) + w])
                    for i in range(8):
                        for j in range(8):
                            hi = (tile[i * 2] >> (7 - j)) & 1
                            lo = (tile[i * 2 + 1] >> (7 - j)) & 1
                            pixels[(w * 8) + j, (h * 8) + i] = COLORS[hi][lo]

        # the number of saved images depends on the parameters for enhancements
        # create list of operations
        enhancements = [(.0, 'n')]  # image with no additional operations

        # range of darken images
        if darkenrange:
            darken.extend(DEFAULT_RANGE)

        # single darken image with specified value
        for v in darken:
            enhancements.append((v / 100, 'd'))

        # range of lighten images
        if lightenrange:
            lighten.extend(DEFAULT_RANGE)

        # single lighten image with specified value
        for v in lighten:
            enhancements.append((v / 100, 'l'))

        # range of multiply images
        if multiplyrange:
            multiply.extend(DEFAULT_RANGE)

        # single multiply image with specified value
        for v in multiply:
            enhancements.append((v / 100, 'm'))

        # image creation and enhancement
        for f, m in enhancements:
            # create single image from RGB channels
            img = Image.merge('RGB', channels[1:])
            img.putalpha(255)
            img = img.convert('RGBA')

            # opacity of the b/W layer
            bwLayer = channels[0]
            bwLayer.putalpha(int(255 * f))
            bwLayer = bwLayer.convert('RGBA')

            # apply opacity layer to helper image
            helperImg = img.copy()
            helperImg.alpha_composite(bwLayer)

            if m == 'd':  # darken
                img = ImageChops.darker(img, helperImg)
            elif m == 'm':  # multiply
                img = ImageChops.multiply(img, helperImg)
            elif m == 'l':  # lighten
                img = ImageChops.lighter(img, helperImg)

            # cropping
            if cropframe:
                img = img.crop((16, 16, (18 * 8), (16 * 8)))

            # resizing
            img = img.resize((img.width * scale, img.height * scale), resample=Image.NEAREST)

            # saving
            img.save(os.path.join(output_dir, f'{file_prefix} {time.strftime("%Y%m%d - %H%M%S")} {c:03d} {m} {int(100 * f)}.png'))


if __name__ == "__main__":
    # get arguments and set default values
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s", "--scale", default=1, type=int, help="scale factor for image resizing as int")
    parser.add_argument("-o", "--out_filename", default='Colorized Game Boy Photo', help="output filename")
    parser.add_argument("-dir", "--output_dir", default='images', help="output directory")
    parser.add_argument("-i", "--in_filename", default='gbDump.out', help="input filename")
    parser.add_argument("-m", "--mute", default=False, action='store_true', help="mutes the scripts outputs")
    parser.add_argument("-f", "--cropframe", default=False, action='store_true', help="crops the frame")
    parser.add_argument("-d", "--darken", default=[], type=int, nargs='+', help="darkens the image by applying the b/w image as layer with the set opacity, generates on image per given value")
    parser.add_argument("-dr", "--darkenrange", action='store_true', help="darkens the image by applying the b/w image as layer with opacity in 10%% increments from 0-100%%, resulting in 10 output images per RGB image")
    parser.add_argument("-l", "--lighten", default=[], type=int, nargs='+', help="lightens the image by applying the b/w image as layer with the set opacity, generates on image per given value")
    parser.add_argument("-lr", "--lightenrange", action='store_true', help="lightens the image by applying the b/w image as layer with opacity in 10%% increments from 0-100%%, resulting in 10 output images per RGB image")
    parser.add_argument("-mu", "--multiply", default=[], type=int, nargs='+', help="multiply layer operation by applying the b/w image as layer with the set opacity, generates on image per given value")
    parser.add_argument("-mr", "--multiplyrange", action='store_true', help="multiply layer operation by applying the b/w image as layer with opacity in 10%% increments from 0-100%%, resulting in 10 output images per RGB image")
    args = parser.parse_args()

    with open(args.in_filename) as input:
        create_image(data=input,
                     mute=args.mute,
                     scale=args.scale,
                     cropframe=args.cropframe,
                     file_prefix=args.out_filename,
                     output_dir=args.output_dir,
                     darkenrange=args.darkenrange,
                     lightenrange=args.lightenrange,
                     multiplyrange=args.multiplyrange,

                     darken=args.darken,
                     lighten=args.lighten,
                     multiply=args.multiply,

                     )
