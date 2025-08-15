from pathlib import Path
from PIL import Image
import tkinter as tk
from tkinter import filedialog

# Verifica se um arquivo é uma imagem
def is_image(camObjeto):
    # Extensões válidas para imagens
    extensoes_imagens = ['.jfif', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']

    return camObjeto.is_file() and camObjeto.suffix.lower() in extensoes_imagens

# Cria uma janela oculta para usar o filedialog
root = tk.Tk()
root.withdraw() # Oculta a janela principal

# Caminho da pasta com os arquivos
#camPasta = Path(input("Informe o caminho das imagens: "))
camPasta = Path(filedialog.askdirectory(title="Selecione a pasta com as imagens"))

if not camPasta:
    print("Nenhuma pasta foi selecionada.")
    exit() # Finaliza o programa

# Arquivo txt onde serão escritos os dados
nomeArquivo = "dados.txt"

# Caminho do arquivo txt
camArquivo = camPasta / nomeArquivo

# Abre o arquivo txt para escrita
dados = open(camArquivo, "w", encoding = "utf-8")

try: 
    # Verifica se o caminho informado existe e é uma pasta válida
    if camPasta.exists() and camPasta.is_dir():
        camObjetos = camPasta.iterdir()

        for camObjeto in camObjetos:
            try: 
                if is_image(camObjeto):
                    imagem = Image.open(camObjeto) # Lê a imagem
                    largura, altura = imagem.size # Obtém o tamanho da imagem

                    # Escreve as informações no arquivo
                    dados.write(f"{camObjeto.name} - Largura: {largura}px, Altura: {altura}px\n")

            except Exception as erro:
                print(f"Erron ao acessar o arquivo {camObjeto.name}: {erro}.")
                continue # Passa para o próximo arquivo
    
    else:
        print("Erro: o caminho informado não existe ou não é uma pasta válida.")

except Exception as erro:
    print(f"Erro ao acessar o caminho: {erro}.")

# Garante que o arquivo seja fechado mesmo se ocorrer um erro
finally: 
    dados.close()