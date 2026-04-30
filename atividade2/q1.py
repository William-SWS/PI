#!/usr/bin/env python3
"""
Aplica 11 filtros (h1..h11) por convolução manual em uma imagem monocromática.

Regras:
- Não usar funções prontas de filtragem (ex: OpenCV `filter2D`, `GaussianBlur`).
- Permitido usar `Pillow` para I/O e `numpy` para operações de array.

Saídas:
- Imagens geradas salvas em `atividade2/saidas/saidas_questao2` como `q1_h1.png` ... `q1_h11.png`.
- `resultados_q1.json` com estatísticas por filtro.
"""
import os
import sys
import json
from argparse import ArgumentParser
from math import exp

import numpy as np
from PIL import Image


def ensure_outdir(path):
	os.makedirs(path, exist_ok=True)


def load_image_grayscale(path):
	img = Image.open(path).convert('L')
	return np.array(img, dtype=np.float32)


def save_image_uint8(arr, path):
	arr_u8 = np.clip(arr, 0, 255).astype(np.uint8)
	Image.fromarray(arr_u8).save(path)


def pad_image(img, pad_h, pad_w, mode='reflect'):
	if mode == 'zero':
		padded = np.zeros((img.shape[0] + 2 * pad_h, img.shape[1] + 2 * pad_w), dtype=img.dtype)
		padded[pad_h:pad_h+img.shape[0], pad_w:pad_w+img.shape[1]] = img
		return padded
	elif mode == 'reflect':
		return np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='reflect')
	else:
		raise ValueError('Unknown pad mode')


def convolve2d(image, kernel, pad_mode='reflect'):
	# kernel: 2D numpy array
	kh, kw = kernel.shape
	ih, iw = image.shape
	ph, pw = kh // 2, kw // 2

	padded = pad_image(image, ph, pw, mode=pad_mode)
	out = np.zeros_like(image, dtype=np.float32)

	# Flip the kernel for convolution (mathematically correct)
	k = np.flip(np.flip(kernel, axis=0), axis=1)

	for y in range(ih):
		for x in range(iw):
			region = padded[y:y+kh, x:x+kw]
			out[y, x] = np.sum(region * k)

	return out


def make_gaussian_kernel(size, sigma):
	ax = np.arange(-size // 2 + 1., size // 2 + 1.)
	xx, yy = np.meshgrid(ax, ax)
	kernel = np.exp(-(xx**2 + yy**2) / (2. * sigma**2))
	kernel = kernel / np.sum(kernel)
	return kernel


def normalize_kernel(kernel):
	s = np.sum(kernel)
	if s != 0:
		return kernel / s
	return kernel


def main():
	p = ArgumentParser()
	p.add_argument('--input', '-i', required=False, help='Caminho da imagem de entrada (qualquer formato). Se omitido, usa atividade2/imageq1.png')
	p.add_argument('--outdir', '-o', default='atividade2/saidas/saidas_questao2', help='Pasta de saída')
	args = p.parse_args()

	inp = args.input
	# Se usuário não forneceu arquivo, usar imageq1.png ao lado deste script
	if not inp:
		default_img = os.path.join(os.path.dirname(__file__), 'imageq1.png')
		if os.path.exists(default_img):
			inp = default_img
			print('Nenhum input fornecido — usando imagem padrão:', inp)
		else:
			p.error('Nenhum arquivo de entrada fornecido e imagem padrão não encontrada: ' + default_img)
	outdir = args.outdir
	ensure_outdir(outdir)

	img = load_image_grayscale(inp)

	# Definição dos 11 filtros (h1..h11)
	# Observação: caso o enunciado forneça kernels específicos, substitua aqui.
	kernels = {}

	# h1: Média 3x3 (box filter)
	kernels['h1'] = np.ones((3,3), dtype=np.float32) / 9.0

	# h2: Gaussian 5x5 aproximado (será gerado manualmente)
	kernels['h2'] = make_gaussian_kernel(5, sigma=1.0)

	# h3: Sobel X
	kernels['h3'] = np.array([[-1,0,1],[-2,0,2],[-1,0,1]], dtype=np.float32)

	# h4: Sobel Y
	kernels['h4'] = np.array([[-1,-2,-1],[0,0,0],[1,2,1]], dtype=np.float32)

	# h5: Prewitt X
	kernels['h5'] = np.array([[-1,0,1],[-1,0,1],[-1,0,1]], dtype=np.float32)

	# h6: Prewitt Y
	kernels['h6'] = np.array([[-1,-1,-1],[0,0,0],[1,1,1]], dtype=np.float32)

	# h7: Laplaciano 3x3
	kernels['h7'] = np.array([[0,-1,0],[-1,4,-1],[0,-1,0]], dtype=np.float32)

	# h8: High-pass (sharpen)
	kernels['h8'] = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]], dtype=np.float32)

	# h9: Emboss
	kernels['h9'] = np.array([[-2,-1,0],[-1,1,1],[0,1,2]], dtype=np.float32)

	# h10: Small averaging 5x5
	kernels['h10'] = np.ones((5,5), dtype=np.float32) / 25.0

	# h11: Unsharp mask kernel (approx) -> original + amount*(original - blurred)
	# We'll implement unsharp via convolution: kernel = delta + amount*(delta - gaussian)
	gauss5 = make_gaussian_kernel(5, sigma=1.0)
	delta = np.zeros((5,5), dtype=np.float32)
	delta[2,2] = 1.0
	amount = 1.0
	kernels['h11'] = delta + amount*(delta - gauss5)

	results = {}

	for i, (name, k) in enumerate(kernels.items(), start=1):
		print(f'Aplicando {name}...')
		out = convolve2d(img, k, pad_mode='reflect')

		# Alguns kernels (gradientes) produzem valores negativos; normalizamos para 0-255
		# Estratégia: reescala linearmente para 0-255 para visualização
		minv, maxv = out.min(), out.max()
		if maxv - minv > 0:
			out_vis = (out - minv) * (255.0 / (maxv - minv))
		else:
			out_vis = np.clip(out, 0, 255)

		fname = os.path.join(outdir, f'q1_{name}.png')
		save_image_uint8(out_vis, fname)

		results[name] = {
			'kernel_shape': k.shape,
			'kernel': k.tolist(),
			'min': float(minv),
			'max': float(maxv),
			'mean': float(np.mean(out)),
			'saved_image': fname
		}

	json_path = os.path.join(outdir, 'resultados_q1.json')
	with open(json_path, 'w', encoding='utf-8') as f:
		json.dump(results, f, indent=2, ensure_ascii=False)

	print('Concluído. Resultados salvos em', outdir)


if __name__ == '__main__':
	main()

