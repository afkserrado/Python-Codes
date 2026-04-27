from pathlib import Path
from moviepy import VideoFileClip
import tkinter as tk
from tkinter import filedialog

# Função para verificar se é um vídeo
def is_video(camObjeto):
    extensoes_video = [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".mpeg"]
    return camObjeto.is_file() and camObjeto.suffix.lower() in extensoes_video

# Função recursiva para processar pastas
def processar_pasta(pasta: Path):
    if not pasta.exists() or not pasta.is_dir():
        return

    total_segundos = 0
    arquivos_videos = []

    # Itera pelos itens da pasta
    for item in pasta.iterdir():
        if is_video(item):
            try:
                video = VideoFileClip(str(item))
                duracao = int(video.duration)
                total_segundos += duracao
                video.close()
                arquivos_videos.append((item.name, duracao))
            except Exception as e:
                print(f"Erro ao acessar {item.name}: {e}")
                arquivos_videos.append((item.name, None))  # Marca como inválido
        elif item.is_dir():
            # Chamada recursiva para subpasta
            processar_pasta(item)

    # Se houver vídeos, cria/atualiza o dados.txt
    if arquivos_videos:
        camArquivo = pasta / "dados.txt"
        with open(camArquivo, "w", encoding="utf-8") as dados:
            for nome, duracao in arquivos_videos:
                if duracao is None:
                    dados.write(f"{nome} - None\n")
                else:
                    horas = duracao // 3600
                    minutos = (duracao % 3600) // 60
                    segundos = duracao % 60
                    tempo = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
                    dados.write(f"{nome} - Duração: {tempo}\n")

            # Duração total da pasta
            horas = total_segundos // 3600
            minutos = (total_segundos % 3600) // 60
            segundos = total_segundos % 60
            tempo_total = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
            dados.write(f"\nDuração total: {tempo_total}\n")
        print(f"Processado: {pasta} → Duração total: {tempo_total}")

# -------------------------------
# Programa principal
# -------------------------------
root = tk.Tk()
root.withdraw()
camPasta = Path(filedialog.askdirectory(title="Selecione a pasta raiz"))

if camPasta:
    processar_pasta(camPasta)
else:
    print("Nenhuma pasta foi selecionada.")
