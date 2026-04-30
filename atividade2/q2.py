#!/usr/bin/env python3
"""
Questao 2 - Correcao Gama (implementacao manual)

Regras atendidas:
- Nao usa funcoes prontas de filtragem.
- Implementa a transformacao gama pixel a pixel.

Saidas:
- atividade2/saidas/saidas_questao2/imagem2_gama_<gamma>.png
- atividade2/saidas/saidas_questao2/comparativo_gama.png
- atividade2/saidas/saidas_questao2/resultados_q2.json
"""

import json
import os
from argparse import ArgumentParser

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


DEFAULT_GAMMAS = [0.25, 0.5, 1.0, 1.5, 2.0, 3.0]


def ensure_outdir(path):
    os.makedirs(path, exist_ok=True)


def resolve_default_input(script_dir):
    candidates = [
        os.path.join(script_dir, "imagem2.jpg"),
        os.path.join(script_dir, "image2.jpg"),
        os.path.join(script_dir, "image2.png"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def load_grayscale_u8(path):
    img = Image.open(path).convert("L")
    return np.array(img, dtype=np.uint8)


def save_grayscale_u8(img_u8, path):
    Image.fromarray(img_u8).save(path)


def correcao_gama_manual(img_u8, gamma):
    if gamma <= 0:
        raise ValueError("gamma deve ser > 0")

    h, w = img_u8.shape
    out = np.zeros((h, w), dtype=np.uint8)
    inv_gamma = 1.0 / gamma

    for y in range(h):
        for x in range(w):
            r = float(img_u8[y, x]) / 255.0
            s = r ** inv_gamma
            val = int(round(s * 255.0))
            if val < 0:
                val = 0
            elif val > 255:
                val = 255
            out[y, x] = val

    return out


def parse_gammas(text):
    values = []
    for token in text.split(","):
        token = token.strip()
        if not token:
            continue
        values.append(float(token))
    if not values:
        raise ValueError("lista de gammas vazia")
    return values


def gerar_comparativo(img_original, resultados, out_path):
    gammas = list(resultados.keys())
    total = len(gammas) + 1

    cols = 4
    rows = int(np.ceil(total / cols))

    plt.figure(figsize=(4 * cols, 3.5 * rows))

    plt.subplot(rows, cols, 1)
    plt.imshow(img_original, cmap="gray", vmin=0, vmax=255)
    plt.title("Original")
    plt.axis("off")

    for i, gamma in enumerate(gammas, start=2):
        plt.subplot(rows, cols, i)
        plt.imshow(resultados[gamma], cmap="gray", vmin=0, vmax=255)
        plt.title(f"gamma = {gamma}")
        plt.axis("off")

    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--input",
        "-i",
        required=False,
        help="Caminho da imagem de entrada. Se omitido, tenta imagem2.jpg/image2.png na pasta atividade2.",
    )
    parser.add_argument(
        "--outdir",
        "-o",
        default=None,
        help="Pasta de saida",
    )
    parser.add_argument(
        "--gammas",
        default=",".join(str(g) for g in DEFAULT_GAMMAS),
        help="Lista de gammas separada por virgula (ex.: 0.25,0.5,1.0)",
    )
    args = parser.parse_args()

    script_dir = os.path.dirname(__file__)
    input_path = args.input if args.input else resolve_default_input(script_dir)
    if not input_path:
        raise FileNotFoundError(
            "Imagem de entrada nao encontrada. Informe --input ou adicione imagem2.jpg/image2.png em atividade2/."
        )

    outdir = args.outdir if args.outdir else os.path.join(script_dir, "saidas", "saidas_questao2")
    ensure_outdir(outdir)

    gammas = parse_gammas(args.gammas)
    img = load_grayscale_u8(input_path)

    resultados_imgs = {}
    metricas = {}

    for gamma in gammas:
        out = correcao_gama_manual(img, gamma)
        resultados_imgs[gamma] = out

        out_name = f"imagem2_gama_{gamma}.png"
        out_path = os.path.join(outdir, out_name)
        save_grayscale_u8(out, out_path)

        metricas[str(gamma)] = {
            "arquivo": out_path,
            "min": int(out.min()),
            "max": int(out.max()),
            "media": float(np.mean(out)),
            "desvio_padrao": float(np.std(out)),
            "shape": [int(out.shape[0]), int(out.shape[1])],
        }

    comp_path = os.path.join(outdir, "comparativo_gama.png")
    gerar_comparativo(img, resultados_imgs, comp_path)

    payload = {
        "input": input_path,
        "outdir": outdir,
        "gammas": gammas,
        "comparativo": comp_path,
        "resultados": metricas,
    }

    json_path = os.path.join(outdir, "resultados_q2.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print("Questao 2 concluida.")
    print(f"Entrada: {input_path}")
    print(f"Saidas em: {outdir}")


if __name__ == "__main__":
    main()
