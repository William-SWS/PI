Como executar a solução da Questão 1 (Atividade 2)

1. Instale dependências (recomendado em virtualenv):

```bash
pip install -r atividade2/requirements.txt
```

2. Execute o script fornecendo uma imagem de entrada (monocromática ou colorida — será convertida para grayscale):

```bash
python atividade2/q1.py --input atividade2/some_image.jpg
```

3. Saídas serão salvas em `atividade2/saidas/saidas_questao2` como `q1_h1.png` ... `q1_h11.png` e `resultados_q1.json`.

4. Verifique executando:

```bash
python atividade2/saidas/saidas_questao2/verify_q1.py
```

Observações:
- As transformações são implementadas por convolução manual (sem uso de funções prontas de filtragem).
- Se o enunciado fornecer kernels específicos para h1..h11, substitua os kernels definidos em `atividade2/q1.py`.

---

Como executar a solução da Questão 2 (correção gama)

1. Execute o script da Q2. Se `--input` não for informado, ele tenta automaticamente:
	- `atividade2/imagem2.jpg`
	- `atividade2/image2.jpg`
	- `atividade2/image2.png`

```bash
python atividade2/q2.py
```

2. Opcionalmente, informe imagem e gammas manualmente:

```bash
python atividade2/q2.py --input atividade2/image2.png --gammas 0.25,0.5,1.0,1.5,2.0,3.0
```

3. Saídas da Q2 em `atividade2/saidas/saidas_questao2`:
	- `imagem2_gama_<gamma>.png`
	- `comparativo_gama.png`
	- `resultados_q2.json`

4. Também foi criado o notebook `atividade2/q2.ipynb` com a mesma implementação manual da Q2.
