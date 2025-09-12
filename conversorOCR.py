import pytesseract
from pdf2image import convert_from_path
import pandas as pd
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

all_data = []

# === 2. Extrair texto com OCR usando image_to_data ===
for page in pages:
    data = pytesseract.image_to_data(page, lang="por", output_type=pytesseract.Output.DATAFRAME)
    
    # Remove linhas sem texto
    data = data[data.text.notna() & (data.text.str.strip() != "")]
    
    # Agrupar palavras por linha (usando número da linha na imagem)
    grouped = data.groupby("line_num")["text"].apply(lambda x: " ".join(x))
    
    all_data.extend(grouped.tolist())

# === 3. Criar DataFrame para exportar ===
# Aqui cada linha será uma linha no Excel; ainda não separa colunas perfeitamente
df = pd.DataFrame(all_data, columns=["Linha"])

# === 4. Exportar para Excel ===
df.to_excel(output_path, index=False)

print(f"✅ Conversão concluída! Arquivo salvo em: {output_path}")