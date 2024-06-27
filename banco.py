menu = """

[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair     

=> """

limite = 3500
saldo = 0
extrato = ""
numer_de_saque = 0
limite_de_saque = 3

while True:
    opcao = input(menu)

    if opcao == 1:
        valor = float(input("informe o valor para depósitar: "))

        if valor >0:
            saldo += valor
            extrato += f"Depósito de: R$ {valor:.2f}\n"

        else:
            print("O valor é invalido.")

    elif opcao == 2:
        valor = float(input("informe o valor para sacar: "))

        excedeu_valor = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saque = numer_de_saque >= limite_de_saque 
    
        if excedeu_limite:
            print("Você excedeu o limite de saque.")

        elif excedeu_saque:
             print("Você excedeu o limite de saques diário, volte amanhâ.")

        elif excedeu_valor:
            print("Você excedeu o limite de saque, tente um valor menor que seu saldo.")

        else:
            print("Valor informado é invalido.")


    elif opcao == 3:
        print("\n=====EXTRATO=====")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")


    elif opcao == 0:
        break

    else:
        print("Tente uma das opções válidas:[1] Depositar, [2] Sacar, [3] Extrato, [0] Sair.")
