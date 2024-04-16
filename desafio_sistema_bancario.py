import textwrap
from abc import ABC, abstractmethod
import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self,conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()     

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._numero
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self,valor):
        saldo = self._saldo
        execedeu_saldo = valor > saldo

        if execedeu_saldo:
            print('Saldo Insuficiente, operação cancelada.')
        elif valor > 0:
            self._saldo -= valor
            print('Saque realizado com sucesso!')
            return True
        else:
            print('O valor informado é inválido. Operação cancelada.')
        
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print('Depósito Realizado com sucesso!')
        else:
            print('Operação não pode ser realizada, o valor informado é inválido.')
            return False
        
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao['tipo'] == 'Saque']
        )

        excedeu_limite = valor > self.limite
        execedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print('O limite de saque é de R$500,00 por saque. Operação cancelada.')
        elif execedeu_saques:
            print('Você atingiu o numero máximo de saques diários. Operação Cancelada.')
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self):
        return f'''\
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
        '''

class Historico:
    def __init__(self):
        self._transacoes = []
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor,
                'data': datetime.now().strftime
                ("%d-%m-%Y' %H:%M:%s"),
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @classmethod
    @abstractmethod
    def registrar(self,conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self.valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)



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

def depositar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_usuarios(cpf, clientes)

    if not cliente:
        print('Cliente não cadastrado')
        return
    
    valor = float(input('Informe o valor do deposito: '))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    Cliente.realizar_transacao(conta,transacao)

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print('Cliente não possui conta')
        return
     
    # FIXME: não permite cliente escolher a conta
    return cliente.contas

def sacar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_usuarios(cpf, clientes)

    if not cliente:
        print('Cliente não cadastrado')
        return
    
    valor = float(input('Informe o valor do saque: '))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    Cliente.realizar_transacao(conta,transacao)  

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_usuarios(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

def criar_usuario(clientes):
    cpf = input('Informe o CPF (somente números): ')
    usuario = filtrar_usuarios(cpf, clientes)

    if usuario:
        print('Já existe usuário com esse CPF cadastrado!')
        return
    
    nome= input('Informe o nome completo: ')
    data_nascimento = input('Informe a data de data de nascimento (dd-mm-aaaa): ')
    endereco = input('Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ')

    clientes.append({'nome': nome, 'data_nascimento':data_nascimento,'cpf':cpf, 'endereco':endereco})

    print('Cliente cadastrado com sucesso!')

def criar_conta(agencia, numero_conta, clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_usuarios(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    conta.append(conta)
    cliente.contas.append(conta)

    print("\n== Conta cadastrada com sucesso! ==")

def filtrar_usuarios(cpf,clientes):
    usuarios_filtrados = [usuario for usuario in clientes if usuario['cpf'] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main():
    contas = []
    clientes = []

    while True:
        
        opcao = menu()

        if opcao == '1':
            depositar(clientes)

        elif opcao == '2':
            sacar(clientes)
        
        elif opcao == '3':
            exibir_extrato(clientes)

        elif opcao == '6':
            criar_usuario(clientes)

        elif opcao == '4':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        
        elif opcao == '5':
            listar_contas(contas)

        elif opcao == '7':
            print('Obrigado por ser nosso cliente, volte sempre!')
            break

        else:
            print('Operação inválida, por favor selecione novamente a operação desejada.')            

main()