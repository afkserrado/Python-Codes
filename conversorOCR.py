import pytesseract
from pdf2image import convert_from_path
import pandas as pd
import re

import pytesseract
from pdf2image import convert_from_path
import pandas as pd
import re
import os

# Caminho do executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Forçar TESSDATA_PREFIX para o diretório tessdata
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"

# Caminhos do PDF e saída
pdf_path = r"C:\Users\ander\Downloads\planilha OCR.pdf"
output_path = r"C:\Users\ander\Downloads\planilha OCR.xlsx"

# Caminho do Poppler
poppler_path = r"C:\Program Files\poppler-25.07.0\Library\bin"

# === 1. Converter PDF em imagens ===
pages = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)

dados_tabelas = []

# === 2. Extrair texto com OCR página por página ===
for i, page in enumerate(pages):
    texto = pytesseract.image_to_string(page, lang="por")
    
    # === 3. Transformar em linhas ===
    linhas = texto.strip().split("\n")
    linhas = [l for l in linhas if l.strip() != ""]  # remove linhas vazias
    
    # Tentativa de separar colunas por múltiplos espaços ou tabulação
    linhas_processadas = [re.split(r"\s{2,}|\t", l) for l in linhas]
    
    # Guardar em lista
    dados_tabelas.extend(linhas_processadas)

# === 4. Exportar para Excel ===
df = pd.DataFrame(dados_tabelas)
df.to_excel(output_path, index=False, header=False)

print(f"✅ Conversão concluída! Arquivo salvo em: {output_path}")
