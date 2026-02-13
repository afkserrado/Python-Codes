import tkinter as tk
from tkinter import filedialog, messagebox

# Inicializa o Tkinter criando a janela raiz
root = tk.Tk()

# Esconde a janela raiz do Tkinter
root.withdraw()

# Abre uma janela para selecionar a pasta desejada e guarda o caminho
cam_origem = filedialog.askdirectory(
    title="Selecione a pasta que contém os arquivos do orçamento", 
    mustexist=True
)

# Valida o caminho
if not cam_origem:
    messagebox.showwarning(
        title="Atenção",
        message="Nenhuma pasta foi selecionada. Operação cancelada."
    )

else:
    print("Pasta selecionada.")

root.destroy() # Encerra o Tkinter

