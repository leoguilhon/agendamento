import re


def validarNome(nome):
    # Verifica se o nome contém apenas letras e espaços
    return all(letra.isalpha() or letra.isspace() for letra in nome)

def validarCPF(cpf):
    # Verifica se o CPF possui 11 dígitos
    return len(cpf) == 11 and cpf.isdigit()

def validarEmail(email):
    # Verifica se o e-mail contém '@'
    return '@' in email

def validarDataAgendamento(data):
    # Verifica se a data de agendamento está no formato xx/xx/xxxx
    return re.match(r'\d{2}/\d{2}/\d{4}', data)