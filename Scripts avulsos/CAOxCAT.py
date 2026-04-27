import os
import re
import PyPDF2

def extrairDados(pasta, lista, padrao, padraoART):
    
    for arquivo in os.listdir(pasta):
        # Inicializando o dicionário
        dictPDF = {"ID": None, "ART": None}
        
        if arquivo.lower().endswith(".pdf"):
            # Junta o caminho da pasta com o nome do arquivo
            caminho_arquivo = os.path.join(pasta, arquivo)

            try:
                # Abrindo o arquivo em modo binário (melhor alternativa para pdfs)
                with open(caminho_arquivo, "rb") as pdf_file:
                    # Lê o pdf
                    pdf = PyPDF2.PdfReader(pdf_file)
                    
                    # Inicialização
                    texto = "" 

                    # Extrai o texto das páginas do pdf
                    for pagina in pdf.pages:
                        texto += pagina.extract_text() or "" # Retorna vazio se retornar None

                    # Busca a ocorrência no texto que bate com o padrão
                    match = padrao.search(texto) 
                    matchART = padraoART.search(texto)

                    # Armazena o par ID (CAO ou CAT) e ART
                    dictPDF["ID"] = match.group(1) if match else None
                    dictPDF["ART"] = matchART.group(1) if matchART else None

                    # Armazena o par na lista
                    lista.append(dictPDF)

            except Exception as e:
                print(f"Erro ao processar {arquivo}: {e}")


# Main
camCAOs = input("Informe o caminho da pasta das CAOs: ")
camCATs = input("Informe o caminho da pasta das CATs: ")
camSaida = input("Informe o caminho do arquivo de saída: ")

# Inicializa as listas
listaCAOs = []
listaCATs = []

# Regex para pegar o número da CAO no formato XXXXX/AAAA
padraoCAO = re.compile(r"Certidão de Acervo Operacional\s*[-–—]\s*CAO nº (\d+/\d{4})")

# Regex para pegar o número da CAT no formato XXXXX/AAAA
padraoCAT = re.compile(r"Certidão de Acervo Técnico nº (\d+/\d{4})")

# Regex para pegar o número da ART no formato UFXXXXXXXXXXX
padraoART = re.compile(r"Número da ART: ([A-Z]{2}\d+)")

# Extrai os dados
extrairDados(camCAOs, listaCAOs, padraoCAO, padraoART)
extrairDados(camCATs, listaCATs, padraoCAT, padraoART)

# Verifica se a CAT tem CAO
for cat_dict in listaCATs:
    art_num = cat_dict["ART"]

    cao_encontrada = None
    for cao_dict in listaCAOs:
        if cao_dict["ART"] == art_num:
            cao_encontrada = cao_dict["ID"]
            break

    cat_dict["CAO"] = cao_encontrada

camSaida = os.path.join(camSaida, "listaCATs.txt")
with open (camSaida, "w", encoding="utf-8") as f:
    for cat_dict in listaCATs:
        linha = f"CAT: {cat_dict['ID']}, ART: {cat_dict['ART']}, CAO: {cat_dict.get('CAO', None)}\n"
        f.write(linha)
    
    f.write("\n")
    for cao_dict in listaCAOs:
        linha = f"CAO: {cao_dict['ID']}, ART: {cao_dict['ART']}\n"
        f.write(linha)

print("Arquivo gerado.")