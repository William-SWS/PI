"""
Questão 3 — Segmentação por Watershed Baseado em Marcadores

Pipeline: threshold -> fechamento -> distance transform ->
         máximos locais -> marcadores -> watershed -> segmentação.

Saída:
    atividade4/imagens/saidas_questao3/  (imagens PNG)
"""

from __future__ import annotations

import heapq
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
OUT_DIR = IMG_DIR / "saidas_questao3"

BINARY_THRESHOLD = 127
CLOSING_KERNEL_SIZE = 5
DISTANCE_THRESHOLD_FRACTION = 0.85


def to_gray(image: np.ndarray) -> np.ndarray:  # BGR -> grayscale (ITU-R BT.601)
    return (
        0.299 * image[:, :, 2] +
        0.587 * image[:, :, 1] +
        0.114 * image[:, :, 0]
    ).astype(np.uint8)


def binarize(image: np.ndarray, threshold: int = BINARY_THRESHOLD) -> np.ndarray:  # 255 se > limiar, 0 caso contrario
    height, width = image.shape
    binary = np.zeros((height, width), dtype=np.uint8)
    for row_index in range(height):
        for column_index in range(width):
            binary[row_index, column_index] = 255 if image[row_index, column_index] > threshold else 0
    return binary


def create_square_kernel(kernel_size: int) -> np.ndarray:  # elemento estruturante quadrado
    return np.ones((kernel_size, kernel_size), dtype=np.uint8)


def erode(binary_image: np.ndarray, kernel: np.ndarray) -> np.ndarray:  # 1 sse todos vizinhos sob o kernel sao 1
    height, width = binary_image.shape
    kernel_height, kernel_width = kernel.shape
    margin_y, margin_x = kernel_height // 2, kernel_width // 2
    output = np.zeros((height, width), dtype=np.uint8)

    for row_index in range(margin_y, height - margin_y):
        for column_index in range(margin_x, width - margin_x):
            region = binary_image[
                row_index - margin_y:row_index - margin_y + kernel_height,
                column_index - margin_x:column_index - margin_x + kernel_width,
            ]
            if np.min(region) == 255:
                output[row_index, column_index] = 255
    return output


def dilate(binary_image: np.ndarray, kernel: np.ndarray) -> np.ndarray:  # 1 sse ao menos um vizinho sob o kernel e 1
    height, width = binary_image.shape
    kernel_height, kernel_width = kernel.shape
    margin_y, margin_x = kernel_height // 2, kernel_width // 2
    output = np.zeros((height, width), dtype=np.uint8)

    for row_index in range(margin_y, height - margin_y):
        for column_index in range(margin_x, width - margin_x):
            region = binary_image[
                row_index - margin_y:row_index - margin_y + kernel_height,
                column_index - margin_x:column_index - margin_x + kernel_width,
            ]
            if np.max(region) == 255:
                output[row_index, column_index] = 255
    return output


def morphological_closing(binary_image: np.ndarray, kernel: np.ndarray) -> np.ndarray:  # dilatacao -> erosao
    return erode(dilate(binary_image, kernel), kernel)


def distance_transform_chamfer(binary_image: np.ndarray) -> np.ndarray:  # distancia de chamfer (3-4-5) em dois passes
    height, width = binary_image.shape
    distance = np.full((height, width), np.inf, dtype=np.float64)

    for row_index in range(height):
        for column_index in range(width):
            if binary_image[row_index, column_index] == 0:
                distance[row_index, column_index] = 0.0

    forward_offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1)]
    forward_weights = [4.0, 3.0, 4.0, 3.0]
    backward_offsets = [(1, -1), (1, 0), (1, 1), (0, 1)]
    backward_weights = [4.0, 3.0, 4.0, 3.0]

    for row_index in range(height):
        for column_index in range(width):
            for (offset_y, offset_x), weight in zip(forward_offsets, forward_weights):
                neighbor_row = row_index + offset_y
                neighbor_column = column_index + offset_x
                if 0 <= neighbor_row < height and 0 <= neighbor_column < width:
                    candidate = distance[neighbor_row, neighbor_column] + weight
                    if candidate < distance[row_index, column_index]:
                        distance[row_index, column_index] = candidate

    for row_index in range(height - 1, -1, -1):
        for column_index in range(width - 1, -1, -1):
            for (offset_y, offset_x), weight in zip(backward_offsets, backward_weights):
                neighbor_row = row_index + offset_y
                neighbor_column = column_index + offset_x
                if 0 <= neighbor_row < height and 0 <= neighbor_column < width:
                    candidate = distance[neighbor_row, neighbor_column] + weight
                    if candidate < distance[row_index, column_index]:
                        distance[row_index, column_index] = candidate

    scaling_denominator = 3.0
    distance /= scaling_denominator
    distance = np.where(binary_image == 255, distance, 0.0)

    return distance


def find_markers_from_distance(
    distance_image: np.ndarray,
    threshold_fraction: float = DISTANCE_THRESHOLD_FRACTION,
) -> np.ndarray:  # maximos locais no distance transform viram marcadores
    height, width = distance_image.shape
    maximum_distance = np.max(distance_image)

    if maximum_distance <= 0:
        return np.zeros((height, width), dtype=np.uint8)

    threshold_value = maximum_distance * threshold_fraction
    high_peak_mask = distance_image >= threshold_value

    markers = np.zeros((height, width), dtype=np.uint8)
    for row_index in range(1, height - 1):
        for column_index in range(1, width - 1):
            if not high_peak_mask[row_index, column_index]:
                continue

            center_value = distance_image[row_index, column_index]
            is_local_maximum = True
            for neighbor_y in range(row_index - 1, row_index + 2):
                for neighbor_x in range(column_index - 1, column_index + 2):
                    if neighbor_y == row_index and neighbor_x == column_index:
                        continue
                    if distance_image[neighbor_y, neighbor_x] > center_value:
                        is_local_maximum = False
                        break
                if not is_local_maximum:
                    break

            if is_local_maximum:
                markers[row_index, column_index] = 255

    return markers


def apply_watershed(distance_image: np.ndarray, marker_mask: np.ndarray) -> np.ndarray:  # inundacao a partir dos marcadores
    height, width = distance_image.shape
    label_map = np.zeros((height, width), dtype=np.int32)
    flood_queue: list[tuple[float, int, int]] = []

    current_label = 0
    for row_index in range(height):
        for column_index in range(width):
            if marker_mask[row_index, column_index] > 0:
                current_label += 1
                label_map[row_index, column_index] = current_label
                heapq.heappush(
                    flood_queue,
                    (-distance_image[row_index, column_index], row_index, column_index),
                )

    neighbor_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while flood_queue:
        _, current_row, current_column = heapq.heappop(flood_queue)
        current_pixel_label = label_map[current_row, current_column]

        for offset_y, offset_x in neighbor_directions:
            neighbor_row = current_row + offset_y
            neighbor_column = current_column + offset_x

            if 0 <= neighbor_row < height and 0 <= neighbor_column < width:
                if label_map[neighbor_row, neighbor_column] == 0 and distance_image[neighbor_row, neighbor_column] > 0:
                    label_map[neighbor_row, neighbor_column] = current_pixel_label
                    heapq.heappush(
                        flood_queue,
                        (-distance_image[neighbor_row, neighbor_column], neighbor_row, neighbor_column),
                    )

    return label_map


def detect_watershed_boundaries(label_map: np.ndarray) -> np.ndarray:  # pixels onde vizinhos tem labels diferentes
    height, width = label_map.shape
    boundary_map = np.zeros((height, width), dtype=np.uint8)
    neighbor_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for row_index in range(height):
        for column_index in range(width):
            current_label = label_map[row_index, column_index]
            if current_label <= 0:
                continue

            for offset_y, offset_x in neighbor_directions:
                neighbor_row = row_index + offset_y
                neighbor_column = column_index + offset_x

                if 0 <= neighbor_row < height and 0 <= neighbor_column < width:
                    neighbor_label = label_map[neighbor_row, neighbor_column]
                    if neighbor_label > 0 and neighbor_label != current_label:
                        boundary_map[row_index, column_index] = 255
                        break

    return boundary_map


def apply_pseudo_colors(label_map: np.ndarray) -> np.ndarray:  # mapeia cada label para uma cor distinta (BGR)
    height, width = label_map.shape
    color_output = np.zeros((height, width, 3), dtype=np.uint8)
    unique_labels = np.unique(label_map)
    valid_labels = [label_value for label_value in unique_labels if label_value > 0]

    np.random.seed(42)
    color_palette = np.random.randint(50, 255, size=(max(len(valid_labels), 1) + 1, 3), dtype=np.uint8)

    for label_value in valid_labels:
        color_index = (label_value - 1) % len(color_palette)
        mask_region = label_map == label_value
        for channel_index in range(3):
            color_output[:, :, channel_index][mask_region] = color_palette[color_index, channel_index]

    return color_output


def normalize_to_uint8(array: np.ndarray) -> np.ndarray:  # normaliza para [0, 255] e converte para uint8
    array_min = np.min(array)
    array_max = np.max(array)

    if array_max - array_min == 0:
        return np.zeros_like(array, dtype=np.uint8)

    normalized = (array - array_min) / (array_max - array_min)
    return (normalized * 255).astype(np.uint8)


def main() -> None:  # pipeline: carrega -> threshold -> fechamento -> dist transform -> markers -> watershed
    log.info("Pipeline de segmentação Watershed")
    log.info("Diretório de saída: %s", OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    image_path = IMG_DIR / "3_chapeus.png"
    log.info("Carregando %s ...", image_path.name)

    color_image = cv2.imread(str(image_path))
    if color_image is None:
        log.error("Falha ao carregar %s", image_path)
        sys.exit(1)

    gray_image = to_gray(color_image)
    cv2.imwrite(str(OUT_DIR / "3_chapeus_grayscale.png"), gray_image)
    log.info("  Grayscale salva (dimensões: %s)", gray_image.shape)

    binary_image = binarize(gray_image)
    cv2.imwrite(str(OUT_DIR / "3_chapeus_threshold.png"), binary_image)
    log.info("  Imagem binária gerada (threshold=%d)", BINARY_THRESHOLD)

    closing_kernel = create_square_kernel(CLOSING_KERNEL_SIZE)
    closed_image = morphological_closing(binary_image, closing_kernel)
    cv2.imwrite(str(OUT_DIR / "3_chapeus_closing.png"), closed_image)
    log.info("  Fechamento morfológico aplicado (kernel %dx%d)", CLOSING_KERNEL_SIZE, CLOSING_KERNEL_SIZE)

    distance_image = distance_transform_chamfer(closed_image)
    distance_visualization = normalize_to_uint8(distance_image)
    cv2.imwrite(str(OUT_DIR / "3_chapeus_distance_transform.png"), distance_visualization)
    log.info("  Distance transform calculado (chamfer 3-4-5)")

    marker_mask = find_markers_from_distance(distance_image)
    cv2.imwrite(str(OUT_DIR / "3_chapeus_markers.png"), marker_mask)
    marker_count = np.sum(marker_mask > 0)
    log.info("  Marcadores encontrados: %d máximos locais", marker_count)

    markers_overlay = color_image.copy()
    overlay_positions = np.where(marker_mask > 0)
    markers_overlay[overlay_positions] = [0, 0, 255]
    cv2.imwrite(str(OUT_DIR / "3_chapeus_markers_overlay.png"), markers_overlay)
    log.info("  Marcadores sobrepostos à imagem original")

    label_map = apply_watershed(distance_image, marker_mask)

    boundary_map = detect_watershed_boundaries(label_map)
    cv2.imwrite(str(OUT_DIR / "3_chapeus_boundaries.png"), boundary_map)
    log.info("  Linhas de watershed detectadas")

    segmented_gray = normalize_to_uint8(label_map.astype(np.float64))
    cv2.imwrite(str(OUT_DIR / "3_chapeus_segmented_gray.png"), segmented_gray)
    log.info("  Segmentação em tons de cinza salva")

    segmented_color = apply_pseudo_colors(label_map)
    cv2.imwrite(str(OUT_DIR / "3_chapeus_segmented_color.png"), segmented_color)
    log.info("  Segmentação colorida gerada")

    boundaries_on_original = color_image.copy()
    boundary_positions = np.where(boundary_map > 0)
    boundaries_on_original[boundary_positions] = [0, 0, 255]
    cv2.imwrite(str(OUT_DIR / "3_chapeus_segmented_output.png"), boundaries_on_original)
    log.info("  Fronteiras sobrepostas à imagem original")

    unique_segments = len(np.unique(label_map)) - 1
    log.info("Concluído! %d segmentos identificados", unique_segments)
    log.info("Todas as imagens salvas em %s", OUT_DIR)


if __name__ == "__main__":
    main()
