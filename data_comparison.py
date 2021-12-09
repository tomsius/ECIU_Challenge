from PIL import Image
import numpy as np
import detection
import sys


def main():
    compare_water("20210419", "20211031")


def compare_water(date_from, date_to):
    water_mask_from = detection.load_mask(f"{sys.path[1]}/water_masks/{date_from}.pkl")
    water_mask_to = detection.load_mask(f"{sys.path[1]}/water_masks/{date_to}.pkl")
    image_to = Image.open(f"{sys.path[1]}/water_only/{date_to}.jpeg")
    more_water_colour = [255, 128, 0]
    less_water_colour = [255, 0, 0]

    water_from = 0
    water_to = 0

    pixels = np.asarray(image_to)
    for i in range(water_mask_from.shape[0]):
        for j in range(water_mask_from.shape[1]):
            if water_mask_from[i, j] == 1 and water_mask_to[i, j] == 0:
                pixels[i, j] = less_water_colour
            elif water_mask_from[i, j] == 0 and water_mask_to[i, j] == 1:
                pixels[i, j] = more_water_colour

            if water_mask_from[i, j] == 1:
                water_from += 1

            if water_mask_to[i, j] == 1:
                water_to += 1

    img = Image.fromarray(pixels)
    img.save(f"{sys.path[1]}/water_comparison/{date_from}-{date_to}.jpeg")

    # 1 pixel = 10x10m = 100 m^2
    water_from_area = water_from * 100
    water_to_area = water_to * 100

    coefficient = water_from_area / water_to_area * 100 - 100 if water_from_area > water_to_area else water_to_area / water_from_area * 100 - 100

    if water_from_area > water_to_area:
        coefficient *= -1

    print(water_from_area, water_to_area)
    print(f"Vandens ploto pokytis: {round(coefficient, 5)}%.")

    return coefficient


def compare_forest():
    pass


if __name__ == "__main__":
    main()
