menu = """

[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

submenu_deposito = """
Depósito realizado com sucesso. Deseja voltar ao menu inicial?

[1] Sim
[2] Não

=> """



while True:
    
    opcao = input(menu)

    if opcao == '1':
        valor = float(input("Informe o valor do depósito: \n => "))
        
        if valor > 0:
            saldo += valor
            extrato += f'+ R${valor:.2f}\n'
            opcao_deposito = input(submenu_deposito)

            if opcao_deposito == '1':
                exit
            else:
                print('Obrigado por ser nosso cliente, volte sempre!')
                break

        else:
            print('Operação falhou, tente novamente.')

    elif opcao == '2':
        valor = float(input("Informe o valor do saque: \n => "))

        if valor > saldo:
            print('Saldo insuficiente. Operação cancelada.')
            exit

        elif valor > 500:
            print('O limite de saque é de R$500,00 por saque. Operação cancelada.')
            exit

        elif numero_saques >= LIMITE_SAQUES:
            print('Você atingiu o limite de saques diários. Tente novamente amanhã.')
            exit

        elif valor <= 500 and valor > 0 and valor <= saldo and numero_saques <= LIMITE_SAQUES:
            saldo -= valor
            numero_saques += 1
            extrato += f'- R${valor:.2f}\n'
            submenu_saque = f"""
Saque realizado com sucesso. 
Você ainda pode realizar {LIMITE_SAQUES-numero_saques} saque(s) hoje.
Deseja voltar ao menu inicial?

[1] Sim
[2] Não

=> """
            opcao_saque = input(submenu_saque)

            if opcao_saque == '1':
                exit 
            else:
                print('Obrigado por ser nosso cliente, volte sempre!')
                break
        else:
            print('Operação falhou, tente novamente.')
    
    elif opcao == '3':
        print(f"""Extrato:
              
{extrato}
--------------
Saldo:R${saldo:.2f}""")
    
    elif opcao == '4':
        print('Obrigado por ser nosso cliente, volte sempre!')
        break

    else:
        print('Operação inválida, por favor selecione novamente a operação desejada.')
        