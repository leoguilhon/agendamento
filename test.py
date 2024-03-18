import base64

# Caminho para o arquivo ICO
caminho_arquivo_ico = 'agendamento.ico'

# Lê o arquivo ICO como bytes
with open('agendamento.ico', 'rb') as arquivo_ico:
    dados_ico = arquivo_ico.read()

# Converte os bytes para Base64
base64_ico = base64.b64encode(dados_ico).decode('utf-8')

print(base64_ico)