from PIL import Image
import numpy as np
import sys
import os


def main():
    files = os.listdir(f"{sys.path[1]}/water_only")
    for file in files:
        if not os.path.exists(f"{sys.path[1]}/transparent_water/{file[:-5]}.png"):
            make_water_mask_transparent(file[:-5])

    files = os.listdir(f"{sys.path[1]}/water_comparison")
    for file in files:
        if not os.path.exists(f"{sys.path[1]}/transparent_comparison/{file[:-5]}.png"):
            make_water_comparison_transparent(file[:-5])


def make_water_mask_transparent(filename):
    img = Image.open(f"{sys.path[1]}/water_only/{filename}.jpeg")
    rgba = img.convert("RGBA")
    data = rgba.getdata()

    newData = []

    for item in data:
        if item[0] != 0 and item[1] != 0 and item[2] != 255:
            newData.append((item[0], item[1], item[2], 0))
        else:
            newData.append(item)

    rgba.putdata(newData)
    rgba.save(f"{sys.path[1]}/transparent_water/{filename}.png", "PNG")


def make_water_comparison_transparent(filename):
    img = Image.open(f"{sys.path[1]}/water_comparison/{filename}.jpeg")
    rgba = img.convert("RGBA")
    datas = rgba.getdata()

    newData = []
    for item in datas:
        if (item[0] != 255 and item[1] != 0 and item[2] != 0) or (item[0] != 255 and item[1] != 128 and item[2] != 0):
            newData.append((item[0], item[1], item[2], 0))
        else:
            newData.append(item)

    rgba.putdata(newData)
    rgba.save(f"{sys.path[1]}/transparent_comparison/{filename}.png", "PNG")


if __name__ == "__main__":
    main()
