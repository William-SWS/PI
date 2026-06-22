# AGENTS.md — PI (Processamento de Imagens)

## Project Structure

```
PI/
├── atividade1/          # 6 basic ops (Jupyter notebooks, PIL)
├── atividade2/          # 11 spatial filters, gamma, FFT (Python CLI, PIL)
│   ├── q1.py, q2.py, questao2.py
│   ├── saidas/
│   └── requirements.txt
├── atividade3/          # DCT compression, image descriptors (Python scripts, OpenCV)
│   ├── scripts/q1.py, q2.py
│   ├── images/, resultados/
│   └── gerar_relatorio.py   (fpdf2)
├── atividade4/          # morphology, Canny+HOG, watershed (Python scripts, OpenCV)
│   ├── questao1.py, questao2.py, questao3.py
│   └── imagens/ (input + saidas_questao{1,2,3}/)
├── engine/              # standalone practice scripts (not imported by atividades)
├── imagens questao 3/   # legacy test images
└── venv/                # Python virtual environment
```

## Execution

```bash
# Atividade 2 (argparse CLI, PIL, JSON output)
pip install -r atividade2/requirements.txt
python atividade2/q1.py --input atividade2/imageq1.png
python atividade2/q2.py --gammas 0.5,1.0,2.0
python atividade2/questao2.py --input atividade2/image2.png

# Atividade 3 (hardcoded paths, OpenCV, no CLI args)
pip install opencv-python numpy matplotlib
python atividade3/scripts/q1.py
python atividade3/scripts/q2.py
python atividade3/gerar_relatorio.py

# Atividade 4 (hardcoded paths, OpenCV, logging)
python atividade4/questao1.py     # -> imagens/saidas_questao1/
python atividade4/questao2.py     # -> imagens/saidas_questao2/
python atividade4/questao3.py     # -> imagens/saidas_questao3/
```

## Library/Pattern by Atividade

| | Library | Args | Output | I/O | Style |
|---|---|---|---|---|---|
| 1 | PIL | None (notebook) | Images | `Image.open` | Notebook cells |
| 2 | PIL | `argparse --input/--outdir` | PNG + JSON | `Image.open/.save` | Scripts, `os.path` |
| 3 | OpenCV | None (hardcoded) | PNG only | `cv2.imread/.imwrite` | Scripts, `os.path` |
| 4 | OpenCV | None (hardcoded) | PNG only | `cv2.imread/.imwrite` | Scripts, `pathlib.Path`, `logging` |

## Code Style (atividade4)

```python
from __future__ import annotations
import logging
import sys
from pathlib import Path
import cv2, numpy as np

log = logging.getLogger(__name__)
SCRIPT_DIR = Path(__file__).resolve().parent
OUT_DIR = SCRIPT_DIR / "imagens" / "saidas_questaoN"

def func(arg: np.ndarray) -> np.ndarray:  # inline comment only (no docstring)
    ...

def main() -> None: ...
if __name__ == "__main__":
    main()
```

## Critical Constraints

- All algorithms must be manual — no `cv2.filter2D`, `cv2.GaussianBlur`, `cv2.dct`, `cv2.morphologyEx`, etc.
- Allowed for I/O only: PIL (`Image.open/.save`) or OpenCV (`cv2.imread/.imwrite`)
- Allowed for computation: NumPy, Matplotlib display/save
- Output images: always PNG, uint8 [0, 255], clipping required
- Luminance: `0.114*B + 0.587*G + 0.299*R` — NOT average of channels; NOT `cv2.cvtColor`
- Image paths resolved via `SCRIPT_DIR` — run scripts from project root (`/home/william/Projetos/PI`)
- OpenCV loads images as BGR; grayscale conversion must be manual

## Common Pitfalls

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'cv2'` | `pip install opencv-python` (not `cv2`) |
| Image not found | Run from project root; scripts use `SCRIPT_DIR`-relative paths |
| Wrong luminance | `0.114*B + 0.587*G + 0.299*R`; openCV BGR channel order matters |
| Output looks wrong | Clip to [0,255], cast to `np.uint8` before saving |
| JSON fails | Wrap numpy values: `int(x)`, `float(x)` |
| Forbidden function used | Replace with manual loops or NumPy ops |
| Color output garbled | OpenCV saves BGR; Matplotlib expects RGB |

## Atividade 3 Specifics

- `q1.py`: DCT compression with manual DCT-II/IDCT-III, configurable `BLOCK_SIZE` (default 64), quality factor, quantization matrix
- `q2.py`: 5 image descriptors — mean, variance, energy, horizontal/vertical difference (manual loops)
- PDF report by `gerar_relatorio.py` (fpdf2) → `relatorio_atividade3.pdf`

## Atividade 4 Specifics

- `questao1.py`: Morphological ops (erosion, dilation, opening, closing) with square SEs of 3, 5, 15 on binary images
- `questao2.py`: Canny stages 1-2 (Gaussian filter, Sobel gradient, magnitude) + simplified HOG descriptor
- `questao3.py`: Marker-based watershed (threshold → closing → distance transform → local maxima → flood fill)
- All scripts use structured logging (`logging.INFO`), full variable names, inline `#` comments
