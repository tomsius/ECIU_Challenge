from PIL import Image
import numpy as np
import detection
import sys


def main():
    remove_clouds_and_snow_over_water("20210419", "20210310")
    fix_undetected_water("20210419", "20210310")


def remove_clouds_and_snow_over_water(base_date, target_date):
    base_water_mask = detection.load_mask(f"{sys.path[1]}/water_masks/{base_date}.pkl")
    target_water_mask = detection.load_mask(f"{sys.path[1]}/water_masks/{target_date}.pkl")
    target_water_image = Image.open(f"{sys.path[1]}/water_only/{target_date}.jpeg")

    pixels = np.asarray(target_water_image)
    for i in range(base_water_mask.shape[0]):
        for j in range(base_water_mask.shape[1]):
            if base_water_mask[i, j] == 1 and pixels[i, j][0] >= 200 and pixels[i, j][1] >= 200 and pixels[i, j][2] >= 0:
                pixels[i, j] = [0, 0, 255]
                target_water_mask[i, j] = 1

    img = Image.fromarray(pixels)
    img.save(f"{sys.path[1]}/water_only/{target_date}.jpeg")
    detection.save_mask(f"{sys.path[1]}/water_masks/{target_date}.pkl", target_water_mask)


def fix_undetected_water(base_date, target_date):
    base_water_mask = detection.load_mask(f"{sys.path[1]}/water_masks/{base_date}.pkl")
    target_water_mask = detection.load_mask(f"{sys.path[1]}/water_masks/{target_date}.pkl")
    target_water_image = Image.open(f"{sys.path[1]}/water_only/{target_date}.jpeg")

    pixels = np.asarray(target_water_image)
    for i in range(base_water_mask.shape[0]):
        for j in range(base_water_mask.shape[1]):
            if base_water_mask[i, j] == 1 and pixels[i, j][0] <= 50 and pixels[i, j][1] <= 50 and pixels[i, j][2] <= 255:
                pixels[i, j] = [0, 0, 255]
                target_water_mask[i, j] = 1

    img = Image.fromarray(pixels)
    img.save(f"{sys.path[1]}/water_only/{target_date}.jpeg")
    detection.save_mask(f"{sys.path[1]}/water_masks/{target_date}.pkl", target_water_mask)


if __name__ == "__main__":
    main()
