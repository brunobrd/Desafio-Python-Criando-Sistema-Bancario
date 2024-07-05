import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self.index]
            return f"""\
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1
class cliente:
    def __init__(self, endenreco):
        self.endenreco = endenreco
        self.contas = []
        self.indece_conta = 0

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 2:
            print("\nVocê excedeu o número de transações de hoje!")
            return
        
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self.saldo = 0
        self.numero = numero
        self.agencia = "0001"
        self. cliente = cliente
        self. historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(Self):
        return Self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property 
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n Operação falhou! Você não tem saldo o suficiente.")

        elif valor > 0:
            self._saldo -= valor
            print("Saque feito com sucesso.")
            return True
        
        else:
          print("\n Operação falhou!")

        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n Depósito realizado com sucesso!")

        else:
            print("\nOperação falhou! O valor informado é inválido.")
            return False
        
        return True
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saque=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saque = limite_saque

    @classmethod
    def nova_conta(cls, cliente, numero, limite, limite_saque):
        return cls(numero,cliente, limite, limite_saque)

    def sacar(self, valor):
        numero_saque = len(
            [transacao for transacao in self.historico.
             trasacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saque = numero_saque >= self._limite_saque

        if excedeu_limite:
            print("Você excedeu o limite de saque.")

        elif excedeu_saque:
            print("O número de saques foi excedido.")

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
    
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if (
                tipo_transacao is None
                or transacao["tipo"].lower() == tipo_transacao.lower()
            ):
                yield transacao

    def transacao_do_dia(Self):
        data_atual = datetime.utcnow().date()
        transacoes = []
        for transacao in Self._transacoes:
            data_transacao = datetime.strptime(
                transacao["data"], "%d-%m-%Y %H:%M:%S"
            ).date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
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
            conta.historico.adcionar_transacao(self)

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

def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"{datetime.now()}: {func.__name__.upper()}")
        return resultado
    
    return envelope

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

def filtrar_cliente(cpf, clientes):
    cliente_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return cliente_filtrados[0] if cliente_filtrados else None

def recuperar_conta_cliente(Cliente):
    if not cliente.contas:
        print("\nCliente não possui conta!")
        return
    
    return cliente.contas[0]

@log_transacao
def depositar(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    valor = float(input("Informe o valor do depósito: "))
    
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

@log_transacao
def sacar(clientes):
    cpf = input("Digite seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

@log_transacao
def extrato(clientes):
    cpf = input ("Digite o seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não encontrado!")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n ===EXTRATO===")
    transacoes = conta.historico.transacoes

    extrato = ""
    tem_trasancao = False
    for transacao in conta.historico.gerar_relatorio(tipo_transacao = "saque"):
        tem_trasancao = True
        extrato += f"\n{transacao['data']}\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
    
    if not tem_trasancao:
        extrato = "Não foi realizada nenhuma mivimentação."


    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("=============")

@log_transacao
def criar_usuario(clientes):
    cpf = input("Digite o seu CPF: ")
    cliente = filtrar_cliente(cpf,clientes)

    if cliente:
        print("\n Já existe um usuário com esse CPF!")
        return
    
    nome = input("Digite seu nome completo:")
    data_nascimento = input("informe sua data de nasciemento (dd-mm-aaaa): ")
    endereco = input ("Digite seu endenreço (logradouro - bairro - cidade): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\nUsuário criado com sucesso!")

@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Digite o seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n ==Conta criada com sucesso!==")

def listar_contas(contas):
    for conta in ContasIterador(contas):
        print("=" *100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes= []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            Depositar(clientes)

        elif opcao == "2":
            Sacar(clientes)

        elif opcao == "3":
            extrato(clientes)

        elif opcao == "4":
            criar_usuario(clientes)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "0":
            break

        else:
            print("Operação falhou! Escolha uma das opções listadas.")

main()
