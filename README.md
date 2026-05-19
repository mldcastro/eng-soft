# Engenharia de Software N

Aqui estão os trabalhos da cadeira INF01127 - Engenharia de Software N.

## Requisitos

Para rodar os códigos deste repositório, você precisa instalar as seguintes ferramentas:

- [`mermaid-cli`](https://github.com/mermaid-js/mermaid-cli) >= 11.12;
  - Esta ferramente é usada para gerar os diagramas UML.
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/#installing-uv) == 0.11.15.
  - Esta ferramente é usada para gerenciar o ambiente Python.

## Convertendo os arquivos `.mmd` em imagens

Você pode usar tanto o script em Python, quanto a CLI oficial do `mermaid`.

Usando o script Python:

```bash
uv run mermaid --file diagrams/some_diagram_code.mmd
```

Usando a CLI do `mermaid`:

```bash
mmdc -i some_diagram_code.mmd -o some_diagram_code.png
```

> [!note]
> A CLI do `mermaid` tem o nome de `mmdc` no terminal.
