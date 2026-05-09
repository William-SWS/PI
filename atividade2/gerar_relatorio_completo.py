#!/usr/bin/env python3
"""
Script para gerar relatório completo da Atividade 2 com imagens e converter para PDF.

Este script:
1. Lê o relatório markdown atual
2. Adiciona imagens em seções apropriadas
3. Gera novo markdown com imagens
4. Converte para PDF usando weasyprint
"""

import os
import sys
from pathlib import Path

import markdown
from weasyprint import HTML, CSS


def get_base_dir():
    """Retorna o diretório base do projeto."""
    return Path(__file__).parent


def read_markdown_report(base_dir):
    """Lê o relatório markdown atual."""
    report_path = base_dir / "RELATORIO_ATIVIDADE2.md"
    with open(report_path, 'r', encoding='utf-8') as f:
        return f.read()


def create_enhanced_markdown(base_dir, original_content):
    """Cria versão melhorada do markdown com imagens."""

    # Caminhos relativos para as imagens
    saidas_q1 = "saidas/saidas_questao1"
    saidas_q2 = "saidas/saidas_questao2"

    # Conteúdo a ser inserido após cada seção
    insertions = {
        # Após "## 3. Imagens Utilizadas"
        "### 3.1 Entrada da Questão 1": f"""
#### Imagem Original

![Imagem Original da Questão 1](imageq1.png)

*Figura 1: Imagem original utilizada para aplicação dos filtros no domínio espacial.*
""",
        "### 3.2 Entrada da Questão 2": f"""
#### Imagem Original

![Imagem Original da Questão 2](image2.png)

*Figura 2: Imagem original utilizada para processamento no domínio da frequência.*
""",
        # Após "### 4.3 Resultados esperados da Questão 1"
        "Os resultados são salvos": f"""

#### 4.3.1 Imagem Original

![Imagem Original](imageq1.png)

#### 4.3.2 Filtros de Suavização

| Média 3x3 | Gaussiano 5x5 | Média 5x5 |
|-----------|---------------|-----------|
| ![Média 3x3]({saidas_q1}/q1_h1.png) | ![Gaussiano 5x5]({saidas_q1}/q1_h2.png) | ![Média 5x5]({saidas_q1}/q1_h10.png) |

*Figura 3: Filtros de suavização aplicados à imagem original.*

#### 4.3.3 Detectores de Borda

| Sobel X | Sobel Y | Prewitt X | Prewitt Y |
|---------|---------|-----------|-----------|
| ![Sobel X]({saidas_q1}/q1_h3.png) | ![Sobel Y]({saidas_q1}/q1_h4.png) | ![Prewitt X]({saidas_q1}/q1_h5.png) | ![Prewitt Y]({saidas_q1}/q1_h6.png) |

*Figura 4: Detectores de borda aplicados à imagem original.*

#### 4.3.4 Filtros de Realce

| Laplaciano | Sharpening | Emboss | Unsharp Mask |
|-------------|------------|--------|--------------|
| ![Laplaciano]({saidas_q1}/q1_h7.png) | ![Sharpening]({saidas_q1}/q1_h8.png) | ![Emboss]({saidas_q1}/q1_h9.png) | ![Unsharp Mask]({saidas_q1}/q1_h11.png) |

*Figura 5: Filtros de realce aplicados à imagem original.*
""",
        # Após "### 5.3 Resultados esperados da Questão 2"
        "Os resultados são organizados": f"""

#### 5.3.1 Espectro de Frequência

![Espectro FFT Centralizado]({saidas_q2}/00_fft/fft_espectro_centralizado.png)

*Figura 6: Espectro de frequência da imagem original após aplicação da FFT e centralização.*

#### 5.3.2 Máscaras de Filtro

| Passa-Baixa r=15 | Passa-Baixa r=30 | Passa-Baixa r=60 |
|------------------|------------------|------------------|
| ![Mask PB r15]({saidas_q2}/01_masks/mask_passabaixa_r15.png) | ![Mask PB r30]({saidas_q2}/01_masks/mask_passabaixa_r30.png) | ![Mask PB r60]({saidas_q2}/01_masks/mask_passabaixa_r60.png) |

| Passa-Alta r=15 | Passa-Alta r=30 | Passa-Alta r=60 |
|-----------------|-----------------|-----------------|
| ![Mask PA r15]({saidas_q2}/01_masks/mask_passaalta_r15.png) | ![Mask PA r30]({saidas_q2}/01_masks/mask_passaalta_r30.png) | ![Mask PA r60]({saidas_q2}/01_masks/mask_passaalta_r60.png) |

| Passa-Faixa 10-30 | Passa-Faixa 20-50 | Rejeita-Faixa 10-30 | Rejeita-Faixa 20-50 |
|-------------------|-------------------|---------------------|---------------------|
| ![Mask PF 10-30]({saidas_q2}/01_masks/mask_passafaixa_r10_30.png) | ![Mask PF 20-50]({saidas_q2}/01_masks/mask_passafaixa_r20_50.png) | ![Mask RF 10-30]({saidas_q2}/01_masks/mask_rejeitafaixa_r10_30.png) | ![Mask RF 20-50]({saidas_q2}/01_masks/mask_rejeitafaixa_r20_50.png) |

*Figura 7: Máscaras de filtro utilizadas no domínio da frequência.*

#### 5.3.3 Resultados da Filtragem

| Passa-Baixa r=15 | Passa-Baixa r=30 | Passa-Baixa r=60 |
|------------------|------------------|------------------|
| ![PB r15]({saidas_q2}/02_filtradas/filtro_passabaixa_r15.png) | ![PB r30]({saidas_q2}/02_filtradas/filtro_passabaixa_r30.png) | ![PB r60]({saidas_q2}/02_filtradas/filtro_passabaixa_r60.png) |

| Passa-Alta r=15 | Passa-Alta r=30 | Passa-Alta r=60 |
|-----------------|-----------------|-----------------|
| ![PA r15]({saidas_q2}/02_filtradas/filtro_passaalta_r15.png) | ![PA r30]({saidas_q2}/02_filtradas/filtro_passaalta_r30.png) | ![PA r60]({saidas_q2}/02_filtradas/filtro_passaalta_r60.png) |

| Passa-Faixa 10-30 | Passa-Faixa 20-50 | Rejeita-Faixa 10-30 | Rejeita-Faixa 20-50 |
|-------------------|-------------------|---------------------|---------------------|
| ![PF 10-30]({saidas_q2}/02_filtradas/filtro_passafaixa_r10_30.png) | ![PF 20-50]({saidas_q2}/02_filtradas/filtro_passafaixa_r20_50.png) | ![RF 10-30]({saidas_q2}/02_filtradas/filtro_rejeitafaixa_r10_30.png) | ![RF 20-50]({saidas_q2}/02_filtradas/filtro_rejeitafaixa_r20_50.png) |

*Figura 8: Imagens filtradas no domínio da frequência.*

#### 5.3.4 Compressão por Magnitude

| Compressão P70 | Compressão P85 | Compressão P95 |
|----------------|----------------|----------------|
| ![Compressão P70]({saidas_q2}/03_compressao/compressao_percentil_70.png) | ![Compressão P85]({saidas_q2}/03_compressao/compressao_percentil_85.png) | ![Compressão P95]({saidas_q2}/03_compressao/compressao_percentil_95.png) |

*Figura 9: Imagens comprimidas por limiar de magnitude no domínio da frequência.*

#### 5.3.5 Análise por Histogramas

A análise por histogramas permite avaliar o impacto da compressão na distribuição de intensidades da imagem. A seguir são apresentados os histogramas da imagem original e das versões comprimidas com diferentes percentis de limiar de magnitude.

##### 5.3.5.1 Histograma da Imagem Original

![Histograma Original]({saidas_q2}/04_histogramas/histograma_original.png)

*Figura 10: Histograma da imagem original, mostrando a distribuição de intensidades sem compressão.*

O histograma original representa a distribuição de intensidades da imagem antes de qualquer processamento de compressão. Esta distribuição serve como referência para comparar os efeitos da compressão por limiar de magnitude.

##### 5.3.5.2 Histograma da Imagem Comprimida (Percentil 70)

![Histograma P70]({saidas_q2}/04_histogramas/histograma_p70.png)

*Figura 11: Histograma da imagem comprimida com percentil 70.*

A compressão com percentil 70 remove 30% dos coeficientes de menor magnitude no domínio da frequência. O histograma resultante mostra uma distribuição de intensidades que mantém boa similaridade com o original, indicando que a qualidade visual é preservada mesmo com esta compressão moderada.

##### 5.3.5.3 Histograma da Imagem Comprimida (Percentil 85)

![Histograma P85]({saidas_q2}/04_histogramas/histograma_p85.png)

*Figura 12: Histograma da imagem comprimida com percentil 85.*

Com o percentil 85, 15% dos coeficientes são removidos. O histograma começa a mostrar alterações mais perceptíveis na distribuição de intensidades, refletindo o aumento da perda de informação espectral. Ainda assim, a estrutura geral da imagem permanece reconhecível.

##### 5.3.5.4 Histograma da Imagem Comprimida (Percentil 95)

![Histograma P95]({saidas_q2}/04_histogramas/histograma_p95.png)

*Figura 13: Histograma da imagem comprimida com percentil 95.*

A compressão com percentil 95 é mais agressiva, removendo apenas 5% dos coeficientes de maior magnitude. O histograma resultante mostra uma distribuição significativamente alterada em relação ao original, indicando maior perda de detalhes e degradação da qualidade visual.

##### 5.3.5.5 Comparativo de Histogramas

![Comparativo de Histogramas]({saidas_q2}/04_histogramas/comparativo_histogramas_original_vs_comprimidas.png)

*Figura 14: Comparativo de histogramas entre imagem original e versões comprimidas.*

O gráfico comparativo permite visualizar simultaneamente a evolução da distribuição de intensidades conforme aumenta o nível de compressão. É possível observar que:

- O histograma P70 (percentil 70) mantém a forma mais próxima do original
- O histograma P85 (percentil 85) mostra desvios moderados
- O histograma P95 (percentil 95) apresenta as maiores alterações

Esta análise demonstra o trade-off entre taxa de compressão e qualidade visual: quanto maior o percentil de limiar, maior a compressão, mas também maior a perda de fidelidade à imagem original.
""",
    }

    # Criar conteúdo melhorado
    enhanced_content = original_content

    # Inserir conteúdo após cada marcador
    for marker, insertion in insertions.items():
        if marker in enhanced_content:
            # Encontrar posição do marcador
            pos = enhanced_content.find(marker)
            if pos != -1:
                # Encontrar o final da linha do marcador
                end_pos = enhanced_content.find('\n', pos)
                if end_pos != -1:
                    # Inserir após a linha do marcador
                    enhanced_content = enhanced_content[:end_pos+1] + insertion + enhanced_content[end_pos+1:]

    return enhanced_content


def save_enhanced_markdown(base_dir, content):
    """Salva o markdown melhorado."""
    output_path = base_dir / "RELATORIO_ATIVIDADE2_COMPLETO.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Markdown melhorado salvo em: {output_path}")
    return output_path


def create_html_from_markdown(base_dir, markdown_path):
    """Converte markdown para HTML."""
    with open(markdown_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Converter markdown para HTML
    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

    # Criar HTML completo com CSS
    html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório Atividade 2</title>
    <style>
        body {{
            font-family: 'DejaVu Sans', Arial, sans-serif;
            line-height: 1.6;
            max-width: 210mm;
            margin: 0 auto;
            padding: 20mm;
            color: #333;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 5px;
            margin-top: 30px;
        }}
        h3 {{
            color: #7f8c8d;
            margin-top: 25px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 10px auto;
        }}
        figcaption {{
            text-align: center;
            font-style: italic;
            color: #666;
            font-size: 0.9em;
            margin-bottom: 20px;
        }}
        pre {{
            background-color: #f8f8f8;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        code {{
            font-family: 'Courier New', monospace;
            background-color: #f8f8f8;
            padding: 2px 5px;
            border-radius: 3px;
        }}
        @page {{
            margin: 20mm;
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>"""

    html_path = base_dir / "RELATORIO_ATIVIDADE2.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_template)

    print(f"✓ HTML gerado em: {html_path}")
    return html_path


def create_pdf_from_html(base_dir, html_path):
    """Converte HTML para PDF usando weasyprint."""
    pdf_path = base_dir / "RELATORIO_ATIVIDADE2.pdf"

    # Ler HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Converter para PDF
    HTML(string=html_content, base_url=str(base_dir)).write_pdf(pdf_path)

    print(f"✓ PDF gerado em: {pdf_path}")
    return pdf_path


def main():
    """Função principal."""
    base_dir = get_base_dir()

    print("=== Gerando Relatório Completo da Atividade 2 ===\n")

    # 1. Ler relatório original
    print("1. Lendo relatório original...")
    original_content = read_markdown_report(base_dir)

    # 2. Criar versão melhorada
    print("2. Criando versão melhorada com imagens...")
    enhanced_content = create_enhanced_markdown(base_dir, original_content)

    # 3. Salvar markdown melhorado
    print("3. Salvando markdown melhorado...")
    md_path = save_enhanced_markdown(base_dir, enhanced_content)

    # 4. Converter para HTML
    print("4. Convertendo para HTML...")
    html_path = create_html_from_markdown(base_dir, md_path)

    # 5. Converter para PDF
    print("5. Convertendo para PDF...")
    pdf_path = create_pdf_from_html(base_dir, html_path)

    print("\n=== Concluído! ===")
    print(f"Arquivos gerados:")
    print(f"  - Markdown: {md_path}")
    print(f"  - HTML: {html_path}")
    print(f"  - PDF: {pdf_path}")


if __name__ == '__main__':
    main()
