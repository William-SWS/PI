# Atividade 1 de Processamento de Imagens

**Prof. Matheus Araújo**

## Questão 1: Compressão de Imagens baseada em DCT

Implemente uma versão simplificada de compressão de imagens baseada na Transformada Discreta do Cosseno (DCT), inspirada no padrão JPEG.

Inicialmente, a imagem deve ser convertida para tons de cinza e dividida em blocos de tamanho fixo (por exemplo, 8×8). Para cada bloco, aplique a DCT bidimensional implementada manualmente e, em seguida, realize a quantização dos coeficientes utilizando uma matriz de quantização simplificada. Após a quantização, reconstrua a imagem aplicando a transformada inversa (IDCT) e recompondo os blocos.

O aluno deverá comparar a imagem original com a reconstruída, analisando as perdas introduzidas no processo, especialmente em termos de perda de detalhes e aparecimento de artefatos de bloco.

## Questão 2: Descritores de Imagens em Tons de Cinza

Desenvolver um conjunto de descritores para caracterizar imagens em tons de cinza, combinando **medidas estatísticas globais** e **informações estruturais simples**.

O aluno deve calcular métricas como:
- Média
- Variância
- Energia da imagem
- Uma medida de variação espacial (diferenças absolutas entre pixels vizinhos - horizontal e vertical)

A partir dessas características, o aluno deverá:
- Comparar pelo menos duas imagens distintas
- Discutir como esses descritores podem ser utilizados para diferenciar padrões visuais (texturas, regiões homogêneas, imagens com alto nível de detalhe)
- Incluir interpretação dos resultados obtidos
- Relacionar com possíveis aplicações em classificação de imagens

### Contexto Ilustrativo

A imagem de exemplo apresenta uma cena em tons de cinza contendo regiões com características distintas: áreas com alta densidade de detalhes estruturais (árvores) e áreas homogêneas (céu). Observa-se que a região correspondente à vegetação apresenta grande variação de intensidades e padrões locais, enquanto a região do céu apresenta baixa variabilidade espacial. Essas diferenças devem ser refletidas nos descritores estatísticos e estruturais calculados ao longo da atividade.

---

## Objetivo

Esta atividade tem como objetivo explorar e consolidar conceitos de compressão, representação e descrição de imagens digitais, por meio da implementação prática de técnicas fundamentais, como transformações e extração de características.

Busca-se desenvolver a compreensão dos princípios que permitem:
- Reduzir redundâncias
- Representar eficientemente os dados visuais
- Descrever quantitativamente o conteúdo das imagens
- Interpretar os impactos dessas abordagens nos resultados obtidos

---

## Regras Gerais

- **Uso de bibliotecas**: É permitido o uso da biblioteca **OpenCV ou PIL** apenas para:
  - Carregamento de imagens
  - Salvamento de imagens

- **Proibição de funções prontas**: Não é permitido utilizar funções prontas da biblioteca para realizar as operações solicitadas nas questões. Todas as transformações devem ser implementadas manualmente pelo aluno.

- **Imagens para testes**: O aluno deve utilizar exclusivamente **imagens relacionadas ao tema do seu trabalho final** como base para testes e demonstrações.

- **Imagens do enunciado**: As imagens apresentadas no enunciado das questões são meramente ilustrativas e **não devem ser utilizadas** na implementação.

- **Formato de desenvolvimento**: O trabalho pode ser desenvolvido em:
  - Scripts Python, ou
  - Jupyter Notebook

- **Convertendo Jupyter Notebook**:
  - O arquivo deve ser convertido para PDF, ou
  - Disponibilizado via Google Colab com link de acesso

- **Data de entrega**: 01/06

---

## Instruções para Entrega

O aluno deverá entregar o trabalho no formato de **relatório em PDF** no classroom, contendo:

- Descrição das implementações realizadas
- Imagens utilizadas (obrigatoriamente relacionadas ao tema do trabalho final)
- Resultados obtidos para cada questão
- Comparações visuais quando aplicável
- Breves análises, interpretações e insights sobre os efeitos observados em cada processamento

O relatório deve ser claro, organizado e apresentar coerência entre os resultados e as explicações.

### Entrega via Jupyter Notebook

Caso o trabalho seja desenvolvido em Jupyter Notebook, o aluno deverá:
- Converter o notebook para PDF, ou
- Disponibilizar o link do Google Colab com acesso público