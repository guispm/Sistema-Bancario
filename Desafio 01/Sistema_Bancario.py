def menu():
    print("=+"*20)
    print("{:^}".format("BEM VINDO AO GBANK"))
    print("=+"*20)
    menu = """
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Nova Conta
    [5] Listar Constas
    [6] Novo Usuário
    [0] Sair

    Digite uma das opções acima: """
    return input(menu)

def depositar(valor, saldo, extrato,/):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito {"."*5} R$ {valor:.2f}\n"
        print(f"OPERAÇÃO REALIZADA!\nFoi depositado R${valor:.2f}\nSALDO: {saldo:.2f}")    
    else:
        print ("OPERAÇÃO NÃO REALIZADA. Valor digitado é inválido.")
    
    return saldo,extrato 

def sacar(*,saldo, valor, extrato, limite, numero_saques, limite_saques):
    if limite_saques > 0:
        valor = int(input("Digite o valor para saque: R$ "))
        if valor > limite:
            print ("OPERAÇÃO NÃO REALIZADA. Valor de máximo de saque é R$ 500,00")
        elif valor > saldo:
            print ("OPERAÇÃO NÃO REALIZADA. Saldo insuficiente!")
        elif valor > 0:
            saldo -= valor
            extrato += f"Saque {"."*8} R$ {valor:.2f}\n"
            numero_saques += 1
            print(f"OPERAÇÃO REALIZADA COM SUCESSO\nFoi sacado R$ {valor:.2f}\nVocê fez  {numero_saques} saques.")
        else:
            print ("OPERAÇÃO NÃO REALIZADA. Valor digitado é inválido.")
    else:
        print(f"OPERAÇÃO NÃO REALIZADA. Quantidade de saques excedido!")

def exibir_extrato(saldo,/, *, extrato):
    print("=-"*20)
    print(extrato)
    print(f"Saldo: R$ {saldo:.2f}")
    print("=-"*20)

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario (cpf,usuarios)
    
    if usuario:
        print("OPERAÇÃO NÃO REALIZADA! Jà existe um usuário com esse CPF")

    nome = input("Informa o nome completo: ")
    data_de_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, número - bairro - cidade/sigla do estado): ")
    usuarios.append ({"nome":nome, "data_de_nascimento": data_de_nascimento, "cpf":cpf, "endereco": endereco})
    print ("OPERAÇÃO REALIZADA COM SUCESSO!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados [0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario (cpf,usuarios)

    if usuario:
        print ("OPERAÇÃO REALIZADA COM SUCESSO!! Conta criada!")
        return ({"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario})
  
def main():

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    usuarios = []
    contas = []
    numero_conta = 1

    while True:
        opcao = menu()
        if opcao == "1":
            valor = int(input("Digite o valor de depósito: R$ "))
            saldo, extrato = depositar(saldo,valor,extrato)

        elif opcao == "2":
            valor = int(input("Digite o valor de depósito: R$ "))
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )
            LIMITE_SAQUES -= LIMITE_SAQUES

        elif opcao == "3":
            exibir_extrato (saldo, extrato=extrato)

        elif opcao == "4":
            criar_usuario(usuarios)

        elif opcao == "5":
            conta = criar_conta (AGENCIA,numero_conta,usuarios)
            if conta:
                contas.append(conta)
                numero_conta =+ 1


        elif opcao == "0":
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
        print("=-"*20)
    print("=-"*20)
    print("SISTEMA ENCERRADO!!!\nObrigado por usar os nossos serviços, até mais!")
    print("=-"*20)

main()