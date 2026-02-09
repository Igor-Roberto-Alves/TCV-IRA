import argparse
import importlib
from itertools import product

import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


def get_kernel_weight(kernel_type, dx, dy):

    dist_sq = dx**2 + dy**2

    if kernel_type == "box":
        return 1.0

    elif kernel_type == "hat":

        wx = max(0, 1 - abs(dx) * 2)
        wy = max(0, 1 - abs(dy) * 2)
        return wx * wy

    elif kernel_type == "gaussian":

        sigma = 0.9
        return np.exp(-dist_sq / (2 * (sigma**2)))

    return 1

def main(args):
    xmin, xmax, ymin, ymax = args.window
    width, height = args.resolution

    # Se nenhum kernel for passado, usa 1 amostra no centro (comportamento original)
    if args.kernel is None:
        num_samples = 1
    else:
        num_samples = args.samples

    # create tensor for image: RGB
    image = np.zeros((height, width, 3))

    # Calculate pixel size in world coordinates
    pixel_width = (xmax - xmin) / width
    pixel_height = (ymax - ymin) / height

    # load scene
    scene = importlib.import_module(args.scene).Scene()

    print(
        f"Renderizando com Kernel: {args.kernel if args.kernel else 'Nenhum'} | Amostras: {num_samples}"
    )

    # Loop principal
    for j, i in tqdm(product(range(height), range(width)), total=height * width):

        accumulated_color = np.array([0.0, 0.0, 0.0])
        total_weight = 0.0

        for _ in range(num_samples):

            # Se kernel foi passado sorteamos um deslocamento tal que o ponto calculado ainda esteja dentro do pixel
            if args.kernel is None:
                dx, dy = 0.0, 0.0
            else:
                dx = np.random.uniform(-0.5, 0.5)
                dy = np.random.uniform(-0.5, 0.5)

            px = xmin + (i + 0.5 + dx) * pixel_width
            py = ymin + (j + 0.5 + dy) * pixel_height
            point = (px, py)

            sample_color = np.array(scene.background.as_list())

            for primitive, color in scene:
                if primitive.in_out(point):
                    sample_color = np.array([color.r, color.g, color.b])
                    break

            weight = get_kernel_weight(args.kernel, dx, dy)

            accumulated_color += sample_color * weight # Termos do somatório
            total_weight += weight

        if total_weight > 0: # Se os pesos não foram todos nulos
            final_color = accumulated_color / total_weight
        else:
            final_color = np.array(scene.background.as_list())

        image[j, i] = final_color

    plt.imsave(args.output, image, vmin=0, vmax=1, origin="lower")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Raster module main function")

    parser.add_argument(
        "-s", "--scene", type=str, help="Scene name", default="mickey_scene"
    )
    parser.add_argument(
        "-w",
        "--window",
        type=float,
        nargs=4,
        help="Window: xmin xmax ymin ymax",
        default=[0, 8.0, 0, 6.0],
    )
    parser.add_argument(
        "-r",
        "--resolution",
        type=int,
        nargs=2,
        help="Resolution: width height",
        default=[800, 600],
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Output file name", default="output.png"
    )

    # Argumento do kernel
    parser.add_argument(
        "-k",
        "--kernel",
        type=str,
        choices=["box", "hat", "gaussian"],
        help="Kernel type: box, hat, gaussian",
        default=None,
    )
    
    # Argumento do número de amostras para a estimação de monte carlo
    parser.add_argument(
        "-n",
        "--samples",
        type=int,
        help="Number of Monte Carlo samples per pixel",
        default=10,
    )

    args = parser.parse_args()
    main(args)
