"""
raster.py  –  renderizador principal
Uso:
    python raster.py -s scene_task1 -n 4 -o out.png
Flags:
    -s  nome do modulo da cena (sem .py)
    -n  amostras por pixel (anti-aliasing / DOF)
    -j  workers paralelos
    -o  arquivo de saida
"""
import random
import argparse
import importlib
import sys
import time
from itertools import product
from functools import partial
from multiprocessing import Pool

import numpy as np
import matplotlib.pyplot as plt

from src.base import Color

try:
    from tqdm import tqdm as _tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False


class Context:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def render_pixel(context, ij):
    i, j = ij
    pixel = Color(0, 0, 0)
    for _ in range(context.num_samples):
        dx = np.random.uniform(-0.5, 0.5)
        dy = np.random.uniform(-0.5, 0.5)
        ray = context.camera.ray(j + 0.5 + dx, i + 0.5 + dy)
        hit_rec = context.scene.hit(ray)
        if hit_rec.hit:
            shaded = hit_rec.material.shade(hit_rec, context.scene)
            pixel  = pixel + shaded / context.num_samples
        else:
            pixel  = pixel + context.scene.background / context.num_samples
    return (i, j, pixel)


def main(args, pool):
    scene      = importlib.import_module(args.scene).Scene()
    camera     = scene.camera
    W, H       = camera.img_width, camera.img_height
    image      = np.zeros((H, W, 3))
    total      = H * W
    done       = 0
    t0         = time.time()

    print(f"Renderizando '{args.scene}'  {W}x{H}  amostras={args.num_samples}  workers={args.num_jobs}")

    context  = Context(scene=scene, camera=camera, num_samples=args.num_samples)
    pixels   = product(range(H), range(W))

    if HAS_TQDM:
        iterator = _tqdm(
            (pool.imap(partial(render_pixel, context), pixels) if args.num_jobs > 1
             else (render_pixel(context, ij) for ij in pixels)),
            total=total
        )
    else:
        if args.num_jobs > 1:
            raw = pool.imap(partial(render_pixel, context), pixels)
        else:
            raw = (render_pixel(context, ij) for ij in pixels)

        def progress_wrap(it):
            for item in it:
                nonlocal done
                done += 1
                if done % 5000 == 0 or done == total:
                    elapsed = time.time() - t0
                    pct = done / total * 100
                    eta = elapsed / done * (total - done) if done else 0
                    sys.stdout.write(f"\r  {pct:5.1f}%  {done}/{total}  ETA {eta:.0f}s   ")
                    sys.stdout.flush()
                yield item
            print()

        iterator = progress_wrap(raw)

    for i, j, pixel in iterator:
        image[i, j] = np.clip(pixel.as_list(), 0, 1)

    plt.imsave(args.output, image, vmin=0, vmax=1, origin='lower')
    print(f"Salvo em: {args.output}  ({time.time()-t0:.1f}s)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--scene',       default='ball_scene')
    parser.add_argument('-n', '--num_samples', type=int, default=1)
    parser.add_argument('-j', '--num_jobs',    type=int, default=4)
    parser.add_argument('-o', '--output',      default='output.png')
    args = parser.parse_args()

    pool = Pool(args.num_jobs)
    main(args, pool)
    pool.close()
    pool.join()
