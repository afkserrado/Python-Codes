import re
import csv
import pdfplumber
from tkinter import Tk, filedialog, messagebox
import os

root = Tk() # Cria a janela raiz (root do window), que funciona como o nó raiz de uma hierarquia de widgets
root.withdraw() # Esconde a janela raiz do tk

# Abre uma janela de seleção de arquivo
caminhoPdf = filedialog.askopenfilename(
    title="Selecione um arquivo",
    filetypes=[("PDF", "*.pdf"), ("Todos arquivos", "*.*")]
)

caminhoDir = os.path.dirname(caminhoPdf)
caminhoCsv = os.path.join(caminhoDir, "composicoes.csv")

#print("Caminho selecionado:" + caminhoPdf)

# Regex para detectar código no início (após espaços)
re_cod_hifen = re.compile(r"^\s*(\d{2}-\d{2}-\d{2}-\d{3})\b") # NN-NN-NN-NNN
re_cod_num   = re.compile(r"^\s*(\d{4,6})\b") # NNNN a NNNNNN
re_cod_I     = re.compile(r"^\s*(I\d+)\b") #IN... (começa com a letra 'I', seguido de um ou mais dígitos)

# Regex para detectar as "colunas" da linha de itens
num_ptbr = r"\d+(?:\.\d{3})*,\d+"
re_item_campos = re.compile(
    rf"^(?P<descricao>.+?)\s+"
    rf"(?P<coef>{num_ptbr})\s+"
    rf"(?P<preco_unit>{num_ptbr})\s+"
    rf"(?P<preco_total>{num_ptbr})$"
)

# Linhas “lixo” (informações fixas do PDF)
lixo_contains = (
    "Encargos Sociais Não Desonerada:",
    "COMPOSIÇÃO ANALÍTICA",
    "Hora",
    "BDI:",
    "Projeto:",
    "Ref.:",
    "TEIXEIRA DE FREITAS - BA",
    "CÓDIGO",
    "Sub Total"
)

registros = [] # Itens extraídos (lista de dicionários)
comp_atual = None # Código da composição atual (None = fora de composição)

# Abre o pdf
with pdfplumber.open(caminhoPdf) as pdf:
    
    # Percorre as páginas do pdf
    for page in pdf.pages:
        
        # Obtém o texto da página atual
        texto = page.extract_text()
        if not texto:
            continue

        # Percorre as linhas do texto atual
        for linha in texto.splitlines():
            # Remove as quebras de linha do lado direito da linha
            linha = linha.rstrip("\n")

            # 1) Normalização
                # Remove espaços no início e no fim da linha
                # Elimina sequência de whitespaces (espaços, tabs, quebras de linha etc.) e cria uma lista sem elementos vazios
                # Troca múltiplos espaços/tabs por um único espaço entre as palavras
            linha_norm = " ".join(linha.split())

            # 2) Linhas ignoradas

            # Pula linhas vazias e cabeçalhos
            if not linha_norm:
                continue

            # Verifica se a linha normalizada contém algum lixo
            # Se tiver lixo, pula a linha
            if any(t in linha_norm for t in lixo_contains):
                continue

            if linha_norm in ("Insumos", "Composição Auxiliar"):
                continue

            # Detecta o fim da composição
            if "Total" in linha_norm:
                comp_atual = None

                # Adiciona uma linha em branco no CSV para separar composições
                registros.append({
                    "cod_composicao": "",
                    "tipo": "",
                    "cod_item": "",
                    "descricao": "",
                    "unidade": "",
                    "coeficiente": "",
                    "preco_unitario": "",
                    "preco_total": "",
                    "linha": ""
                })

                continue

            # Verifica se a linha começa com um código de CPU/insumo
            m_hifen = re_cod_hifen.match(linha)
            m_num   = re_cod_num.match(linha)
            m_i     = re_cod_I.match(linha)

            # Ignora linhas que não começam com código de CPU/insumo
            if not (m_hifen or m_num or m_i):
                continue

            # 3) Linhas buscadas

            # Título da composição
            if comp_atual is None and not m_i: 
                # Obtém o código da linha
                comp_atual = (m_hifen or m_num).group(1)

                # Guarda a linha atual
                registros.append({
                    "cod_composicao": comp_atual,
                    "tipo": "CABECALHO",
                    "linha": linha.strip(), 
                })

                continue

            # Itens da composição
            if comp_atual is not None:
                # Obtém o código da linha
                codigo_item = (m_hifen or m_num or m_i).group(1)

                m = re_item_campos.match(linha_norm)

                if m:
                    descricao = m.group("descricao")
                    coef = m.group("coef")
                    preco_unit = m.group("preco_unit")
                    preco_total = m.group("preco_total")
                else:
                    # fallback: não conseguiu separar, guarda a linha inteira
                    descricao = linha_norm
                    coef = preco_unit = preco_total = ""

                # Guarda a linha atual
                registros.append({
                    "cod_composicao": comp_atual,
                    "tipo": "ITEM",
                    "cod_item": codigo_item,
                    "descricao": descricao,
                    "unidade": "",
                    "coeficiente": coef,
                    "preco_unitario": preco_unit,
                    "preco_total": preco_total,
                    "linha": linha.strip(), 
                })

# Cria um arquivo csv em modo de escrita
with open(caminhoCsv, "w", newline="", encoding="utf-8") as f:
    fieldnames = [
        "cod_composicao", "tipo", "cod_item",
        "descricao", "unidade", "coeficiente",
        "preco_unitario", "preco_total",
        "linha"
    ]

    # Define o escritor de um arquivo, as colunas e a ordem delas
    w = csv.DictWriter(f, fieldnames=fieldnames) 

    # Escreve o cabeçalho na primeira linha do csv, com os campos definidos em fieldnames
    w.writeheader()

    # Escreve as linhas
    w.writerows(registros)

# Mensagem de confirmação
messagebox.showinfo("Concluído", f"CSV gerado em:\n{caminhoCsv}")