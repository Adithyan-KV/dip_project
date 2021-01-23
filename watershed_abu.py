from pathlib import Path
import skimage.io as sk
import matplotlib.pyplot as plt
import cv2
import numpy as np
import skimage.filters as skf
from skimage.measure import label

def watershed(image_path:Path):
    image = sk.imread(image_path, as_gray=True)
    image = skf.gaussian(image, sigma=8)
    gradient = cv2.Laplacian(image, cv2.CV_8U, ksize=9)

    grad_min, grad_max = gradient.min(), gradient.max()

    for n in range(grad_min+1, grad_max+2):
        bin_image = gradient >= n
        

    plt.subplot(121)
    plt.imshow(bin_image, cmap='gray')
    plt.subplot(122)
    plt.imshow(comp, cmap='gray')
    plt.show()

def main():
    image_path = Path("coins.jpg")

    watershed(image_path)

if __name__ == "__main__":
    main()