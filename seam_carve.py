import numpy as np
import matplotlib.pyplot as plt
import skimage.io as io
import skimage.color as col
import skimage.filters as flt
from numba import jit

def main():
    image = io.imread('landscape.jpg')
    carved = seam_carve(image, 550)

def seam_carve(image, width):
    crop_iterations = image.shape[1]-width
    image_gray = col.rgb2gray(image)*255
    edge_map = flt.sobel(image_gray)
    current_image = image
    current_edge_map = edge_map
    energy_map, backtrack = get_energy_map(edge_map)
    seam = get_seam_data(energy_map,backtrack)
    for i in range(crop_iterations):
        current_image, current_edge_map = carve_seam_by_one_pixel(current_image, seam, current_edge_map)
        # recalculating energies
        energy_map, backtrack = get_energy_map(current_edge_map)
        seam = get_seam_data(energy_map, backtrack)
    print(current_image.max(),current_image.min())
    plt.imshow(current_image/255)
    plt.show()

@jit
def carve_seam_by_one_pixel(image, seam, edge_data):
    height,width,channels = image.shape
    resized_image = np.zeros((height, width-1, channels))
    resized_edge_map = np.zeros((height, width-1))
    print(resized_edge_map.shape)
    for row, column in enumerate(seam):
            # copy every pixel before seam
            resized_image[-row, :column, :] = image[-row, :column, :]
            resized_edge_map[-row, :column] = edge_data[-row, :column]
            # if there are pixels after seam copy them too
            if column != image.shape[1]-1:
                resized_image[-row, column:, :] = image[-row, column+1:, :]
                resized_edge_map[-row, column:] = edge_data[-row, column+1:]
    return resized_image, resized_edge_map
    pass

@jit
def get_energy_map(edge_data):
        height, width = edge_data.shape
        energy_map = np.zeros_like(edge_data)
        energy_map[0] = edge_data[0]
        backtrack = np.zeros_like(energy_map, dtype=np.int)
        # computing energy with a dynamic programming approach
        # skipping first row in loop
        for y in range(1, height):
            for x in range(width):
                # handling left edge
                if x == 0:
                    min_energy_of_prev_row = min(energy_map[y-1, x:x+2])
                    offset = np.argmin(energy_map[y-1, x: x+2])
                    index_min = x + offset
                # handling right edge
                elif x == width-1:
                    min_energy_of_prev_row = min(energy_map[y-1, x-1: x+1])
                    offset = np.argmin(energy_map[y-1, x-1: x+1])-1
                    index_min = x + offset
                # general case
                else:
                    min_energy_of_prev_row = min(energy_map[y-1, x-1: x+2])
                    offset = np.argmin(energy_map[y-1, x-1: x+2])-1
                    index_min = x + offset
                energy_map[y, x] = edge_data[y, x] + min_energy_of_prev_row
                backtrack[y, x] = index_min
        return energy_map, backtrack

@jit
def get_seam_data(energy_map, backtrack):
    seam_x_indices = np.zeros(backtrack.shape[0], dtype=np.int32)
    min_energy_pixel = np.argmin(energy_map[-1])
    for i in range(backtrack.shape[0]):
        seam_x_indices[i] = min_energy_pixel
        min_energy_pixel = backtrack[-i-1, min_energy_pixel]
    return seam_x_indices

if __name__ == '__main__':
    main()