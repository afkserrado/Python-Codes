import re
import csv
import pdfplumber
from services.unidades import UNIDADES_VALIDAS


def eh_fragmento_curto_de_continuacao(texto):
    texto = " ".join(texto.split())

    if not texto:
        return False

    if re.fullmatch(r"\d+\)?", texto):
        return True

    if re.fullmatch(r"[A-Z]{2,}[_/-]?\d+(?:/\d+)?\)?", texto):
        return True

    if len(texto) <= 12 and re.fullmatch(r"[A-Z0-9/().,_+-]+", texto):
        return True

    return False


def juntar_linhas_descricao(texto_anterior, novo_texto, min_palavras=3):
    a = " ".join(texto_anterior.split())
    b = " ".join(novo_texto.split())

    if not a:
        return b
    if not b:
        return a

    if eh_fragmento_curto_de_continuacao(b):
        return a + " " + b

    palavras_a = a.split()
    palavras_b = b.split()

    max_sobreposicao = min(len(palavras_a), len(palavras_b))

    for n in range(max_sobreposicao, min_palavras - 1, -1):
        if palavras_a[-n:] == palavras_b[:n]:
            return " ".join(palavras_a + palavras_b[n:])

    return a + " " + b


def finalizar_cabecalho_pendente(cabecalho_pendente, registros):
    """
    Grava o cabeçalho pendente nos registros.
    A unidade já foi extraída na inicialização do cabeçalho (primeira linha),
    então aqui apenas consolidamos o que está armazenado.
    """
    if not cabecalho_pendente:
        return

    registros.append({
        "cod_composicao": cabecalho_pendente["cod_composicao"],
        "tipo": "CABECALHO",
        "cod_item": cabecalho_pendente["cod_item"],
        "descricao": " ".join(cabecalho_pendente["descricao"].split()),
        "unidade": cabecalho_pendente["unidade"],
        "coeficiente": "",
        "preco_unitario": "",
        "preco_total": "",
        "linha": " ".join(cabecalho_pendente["linha"].split())
    })


def processar_pdf(caminho_pdf, caminho_csv):
    re_cod_hifen = re.compile(r"^\s*(\d{2}-\d{2}-\d{2}-\d{3})\b")
    re_cod_num = re.compile(r"^\s*(\d{4,6})\b")
    re_cod_I = re.compile(r"^\s*(I\d+)\b")

    num_ptbr = r"\d+(?:\.\d{3})*,\d+"
    regex_unid = r"(?:%s)" % "|".join(re.escape(u) for u in UNIDADES_VALIDAS)

    re_item_completo = re.compile(
        rf"^(?P<descricao>.+?)\s+"
        rf"(?P<unidade>{regex_unid})\s+"
        rf"(?P<coef>{num_ptbr})\s+"
        rf"(?P<preco_unit>{num_ptbr})\s+"
        rf"(?P<preco_total>{num_ptbr})$"
    )

    # Regex para extrair a unidade do fim da primeira linha do cabeçalho.
    # Estrutura da primeira linha: <descricao_inicial> <unidade>
    # A unidade é a coluna UNID. do PDF, que aparece ao final da linha extraída.
    re_cabecalho_unidade = re.compile(
        rf"^(?P<descricao>.+?)\s+(?P<unidade>{regex_unid})$"
    )

    lixo_contains = (
        "Encargos Sociais Não Desonerada:",
        "COMPOSIÇÃO ANALÍTICA",
        "Hora",
        "BDI:",
        "Projeto:",
        "Ref.:",
        "TEIXEIRA DE FREITAS - BA",
        "CÓDIGO",
        "Sub Total",
        "Data do Relatório:"
    )

    registros = []
    comp_atual = None
    cabecalho_pendente = None

    with pdfplumber.open(caminho_pdf) as pdf:
        for page in pdf.pages:
            texto = page.extract_text()
            if not texto:
                continue

            for linha in texto.splitlines():
                linha = linha.rstrip("\n")
                linha_norm = " ".join(linha.split())

                if not linha_norm:
                    continue

                if any(t in linha_norm for t in lixo_contains):
                    continue

                if linha_norm in ("Insumos", "Composição Auxiliar"):
                    continue

                if "Total" in linha_norm:
                    finalizar_cabecalho_pendente(cabecalho_pendente, registros)
                    cabecalho_pendente = None
                    comp_atual = None

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

                m_hifen = re_cod_hifen.match(linha)
                m_num = re_cod_num.match(linha)
                m_i = re_cod_I.match(linha)
                m_cod = m_hifen or m_num or m_i

                # Início de nova composição (cabeçalho)
                if comp_atual is None and m_cod and not m_i:
                    codigo_comp = m_cod.group(1)
                    comp_atual = codigo_comp

                    # Remove o código do início da linha
                    linha_sem_codigo = linha_norm[m_cod.end():].strip()

                    # Tenta extrair a unidade do FIM da primeira linha.
                    # Esta é a única linha onde a unidade (coluna UNID. do PDF)
                    # aparece. Linhas de continuação são apenas texto de descrição.
                    m_cab = re_cabecalho_unidade.match(linha_sem_codigo)

                    if m_cab:
                        descricao_inicial = m_cab.group("descricao").strip()
                        unidade_cab = m_cab.group("unidade").strip()
                    else:
                        descricao_inicial = linha_sem_codigo
                        unidade_cab = ""

                    cabecalho_pendente = {
                        "cod_composicao": codigo_comp,
                        "cod_item": codigo_comp,
                        "descricao": descricao_inicial,
                        "unidade": unidade_cab,
                        "linha": linha_norm
                    }
                    continue

                # Cabeçalho ainda aberto: acumula linhas de continuação
                if cabecalho_pendente is not None:
                    if m_cod is None:
                        # Linha sem código = continuação da descrição do cabeçalho.
                        # Nunca extrai unidade aqui: estas linhas são só texto.
                        cabecalho_pendente["descricao"] = juntar_linhas_descricao(
                            cabecalho_pendente["descricao"],
                            linha_norm
                        )
                        cabecalho_pendente["linha"] = juntar_linhas_descricao(
                            cabecalho_pendente["linha"],
                            linha_norm
                        )
                        continue

                    # Linha com código: verifica se já é item completo
                    linha_sem_codigo_tmp = linha_norm[m_cod.end():].strip()
                    m_item_tmp = re_item_completo.match(linha_sem_codigo_tmp)

                    if not m_i and not m_item_tmp:
                        # Ainda é continuação do cabeçalho
                        cabecalho_pendente["descricao"] = juntar_linhas_descricao(
                            cabecalho_pendente["descricao"],
                            linha_norm # <--- CORRIGIDO: Usa a linha inteira, preservando o número
                        )
                        cabecalho_pendente["linha"] = juntar_linhas_descricao(
                            cabecalho_pendente["linha"],
                            linha_norm
                        )
                        continue

                # Linha sem código: continuação do item anterior
                if not m_cod:
                    if (
                        comp_atual is not None and
                        registros and
                        registros[-1]["tipo"] == "ITEM" and
                        registros[-1]["cod_composicao"] == comp_atual
                    ):
                        registros[-1]["descricao"] = juntar_linhas_descricao(
                            registros[-1]["descricao"],
                            linha_norm
                        )
                        registros[-1]["linha"] = juntar_linhas_descricao(
                            registros[-1]["linha"],
                            linha.strip()
                        )
                    continue

                # Item da composição
                if comp_atual is not None:
                    codigo_item = m_cod.group(1)
                    linha_sem_codigo = linha_norm[m_cod.end():].strip()
                    m_item = re_item_completo.match(linha_sem_codigo)

                    if m_item:
                        if cabecalho_pendente is not None:
                            finalizar_cabecalho_pendente(cabecalho_pendente, registros)
                            cabecalho_pendente = None

                        registros.append({
                            "cod_composicao": comp_atual,
                            "tipo": "ITEM",
                            "cod_item": codigo_item,
                            "descricao": m_item.group("descricao"),
                            "unidade": m_item.group("unidade"),
                            "coeficiente": m_item.group("coef"),
                            "preco_unitario": m_item.group("preco_unit"),
                            "preco_total": m_item.group("preco_total"),
                            "linha": linha.strip()
                        })
                    else:
                        if (
                            registros and
                            registros[-1]["tipo"] == "ITEM" and
                            registros[-1]["cod_composicao"] == comp_atual
                        ):
                            registros[-1]["descricao"] = juntar_linhas_descricao(
                                registros[-1]["descricao"],
                                linha_norm
                            )
                            registros[-1]["linha"] = juntar_linhas_descricao(
                                registros[-1]["linha"],
                                linha.strip()
                            )

                    continue

    if cabecalho_pendente is not None:
        finalizar_cabecalho_pendente(cabecalho_pendente, registros)

    with open(caminho_csv, "w", newline="", encoding="utf-8-sig") as f:
        fieldnames = [
            "cod_composicao", "tipo", "cod_item",
            "descricao", "unidade", "coeficiente",
            "preco_unitario", "preco_total",
            "linha"
        ]

        w = csv.DictWriter(f, fieldnames=fieldnames, delimiter="|")
        w.writeheader()
        w.writerows(registros)