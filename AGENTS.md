# AGENTS.md - PI Project (Processamento de Imagens)

## Project Overview
**PI** is an educational image processing project emphasizing **manual algorithm implementations**. Two activities (atividade1, atividade2) contain Jupyter notebooks paired with Python CLI scripts that process images, calculate metrics, and output structured JSON results.

### Key Constraints
- ⚠️ **Manual implementation required**: No ready-made library filters (`cv2.filter2D`, `cv2.GaussianBlur`, etc.)
- ✓ **Allowed libraries**: PIL/Pillow for I/O, NumPy for arrays, Matplotlib for visualization
- ✓ **All I/O structured**: JSON metadata + PNG images in `saidas/saidas_questaoX/` directories

---

## File Organization

```
PI/
├── atividade1/                 # Activity 1 (basic operations)
├── atividade2/                 # Activity 2 (Q1: filters, Q2: gamma, Q2B: FFT)
│   ├── q1.py, q1.ipynb        # 11 spatial filters (manual convolution)
│   ├── q2.py, q2.ipynb        # Gamma correction
│   ├── questao2.py            # FFT domain filtering
│   ├── requirements.txt        # Dependencies: Pillow, numpy, matplotlib, opencv-python
│   ├── README.md              # Execution guide
│   └── saidas/                # Outputs directory
├── engine/                     # Shared utilities (metricas.py, fourier.py, gaussian.py, etc.)
├── imagens questao 3/         # Test images
└── .git/                       # Version control
```

---

## How to Execute

### Quick Start
```bash
cd /home/william/Projetos/PI
pip install -r atividade2/requirements.txt

# Run Q1 (spatial filters)
python atividade2/q1.py --input atividade2/imageq1.png

# Run Q2 (gamma correction)
python atividade2/q2.py --gammas 0.5,1.0,2.0

# Run Q2B (FFT domain)
python atividade2/questao2.py --input atividade2/image2.png
```

### Standard CLI Arguments
- `--input` / `-i`: Image path (required or auto-detects fallback)
- `--outdir` / `-o`: Output directory (defaults to `atividade2/saidas/saidas_questaoX`)
- Question-specific: `--gammas`, `--radii`, `--percentiles`, `--band_pairs`

---

## Key Files to Reference

| File | Purpose | Pattern |
|------|---------|---------|
| [atividade2/q1.py](atividade2/q1.py) | Manual convolution (11 kernels) | CLI + JSON metrics |
| [atividade2/q2.py](atividade2/q2.py) | Pixel-wise gamma transform | Multi-output handling |
| [atividade2/questao2.py](atividade2/questao2.py) | FFT filtering + compression | Complex workflow with masks |
| [atividade2/README.md](atividade2/README.md) | Execution docs | Latest Q1/Q2 commands |
| [engine/metricas.py](engine/metricas.py) | Statistics helpers | Reusable metric calculation |

---

## Core Conventions

### 1. Image I/O
```python
# Load
img = Image.open(path).convert('L')  # Grayscale with PIL
arr = np.array(img, dtype=np.float32)

# Grayscale conversion (manual, NOT cv2.cvtColor)
gray = 0.114 * b_chan + 0.587 * g_chan + 0.299 * r_chan  # Luminance formula

# Save
arr_u8 = np.clip(arr, 0, 255).astype(np.uint8)
Image.fromarray(arr_u8).save(output_path)
```

### 2. Output Structure (Always)
- **Images**: `q1_h1.png`, `q1_h2.png`, ..., `imagem2_gama_0.5.png`, etc.
- **Metadata**: `resultado_metricas_execucao.json` with timestamp, parameters, metrics

### 3. Metrics JSON Format
```json
{
  "timestamp": "2026-05-09T10:30:00",
  "input": "/path/to/image.jpg",
  "outdir": "/path/to/saidas/",
  "parameters": {...},
  "resultados": {
    "filename": {
      "arquivo": "path/to/output.png",
      "min": 0,
      "max": 255,
      "mean": 128.5,
      "desvio_padrao": 50.2,
      "shape": [400, 680]
    }
  }
}
```

### 4. For Every Output Image, Calculate
```python
{
    "min": int(img.min()),
    "max": int(img.max()),
    "mean": float(np.mean(img)),
    "desvio_padrao": float(np.std(img)),  # Portuguese key name
    "shape": [int(img.shape[0]), int(img.shape[1])]
}
```

---

## Common Patterns

### CLI Setup
```python
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--input', '-i', required=False)
parser.add_argument('--outdir', '-o', default='atividade2/saidas/saidas_questao2')
args = parser.parse_args()

if not args.input:
    default = os.path.join(os.path.dirname(__file__), 'imagem_padrao.jpg')
    if os.path.exists(default):
        args.input = default
    else:
        parser.error('No input image found')
```

### Directory Handling
```python
def ensure_outdir(path):
    os.makedirs(path, exist_ok=True)

ensure_outdir(args.outdir)
```

### Normalize to uint8 (for visualization)
```python
def minmax_to_uint8(arr):
    arr = np.asarray(arr, dtype=np.float32)
    min_v, max_v = float(arr.min()), float(arr.max())
    if max_v <= min_v:
        return np.zeros_like(arr, dtype=np.uint8)
    norm = (arr - min_v) * (255.0 / (max_v - min_v))
    return np.clip(norm, 0, 255).astype(np.uint8)
```

### Save Results
```python
payload = {
    "input": str(input_path),
    "outdir": str(output_dir),
    "parameters": {...},
    "resultados": metrics_dict
}
with open(os.path.join(args.outdir, 'resultado_metricas_execucao.json'), 'w') as f:
    json.dump(payload, f, indent=2, ensure_ascii=False)
```

---

## ⚠️ Common Pitfalls

| Problem | Solution |
|---------|----------|
| Module import fails | `pip install -r atividade2/requirements.txt` from project root |
| Image not found | Use absolute paths or place in script directory; check fallback chain |
| Wrong color formula | Use EXACT luminance: `0.114*B + 0.587*G + 0.299*R` (not avg) |
| JSON serialization error | Wrap NumPy: `int(x)`, `float(x)` |
| Output image looks wrong | Ensure uint8 conversion + clipping to [0, 255] |
| "Forbidden function used" | Replace `cv2.filter2D()` with manual convolution loops |

---

## Implementation Checklist for New Scripts

- [ ] Accept `--input`, `--outdir`, and question-specific params via argparse
- [ ] Implement core algorithm **manually** (no library shortcuts)
- [ ] Load images with PIL, convert to uint8 for saving
- [ ] Calculate metrics (min, max, mean, std, shape) for all outputs
- [ ] Normalize output arrays using `minmax_to_uint8()` before saving
- [ ] Save all images as PNG with descriptive filenames
- [ ] Generate `resultado_metricas_execucao.json` with complete metadata
- [ ] Include docstring explaining rules and output locations
- [ ] Test with sample image; verify outputs exist and JSON is valid
- [ ] Use Portuguese key names in JSON (`desvio_padrao`, not `std_dev`)

---

## Debugging Commands

```bash
# Verify dependencies
python -c "import PIL, numpy, cv2, matplotlib; print('✓ All deps OK')"

# Test script help
python atividade2/q1.py --help

# Validate JSON output
python -m json.tool atividade2/saidas/saidas_questao2/resultado_metricas_execucao.json

# List outputs
ls -lah atividade2/saidas/saidas_questao2/
```

---

## Next Steps for Customization

Consider adding agent skills for:
- **Backend Development**: Setup validation, error handling patterns
- **Testing**: Pytest structure for image comparison tests
- **Documentation**: Standard docstring format for image processing functions
- **Security**: Input validation for file paths and numeric parameters
