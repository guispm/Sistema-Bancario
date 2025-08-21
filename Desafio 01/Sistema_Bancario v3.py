from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self,endereco):
        self._endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self,conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
        super().__init__(endereco)

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls,cliente,numero):
        return cls(cliente , numero)

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self,valor):
        saldo = self._saldo
        exedeu_saldo = valor > saldo
        if exedeu_saldo:
            print ("OPERAÇÃO NÃO REALIZADA. Saldo insuficiente!")
        elif valor > 0:
            saldo -= valor
            print(f"OPERAÇÃO REALIZADA COM SUCESSO\nFoi sacado R$ {valor:.2f}")
            return True
        else:
            print ("OPERAÇÃO NÃO REALIZADA. Valor digitado é inválido.")
            return False
        
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"OPERAÇÃO REALIZADA!\nFoi depositado R${valor:.2f}")    
        else:
            print ("OPERAÇÃO NÃO REALIZADA. Valor digitado é inválido.")
            return False
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len (
            [transacao for transacao in self.historico.transacoes if transacao ["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("OPERAÇÃO NÃO REALIZADA. Valor de máximo de saque é R$ 500,00")
        elif excedeu_saques:
            print(f"OPERAÇÃO NÃO REALIZADA. Quantidade de saques excedido!")
        else: 
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t {self.agencia}
            C/C:\t\t {self.numero}
            Titular:\t {self.cliente.nome}
            """

class Historico:
    def __init__(self):
        self._transcoes = []

    @property
    def transacoes(self):
        return self.transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime ("%d-%m-%Y %H:%M:%s"),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

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


def menu():
    print("=+"*20)
    print("{:^}".format("BEM VINDO AO GBANK"))
    print("=+"*20)
    menu = """
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Nova Conta
    [5] Listar Contas
    [6] Novo Usuário
    [0] Sair

    Digite uma das opções acima: """
    return input(menu)

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente (cpf, clientes)
    if not clientes:
        print ("OPERAÇÃO NÃO REALIDAZA. Cliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not clientes:
        print ("OPERAÇÃO NÃO REALIDAZA. Cliente não encontrado!")
        return
    
    valor = float(input("Informe o valor de saque: "))
    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print ("OPERAÇÃO NÃO REALIDAZA. Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n============ EXTRATO ============")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao["tipo"]}:\n\tR$ {transacao["valor"]:.2f}"

        print(extrato)
        print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
        print ("="*20)

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente (cpf,cliente)
    
    if cliente:
        print("OPERAÇÃO NÃO REALIZADA! Jà existe um usuário com esse CPF")
        return

    nome = input("Informa o nome completo: ")
    data_de_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, número - bairro - cidade/sigla do estado): ")
    cliente.append ({"nome":nome, "data_de_nascimento": data_de_nascimento, "cpf":cpf, "endereco": endereco})
    cliente = PessoaFisica(nome=nome, data_nascimento=data_de_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print ("OPERAÇÃO REALIZADA COM SUCESSO!")

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados [0] if clientes_filtrados else None

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf,clientes)

    if not cliente:
        print ("OPERAÇÃO REALIZADA NÃO REALIZADA! Cliente não encontrado!")
        return 
    
    conta = ContaCorrente.nova_conta(cliente=cliente,numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("OPERAÇÃO REALIZADA COM SUCESSO! Conta criada")

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("OPERAÇÃO NÃO REALIZADA. Cliente não possui conta!")
        return
    return cliente.contas[0]

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(conta)

def main():

    clientes = []
    contas = []

    while True:
        opcao = menu()
        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
            exibir_extrato (clientes)

        elif opcao == "4":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        
        elif opcao == "5":
            listar_contas(contas)

        elif opcao == "6":
            criar_cliente(clientes)

        elif opcao == "0":
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
        print("=-"*20)
    print("=-"*20)
    print("SISTEMA ENCERRADO!!!\nObrigado por usar os nossos serviços, até mais!")
    print("=-"*20)

main()