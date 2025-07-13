import textwrap
from abc import ABC
from datetime import datetime

class ContaIterador:
    def __init__(self, contas):
        pass

    def __iter__(self):
        pass

    def __next__(self):
        pass


class Cliente:
    def __init__(self, endereco):
        self._endenreco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta) #adiciona a conta recebida por parâmetro no array de contas 


class PessoaFisica(Cliente): #classe extendida da classe Cliente
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco) #chamou o construtor da classe pai Cliente com o argumento que ele pede
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico() #é do tipo classe. Uma conta tem um histórico e um histórico pertence a uma conta.

    @classmethod
    def nova_conta(cls, cliente, numero): #recebe como argumento Cliente e número. #método de fábrica que cria algo. Esse método vai receber um cliente e o número e tem que retornar o objeto conta. 
        return cls(numero, cliente) # retorna uma instância de conta
    
    #abaixo foi criado propriedades para acessar os dados 
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
        return self._cliente
    
    @property
    def historico(self):
        return self._historico


    def sacar(self, valor): #recebe um valor float e retornar um booleano
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n\033[31m[ERRO!] - Saldo insuficiente.\033[m")
        
        elif valor > 0:
            self._saldo -= valor
            print("\n\033[32mSaque realizado com sucesso.\033[m")
            return True
        
        else:
            print("\n\033[31mDigite um valor válido.\033[m")
            return False
            

    def depositar(self, valor): #recebe um valor que é float e retorna um booleano. A intencao do é saber se a oprecao aconteceu com sucesso ou falha. 
        if valor > 0: #verificar se o valor informado é maior que 0
            self._saldo += valor
            print("\n\033[32mDepósito realizado com sucesso.\033[m")
        else:
            print("\n\033[31mDigite um valor válido.\033[m")
            return False
        
        return True


class ContaCorrente(Conta): #tem tudo que a conta mae tem + o limite
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n\033[31m[ERRO!] - Valor do saque ultaprassa o limite.\033[m")
        
        elif excedeu_saques:
            erro = """
----------------------------------
\033[31mLimite de saques diário atingido.\033[m
----------------------------------
"""
            print(erro)
        
        else:
            return super().sacar(valor)
        
        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico():
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
                "data": datetime.now().strftime("%d-%m-%Y  %H:%M:%s")
            }
        )

    def gerar_relatorio(self, tipo_transacao=None):
        pass


class Transacao(ABC): #criando uma classe abstrata extendiad do ABC
    @property
    def valor(self):
        pass

    @classmethod
    def regitar(self, conta):
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
        return self._valor
    
    def registrar(self, conta):
        sucesso_trransacao = conta.depositar(self.valor)

        if sucesso_trransacao:
            conta.historico.adicionar_transacao(self)

def log_transacao(func):
    pass

def menu():
    menu = '''

[1] - Depositar
[2] - Sacar
[3] - Extrato
[4] - Cadastrar usuário
[5] - Criar conta
[6] - Listar Contas

[0] - Sair

>>> '''

    return int(input(textwrap.dedent(menu)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 1:
            depositar(clientes)

        elif opcao == 2:
            sacar(clientes)

        elif opcao == 3:
            exibir_extrato(clientes)

        elif opcao == 4:
            criar_cliente(clientes)

        elif opcao == 5:
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == 6:
            listar_contas(contas)

        elif opcao == 0:
            break
        else:
            print("\nOpção inválida! Por favor selecione novamente a opção desejada.")


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n\033[31mCliente não encontrado!\033[m")
        return
    
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n\033[31mCliente não possui conta!\033[m")
        return

    #FIXME #não permite cliente escolher a conta
    return cliente.contas[0]


@log_transacao
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\033[31mCliente não encontrado!\033[m")
        return
    
    valor = float(input("Informe o valor dos aque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


@log_transacao
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\033[31mCliente não encontrado!\033[m")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print('''
-------------------------
         EXTRATO         
-------------------------
        ''')
    # TODO: atualizar a implementação para utilizar o gerador definido em Historico
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\t\tR$ {transacao['valor']:.2f}"
    
    print(extrato)
    print(f"\nSaldo: \n\t\ttR$ {conta.saldo:.2f}")
    print()
    print(f"-"*25)


@log_transacao
def criar_cliente(clientes):
    print('''
--------------------------
    CADASTRAR USUÁRIO         
--------------------------
        ''')
    
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print(f"\033[31m\nO CPF nº {cpf} já cadastrado.\033[m")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço: ")

    cliente= PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n\033[32mUsuário cadastrado com sucesso.\033[m")


@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\033[31mCliente não encontrado! Criação de conta encerrada.\033[m")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)


    print("\033[32mConta criada com sucesso.\033[m")


def listar_contas(contas):
    # TODO: alterar implementação, para utilizar a classe ContaIterador
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

main()