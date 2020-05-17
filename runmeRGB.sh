#!/bin/bash
cd "$(dirname "$0")"
python3 rgbDump2img.py -mu 100 -s 4 -i gbDumpRGB2.out
