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

    more_water = 0
    less_water = 0

    pixels = np.asarray(image_to)
    for i in range(water_mask_from.shape[0]):
        for j in range(water_mask_from.shape[1]):
            if water_mask_from[i, j] == 1 and water_mask_to[i, j] == 0:
                pixels[i, j] = less_water_colour
                less_water += 1
            elif water_mask_from[i, j] == 0 and water_mask_to[i, j] == 1:
                pixels[i, j] = more_water_colour
                more_water += 1

    img = Image.fromarray(pixels)
    img.save(f"{sys.path[1]}/water_comparison/{date_from}-{date_to}.jpeg")

    # 1 pixel = 10x10m = 100 m^2
    more_water_area = more_water * 100
    less_water_area = less_water * 100

    # positive - more water than before, negative - less water than before
    difference = more_water_area - less_water_area
    change_percentage = abs(difference) / (water_mask_from.shape[0] * water_mask_from.shape[1] * 100) * 100
    print(f"Aptikta daugiau vandens: {more_water_area} m^2. Aptika mažiau vandens: {less_water_area} m^2. Pokytis: {difference} m^2 arba {round(change_percentage, 5)}%.")

    return more_water_area, less_water_area, change_percentage


def compare_forest():
    pass


if __name__ == "__main__":
    main()
