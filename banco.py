import textwrap

def menu():
    menu = """\n
    ====== MENU ======
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNovo Usuario
    [5]\tCriar Conta
    [6]\tListar Contas
    [0]\tSair
    => """
    return input(textwrap.dedent(menu))

def sacar(*, saldo, valor, extrato, limite, numero_de_saque, limite_de_Saque):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saque = numero_de_saques >= limite_de_Saque

    if excedeu_saldo:
        print("\n Operação falhou! Você não tem saldo o suficiente.")

    elif excedeu_limite:
        print("O valor do saque ultrapassou o limite.")

    elif excedeu_saque:
        print("Número máximo de saque foi excedido.")    
    
    
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor :.2f}\n"
        numero_de_saques += 1
        print("\n Saque realizado com sucesso!")

    else:
        print("O valor informado é inválido.")

    return saldo, extrato
        
def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += ("\n Depósito realizado com sucesso!")

    else:
        print("\nO valor informado é inválido.")

    return saldo, extrato

def extrato(saldo, / , *, extrato):
    print("\n===EXTRATO===")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR${saldo:.2f}")

def criar_usuario(usuarios):
    cpf = input("Informe o seu CPF:")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nJá existe um usuário com esse CPF")

    nome = input("Digite seu nome completo:")
    data_nascimento = input("Informe a sua data de nascimento: ")
    endereco = input("Informe o seu Endereço: ")

    usuarios.append({"nome": nome,"data_nascimento": data_nascimento, "CPF": cpf, "endereco": endereco})
    print("Usuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados [0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o seu CPF:")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuarios:
        print("\nConta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\n Usuário não encontrado, fluxo de criação de conta encerado!")
    
def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUE = 3
    AGENCIA= "0001"
    limite = 3500
    saldo = 0
    extrato = ""
    numero_de_saque = 0
    usarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            valor = float(input("informe o valor para depósitar: "))

            saldo, extrato = depositar(valor,saldo, extrato)

        elif opcao == "2":
            valor = float(input("informe o valor para sacar: "))

            saldo, extrato = sacar(
                saldo = saldo,
                valor = valor,
                extrato = extrato,
                limite = limite,
                numero_de_saque = numero_de_saque,
                limite_de_Saque = LIMITE_SAQUE,
            )

        elif opcao == "3":
            extrato(saldo, extrato = extrato)

        elif opcao == "4":
            criar_usuario(usarios)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usarios)

            if conta:
                contas.append(conta)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "0":
            break

        else:
            print("Tente uma das opções válidas:[1] Depositar, [2] Sacar, [3] Extrato, [4] Novo Usuario, [5] Criar Conta, [6] Listar Contas, [0] Sair.")


main()