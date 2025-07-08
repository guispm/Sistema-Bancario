print("=+"*20)
print("{:^}".format("BEM VINDO AO GBANK"))
print("=+"*20)

menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair

Digite uma das opções acima: """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)
    if opcao == "1":
        valor = int(input("Digite o valor de depósito: R$ "))
        print("=-"*20)
        if valor > 0:
            saldo += valor
            extrato += f"Depósito {"."*5} R$ {valor:.2f}\n"
            print(f"OPERAÇÃO REALIZADE !\nFoi depositado R${valor:.2f}\nSALDO: {saldo:.2f}")    
        else:
            print ("OPERAÇÃO NÃO REALIZADA. Valor digitado é inválido.")

    elif opcao == "2":
        if numero_saques < 3:
            valor = int(input("Digite o valor para saque: R$ "))
            if valor > 500:
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
            print("OPERAÇÃO NÃO REALIZADA. Quantidade de saques excedido !")

    elif opcao == "3":
        print("=-"*20)
        print(extrato)
        print(f"Saldo: R$ {saldo:.2f}")
        print("=-"*20) 
    elif opcao == "0":
        break
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
    print("=-"*20)
print("=-"*20)
print("SISTEMA ENCERRADO!!!\nObrigado por usar os nossos serviços, até mais!")
print("=-"*20)