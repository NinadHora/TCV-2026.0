import argparse
import importlib
import math
from itertools import product

import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


def sample_color(scene, point):
    """Determine color at a given point in the scene."""
    for primitive, color in scene:
        if primitive.in_out(point):
            return [color.r, color.g, color.b]
    return scene.background.as_list()


def box_filter(dx, dy, radius):
    """Box filter: uniform weight within radius."""
    if abs(dx) <= radius and abs(dy) <= radius:
        return 1.0
    return 0.0


def hat_filter(dx, dy, radius):
    """Hat (tent/triangle) filter: linear falloff."""
    d = math.sqrt(dx * dx + dy * dy)
    if d >= radius:
        return 0.0
    return 1.0 - d / radius


def gaussian_filter(dx, dy, sigma):
    """Gaussian filter."""
    d2 = dx * dx + dy * dy
    return math.exp(-d2 / (2.0 * sigma * sigma))


FILTERS = {
    'none': None,
    'box': box_filter,
    'hat': hat_filter,
    'gaussian': gaussian_filter,
}


def main(args):
    xmin, xmax, ymin, ymax = args.window
    width, height = args.resolution

    image = np.zeros((height, width, 3))

    pixel_w = (xmax - xmin) / width
    pixel_h = (ymax - ymin) / height

    x_coords = [xmin + (xmax - xmin) * (i + 0.5) / width for i in range(width)]
    y_coords = [ymin + (ymax - ymin) * (j + 0.5) / height for j in range(height)]

    scene = importlib.import_module(args.scene).Scene()

    filter_func = FILTERS.get(args.filter, None)
    n_samples = args.samples

    if filter_func is None or n_samples <= 1:
        # No anti-aliasing
        for j, i in tqdm(product(range(height), range(width)), total=height * width):
            point = (x_coords[i], y_coords[j])
            image[j, i] = sample_color(scene, point)
    else:
        # Anti-aliasing with supersampling
        grid_size = int(math.sqrt(n_samples))
        if grid_size < 1:
            grid_size = 1
        radius = max(pixel_w, pixel_h)
        sigma = radius / 2.0  # for gaussian

        for j, i in tqdm(product(range(height), range(width)), total=height * width):
            cx, cy = x_coords[i], y_coords[j]
            total_color = np.array([0.0, 0.0, 0.0])
            total_weight = 0.0

            for sj in range(grid_size):
                for si in range(grid_size):
                    # Sub-pixel offset
                    dx = pixel_w * ((si + 0.5) / grid_size - 0.5)
                    dy = pixel_h * ((sj + 0.5) / grid_size - 0.5)
                    sx = cx + dx
                    sy = cy + dy

                    if args.filter == 'gaussian':
                        w = filter_func(dx, dy, sigma)
                    else:
                        w = filter_func(dx, dy, radius)

                    color = sample_color(scene, (sx, sy))
                    total_color += w * np.array(color)
                    total_weight += w

            if total_weight > 0:
                image[j, i] = total_color / total_weight
            else:
                image[j, i] = sample_color(scene, (cx, cy))

    plt.imsave(args.output, image, vmin=0, vmax=1, origin='lower')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Raster module main function")
    parser.add_argument('-s', '--scene', type=str, help='Scene name', default='mickey_scene')
    parser.add_argument('-w', '--window', type=float, nargs=4, help='Window: xmin xmax ymin ymax', default=[0, 8.0, 0, 6.0])
    parser.add_argument('-r', '--resolution', type=int, nargs=2, help='Resolution: width height', default=[800, 600])
    parser.add_argument('-o', '--output', type=str, help='Output file name', default='output.png')
    parser.add_argument('-f', '--filter', type=str, choices=['none', 'box', 'hat', 'gaussian'], default='none', help='Anti-aliasing filter')
    parser.add_argument('-n', '--samples', type=int, default=1, help='Number of samples per pixel (use perfect squares: 4, 9, 16, 25)')
    args = parser.parse_args()

    main(args)