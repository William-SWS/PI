"""
Questão 1 — Operações Morfológicas em Imagens Binárias

Saída:
    atividade4/imagens/saidas_questao1/  (28 imagens PNG)
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
OUT_DIR = IMG_DIR / "saidas_questao1"
TAMANHOS_EE = [3, 5, 15]
LIMIAR = 127


def to_gray(img: np.ndarray) -> np.ndarray:  # BGR -> grayscale (ITU-R BT.601)
    return (
        0.299 * img[:, :, 2] +
        0.587 * img[:, :, 1] +
        0.114 * img[:, :, 0]
    ).astype(np.uint8)


def binarizar(img: np.ndarray, limiar: int = LIMIAR) -> np.ndarray:  # 255 se > limiar, 0 c.c.
    h, w = img.shape
    binaria = np.zeros((h, w), dtype=np.uint8)
    for y in range(h):
        row = img[y, :]
        for x in range(w):
            binaria[y, x] = 255 if row[x] > limiar else 0
    return binaria


def criar_ee(tamanho: int) -> np.ndarray:  # elemento estruturante quadrado
    return np.ones((tamanho, tamanho), dtype=np.uint8)


def erosao(img: np.ndarray, ee: np.ndarray) -> np.ndarray:  # 1 sse todos vizinhos == 1
    h, w = img.shape
    eh, el = ee.shape
    mh, ml = eh // 2, el // 2
    out = np.zeros((h, w), dtype=np.uint8)

    for y in range(mh, h - mh):
        for x in range(ml, w - ml):
            if np.min(img[y - mh:y - mh + eh, x - ml:x - ml + el]) == 255:
                out[y, x] = 255
    return out


def dilatacao(img: np.ndarray, ee: np.ndarray) -> np.ndarray:  # 1 sse algum vizinho == 1
    h, w = img.shape
    eh, el = ee.shape
    mh, ml = eh // 2, el // 2
    out = np.zeros((h, w), dtype=np.uint8)

    for y in range(mh, h - mh):
        for x in range(ml, w - ml):
            if np.max(img[y - mh:y - mh + eh, x - ml:x - ml + el]) == 255:
                out[y, x] = 255
    return out


def abertura(img: np.ndarray, ee: np.ndarray) -> np.ndarray:  # erosao -> dilatacao
    return dilatacao(erosao(img, ee), ee)


def fechamento(img: np.ndarray, ee: np.ndarray) -> np.ndarray:  # dilatacao -> erosao
    return erosao(dilatacao(img, ee), ee)


def processar_imagem(img_bin: np.ndarray, nome: str, outdir: Path) -> None:  # 4 ops x 3 EE
    log.info("Processando %s ...", nome)

    for tam in TAMANHOS_EE:
        ee = criar_ee(tam)
        suf = f"ee{tam}x{tam}"

        ops: dict[str, np.ndarray] = {
            "erosao": erosao(img_bin, ee),
            "dilatacao": dilatacao(img_bin, ee),
            "abertura": abertura(img_bin, ee),
            "fechamento": fechamento(img_bin, ee),
        }

        for op_name, resultado in ops.items():
            path = outdir / f"{nome}_{op_name}_{suf}.png"
            cv2.imwrite(str(path), resultado)
            log.debug("  -> %s", path.name)

    log.info("  %s — concluído (4 ops × %d EE)", nome, len(TAMANHOS_EE))


def main() -> None:  # pipeline: carrega -> grayscale -> binaria -> morfologia
    log.info("Pipeline de operações morfológicas")
    log.info("Diretório de saída: %s", OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    entradas = [
        ("1_terno", IMG_DIR / "1_terno.png"),
        ("1_vestido", IMG_DIR / "1_vestido.png"),
    ]

    for nome, path in entradas:
        log.info("Carregando %s ...", path.name)
        img = cv2.imread(str(path))
        if img is None:
            log.error("Falha ao carregar %s", path)
            sys.exit(1)

        gray = to_gray(img)
        cv2.imwrite(str(OUT_DIR / f"{nome}_gray.png"), gray)
        log.info("  Grayscale salva.")

        binaria = binarizar(gray)
        cv2.imwrite(str(OUT_DIR / f"{nome}_binaria.png"), binaria)
        log.info("  Binária salva (limiar=%d).", LIMIAR)

        processar_imagem(binaria, nome, OUT_DIR)

    total = len(entradas) * (1 + 1 + len(TAMANHOS_EE) * 4)
    log.info("Concluído! %d imagens geradas em %s", total, OUT_DIR)


if __name__ == "__main__":
    main()
