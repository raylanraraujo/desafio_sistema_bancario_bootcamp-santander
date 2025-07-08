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
    def __init__(self, numero, cliente, historico):
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
            self._saldo += saldo
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
            return f""""\
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
                "data": datetime.now().strtime("%d-%m-%Y  %H:%M:%s")
            }
        )


class Transacao(ABC): #criando uma classe abstrata extendiad do ABC
    @property
    def valor(self):
        pass

    @classmethod
    def regitar(self, conta):
        pass



