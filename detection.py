import waterdetect as wd
from PIL import Image
import pickle as pkl
import numpy as np
import cv2
import sys
import os


def main():
    print("Starting...")

    for directory in os.listdir("input"):
        print(f"Analyzing {directory}...")
        filename = directory[-20:-12]
        pickle_path = f"water_masks/{filename}.pkl"

        # sugeneruoti nauja water_mask, jei nera tos dienos pickle
        if not os.path.exists(pickle_path):
            print(f"Detecting water for {directory}. This will take a while...")
            detect_water(directory, pickle_path)

        # nuskaityti water_mask is pickle
        print(f"Loading water_mask pickle of {directory}...")
        kaunas_water_mask = load_mask(pickle_path)

        # paimti originalu TCI kokybes nuotrauka
        print(f"Loading original picture of {directory}...")
        dynamic_directory_name, tci_filename = get_tci_path(directory)
        image = Image.open(f"input/{directory}/GRANULE/{dynamic_directory_name}/IMG_DATA/R10m/{tci_filename}")

        # paimti toki pati plota kaip ir water_mask
        print(f"Cropping original picture {tci_filename}...")
        cropping_area = (8250, 1000, 10000, 1800)
        cropped_image = image.crop(cropping_area)
        cropped_image.save(f"cropped_images/{filename}.jpeg")

        pickle_path = f"forest_masks/{filename}.pkl"

        # sugeneruoti nauja forest_mask, jei nera tos dienos pickle
        if not os.path.exists(pickle_path):
            print(f"Detecting forest for {directory}...")
            detect_forest(f"cropped_images/{filename}.jpeg", pickle_path)

        # nuskaityti forest_mask is pickle
        print(f"Loading forest_mask pickle of {directory}...")
        kaunas_forest_mask = load_mask(pickle_path)

        # pritaikyti visas mask
        print(f"Applying masks for {directory}...")
        apply_masks(cropped_image, kaunas_water_mask, kaunas_forest_mask, filename)


    print("Done...")


def detect_water(orto_path, pickle_path):
    # labai ilga operacija (~5-10 minuciu), naudoja daug kompiuterio resursu
    mask = wd.DWWaterDetect.run_water_detect(input_folder=f"{sys.path[1]}/input/{orto_path}", output_folder=f"{sys.path[1]}/output", single_mode=True, product=wd.DWProducts.Sentinel2_ESA, config_file='WaterDetect.ini')

    # issaugoja water_mask, kad nereiketu is naujo analizuoti
    save_mask(pickle_path, mask.water_mask[1000:1800, 8250:10000])


def load_mask(path):
    file = open(path, 'rb')
    data = pkl.load(file)
    file.close()

    return data


def save_mask(path, data):
    file = open(path, "wb")
    pkl.dump(data, file)
    file.close()


def get_tci_path(directory):
    dynamic_directory_name = os.listdir(f"input/{directory}/GRANULE")[0]

    for file in os.listdir(f"input/{directory}/GRANULE/{dynamic_directory_name}/IMG_DATA/R10m"):
        if file[-11:-8] == "TCI":
            return dynamic_directory_name, file


def detect_forest(image_path, pickle_path):
    img = cv2.imread(image_path)

    # ---------------------------------
    # nuo situ ribu priklauso misko atpazinimas
    upperbound = np.array([50, 50, 50])
    lowerbound = np.array([20, 20, 20])
    # ---------------------------------

    mask = cv2.inRange(img, lowerbound, upperbound)
    imask = mask > 0
    white = np.full_like(img, [255, 255, 255], np.uint8)

    result = np.zeros_like(img, np.uint8)
    result[imask] = white[imask]

    cv2.imwrite("vegitation.jpg", result)
    im = cv2.imread("vegitation.jpg", cv2.IMREAD_GRAYSCALE)

    blur = cv2.GaussianBlur(im, (11, 11), 0)
    _, forest_mask = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    os.remove("vegitation.jpg")

    # issaugoja forest_mask, kad nereiketu is naujo analizuoti
    save_mask(pickle_path, forest_mask)


def apply_masks(image, water_mask, forest_mask, filename):
    # pritaiko water_mask
    pixels = np.asarray(image)

    new_pixels = apply_mask(pixels, water_mask, 1, [0, 0, 255])
    img = Image.fromarray(new_pixels)
    img.save(f"water_only/{filename}.jpeg")

    # pritaiko forest_mask
    pixels = np.asarray(image)

    new_pixels = apply_mask(pixels, forest_mask, 255, [0, 255, 0])
    img = Image.fromarray(new_pixels)
    img.save(f"forest_only/{filename}.jpeg")

    # pritaiko water_mask ir forest_mask
    pixels = np.asarray(image)

    new_pixels = apply_mask(pixels, forest_mask, 255, [0, 255, 0])
    new_pixels = apply_mask(new_pixels, water_mask, 1, [0, 0, 255])
    img = Image.fromarray(new_pixels)
    img.save(f"water_and_forest/{filename}.jpeg")


def apply_mask(pixels, mask, mask_value, colour):
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            if mask[i, j] == mask_value:
                pixels[i, j] = colour

    return pixels


if __name__ == "__main__":
    main()
