import os
import threading
from tkinter import Tk, filedialog, messagebox

# Importa a janela de espera (barra de progresso)
from ui.wait_window import WaitWindow

# Importa a função responsável por processar o PDF e gerar o CSV
from services.parser_conder import processar_pdf


# Cria a janela raiz do Tkinter
root = Tk()

# Esconde a janela principal, deixando apenas os diálogos aparecerem
root.withdraw()

# Variáveis usadas para informar se o processamento deu certo
# ou se ocorreu algum erro durante a execução da thread
erro_processamento = None
processamento_ok = False


# Abre a janela de seleção de arquivo
# O usuário deve escolher um PDF para ser processado
caminho_pdf = filedialog.askopenfilename(
    title="Selecione um arquivo",
    filetypes=[("PDF", "*.pdf"), ("Todos arquivos", "*.*")]
)


# Se o usuário cancelar a seleção, exibe aviso e encerra o programa
if not caminho_pdf:
    messagebox.showinfo("Cancelado", "Nenhum arquivo foi selecionado.")
    root.destroy()
    raise SystemExit


# Cria e exibe a janela de aguarde
wait = WaitWindow(root)
wait.show()


# Obtém a pasta do PDF selecionado
caminho_dir = os.path.dirname(caminho_pdf)

# Monta o caminho do CSV de saída na mesma pasta do PDF
caminho_csv = os.path.join(caminho_dir, "composicoes.csv")


def tarefa():
    """
    Função executada em uma thread separada.
    Ela chama o parser do PDF e registra se deu certo ou se houve erro.
    """
    global erro_processamento, processamento_ok

    try:
        # Processa o PDF e gera o CSV
        processar_pdf(caminho_pdf, caminho_csv)

        # Marca que o processamento terminou com sucesso
        processamento_ok = True

    except Exception as e:
        # Guarda a mensagem de erro para ser exibida depois na interface
        erro_processamento = str(e)


def verificar_fim():
    """
    Verifica periodicamente se a thread ainda está rodando.
    Se a thread terminou, fecha a janela de aguarde e mostra o resultado.
    """
    # Se a thread ainda estiver em execução,
    # agenda uma nova verificação daqui a 100 ms
    if thread.is_alive():
        root.after(100, verificar_fim)

    else:
        # Fecha a janela de aguarde
        wait.close()

        # Se houve erro, mostra uma mensagem de erro
        if erro_processamento:
            messagebox.showerror("Erro", f"Ocorreu um erro:\n{erro_processamento}")

        # Se terminou com sucesso, mostra a mensagem final
        elif processamento_ok:
            messagebox.showinfo("Concluído", f"CSV gerado em:\n{caminho_csv}")

        # Encerra a aplicação
        root.destroy()


# Cria uma thread para executar a função tarefa()
# Isso evita travar a interface durante o processamento do PDF
thread = threading.Thread(target=tarefa)

# Inicia a execução da thread
thread.start()

# Inicia a checagem periódica para saber quando a thread termina
verificar_fim()

# Inicia o loop principal do Tkinter
root.mainloop()