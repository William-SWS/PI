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
