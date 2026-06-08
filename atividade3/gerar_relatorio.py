import os
from fpdf import FPDF

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTADOS_DIR = os.path.join(SCRIPT_DIR, "resultados")
IMAGES_DIR = os.path.join(SCRIPT_DIR, "images")


class RelatorioPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.cell(0, 8, "Processamento de Imagens - Atividade 3", align="C")
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Pagina {self.page_no()}/{{nb}}", align="C")

    def titulo_secao(self, texto):
        self.set_font("Helvetica", "B", 14)
        self.ln(4)
        self.cell(0, 10, texto, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)
        self.set_draw_color(0)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def subtitulo(self, texto):
        self.set_font("Helvetica", "B", 11)
        self.ln(2)
        self.cell(0, 8, texto)
        self.ln(6)

    def corpo(self, texto):
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5, texto)
        self.ln(2)

    def insere_imagem(self, path, largura, legenda=""):
        if os.path.exists(path):
            self.image(path, w=largura)
            self.ln(1)
            if legenda:
                self.set_font("Helvetica", "I", 9)
                self.cell(0, 5, legenda, align="C")
                self.ln(5)
        else:
            self.corpo(f"[Imagem nao encontrada: {path}]")
        self.ln(2)


def gerar_relatorio():
    pdf = RelatorioPDF()
    pdf.alias_nb_pages()

    # ================================================================
    # CAPA
    # ================================================================
    pdf.add_page()
    pdf.ln(50)
    pdf.set_font("Helvetica", "B", 22)
    pdf.cell(0, 12, "Atividade 3", align="C")
    pdf.ln(14)
    pdf.set_font("Helvetica", "", 14)
    pdf.cell(0, 8, "Processamento de Imagens", align="C")
    pdf.ln(14)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 7, "Prof. Matheus Araujo", align="C")
    pdf.ln(20)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Samuel William Silva Almeida", align="C")
    pdf.ln(30)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, "Questao 1 - Compressao de Imagem com DCT", align="C")
    pdf.ln(7)
    pdf.cell(0, 6, "Questao 2 - Descritores de Imagens em Tons de Cinza", align="C")

    # ================================================================
    # QUESTAO 1 - COMPRESSAO DCT
    # ================================================================
    pdf.add_page()
    pdf.titulo_secao("Questao 1 - Compressao de Imagem com DCT")

    pdf.subtitulo("Implementacao")
    pdf.corpo(
        "A compressao foi implementada seguindo as etapas do padrao JPEG, "
        "com todas as transformacoes realizadas manualmente. "
        "A imagem colorida foi convertida para tons de cinza utilizando a "
        "formula de luminancia (0.299*R + 0.587*G + 0.114*B), sem uso de "
        "funcoes prontas do OpenCV."
    )
    pdf.corpo(
        "A imagem foi dividida em blocos de 64x64 pixels. Para cada bloco, "
        "aplicou-se a DCT-II bidimensional manual (O(N^4) por bloco), "
        "seguida de quantizacao dos coeficientes utilizando a matriz de "
        "luminancia padrao do JPEG, expandida via produto de Kronecker "
        "para 64x64 e multiplicada por um fator de qualidade 2.0 para "
        "aumentar a compressao. Apos a desquantizacao, a IDCT-III "
        "reconstruiu cada bloco, e os blocos foram recombinados para "
        "formar a imagem final."
    )
    pdf.corpo(
        "A imagem utilizada foi 'runner.png', relacionada ao tema do "
        "trabalho final (blusas/vestuario esportivo). Por ser uma imagem "
        "com detalhes finos (tecido, dobras, iluminacao), os efeitos da "
        "compressao sao particularmente visiveis."
    )

    pdf.subtitulo("Resultados Visuais")
    pdf.corpo(
        "A figura a seguir apresenta a imagem original em tons de cinza, "
        "a versao reconstruida apos compressao DCT e o mapa de diferenca "
        "(valor absoluto da subtracao entre original e reconstruida)."
    )
    pdf.ln(2)

    orig_path = os.path.join(RESULTADOS_DIR, "q3_64x64", "original_cinza.png")
    pdf.insere_imagem(orig_path, 170, "Original em tons de cinza")

    recon_path = os.path.join(RESULTADOS_DIR, "q3_64x64", "imagem_reconstruida.png")
    pdf.insere_imagem(recon_path, 170, "Reconstruida apos DCT + quantizacao")

    diff_path = os.path.join(RESULTADOS_DIR, "q3_64x64", "diferenca.png")
    pdf.insere_imagem(diff_path, 170, "Diferenca absoluta entre original e reconstruida")

    pdf.subtitulo("Analise dos Resultados")
    pdf.corpo(
        "Observa-se que a imagem reconstruida apresenta perda de qualidade "
        "em relacao a original, especialmente nas regioes com alta frequencia "
        "espacial, como bordas e texturas finas do tecido. O mapa de diferenca "
        "evidencia que os maiores erros estao concentrados nessas regioes, "
        "enquanto areas homogeneas (como o fundo) sao bem reconstruidas."
    )
    pdf.corpo(
        "O uso de blocos 64x64 (maiores que os 8x8 do JPEG padrao) "
        "introduz artefatos de bloco mais perceptiveis, pois cada bloco "
        "e processado de forma independente, gerando descontinuidades "
        "nas fronteiras. Alem disso, o fator de qualidade 2.0 aumenta "
        "a quantizacao, descartando mais coeficientes de alta frequencia "
        "e contribuindo para o efeito de borramento."
    )
    pdf.corpo(
        "A DCT concentra a maior parte da energia em poucos coeficientes "
        "(baixas frequencias), o que permite uma compressao significativa "
        "com perda controlada. A quantizacao agressiva dos coeficientes "
        "de alta frequencia e o principal responsavel pela perda de "
        "detalhes finos, mas tambem o mecanismo que reduz o tamanho dos "
        "dados."
    )

    # ================================================================
    # QUESTAO 2 - DESCRITORES
    # ================================================================
    pdf.add_page()
    pdf.titulo_secao("Questao 2 - Descritores de Imagens em Tons de Cinza")

    pdf.subtitulo("Implementacao")
    pdf.corpo(
        "Foram implementados manualmente cinco descritores para caracterizar "
        "imagens em tons de cinza, combinando medidas estatisticas globais "
        "e medidas estruturais locais:"
    )
    desc_list = [
        "- Media (brilho geral): soma de todos os pixels dividida pelo total.",
        "- Variancia (contraste global): media do quadrado da diferenca de cada pixel em relacao a media.",
        "- Energia (uniformidade): soma das probabilidades ao quadrado do histograma.",
        "- Diferenca Horizontal: media das diferencas absolutas entre pixels vizinhos na horizontal.",
        "- Diferenca Vertical: media das diferencas absolutas entre pixels vizinhos na vertical.",
    ]
    for item in desc_list:
        pdf.corpo(item)

    pdf.corpo(
        "Foram utilizadas duas imagens do tema vestuario: 'blusa2.png' "
        "(Imagem 1) e 'jacket2.png' (Imagem 2). Ambas foram convertidas "
        "para tons de cinza com a formula de luminancia antes da extracao "
        "dos descritores."
    )

    pdf.subtitulo("Imagens Utilizadas")
    img1_path = os.path.join(RESULTADOS_DIR, "q4", "imagem1_gray.png")
    img2_path = os.path.join(RESULTADOS_DIR, "q4", "imagem2_gray.png")
    pdf.insere_imagem(img1_path, 80, "Imagem 1 - blusa2.png (cinza)")
    pdf.insere_imagem(img2_path, 80, "Imagem 2 - jacket2.png (cinza)")

    pdf.subtitulo("Tabela de Descritores")
    dados = {
        "Media":            ("128.18", "202.41"),
        "Variancia":       ("3266.91", "6905.87"),
        "Energia":         ("0.0085", "0.4100"),
        "Dif. Horizontal": ("5.58", "3.79"),
        "Dif. Vertical":   ("8.23", "2.20"),
    }
    col_w = [50, 55, 55]

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(col_w[0], 8, "Descritor", border=1, align="C")
    pdf.cell(col_w[1], 8, "Imagem 1 (blusa2)", border=1, align="C")
    pdf.cell(col_w[2], 8, "Imagem 2 (jacket2)", border=1, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", "", 10)
    for desc, (v1, v2) in dados.items():
        pdf.cell(col_w[0], 7, desc, border=1, align="C")
        pdf.cell(col_w[1], 7, v1, border=1, align="C")
        pdf.cell(col_w[2], 7, v2, border=1, align="C")
        pdf.ln()
    pdf.ln(4)

    pdf.subtitulo("Grafico Comparativo")
    graf_path = os.path.join(RESULTADOS_DIR, "q4", "comparacao_descritores.png")
    pdf.insere_imagem(graf_path, 170, "Comparacao dos descritores entre as duas imagens")

    pdf.subtitulo("Interpretacao dos Resultados")
    pdf.corpo(
        "A Imagem 2 (jacket2) apresenta media significativamente maior "
        "(202.41 contra 128.18), indicando uma cena mais clara. Sua "
        "variancia tambem e mais que o dobro (6905.87 contra 3266.91), "
        "revelando maior contraste e distribuicao mais ampla dos niveis "
        "de cinza."
    )
    pdf.corpo(
        "A Energia e um descritor particularmente revelador: a Imagem 1 "
        "(0.0085) tem energia muito baixa, indicando maior dispersao dos "
        "niveis de cinza (histograma mais espalhado). A Imagem 2 (0.4100) "
        "tem energia alta, sugerindo um histograma concentrado em poucos "
        "niveis de cinza, consistente com uma imagem de fundo claro e "
        "objeto escuro (distribuicao bimodal)."
    )
    pdf.corpo(
        "As diferencas espaciais (horizontal e vertical) sao mais altas "
        "na Imagem 1 (5.58 e 8.23) do que na Imagem 2 (3.79 e 2.20). "
        "Isso indica que a Imagem 1 possui mais textura e variacao "
        "local entre pixels vizinhos, sugestivo de uma superficie com "
        "mais detalhes (dobras, estampas, iluminacao irregular). "
        "Ja a Imagem 2 tem diferencas espaciais menores, coerente com "
        "uma superficie mais lisa e homogenea."
    )
    pdf.corpo(
        "Aplicacao pratica: esses descritores podem ser usados em "
        "sistemas de classificacao de imagens para distinguir tipos "
        "de tecido, nivel de detalhamento ou condicoes de iluminacao. "
        "Por exemplo, uma blusa lisa teria energia maior e diferencas "
        "espaciais menores que uma blusa estampada. Em conjunto, media "
        "e variancia ajudam a separar imagens por brilho e contraste "
        "global, enquanto as diferencas horizontais/verticais capturam "
        "a textura."
    )

    # Salvar PDF
    output_path = os.path.join(SCRIPT_DIR, "relatorio_atividade3.pdf")
    pdf.output(output_path)
    print(f"Relatorio salvo em: {output_path}")
    return output_path


if __name__ == "__main__":
    gerar_relatorio()
