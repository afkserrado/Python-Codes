import re
import csv
import pdfplumber


def processar_pdf(caminho_pdf, caminho_csv):
    """
    Extrai composições de preço unitário de um PDF modelo CONDER/BA
    e salva os dados em um arquivo CSV.

    caminho_pdf  -> caminho do arquivo PDF de entrada
    caminho_csv  -> caminho do arquivo CSV de saída
    """
    # Regex para detectar código de composição/insumo no início da linha
    # Ex.: "12-34-56-789", "12345", "I123"
    re_cod_hifen = re.compile(r"^\s*(\d{2}-\d{2}-\d{2}-\d{3})\b")
    re_cod_num   = re.compile(r"^\s*(\d{4,6})\b")
    re_cod_I     = re.compile(r"^\s*(I\d+)\b")

    # Padrão de número brasileiro (com pontos milhares e vírgula decimal)
    # Ex.: "1.234,50"
    num_ptbr = r"\d+(?:\.\d{3})*,\d+"

    # Regex para separar a linha de item de composição em campos
    # A linha tem padrão: <descricao> <coef> <preco_unit> <preco_total>
    re_item_campos = re.compile(
        rf"^(?P<descricao>.+?)\s+"
        rf"(?P<coef>{num_ptbr})\s+"
        rf"(?P<preco_unit>{num_ptbr})\s+"
        rf"(?P<preco_total>{num_ptbr})$"
    )

    # Linhas fixas de cabeçalho/rodapé que devem ser ignoradas
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

    # Lista que acumulará todos os registros (cabeçalhos + itens)
    registros = []

    # Variável que guarda o código da composição atual (None = fora de composição)
    comp_atual = None

    # Abre o PDF para extração de texto
    with pdfplumber.open(caminho_pdf) as pdf:
        # Percorre todas as páginas do PDF
        for page in pdf.pages:
            texto = page.extract_text()
            if not texto:
                continue

            # Percorre cada linha do texto extraído
            for linha in texto.splitlines():
                # Remove quebras de linha à direita
                linha = linha.rstrip("\n")

                # Normaliza a linha: remove espaços extras e junta em uma única string
                linha_norm = " ".join(linha.split())

                # Pula linhas vazias
                if not linha_norm:
                    continue

                # Pula linhas que contiverem qualquer um dos textos de "lixo"
                if any(t in linha_norm for t in lixo_contains):
                    continue

                # Pula linhas de seções auxiliares
                if linha_norm in ("Insumos", "Composição Auxiliar"):
                    continue

                # Detecta o fim da composição atual (aparece "Total")
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

                # Verifica se a linha começa com algum código (CPU/insumo)
                m_hifen = re_cod_hifen.match(linha)
                m_num   = re_cod_num.match(linha)
                m_i     = re_cod_I.match(linha)

                # Se não começar com código, pula esta linha
                if not (m_hifen or m_num or m_i):
                    continue

                # Caso esteja fora de qualquer composição e o código não for "I..." (insumo):
                # trata como cabeçalho de uma nova composição
                if comp_atual is None and not m_i:
                    comp_atual = (m_hifen or m_num).group(1)
                    registros.append({
                        "cod_composicao": comp_atual,
                        "tipo": "CABECALHO",
                        "linha": linha.strip(),
                    })
                    continue

                # Caso esteja dentro de uma composição:
                # trata a linha como item (insumo/mão de obra/equipamento)
                if comp_atual is not None:
                    codigo_item = (m_hifen or m_num or m_i).group(1)
                    # Tenta separar a linha em campos usando o regex de item
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

    # Salva os registros em um arquivo CSV
    with open(caminho_csv, "w", newline="", encoding="utf-8-sig") as f:
        # Define os nomes das colunas do CSV
        fieldnames = [
            "cod_composicao", "tipo", "cod_item",
            "descricao", "unidade", "coeficiente",
            "preco_unitario", "preco_total",
            "linha"
        ]

        # Criador de CSV baseado em dicionários
        w = csv.DictWriter(f, fieldnames=fieldnames, delimiter="|")

        # Escreve o cabeçalho (nomes das colunas)
        w.writeheader()

        # Escreve uma linha de CSV para cada registro
        w.writerows(registros)