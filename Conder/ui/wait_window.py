# Importa o widget Toplevel, usado para criar uma nova janela filha,
# e o widget Label, usado para mostrar textos na interface.
from tkinter import Toplevel, Label

# Importa o módulo ttk, que contém widgets visuais mais modernos do Tkinter,
# como a barra de progresso.
from tkinter import ttk

# Classe responsável por criar, mostrar e fechar a janela de espera.
class WaitWindow:

    # parent   -> janela "pai"
    # titulo   -> texto que aparece na barra de título da janela
    # mensagem -> texto exibido dentro da janela
    def __init__(self, parent, titulo="Aguarde", mensagem="Processando PDF...\nAguarde."):

        # Cria uma nova janela do tipo Toplevel.
        # Essa janela fica vinculada à janela pai (parent),
        # mas funciona como uma janela separada.
        self.window = Toplevel(parent)

        # Define o título da janela.
        self.window.title(titulo)

        # Define o tamanho da janela: 300 pixels de largura por 100 de altura.
        self.window.geometry("300x100")

        # Impede que o usuário redimensione a janela:
        # False para largura, False para altura.
        self.window.resizable(False, False)

        # Faz a janela capturar o foco dos eventos do Tkinter.
        # Na prática, isso transforma essa janela em "modal":
        # enquanto ela estiver aberta, o usuário não interage com a janela principal.
        self.window.grab_set()

        # Cria um rótulo (Label) dentro da janela de espera.
        # self.window é o widget pai do Label.
        # text=mensagem define o texto mostrado.
        # pady=10 adiciona espaço vertical interno para o texto não ficar colado.
        # .pack() posiciona o widget automaticamente na janela.
        Label(self.window, text=mensagem, pady=10).pack()

        # Cria uma barra de progresso visual.
        # self.window             -> janela onde a barra será exibida
        # mode="indeterminate"    -> modo indefinido, usado quando não sabemos
        #                            a porcentagem exata do progresso
        # length=250             -> largura visual da barra em pixels
        # Nesse modo, a barra fica animando de um lado para o outro
        # para indicar que algo está acontecendo.
        self.barra = ttk.Progressbar(self.window, mode="indeterminate", length=250)

        # Exibe a barra na janela usando pack().
        # pady=10 adiciona espaço vertical em volta da barra.
        self.barra.pack(pady=10)

    # Método responsável por exibir/ativar a animação da janela de espera.
    def show(self):

        # Inicia a animação automática da barra de progresso.
        # O valor 10 representa o intervalo, em milissegundos,
        # entre os avanços da animação.
        self.barra.start(10)

        # Força a janela a ser atualizada imediatamente.
        # Isso é importante para garantir que a janela apareça na tela
        # antes do processamento pesado começar.
        self.window.update()

    # Método responsável por encerrar a janela de espera.
    def close(self):

        # Para a animação da barra de progresso.
        self.barra.stop()

        # Destrói a janela completamente, removendo-a da interface.
        self.window.destroy()