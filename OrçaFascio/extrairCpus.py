import re
import csv
import pdfplumber
from tkinter import Tk, filedialog, messagebox
import os

from bases import bases
from functions import addRegistro, template

# Tk root
root = Tk()
root.withdraw()

# Seleciona PDF
caminhoPdf = filedialog.askopenfilename(
    title="Selecione um arquivo",
    filetypes=[("PDF", "*.pdf"), ("Todos arquivos", "*.*")]
)

if not caminhoPdf:
    raise SystemExit("Nenhum arquivo selecionado.")

caminhoDir = os.path.dirname(caminhoPdf)
caminhoCsv = os.path.join(caminhoDir, "composicoes.csv")

# Pergunta sobre coluna %
percentFlag = messagebox.askyesno(
    title="Coluna de porcentagem",
    message="O PDF tem coluna de porcentagem?"
)

registros = []
linhas = []

target = re.compile(r"^(?:Composição(?:\s+Auxiliar)?|Insumo|Auxiliar)\b")

ignorados = ("AGETOP RODOVIARIA", "DERPR", "SETOP", "SICRO")
ignorFlag = False
inTableFlag = False

bases_pattern = "|".join(map(re.escape, sorted(bases, key=len, reverse=True)))

re_sem_pct = re.compile(
    rf"^(?P<categoria>Composição(?:\s+Auxiliar)?|Insumo)\s+"
    rf"(?P<codigo>\d+)\s+"
    rf"(?P<banco>{bases_pattern})\b"
    rf".*?\s+(?P<unidade>\S+)\s+"
    rf"(?P<quant>\d+,\d{{7}})\s+"
    rf"(?P<valor_unit>\d+,\d{{2}})\s+"
    rf"(?P<total>\d+,\d{{2}})\s*$"
)

re_com_pct = re.compile(
    rf"^(?P<categoria>Composição(?:\s+Auxiliar)?|Insumo)\s+"
    rf"(?P<codigo>\d+)\s+"
    rf"(?P<banco>{bases_pattern})\b"
    rf".*?\s+(?P<unidade>\S+)\s+"
    rf"(?P<quant>\d+,\d{{7}})\s+"
    rf"(?P<pct>\d+,\d{{7}})\s+"
    rf"(?P<valor_unit>\d+,\d{{2}})\s+"
    rf"(?P<total>\d+,\d{{2}})\s*$"
)

# 1) Extrair linhas do PDF
with pdfplumber.open(caminhoPdf) as pdf:
    for page in pdf.pages:
        texto = page.extract_text()
        
        # Texto vazio
        if not texto:
            continue

        for linha in texto.splitlines():
            linha_norm = " ".join(linha.rstrip("\n").split())

            # Linha vazia
            if not linha_norm:
                continue

            if "CódigoBanco Descrição" in linha_norm:
                inTableFlag = True
                continue

            # Marcar composição ignorada
            if any(t in linha_norm for t in ignorados):
                ignorFlag = True
                continue

            # fim da composição
            if "MO sem LS =>" in linha_norm or "Valor do BDI =>" in linha_norm:
                linhas.append("")   # separador
                inTableFlag = False
                continue

            # filtra só categorias válidas
            if not target.match(linha_norm):
                continue

            # caso quebrado: "Composição" + "Auxiliar" em linha seguinte
            if linha_norm.startswith("Auxiliar"):
                if (
                    linhas
                    and linhas[-1].startswith("Composição")
                    and not linhas[-1].startswith("Composição Auxiliar")
                ):
                    linhas[-1] = linhas[-1].replace("Composição", "Composição Auxiliar", 1)
                continue

            # adiciona a linha (Composição / Composição Auxiliar / Insumo / Auxiliar)
            if inTableFlag:   
                linhas.append(linha_norm)

# Debug
caminhoTxt = os.path.join(caminhoDir, "debug_linhas.txt")
with open(caminhoTxt, "w", encoding="utf-8") as f:
    for linha in linhas:
        f.write(linha)

# 2) Parse das linhas em registros
re_linha = re_com_pct if percentFlag else re_sem_pct

for linha in linhas:
    if not linha:  # separador
        valores = ["", "", "", "", "", "", ""]
        addRegistro(registros, valores)
        continue

    m = re_linha.match(linha)
    if not m:
        # Se quiser depurar, descomente:
        # print("NÃO CASOU:", linha)
        continue

    categoria = m.group("categoria")
    codigo = m.group("codigo")
    banco = m.group("banco")
    quant = m.group("quant")
    valor_unit = m.group("valor_unit")
    total = m.group("total")
    pct = m.group("pct") if percentFlag else "0,0000000"

    valores = [categoria, codigo, banco, quant, pct, valor_unit, total]
    addRegistro(registros, valores)

# 3) Exportar CSV
with open(caminhoCsv, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=list(template.keys()), delimiter=";")
    writer.writeheader()
    writer.writerows(registros)

messagebox.showinfo(
    title="Concluído",
    message=f"CSV gerado em:\n{caminhoCsv}\n\nRegistros: {len(registros)}"
)