
# Atividade 1 de Processamento de Imagens



**Prof. Matheus Araújo**

### 1. Operações Morfológicas



Implemente as operações morfológicas de erosão e dilatação em imagens binárias (obtidas de imagens do seu tema), utilizando diferentes tamanhos de elemento estruturante definidos pelo aluno (por exemplo, uma máscara 3x3, 5x5 e 15x15). A partir dessas operações, construa também as operações de abertura e fechamento, analisando seus efeitos sobre as imagens. O aluno deverá aplicar essas transformações em pelo menos duas imagens binárias contendo objetos com ruídos e pequenas imperfeições, comparando os resultados obtidos em cada etapa.

> *(O documento apresenta exemplos visuais destas etapas: Original, Erosion, Dilation, Opening e Closing)*.
> 
> 

### 2. Filtros e Detecção de Bordas (Canny e HOG)



Implemente as duas primeiras etapas do algoritmo de detecção de bordas de Canny: suavização por filtro gaussiano e cálculo do gradiente da imagem. O aluno deve inicialmente aplicar um filtro gaussiano para reduzir ruídos e, em seguida, calcular as componentes do gradiente (por exemplo, utilizando operadores do tipo Sobel implementados manualmente). A partir disso, deve-se obter a magnitude do gradiente e analisar as regiões de maior variação de intensidade.

Como extensão, o aluno deverá utilizar as informações de magnitude e orientação do gradiente para implementar o descritor Histogram of Oriented Gradients (HOG) de forma simplificada, dividindo a imagem em células (por exemplo, 8x8 pixels) e construindo histogramas de orientação ponderados pela magnitude do gradiente em cada célula. Ao final, deve-se apresentar e analisar os vetores de características gerados, discutindo como eles representam a estrutura e as bordas da imagem.

> *(O documento exibe gráficos e exemplos visuais das saídas do Canny e do descritor HOG)*.
> 
> 

### 3. Segmentação (Watershed)



Implemente um método de segmentação baseado em marcadores seguido da aplicação do algoritmo Watershed, de forma a separar objetos em uma imagem com regiões próximas ou parcialmente sobrepostas. Inicialmente, o aluno deve preparar a imagem por meio de uma técnica que facilite a identificação das regiões de interesse, como limiarização (thresholding), operações morfológicas ou análise da distância (distance transform) aplicada sobre uma imagem binária.

A partir dessa etapa, devem ser definidos marcadores para regiões de primeiro plano (objetos) e, opcionalmente, de fundo, que servirão como base para o processo de segmentação. Em seguida, o algoritmo Watershed deve ser implementado (versão simples), considerando o conceito de crescimento de regiões a partir desses marcadores, onde os limites entre regiões são definidos pelas "linhas de separação" formadas durante o processo. O aluno deverá apresentar e analisar os resultados da segmentação, discutindo a capacidade do método em separar objetos adjacentes e a influência da etapa de pré-processamento na qualidade final.

> *(O documento inclui um fluxo visual das etapas: Original image, Threshold, Closing, Distance transform, Local maximum, Markers, Segmented - gray, Segmented - color, Output image)*.
> 
> 

---

## Objetivo



Esta atividade tem como objetivo introduzir técnicas fundamentais de morfologia matemática e segmentação de imagens, por meio da implementação prática de operadores que permitem extrair, separar e estruturar informações relevantes em imagens digitais. Busca-se desenvolver a compreensão dos efeitos dessas operações na análise de formas, bordas e regiões.

## Regras Gerais



* É permitido o uso da biblioteca OpenCV ou PIL apenas para:


* Carregamento de imagens;


* Salvamento de imagens.




* Não é permitido utilizar funções prontas da biblioteca para realizar as operações solicitadas nas questões.


* Todas as transformações devem ser implementadas manualmente pelo aluno.


* O aluno deve utilizar exclusivamente imagens relacionadas ao tema do seu trabalho final como base para testes e demonstrações.


* As imagens apresentadas no enunciado das questões são meramente ilustrativas e não devem ser utilizadas na implementação.


* O trabalho pode ser desenvolvido em:


* Scripts Python, ou


* Jupyter Notebook.




* Caso utilize Jupyter Notebook:


* O arquivo deve ser convertido para PDF, ou


* Disponibilizado via Google Colab com link de acesso.




* **Data de entrega:** 22/06



## Instruções para Entrega



O aluno deverá entregar o trabalho no formato de relatório em PDF no classroom, contendo:

* Descrição das implementações realizadas;


* Imagens utilizadas (obrigatoriamente relacionadas ao tema do trabalho final);


* Resultados obtidos para cada questão;


* Comparações visuais quando aplicável;


* Breves análises, interpretações e insights sobre os efeitos observados em cada processamento.



O relatório deve ser claro, organizado e apresentar coerência entre os resultados e as explicações.

Caso o trabalho seja desenvolvido em Jupyter Notebook, o aluno deverá:

* Converter o notebook para PDF, ou


* Disponibilizar o link do Google Colab com acesso público.