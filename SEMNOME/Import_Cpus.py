import tkinter as tk
from tkinter import filedialog
from openpyxl import load_workbook
from pathlib import Path

from ExcelLoader import ExcelLoader
from Cpus import Cpus

# Inicializa o Tkinter criando a janela raiz
root = tk.Tk()

# Esconde a janela raiz do Tkinter
root.withdraw()

# Abre uma janela para selecionar o arquivo desejado
wb_dest_path_name = filedialog.askopenfilename(
    title="Selecione o arquivo do orçamento",
    filetypes=[("Arquivos Excel", "*.xlsx *.xlsm *.xlsb")]
)

wb_dest_path = Path(wb_dest_path_name)
path = wb_dest_path.parent

#print(f"path: {path}")
#print(f"wb_dest_path: {wb_dest_path}")

wb_orig_name = "CPUs.xlsx"
ws_orig_name = "CPUs"
wb_dest = load_workbook(wb_dest_path, keep_vba=True)
ws_dest_name = "CPUs"
ws_dest = wb_dest[ws_dest_name]

obj_Cpus = Cpus(path, wb_orig_name, ws_orig_name, wb_dest, ws_dest)
obj_Cpus.open_workbooks()
obj_Cpus.import_data()
wb_dest.save(wb_dest_path)
obj_Cpus.ajust_layout(wb_dest_path_name, ws_dest_name)