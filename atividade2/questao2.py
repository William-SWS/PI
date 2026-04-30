#!/usr/bin/env python3
"""
Questao 2 - Filtragem e compressao no dominio da frequencia (FFT)

Este script implementa, em um unico arquivo, o fluxo solicitado no enunciado:
1) abrir imagem em escala de cinza;
2) aplicar FFT 2D;
3) centralizar o espectro (componente de frequencia zero no centro);
4) criar mascaras para filtros passa-baixa, passa-alta, passa-faixa e rejeita-faixa;
5) filtrar no dominio da frequencia por multiplicacao espectro x mascara;
6) reconstruir imagem no dominio espacial por IFFT;
7) comprimir no dominio da frequencia removendo coeficientes de baixa magnitude;
8) apresentar histogramas antes e apos compressao.

Saidas principais (todas em atividade2/saidas/saidas_questao2, por padrao):
- 00_fft/............ espectro da imagem original (diagnostico da etapa FFT)
- 01_masks/.......... mascaras dos filtros (o que cada filtro preserva/atenua)
- 02_filtradas/...... imagens reconstruidas apos cada filtro
- 03_compressao/..... imagens reconstruidas apos compressao por limiar
- 04_histogramas/.... histogramas da imagem original e comprimidas
- resultados_questao2.json ... metadados, parametros e estatisticas resumidas
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


DEFAULT_LOW_HIGH_RADII = [15, 30, 60]
DEFAULT_BAND_PAIRS = [(10, 30), (20, 50)]
DEFAULT_COMPRESS_PERCENTILES = [70, 85, 95]


@dataclass
class FilterResult:
    name: str
    parameter: str
    output_image: str
    output_spectrum: str
    output_mask: str
    stats: Dict[str, float]


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def find_default_input(script_dir: str) -> str:
    candidates = [
        os.path.join(script_dir, "image2.png"),
        os.path.join(script_dir, "imagem2.png"),
        os.path.join(script_dir, "image2.jpg"),
        os.path.join(script_dir, "imagem2.jpg"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(
        "Imagem de entrada nao encontrada. Informe --input ou adicione image2.png/imagem2.png em atividade2/."
    )


def load_image_gray_float(path: str) -> np.ndarray:
    img = Image.open(path).convert("L")
    return np.array(img, dtype=np.float32)


def save_uint8(arr_uint8: np.ndarray, path: str) -> None:
    Image.fromarray(arr_uint8).save(path)


def minmax_to_uint8(arr: np.ndarray) -> np.ndarray:
    arr = np.asarray(arr, dtype=np.float32)
    min_v = float(arr.min())
    max_v = float(arr.max())
    if max_v <= min_v:
        return np.zeros_like(arr, dtype=np.uint8)
    norm = (arr - min_v) * (255.0 / (max_v - min_v))
    return np.clip(norm, 0, 255).astype(np.uint8)


def parse_int_list(text: str) -> List[int]:
    values: List[int] = []
    for token in text.split(","):
        token = token.strip()
        if not token:
            continue
        values.append(int(token))
    if not values:
        raise ValueError("Lista de inteiros vazia")
    return values


def parse_band_pairs(text: str) -> List[Tuple[int, int]]:
    """
    Formato esperado: "10-30,20-50"
    """
    pairs: List[Tuple[int, int]] = []
    for block in text.split(","):
        block = block.strip()
        if not block:
            continue
        parts = block.split("-")
        if len(parts) != 2:
            raise ValueError(f"Par invalido: {block}. Use formato r1-r2.")
        r1 = int(parts[0].strip())
        r2 = int(parts[1].strip())
        if r1 >= r2:
            raise ValueError(f"Par invalido: {block}. Necessario r1 < r2.")
        pairs.append((r1, r2))
    if not pairs:
        raise ValueError("Lista de pares de faixa vazia")
    return pairs


def frequency_distance_grid(shape: Tuple[int, int]) -> np.ndarray:
    rows, cols = shape
    crow, ccol = rows // 2, cols // 2

    u = np.arange(rows)
    v = np.arange(cols)
    U, V = np.meshgrid(u, v, indexing="ij")

    D = np.sqrt((U - crow) ** 2 + (V - ccol) ** 2)
    return D


def make_lowpass_mask(D: np.ndarray, radius: int) -> np.ndarray:
    return (D <= radius).astype(np.float32)


def make_highpass_mask(D: np.ndarray, radius: int) -> np.ndarray:
    return (D > radius).astype(np.float32)


def make_bandpass_mask(D: np.ndarray, r1: int, r2: int) -> np.ndarray:
    return ((D >= r1) & (D <= r2)).astype(np.float32)


def make_bandreject_mask(D: np.ndarray, r1: int, r2: int) -> np.ndarray:
    return (1.0 - make_bandpass_mask(D, r1, r2)).astype(np.float32)


def spectrum_log_uint8(F_shift: np.ndarray) -> np.ndarray:
    mag = np.abs(F_shift)
    log_mag = np.log1p(mag)
    return minmax_to_uint8(log_mag)


def apply_frequency_filter(
    F_shift: np.ndarray,
    mask: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Retorna:
    - imagem reconstruida no dominio espacial (uint8 para visualizacao)
    - espectro filtrado (uint8, escala log para visualizacao)
    """
    G_shift = F_shift * mask

    g_ishift = np.fft.ifftshift(G_shift)
    g_back = np.fft.ifft2(g_ishift)
    g_real = np.real(g_back)

    img_u8 = minmax_to_uint8(g_real)
    spec_u8 = spectrum_log_uint8(G_shift)
    return img_u8, spec_u8


def image_stats(img_u8: np.ndarray) -> Dict[str, float]:
    return {
        "min": int(img_u8.min()),
        "max": int(img_u8.max()),
        "media": float(np.mean(img_u8)),
        "desvio_padrao": float(np.std(img_u8)),
        "shape": [int(img_u8.shape[0]), int(img_u8.shape[1])],
    }


def save_histogram(img_u8: np.ndarray, out_path: str, title: str) -> None:
    """
    Histograma de intensidades da imagem (0..255).
    Esta saida ajuda a analisar a distribuicao tonal antes/depois da compressao.
    """
    plt.figure(figsize=(8, 4.2))
    plt.hist(img_u8.ravel(), bins=256, range=(0, 255), color="#2368B5", alpha=0.9)
    plt.title(title)
    plt.xlabel("Intensidade")
    plt.ylabel("Frequencia")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def save_histogram_comparison(original: np.ndarray, compressed: Dict[str, np.ndarray], out_path: str) -> None:
    """
    Comparativo consolidado de histogramas:
    - Curva da imagem original
    - Curvas das versoes comprimidas
    """
    plt.figure(figsize=(9.5, 5))

    hist_o, bins = np.histogram(original.ravel(), bins=256, range=(0, 255))
    centers = (bins[:-1] + bins[1:]) / 2.0
    plt.plot(centers, hist_o, label="Original", linewidth=2)

    for label, img in compressed.items():
        hist_c, _ = np.histogram(img.ravel(), bins=256, range=(0, 255))
        plt.plot(centers, hist_c, label=f"Comprimida {label}", linewidth=1.3)

    plt.title("Comparacao de histogramas: antes vs apos compressao")
    plt.xlabel("Intensidade")
    plt.ylabel("Frequencia")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def compress_by_magnitude_threshold(
    F_shift: np.ndarray,
    percentile: int,
) -> Tuple[np.ndarray, Dict[str, float]]:
    """
    Estrategia de compressao:
    - Calcula magnitude do espectro
    - Encontra limiar no percentil informado
    - Zera coeficientes com magnitude abaixo do limiar
    """
    magnitude = np.abs(F_shift)
    thr = float(np.percentile(magnitude, percentile))

    keep_mask = magnitude >= thr
    F_comp_shift = F_shift * keep_mask

    g_ishift = np.fft.ifftshift(F_comp_shift)
    g_back = np.fft.ifft2(g_ishift)
    g_real = np.real(g_back)
    img_u8 = minmax_to_uint8(g_real)

    total = int(keep_mask.size)
    kept = int(np.count_nonzero(keep_mask))
    zeroed = total - kept

    stats = {
        "percentil": int(percentile),
        "limiar_magnitude": thr,
        "coeficientes_totais": total,
        "coeficientes_mantidos": kept,
        "coeficientes_zerados": zeroed,
        "taxa_zerados": float(zeroed / total),
    }
    return img_u8, stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Questao 2 - FFT, filtros e compressao")
    parser.add_argument("--input", "-i", default=None, help="Imagem de entrada (grayscale ou colorida)")
    parser.add_argument("--outdir", "-o", default=None, help="Pasta de saida")
    parser.add_argument(
        "--low-high-radii",
        default=",".join(str(v) for v in DEFAULT_LOW_HIGH_RADII),
        help="Raios para filtros passa-baixa/passa-alta. Ex.: 15,30,60",
    )
    parser.add_argument(
        "--band-pairs",
        default=",".join(f"{a}-{b}" for a, b in DEFAULT_BAND_PAIRS),
        help="Pares r1-r2 para passa-faixa/rejeita-faixa. Ex.: 10-30,20-50",
    )
    parser.add_argument(
        "--compress-thresholds",
        default=",".join(str(v) for v in DEFAULT_COMPRESS_PERCENTILES),
        help="Percentis para compressao por magnitude. Ex.: 70,85,95",
    )
    args = parser.parse_args()

    script_dir = os.path.dirname(__file__)
    input_path = args.input if args.input else find_default_input(script_dir)
    outdir = args.outdir if args.outdir else os.path.join(script_dir, "saidas", "saidas_questao2")

    radii = parse_int_list(args.low_high_radii)
    band_pairs = parse_band_pairs(args.band_pairs)
    compress_percentiles = parse_int_list(args.compress_thresholds)

    # Organizacao das saidas por etapa para facilitar a interpretacao da correcao.
    out_fft = os.path.join(outdir, "00_fft")
    out_masks = os.path.join(outdir, "01_masks")
    out_filtered = os.path.join(outdir, "02_filtradas")
    out_compress = os.path.join(outdir, "03_compressao")
    out_hist = os.path.join(outdir, "04_histogramas")

    for p in [outdir, out_fft, out_masks, out_filtered, out_compress, out_hist]:
        ensure_dir(p)

    # (i) Leitura da imagem de entrada convertida para escala de cinza.
    img = load_image_gray_float(input_path)
    img_u8 = np.clip(img, 0, 255).astype(np.uint8)

    # (ii) Aplicacao da FFT.
    F = np.fft.fft2(img)

    # (iii) Centralizacao da componente de frequencia-zero.
    F_shift = np.fft.fftshift(F)

    # Saida de diagnostico: espectro centralizado da imagem original.
    spec_orig_u8 = spectrum_log_uint8(F_shift)
    spec_orig_path = os.path.join(out_fft, "fft_espectro_centralizado.png")
    save_uint8(spec_orig_u8, spec_orig_path)

    # Geracao da grade de distancias para construir as mascaras.
    D = frequency_distance_grid(img.shape)

    results_filters: List[FilterResult] = []

    # (iv) Criacao das mascaras e (v)-(vi) aplicacao/reconstrucao para passa-baixa e passa-alta.
    for r in radii:
        # Passa-baixa: preserva componentes de baixa frequencia (suavizacao).
        lp_mask = make_lowpass_mask(D, r)
        lp_mask_path = os.path.join(out_masks, f"mask_passabaixa_r{r}.png")
        save_uint8((lp_mask * 255).astype(np.uint8), lp_mask_path)

        lp_img_u8, lp_spec_u8 = apply_frequency_filter(F_shift, lp_mask)
        lp_img_path = os.path.join(out_filtered, f"filtro_passabaixa_r{r}.png")
        lp_spec_path = os.path.join(out_filtered, f"espectro_passabaixa_r{r}.png")
        save_uint8(lp_img_u8, lp_img_path)
        save_uint8(lp_spec_u8, lp_spec_path)

        results_filters.append(
            FilterResult(
                name="passa-baixa",
                parameter=f"r={r}",
                output_image=lp_img_path,
                output_spectrum=lp_spec_path,
                output_mask=lp_mask_path,
                stats=image_stats(lp_img_u8),
            )
        )

        # Passa-alta: atenua baixas frequencias e destaca detalhes/bordas.
        hp_mask = make_highpass_mask(D, r)
        hp_mask_path = os.path.join(out_masks, f"mask_passaalta_r{r}.png")
        save_uint8((hp_mask * 255).astype(np.uint8), hp_mask_path)

        hp_img_u8, hp_spec_u8 = apply_frequency_filter(F_shift, hp_mask)
        hp_img_path = os.path.join(out_filtered, f"filtro_passaalta_r{r}.png")
        hp_spec_path = os.path.join(out_filtered, f"espectro_passaalta_r{r}.png")
        save_uint8(hp_img_u8, hp_img_path)
        save_uint8(hp_spec_u8, hp_spec_path)

        results_filters.append(
            FilterResult(
                name="passa-alta",
                parameter=f"r={r}",
                output_image=hp_img_path,
                output_spectrum=hp_spec_path,
                output_mask=hp_mask_path,
                stats=image_stats(hp_img_u8),
            )
        )

    # (iv) Criacao das mascaras e (v)-(vi) aplicacao/reconstrucao para passa-faixa e rejeita-faixa.
    for r1, r2 in band_pairs:
        # Passa-faixa: preserva apenas componentes entre r1 e r2.
        bp_mask = make_bandpass_mask(D, r1, r2)
        bp_mask_path = os.path.join(out_masks, f"mask_passafaixa_r{r1}_{r2}.png")
        save_uint8((bp_mask * 255).astype(np.uint8), bp_mask_path)

        bp_img_u8, bp_spec_u8 = apply_frequency_filter(F_shift, bp_mask)
        bp_img_path = os.path.join(out_filtered, f"filtro_passafaixa_r{r1}_{r2}.png")
        bp_spec_path = os.path.join(out_filtered, f"espectro_passafaixa_r{r1}_{r2}.png")
        save_uint8(bp_img_u8, bp_img_path)
        save_uint8(bp_spec_u8, bp_spec_path)

        results_filters.append(
            FilterResult(
                name="passa-faixa",
                parameter=f"r1={r1},r2={r2}",
                output_image=bp_img_path,
                output_spectrum=bp_spec_path,
                output_mask=bp_mask_path,
                stats=image_stats(bp_img_u8),
            )
        )

        # Rejeita-faixa: remove componentes entre r1 e r2.
        br_mask = make_bandreject_mask(D, r1, r2)
        br_mask_path = os.path.join(out_masks, f"mask_rejeitafaixa_r{r1}_{r2}.png")
        save_uint8((br_mask * 255).astype(np.uint8), br_mask_path)

        br_img_u8, br_spec_u8 = apply_frequency_filter(F_shift, br_mask)
        br_img_path = os.path.join(out_filtered, f"filtro_rejeitafaixa_r{r1}_{r2}.png")
        br_spec_path = os.path.join(out_filtered, f"espectro_rejeitafaixa_r{r1}_{r2}.png")
        save_uint8(br_img_u8, br_img_path)
        save_uint8(br_spec_u8, br_spec_path)

        results_filters.append(
            FilterResult(
                name="rejeita-faixa",
                parameter=f"r1={r1},r2={r2}",
                output_image=br_img_path,
                output_spectrum=br_spec_path,
                output_mask=br_mask_path,
                stats=image_stats(br_img_u8),
            )
        )

    # Compressao no dominio da frequencia por limiar de magnitude.
    # Esta etapa elimina coeficientes de baixa magnitude para reduzir informacao espectral.
    compressed_images: Dict[str, np.ndarray] = {}
    compress_entries = []

    for pctl in compress_percentiles:
        comp_img_u8, comp_stats = compress_by_magnitude_threshold(F_shift, pctl)

        key = f"p{pctl}"
        comp_img_path = os.path.join(out_compress, f"compressao_percentil_{pctl}.png")
        save_uint8(comp_img_u8, comp_img_path)

        compressed_images[key] = comp_img_u8
        entry = {
            "label": key,
            "arquivo": comp_img_path,
            "compressao": comp_stats,
            "imagem": image_stats(comp_img_u8),
        }
        compress_entries.append(entry)

    # Histogramas antes e apos compressao (exigencia explicita do enunciado).
    hist_original_path = os.path.join(out_hist, "histograma_original.png")
    save_histogram(img_u8, hist_original_path, "Histograma - Imagem Original")

    hist_compressed_paths = {}
    for key, comp_img in compressed_images.items():
        path = os.path.join(out_hist, f"histograma_{key}.png")
        save_histogram(comp_img, path, f"Histograma - Imagem Comprimida ({key})")
        hist_compressed_paths[key] = path

    hist_compare_path = os.path.join(out_hist, "comparativo_histogramas_original_vs_comprimidas.png")
    save_histogram_comparison(img_u8, compressed_images, hist_compare_path)

    # Relatorio consolidado para rastreabilidade da correcao.
    payload = {
        "input": os.path.abspath(input_path),
        "outdir": os.path.abspath(outdir),
        "parametros": {
            "low_high_radii": radii,
            "band_pairs": band_pairs,
            "compress_threshold_percentiles": compress_percentiles,
        },
        "fft": {
            "espectro_centralizado": spec_orig_path,
        },
        "filtros": [
            {
                "tipo": r.name,
                "parametro": r.parameter,
                "mascara": r.output_mask,
                "espectro_filtrado": r.output_spectrum,
                "imagem_filtrada": r.output_image,
                "estatisticas": r.stats,
            }
            for r in results_filters
        ],
        "compressao": compress_entries,
        "histogramas": {
            "original": hist_original_path,
            "comprimidas": hist_compressed_paths,
            "comparativo": hist_compare_path,
        },
    }

    json_path = os.path.join(outdir, "resultados_questao2.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print("Questao 2 concluida com sucesso.")
    print(f"Entrada: {os.path.abspath(input_path)}")
    print(f"Saidas em: {os.path.abspath(outdir)}")
    print(f"Relatorio JSON: {json_path}")


if __name__ == "__main__":
    main()
