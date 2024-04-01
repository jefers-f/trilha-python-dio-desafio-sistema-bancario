import textwrap

def menu():
    menu = """
    ================= Menu ===================
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Nova Conta
    [5] Lista Contas
    [6] Novo Usuário
    [7] Sair
    => """
    return input(textwrap.dedent(menu))

def depositar(saldo,valor, extrato, /):
    if valor > 0:
            saldo += valor
            extrato += f'+ R${valor:.2f}\n'
            print('Depósito Realizado com sucesso!')
    else:
        print('Operação não pode ser realizada, o valor informado é inválido.')

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    execedeu_saldo = valor > saldo
    execedeu_limite = valor > limite
    execedeu_saques = numero_saques >= limite_saques

    if execedeu_saldo:
        print('Saldo Insuficiente, operação cancelada.')
    elif execedeu_limite:
        print('O limite de saque é de R$500,00 por saque. Operação cancelada.')
    elif execedeu_saques:
        print('Você atingiu o numero máximo de saques diários. Operação Cancelada.')
    elif valor > 0:
        saldo -= valor
        numero_saques += 1
        extrato += f'- R${valor:.2f}\n'
        print('Saque realizado com sucesso!')
    else:
        print('O valor informado é inválido. Operação cancelada.')
    
    return saldo, extrato

def exibir_extrato(saldo,/,*,extrato):
    print(f"""Extrato:
              
{extrato}
--------------
Saldo:R${saldo:.2f}""")

def criar_usuario(usuarios):
    cpf = input('Informe o CPF (somente números): ')
    usuario = filtrar_usuarios(cpf, usuarios)

    if usuario:
        print('Já existe usuário com esse CPF cadastrado!')
        return
    
    nome= input('Informe o nome completo: ')
    data_nascimento = input('Informe a data de data de nascimento (dd-mm-aaaa): ')
    endereco = input('Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ')

    usuarios.append({'nome': nome, 'data_nascimento':data_nascimento,'cpf':cpf, 'endereco':endereco})

    print('Usuário cadastrado com sucesso!')

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('Informe o CPF do usuário: ')
    usuario = filtrar_usuarios(cpf,usuarios)

    if usuario:
        print('Conta Cadastrada com sucesso!')
        return{'agencia':agencia, 'numero_conta':numero_conta, 'usuario': usuario}
    
    print('Usuário não encontrado, operação cancelada.')

def filtrar_usuarios(cpf,usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def listar_contas(contas):
    for conta in contas:
        linha = f'''\
        Agência: {conta['agencia']}
        C/C: {conta['numero_conta']}
        Titular: {conta['usuario']['nome']}
    '''
        print('='*100)
        print(textwrap.dedent(linha))

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    usuarios = []
    contas = []
    AGENCIA = '0001'

    while True:
        
        opcao = menu()

        if opcao == '1':
            valor = float(input("Informe o valor do depósito: \n => "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == '2':
            valor = float(input("Informe o valor do saque: \n => "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )
        
        elif opcao == '3':
            exibir_extrato(saldo,extrato=extrato)

        elif opcao == '6':
            criar_usuario(usuarios)

        elif opcao == '4':
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA,numero_conta, usuarios)
            
            if conta:
                contas.append(conta)
        
        elif opcao == '5':
            listar_contas(contas)

        elif opcao == '7':
            print('Obrigado por ser nosso cliente, volte sempre!')
            break

        else:
            print('Operação inválida, por favor selecione novamente a operação desejada.')            

main()