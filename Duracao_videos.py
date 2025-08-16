from pathlib import Path
from moviepy import VideoFileClip
import tkinter as tk
from tkinter import filedialog

# Verifica se um arquivo é um vídeo
def is_video(camObjeto):
    # Extensões válidas para imagens
    extensoes_video = [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".mpeg"]

    return camObjeto.is_file() and camObjeto.suffix.lower() in extensoes_video

# Cria uma janela oculta para usar o filedialog
root = tk.Tk() # Cria a janela principal do Tkinter (necessária para inicializar a biblioteca)
root.withdraw() # Oculta essa janela, para que o usuário veja apenas a caixa de diálogo

# Caminho da pasta com os vídeos
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

        # Duração total
        total_segundos = 0

        for camObjeto in camObjetos:
            try: 
                if is_video(camObjeto):
                    video = VideoFileClip(camObjeto) # Lê o vídeo
                    duracao = int(video.duration) # Obtém a duração
                    total_segundos += duracao
                    video.close() # Fecha o vídeo
                    
                    # Converte para hh:mm:ss fixo
                    horas = duracao // 3600
                    minutos = (duracao % 3600) // 60
                    segundos = duracao % 60
                    tempo = f"{horas:02d}:{minutos:02d}:{segundos:02d}"

                    # Escreve as informações no arquivo
                    dados.write(f"{camObjeto.name} - Duração: {tempo}\n")

            except Exception as erro:
                print(f"Erron ao acessar o arquivo {camObjeto.name}: {erro}.")
                continue # Passa para o próximo arquivo
        
        # Escreve a duração total (soma de todos os vídeos)
        horas = total_segundos // 3600
        minutos = (total_segundos % 3600) // 60
        segundos = total_segundos % 60
        tempo = f"{horas:02d}:{minutos:02d}:{segundos:02d}"

        # Escreve as informações no arquivo
        dados.write(f"Duração total: {tempo}\n")

    else:
        print("Erro: o caminho informado não existe ou não é uma pasta válida.")

except Exception as erro:
    print(f"Erro ao acessar o caminho: {erro}.")

# Garante que o arquivo seja fechado mesmo se ocorrer um erro
finally: 
    dados.close()