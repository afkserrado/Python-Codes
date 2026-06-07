# Extrator de Composições CONDER/BA

Aplicativo em Python para extrair composições de preços unitários de serviços de engenharia a partir de um PDF no modelo CONDER/BA e exportar os dados para um arquivo CSV delimitado por `|`.

## O que o programa faz

- Abre uma janela para o usuário selecionar um arquivo PDF.
- Lê o conteúdo do PDF com `pdfplumber`.
- Identifica composições e itens por meio de expressões regulares.
- Ignora linhas fixas de cabeçalho e rodapé do modelo.
- Gera um arquivo `composicoes.csv` na mesma pasta do PDF selecionado.
- Exibe uma mensagem ao final informando onde o CSV foi salvo.

## Requisitos

### Para rodar o script Python

- Python 3 instalado
- Biblioteca `pdfplumber`

Instalação:

```bash
pip install pdfplumber
```

### Para gerar um executável Windows

- PyInstaller instalado

Instalação:

```bash
pip install pyinstaller
```

## Como usar o script

Execute:

```bash
python app.py
```

Em seguida:

1. Selecione o PDF desejado na janela de arquivo.
2. Aguarde o processamento.
3. O arquivo `composicoes.csv` será criado na mesma pasta do PDF.

Se o usuário cancelar a seleção do arquivo, o programa encerra sem erro.

## Como gerar o `.exe`

No Windows, dentro da pasta do projeto, execute:

```powershell
python -m PyInstaller --onefile --windowed --name app app.py
```

Isso gera o executável em:

```text
dist\app.exe
```

### Significado das opções

- `--onefile`: empacota tudo em um único arquivo `.exe`
- `--windowed`: impede a abertura do terminal junto com a aplicação
- `--name app`: define o nome do executável como `app.exe`

## Como atualizar o executável

Sempre que o código for alterado, gere o executável novamente com o mesmo comando:

```powershell
python -m PyInstaller --onefile --windowed --name app app.py
```

## Estrutura esperada do projeto

```text
Conder/
├── app.py
├── build/
├── dist/
└── app.spec
```

## Saída gerada

O CSV gerado possui as colunas:

- `cod_composicao`
- `tipo`
- `cod_item`
- `descricao`
- `unidade`
- `coeficiente`
- `preco_unitario`
- `preco_total`
- `linha`

O separador utilizado no arquivo é `|`.

## Observações

- O arquivo CSV é salvo com codificação `utf-8-sig`, o que facilita a abertura no Excel.
- Caso o PDF tenha variações grandes de layout em relação ao modelo CONDER/BA, pode ser necessário ajustar as expressões regulares.
- As pastas `build` e `dist` são criadas pelo PyInstaller.
- O arquivo `app.spec` também é gerado automaticamente pelo PyInstaller.
