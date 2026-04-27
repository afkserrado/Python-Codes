# Funções auxiliares

# Modelo dos registros
template = {
    "categoria": None,
    "codigo": None,
    "banco": None,
    "quantidade": None,
    "porcentagem": None,
    "valor_unit": None,
    "total": None,
}

# Adiciona um registro à lista de registros
def addRegistro(registros, valores):
    registro = template.copy()

    for chave, valor in zip(registro.keys(), valores):
        registro[chave] = valor

    registros.append(registro)