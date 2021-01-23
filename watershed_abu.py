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
        T = gradient >= n
        
        if n == grad_min + 1:
            C = T
            C_prev = T
        else:
            conn_comp, num_comp = label(T, return_num=True, background=1)
            for i in range(1, num_comp+1):
                comp = conn_comp == i
                common = not(C) and comp
                common_comps, num = label(common, return_num=True, background=0)
                

             




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