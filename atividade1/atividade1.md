Claro! Aqui está o texto extraído do arquivo `Atividade1PI.pdf`:

---

## Página 1

**1.** Implementar um efeito de esboço a lápis em uma imagem por meio dos seguintes passos:  
(i) Converter a imagem colorida para níveis de cinza,  
(ii) Aplicar um filtro de desfoque gaussiano (por exemplo, com uma máscara de 21×21 pixels) para suavizar os detalhes da imagem e  
(iii) Dividir a imagem em tons de cinza pela versão desfocada para realçar os contornos.



**2.** Aplicar a correção gama para ajustar o brilho de uma imagem monocromática A de entrada e gerar uma imagem monocromática B de saída. A transformação pode ser realizada:  
(i) convertendo-se as intensidades dos pixels para o intervalo de [0, 255] para [0, 1],  
(ii) Aplicando-se a equação B = A^(1/ν),  
(iii) Convertendo-se os valores resultantes de volta para o intervalo [0, 255].  
Realizar a correção com diferentes valores de γ.

---

## Página 2

**3.** Combinar duas imagens monocromáticas de mesmo tamanho por meio da média ponderada de seus níveis de cinza.

**4.** Dada (a) uma imagem monocromática, transformar seu espaço de intensidades (níveis de cinza) para:  
(b) obter o negativo da imagem, ou seja, o nível de cinza 0 será convertido para 255, o nível 1 para 254 e assim por diante,  
(c) converter o intervalo de intensidades para [100, 200],  
(d) inverter os valores dos pixels das linhas pares da imagem, ou seja, os valores dos pixels da linha 0 serão posicionados da direita para esquerda, os valores dos pixels da linha 2 serão posicionados da direita para a esquerda e assim por diante,  
(e) espelhar as linhas da metade superior da imagem na parte inferior da imagem e  
(f) aplicar um espelhamento vertical na imagem levando-se em conta todas as linhas da imagem.

---

## Página 3

**5.** Construir um mosaico de 4 × 4 blocos a partir de uma imagem monocromática. A disposição dos blocos deve seguir a numeração mostrada na figura (c).

*(Figuras repetidas na sequência)*

**6.** Quantização refere-se ao número de níveis de cinza usados para representar uma imagem monocromática. A quantização está relacionada à profundidade de uma imagem, a qual corresponde ao número de bits necessários para armazenar a imagem. Representar uma imagem com diferentes níveis de quantização.



---

## Página 4

**Objetivo**  
Esta atividade tem como objetivo introduzir conceitos fundamentais de processamento digital de imagens por meio da implementação manual de técnicas clássicas, reforçando o entendimento dos algoritmos envolvidos.

**Regras Gerais**

- É permitido o uso da biblioteca OpenCV ou PIL apenas para:
  - Carregamento de imagens;
  - Salvamento de imagens.
- Não é permitido utilizar funções prontas da biblioteca para realizar as operações solicitadas nas questões. Todas as transformações devem ser implementadas manualmente pelo aluno.
- O aluno deve utilizar exclusivamente imagens relacionadas ao tema do seu trabalho final como base para testes e demonstrações.
- As imagens apresentadas no enunciado das questões são meramente ilustrativas e não devem ser utilizadas na implementação.
- O trabalho pode ser desenvolvido em:
  - Scripts Python, ou
  - Jupyter Notebook.
- Caso utilize Jupyter Notebook:
  - O arquivo deve ser convertido para PDF, ou
  - Disponibilizado via Google Colab com link de acesso.
- Data de entrega: 15/04

**Instruções para Entrega**

O aluno deverá entregar o trabalho no formato de relatório em PDF no classroom, contendo:
- Descrição das implementações realizadas;
- Imagens utilizadas (obrigatoriamente relacionadas ao tema do trabalho final);
- Resultados obtidos para cada questão;
- Comparações visuais quando aplicável;
- Breves análises, interpretações e insights sobre os efeitos observados em cada processamento.

O relatório deve ser claro, organizado e apresentar coerência entre os resultados e as explicações.

Caso o trabalho seja desenvolvido em Jupyter Notebook, o aluno deverá:
- Converter o notebook para PDF, ou
- Disponibilizar o link do Google Colab com acesso público.

---

Se precisar de ajuda para implementar alguma das questões, é só avisar!