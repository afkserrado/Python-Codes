import os

def capitalizar_nomes_arquivos(caminho_pasta):
    # Verifica se o diretório existe
    if os.path.exists(caminho_pasta) and os.path.isdir(caminho_pasta):
        # Percorre todos os arquivos na pasta
        for arquivo in os.listdir(caminho_pasta):
            # Cria o caminho completo do arquivo
            caminho_arquivo = os.path.join(caminho_pasta, arquivo)
            
            # Verifica se é um arquivo (não uma subpasta)
            if os.path.isfile(caminho_arquivo):
                # Capitaliza o nome do arquivo (preserva a extensão)
                nome, extensao = os.path.splitext(arquivo)
                nome_capitalizado = nome.upper() + extensao
                
                # Cria o novo caminho com o nome capitalizado
                novo_caminho = os.path.join(caminho_pasta, nome_capitalizado)
                
                # Renomeia o arquivo
                os.rename(caminho_arquivo, novo_caminho)
                print(f"Arquivo renomeado: {arquivo} -> {nome_capitalizado}")
    else:
        print("O caminho fornecido não é válido ou não é uma pasta.")

# Caminho da pasta (ajuste conforme necessário)
caminho_pasta = r"C:\Users\ander\OneDrive\_APS LICITAÇÕES OPERACIONAL\04. LOGOS E ASSINATURAS CLIENTES"  # Substitua pelo caminho desejado

# Chama a função para renomear os arquivos
capitalizar_nomes_arquivos(caminho_pasta)
