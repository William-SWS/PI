"""
Gera o relatório PDF da Atividade 4 — Processamento de Imagens.
"""

from __future__ import annotations

from pathlib import Path

from fpdf import FPDF

SCRIPT_DIR = Path(__file__).resolve().parent
OUT_DIR1 = SCRIPT_DIR / "imagens" / "saidas_questao1"
OUT_DIR2 = SCRIPT_DIR / "imagens" / "saidas_questao2"
OUT_DIR3 = SCRIPT_DIR / "imagens" / "saidas_questao3"

FONT_DIR = Path("/usr/share/fonts/TTF")


class Relatorio(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("DJV", "", FONT_DIR / "DejaVuSans.ttf", uni=True)
        self.add_font("DJV", "B", FONT_DIR / "DejaVuSans-Bold.ttf", uni=True)
        self.add_font("DJVM", "", FONT_DIR / "DejaVuSansMono.ttf", uni=True)

    def header(self):
        if self.page_no() > 1:
            self.set_font("DJV", "", 8)
            self.cell(0, 8, "Processamento de Imagens — Atividade 4", align="C", new_x="LMARGIN", new_y="NEXT")
            self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("DJV", "", 8)
        self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", align="C")

    def secao(self, titulo):
        self.set_font("DJV", "B", 14)
        self.ln(4)
        self.cell(0, 10, titulo, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 0, 0)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def subsecao(self, titulo):
        self.set_font("DJV", "B", 11)
        self.ln(2)
        self.cell(0, 8, titulo, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def paragrafo(self, texto):
        self.set_font("DJV", "", 10)
        self.multi_cell(0, 5, texto)
        self.ln(2)

    def codigo(self, texto):
        self.set_font("DJVM", "", 7.5)
        self.set_fill_color(240, 240, 240)
        for linha in texto.strip().split("\n"):
            self.cell(0, 4.5, "  " + linha, new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(2)

    def imagem(self, path, w=80):
        if path.exists():
            self.image(str(path), x=(self.w - w) / 2, w=w)
            self.ln(2)


def main():
    pdf = Relatorio()
    pdf.alias_nb_pages()

    # --- CAPA ---
    pdf.add_page()
    pdf.ln(60)
    pdf.set_font("DJV", "B", 22)
    pdf.cell(0, 14, "Universidade Estadual do Ceará", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DJV", "", 14)
    pdf.cell(0, 10, "Curso de Ciência da Computação", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, "Disciplina: Processamento de Imagens", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font("DJV", "B", 18)
    pdf.cell(0, 12, "Atividade 4 — Relatório", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font("DJV", "", 12)
    pdf.cell(0, 8, "Aluno: Samuel William Silva Almeida", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Professor: Matheus Araújo", align="C", new_x="LMARGIN", new_y="NEXT")


    # --- INTRODUÇÃO ---
    pdf.add_page()
    pdf.secao("1. Introdução")
    pdf.paragrafo(
        "Esta atividade tem como objetivo introduzir técnicas fundamentais de "
        "morfologia matemática e segmentação de imagens, por meio da implementação "
        "prática de operadores que permitem extrair, separar e estruturar informações "
        "relevantes em imagens digitais. Foram implementados três conjuntos de algoritmos: "
        "operações morfológicas (erosão, dilatação, abertura e fechamento), detecção de "
        "bordas com as primeiras etapas do algoritmo de Canny juntamente com o descritor "
        "HOG simplificado, e segmentação por watershed baseado em marcadores."
    )
    pdf.paragrafo(
        "Todas as implementações foram feitas manualmente em Python, utilizando as "
        "bibliotecas OpenCV e NumPy. O OpenCV foi utilizado exclusivamente para "
        "carregamento e salvamento de imagens, enquanto o NumPy foi empregado para "
        "as operações computacionais. O tema central das imagens utilizadas é o "
        "universo da moda e vestuário: temos fotos de ternos, vestidos, modelos "
        "e pilhas de roupas."
    )

    # --- QUESTÃO 1 ---
    pdf.add_page()
    pdf.secao("2. Questão 1 — Operações Morfológicas")
    pdf.paragrafo(
        "Foram implementadas as operações morfológicas de erosão e dilatação em imagens "
        "binárias obtidas a partir de duas imagens do tema (terno e vestido). Utilizaram-se "
        "elementos estruturantes quadrados de três tamanhos distintos: 3×3, 5×5 e 15×15. "
        "A partir dessas operações primitivas, construíram-se também as operações de "
        "abertura (erosão seguida de dilatação) e fechamento (dilatação seguida de erosão)."
    )

    pdf.subsecao("2.1 Implementação")
    pdf.codigo(
        """def criar_ee(tamanho):
    return np.ones((tamanho, tamanho), dtype=np.uint8)

def erosao(img, ee):
    for y in range(mh, h - mh):
        for x in range(ml, w - ml):
            if np.min(img[y-mh:y-mh+eh, x-ml:x-ml+el]) == 255:
                out[y, x] = 255

def dilatacao(img, ee):
    for y in range(mh, h - mh):
        for x in range(ml, w - ml):
            if np.max(img[y-mh:y-mh+eh, x-ml:x-ml+el]) == 255:
                out[y, x] = 255

def abertura(img, ee):
    return dilatacao(erosao(img, ee), ee)

def fechamento(img, ee):
    return erosao(dilatacao(img, ee), ee)"""
    )

    pdf.subsecao("2.2 Imagens originais e binarizadas")
    pdf.paragrafo(
        "As imagens do terno e do vestido foram convertidas para tons de cinza "
        "utilizando a fórmula de luminância ITU-R BT.601 (0,299R + 0,587G + 0,114B) "
        "e binarizadas com limiar 127."
    )
    pdf.imagem(OUT_DIR1 / "1_terno_gray.png", w=65)
    pdf.imagem(OUT_DIR1 / "1_terno_binaria.png", w=65)
    pdf.imagem(OUT_DIR1 / "1_vestido_gray.png", w=65)
    pdf.imagem(OUT_DIR1 / "1_vestido_binaria.png", w=65)

    pdf.subsecao("2.3 Resultados — Erosão, Dilatação, Abertura e Fechamento")
    pdf.paragrafo(
        "As figuras a seguir apresentam os resultados para cada operação com elementos "
        "estruturantes de 3×3, 5×5 e 15×15. Observa-se que, com EE 3×3, as alterações "
        "são sutis; com EE 5×5, os efeitos tornam-se mais pronunciados; já com EE 15×15, "
        "ocorre transformação significativa."
    )

    for nome_img in ["1_terno", "1_vestido"]:
        pdf.subsecao(f"Resultados — {'Terno' if 'terno' in nome_img else 'Vestido'}")
        for op in ["erosao", "dilatacao", "abertura", "fechamento"]:
            path = OUT_DIR1 / f"{nome_img}_{op}_ee5x5.png"
            pdf.imagem(path, w=60)

    pdf.paragrafo(
        "Análise: A erosão reduz o tamanho dos objetos, eliminando pequenas projeções "
        "e ruídos. A dilatação expande os objetos, preenchendo pequenos buracos. "
        "A abertura suaviza contornos e remove protuberâncias finas. O fechamento "
        "preenche pequenos laços e une regiões próximas. A escolha do tamanho do "
        "EE depende da escala dos detalhes que se deseja preservar ou remover."
    )

    # --- QUESTÃO 2 ---
    pdf.add_page()
    pdf.secao("3. Questão 2 — Filtros, Detecção de Bordas (Canny) e HOG")
    pdf.paragrafo(
        "Implementaram-se as duas primeiras etapas do algoritmo de detecção de bordas "
        "de Canny: (1) suavização por filtro gaussiano com kernel 5×5 e σ = 1,4 e "
        "(2) cálculo do gradiente utilizando operadores de Sobel 3×3 implementados "
        "manualmente. Como extensão, implementou-se o descritor HOG simplificado com "
        "células de 8×8 pixels e 9 bins de orientação."
    )

    pdf.subsecao("3.1 Implementação")
    pdf.codigo(
        """def gaussian_kernel_2d(kernel_size, sigma):
    kernel = np.zeros((kernel_size, kernel_size))
    center = kernel_size // 2
    for i in range(kernel_size):
        for j in range(kernel_size):
            dx, dy = i - center, j - center
            kernel[i,j] = exp(-(dx**2+dy**2)/(2*sigma**2)) / (2*pi*sigma**2)
    return kernel / kernel.sum()

def convolve_2d(image, kernel):
    padded = np.pad(image, pad_width=..., mode="edge")
    for i in range(height):
        for j in range(width):
            output[i,j] = np.sum(padded[i:i+kh, j:j+kw] * kernel)

def sobel_gradient(image):
    gx = convolve_2d(image, [[-1,0,1],[-2,0,2],[-1,0,1]])
    gy = convolve_2d(image, [[-1,-2,-1],[0,0,0],[1,2,1]])
    return np.sqrt(gx**2 + gy**2), np.arctan2(gy, gx)"""
    )

    pdf.subsecao("3.2 Imagem de entrada")
    pdf.paragrafo("A imagem utilizada foi a de um modelo (2_modelo.png), relacionada ao tema moda e vestuário.")
    pdf.imagem(OUT_DIR2 / "2_modelo_grayscale.png", w=80)

    pdf.subsecao("3.3 Filtro Gaussiano e Gradientes")
    pdf.paragrafo(
        "O filtro gaussiano suaviza a imagem, reduzindo ruídos antes do cálculo do gradiente. "
        "As componentes do gradiente nos eixos X e Y foram calculadas com os operadores "
        "Sobel. A magnitude do gradiente evidencia as bordas."
    )
    pdf.imagem(OUT_DIR2 / "2_modelo_gaussian_filtered.png", w=60)
    pdf.imagem(OUT_DIR2 / "2_modelo_gradient_x.png", w=60)
    pdf.imagem(OUT_DIR2 / "2_modelo_gradient_y.png", w=60)
    pdf.imagem(OUT_DIR2 / "2_modelo_gradient_magnitude.png", w=80)

    pdf.subsecao("3.4 Descritor HOG")
    pdf.paragrafo(
        "O HOG divide a imagem em células de 8×8 pixels. Para cada pixel, o ângulo de "
        "orientação do gradiente é quantizado em um dos 9 bins (0°–180°) e o histograma "
        "é ponderado pela magnitude do gradiente. A visualização abaixo mostra linhas "
        "proporcionais ao valor de cada bin em cada célula."
    )
    pdf.codigo(
        """def hog_descriptor(magnitude, orientation, cell_size=8, nbins=9):
    for each cell:
        hist = zeros(nbins)
        for each pixel in cell:
            bin = quantize(orientation[pixel], nbins)
            hist[bin] += magnitude[pixel]
        cell_histograms.append(hist)
    return cell_histograms"""
    )
    pdf.imagem(OUT_DIR2 / "2_modelo_hog_visualization.png", w=80)

    pdf.paragrafo(
        "O vetor de características gerado possui 69×127 células × 9 bins = "
        "aproximadamente 79 mil features. Cada feature representa a contribuição "
        "de uma orientação específica em uma região local, capturando a estrutura "
        "das bordas da imagem de forma compacta."
    )

    # --- QUESTÃO 3 ---
    pdf.add_page()
    pdf.secao("4. Questão 3 — Segmentação Watershed")
    pdf.paragrafo(
        "Implementou-se um método de segmentação baseado em marcadores seguido da "
        "aplicação do algoritmo Watershed, com o objetivo de separar objetos em "
        "regiões próximas ou parcialmente sobrepostas. A imagem utilizada foi a de "
        "chapéus empilhados (3_chapeus.png)."
    )

    pdf.subsecao("4.1 Pipeline")
    pdf.paragrafo(
        "O pipeline segue as etapas: (1) limiarização (threshold=127) para binarização; "
        "(2) fechamento morfológico com kernel 5×5 para limpeza de ruídos; "
        "(3) distance transform de Chamfer 3-4-5 em dois passes para gerar o mapa de "
        "distâncias; (4) identificação de máximos locais (acima de 85% do valor máximo) "
        "como marcadores de primeiro plano; (5) watershed por inundação com priority "
        "queue ordenada por distância decrescente; (6) detecção das linhas de fronteira "
        "entre segmentos adjacentes."
    )

    pdf.subsecao("4.2 Implementação")
    pdf.codigo(
        """def distance_transform_chamfer(binary):
    # Forward pass: top-left to bottom-right
    for y in range(height):
        for x in range(width):
            d[y,x] = min(d[y,x], d[y-1,x-1]+4, d[y-1,x]+3,
                         d[y-1,x+1]+4, d[y,x-1]+3)
    # Backward pass: bottom-right to top-left
    for y in reversed range(height):
        for x in reversed range(width):
            d[y,x] = min(d[y,x], d[y+1,x-1]+4, d[y+1,x]+3,
                         d[y+1,x+1]+4, d[y,x+1]+3)
    return d / 3.0

def watershed(distance, markers):
    heap = []  # priority queue by -distance
    for each marker pixel: push to heap
    while heap:
        _, y, x = heappop(heap)
        label = labels[y,x]
        for neighbor (4-dir):
            if unlabeled and distance > 0:
                labels[ny,nx] = label
                heappush(heap, (-distance[ny,nx], ny, nx))"""
    )

    pdf.subsecao("4.3 Etapas intermediárias")
    pdf.imagem(OUT_DIR3 / "3_chapeus_grayscale.png", w=70)
    pdf.imagem(OUT_DIR3 / "3_chapeus_threshold.png", w=70)
    pdf.imagem(OUT_DIR3 / "3_chapeus_closing.png", w=70)

    pdf.paragrafo("Distance transform (Chamfer) e marcadores (máximos locais):")
    pdf.imagem(OUT_DIR3 / "3_chapeus_distance_transform.png", w=70)
    pdf.imagem(OUT_DIR3 / "3_chapeus_markers.png", w=70)
    pdf.imagem(OUT_DIR3 / "3_chapeus_markers_overlay.png", w=80)

    pdf.subsecao("4.4 Resultado da segmentação")
    pdf.imagem(OUT_DIR3 / "3_chapeus_segmented_gray.png", w=60)
    pdf.imagem(OUT_DIR3 / "3_chapeus_segmented_color.png", w=60)
    pdf.imagem(OUT_DIR3 / "3_chapeus_segmented_output.png", w=80)

    pdf.paragrafo(
        "Foram identificados 62 segmentos na imagem de chapéus. O algoritmo conseguiu "
        "separar adequadamente os chapéus sobrepostos. A etapa de fechamento morfológico "
        "foi fundamental para reduzir ruídos que causariam super-segmentação. O limiar "
        "de 85% do valor máximo do distance transform na seleção de marcadores mostrou-se "
        "adequado para identificar os centros dos objetos com poucos marcadores espúrios."
    )

    # --- CONCLUSÃO ---
    pdf.add_page()
    pdf.secao("5. Conclusão")
    pdf.paragrafo(
        "A atividade 4 de Processamento de Imagens permitiu a implementação prática de "
        "técnicas fundamentais de morfologia matemática, detecção de bordas e segmentação "
        "de imagens. As operações morfológicas demonstraram como diferentes tamanhos de "
        "elemento estruturante afetam a forma de objetos binários. O filtro gaussiano e "
        "o gradiente Sobel constituem as bases do detector de bordas de Canny, enquanto "
        "o HOG mostrou-se capaz de capturar a estrutura direcional das bordas. A "
        "segmentação watershed revelou-se eficaz para separar objetos adjacentes, "
        "desde que o pré-processamento seja adequado."
    )


    # --- SALVAR ---
    pdf_path = SCRIPT_DIR / "relatorio_atividade4.pdf"
    pdf.output(str(pdf_path))
    print(f"Relatório salvo em {pdf_path}")


if __name__ == "__main__":
    main()
