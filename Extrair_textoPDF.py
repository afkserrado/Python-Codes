import PyPDF2
import openpyxl

# Função para extrair texto de cada página do PDF
def extrair_texto_pdf(caminho_pdf):
    with open(caminho_pdf, 'rb') as arquivo_pdf:
        leitor_pdf = PyPDF2.PdfReader(arquivo_pdf)
        texto = []
        for pagina in leitor_pdf.pages:
            texto.append(pagina.extract_text())
        return texto

# Função para salvar o texto extraído em uma planilha Excel
def salvar_em_excel(texto, caminho_excel):
    # Cria uma nova planilha Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Texto PDF"
    
    linha_excel = 1  # Começando da primeira linha da planilha

    for pagina in texto:
        # Dividir as linhas por quebra de linha
        linhas = pagina.split('\n')
        for linha in linhas:
            # Verifica se a linha não está vazia
            if linha.strip():
                ws[f'A{linha_excel}'] = linha
                linha_excel += 1  # Avança para a próxima linha

    # Salva a planilha
    wb.save(caminho_excel)
    print(f"Planilha salva em {caminho_excel}")

# Caminho do arquivo PDF e caminho da planilha Excel
caminho_pdf = ''
caminho_excel = ''

# Extrai o texto do PDF e salva em Excel
texto_extraido = extrair_texto_pdf(caminho_pdf)
salvar_em_excel(texto_extraido, caminho_excel)
