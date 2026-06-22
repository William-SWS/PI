"""
Questão 2 — Filtros, Detecção de Bordas (Canny) e HOG

Implementa as duas primeiras etapas do Canny (filtro gaussiano +
gradiente Sobel) e o descritor HOG simplificado.

Saída:
    atividade4/imagens/saidas_questao2/  (imagens PNG)
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import cv2
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

SCRIPT_DIR = Path(__file__).resolve().parent
IMG_DIR = SCRIPT_DIR / "imagens"
OUT_DIR = IMG_DIR / "saidas_questao2"

GAUSSIAN_KERNEL_SIZE = 5
GAUSSIAN_SIGMA = 1.4
SOBEL_KERNEL_SIZE = 3
HOG_CELL_SIZE = 8
HOG_NUMBER_OF_BINS = 9


def to_gray(image: np.ndarray) -> np.ndarray:  # BGR -> grayscale (ITU-R BT.601)
    return (
        0.299 * image[:, :, 2] +
        0.587 * image[:, :, 1] +
        0.114 * image[:, :, 0]
    ).astype(np.uint8)


def gaussian_kernel_2d(kernel_size: int, sigma: float) -> np.ndarray:  # kernel gaussiano 2D manual
    kernel = np.zeros((kernel_size, kernel_size), dtype=np.float64)
    center = kernel_size // 2

    for row_index in range(kernel_size):
        for column_index in range(kernel_size):
            displacement_x = row_index - center
            displacement_y = column_index - center
            kernel[row_index, column_index] = (
                np.exp(-(displacement_x ** 2 + displacement_y ** 2) / (2.0 * sigma ** 2))
                / (2.0 * np.pi * sigma ** 2)
            )

    kernel_sum = np.sum(kernel)
    if kernel_sum > 0:
        kernel /= kernel_sum

    return kernel


def convolve_2d(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:  # convolucao 2D manual
    image_height, image_width = image.shape
    kernel_height, kernel_width = kernel.shape
    kernel_center_y = kernel_height // 2
    kernel_center_x = kernel_width // 2

    padded_image = np.pad(
        image,
        pad_width=((kernel_center_y, kernel_center_y), (kernel_center_x, kernel_center_x)),
        mode="edge",
    )

    output = np.zeros_like(image, dtype=np.float64)

    for row_index in range(image_height):
        for column_index in range(image_width):
            region = padded_image[
                row_index:row_index + kernel_height,
                column_index:column_index + kernel_width,
            ]
            output[row_index, column_index] = np.sum(region * kernel)

    return output


def sobel_operator_x(image: np.ndarray) -> np.ndarray:  # gradiente horizontal (Sobel)
    kernel_x = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1],
    ], dtype=np.float64)

    return convolve_2d(image, kernel_x)


def sobel_operator_y(image: np.ndarray) -> np.ndarray:  # gradiente vertical (Sobel)
    kernel_y = np.array([
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1],
    ], dtype=np.float64)

    return convolve_2d(image, kernel_y)


def gradient_magnitude(gradient_x: np.ndarray, gradient_y: np.ndarray) -> np.ndarray:  # sqrt(gx^2 + gy^2)
    return np.sqrt(gradient_x ** 2 + gradient_y ** 2)


def gradient_orientation(gradient_x: np.ndarray, gradient_y: np.ndarray) -> np.ndarray:  # arctan2(gy, gx) em radianos
    return np.arctan2(gradient_y, gradient_x)


def normalize_to_uint8(array: np.ndarray) -> np.ndarray:  # normaliza para [0, 255] e converte para uint8
    array_min = np.min(array)
    array_max = np.max(array)

    if array_max - array_min == 0:
        return np.zeros_like(array, dtype=np.uint8)

    normalized = (array - array_min) / (array_max - array_min)
    return (normalized * 255).astype(np.uint8)


def hog_descriptor(
    magnitude: np.ndarray,
    orientation: np.ndarray,
    cell_size: int = HOG_CELL_SIZE,
    number_of_bins: int = HOG_NUMBER_OF_BINS,
) -> tuple[np.ndarray, list[list[np.ndarray]]]:  # retorna (imagem_hog_visualizada, histogramas_por_celula)
    image_height, image_width = magnitude.shape
    cells_vertical = image_height // cell_size
    cells_horizontal = image_width // cell_size

    bin_edges = np.linspace(0, np.pi, number_of_bins + 1)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0

    orientation_unsigned = np.where(orientation < 0, orientation + np.pi, orientation)
    orientation_unsigned = np.where(orientation_unsigned >= np.pi, orientation_unsigned - np.pi, orientation_unsigned)

    cell_histograms: list[list[np.ndarray]] = []

    for cell_row in range(cells_vertical):
        row_histograms: list[np.ndarray] = []

        for cell_column in range(cells_horizontal):
            row_start = cell_row * cell_size
            row_end = row_start + cell_size
            column_start = cell_column * cell_size
            column_end = column_start + cell_size

            cell_magnitude = magnitude[row_start:row_end, column_start:column_end]
            cell_orientation = orientation_unsigned[row_start:row_end, column_start:column_end]

            histogram = np.zeros(number_of_bins, dtype=np.float64)

            for pixel_row in range(cell_size):
                for pixel_column in range(cell_size):
                    pixel_angle = cell_orientation[pixel_row, pixel_column]
                    pixel_weight = cell_magnitude[pixel_row, pixel_column]

                    bin_index = np.digitize(pixel_angle, bin_edges) - 1
                    bin_index = min(bin_index, number_of_bins - 1)
                    histogram[bin_index] += pixel_weight

            row_histograms.append(histogram)

        cell_histograms.append(row_histograms)

    visualization = np.zeros(
        (cells_vertical * cell_size, cells_horizontal * cell_size),
        dtype=np.float64,
    )

    for cell_row in range(cells_vertical):
        for cell_column in range(cells_horizontal):
            histogram = cell_histograms[cell_row][cell_column]
            histogram_max = np.max(histogram) if np.max(histogram) > 0 else 1.0

            row_offset = cell_row * cell_size
            column_offset = cell_column * cell_size

            for bin_index in range(number_of_bins):
                bin_value = histogram[bin_index] / histogram_max
                angle = bin_centers[bin_index]
                line_length = int(bin_value * cell_size * 0.5)

                center_x = column_offset + cell_size // 2
                center_y = row_offset + cell_size // 2

                endpoint_x = int(center_x + line_length * np.cos(angle))
                endpoint_y = int(center_y + line_length * np.sin(angle))

                start_x = int(center_x - line_length * np.cos(angle))
                start_y = int(center_y - line_length * np.sin(angle))

                for interpolation_point in np.linspace(0, 1, max(1, line_length)):
                    point_x = int(start_x + interpolation_point * (endpoint_x - start_x))
                    point_y = int(start_y + interpolation_point * (endpoint_y - start_y))

                    if 0 <= point_y < visualization.shape[0] and 0 <= point_x < visualization.shape[1]:
                        visualization[point_y, point_x] = 255

    return normalize_to_uint8(visualization), cell_histograms


def main() -> None:  # pipeline: carrega -> grayscale -> gaussiano -> gradiente -> HOG
    log.info("Pipeline de detecção de bordas e HOG")
    log.info("Diretório de saída: %s", OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    imagem_path = IMG_DIR / "2_modelo.png"
    log.info("Carregando %s ...", imagem_path.name)

    imagem_colorida = cv2.imread(str(imagem_path))
    if imagem_colorida is None:
        log.error("Falha ao carregar %s", imagem_path)
        sys.exit(1)

    imagem_cinza = to_gray(imagem_colorida)
    cv2.imwrite(str(OUT_DIR / "2_modelo_grayscale.png"), imagem_cinza)
    log.info("  Grayscale salva (dimensões: %s)", imagem_cinza.shape)

    kernel_gaussiano = gaussian_kernel_2d(GAUSSIAN_KERNEL_SIZE, GAUSSIAN_SIGMA)
    imagem_suavizada = convolve_2d(imagem_cinza.astype(np.float64), kernel_gaussiano)
    imagem_suavizada_uint8 = normalize_to_uint8(imagem_suavizada)
    cv2.imwrite(str(OUT_DIR / "2_modelo_gaussian_filtered.png"), imagem_suavizada_uint8)
    log.info(
        "  Filtro gaussiano aplicado (kernel %dx%d, sigma=%.1f)",
        GAUSSIAN_KERNEL_SIZE, GAUSSIAN_KERNEL_SIZE, GAUSSIAN_SIGMA,
    )

    gradiente_x = sobel_operator_x(imagem_suavizada)
    gradiente_y = sobel_operator_y(imagem_suavizada)
    cv2.imwrite(str(OUT_DIR / "2_modelo_gradient_x.png"), normalize_to_uint8(gradiente_x))
    cv2.imwrite(str(OUT_DIR / "2_modelo_gradient_y.png"), normalize_to_uint8(gradiente_y))
    log.info("  Gradientes Sobel calculados (X e Y)")

    magnitude_gradiente = gradient_magnitude(gradiente_x, gradiente_y)
    cv2.imwrite(str(OUT_DIR / "2_modelo_gradient_magnitude.png"), normalize_to_uint8(magnitude_gradiente))
    log.info("  Magnitude do gradiente salva")

    orientacao_gradiente = gradient_orientation(gradiente_x, gradiente_y)

    hog_normalized_magnitude = normalize_to_uint8(magnitude_gradiente).astype(np.float64)
    hog_visualization, histogramas = hog_descriptor(
        hog_normalized_magnitude, orientacao_gradiente,
    )
    cv2.imwrite(str(OUT_DIR / "2_modelo_hog_visualization.png"), hog_visualization)
    log.info(
        "  HOG descritor calculado (células %dx%d, %d bins por célula)",
        HOG_CELL_SIZE, HOG_CELL_SIZE, HOG_NUMBER_OF_BINS,
    )

    total_cells_vertical = len(histogramas)
    total_cells_horizontal = len(histogramas[0]) if histogramas else 0

    with open(str(OUT_DIR / "2_modelo_hog_descriptor.txt"), "w", encoding="utf-8") as descriptor_file:
        descriptor_file.write("HOG Descriptor - Feature Vectors\n")
        descriptor_file.write(f"Cell Size: {HOG_CELL_SIZE}x{HOG_CELL_SIZE}\n")
        descriptor_file.write(f"Number of Bins: {HOG_NUMBER_OF_BINS}\n")
        descriptor_file.write(f"Grid: {total_cells_vertical}x{total_cells_horizontal} cells\n")
        descriptor_file.write(f"Total Features: {total_cells_vertical * total_cells_horizontal * HOG_NUMBER_OF_BINS}\n")
        descriptor_file.write("=" * 60 + "\n\n")

        for cell_row in range(total_cells_vertical):
            for cell_column in range(total_cells_horizontal):
                histogram = histogramas[cell_row][cell_column]
                descriptor_file.write(
                    f"Cell [{cell_row},{cell_column}]: "
                    f"{'  '.join(f'{value:.2f}' for value in histogram)}\n"
                )

    log.info("  Vetores de características salvos em 2_modelo_hog_descriptor.txt")
    log.info("Concluído! Imagens e descritor salvos em %s", OUT_DIR)


if __name__ == "__main__":
    main()
