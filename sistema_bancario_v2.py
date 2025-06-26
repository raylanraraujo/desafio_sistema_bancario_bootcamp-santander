menu = '''

[1] - Depositar
[2] - Sacar
[3] - Extrato
[4] - Cadastrar usuário
[5] - Criar conta
[6] - Print usuarios

[0] - Sair

>>> '''
AGENCIA = "0001"
LIMITE_SAQUES = 3
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
despedida = ('''
---------------------------------------------------
  Obrigado por usar nossos serviços. Volte sempre.
---------------------------------------------------
      
''')
usuarios = []
contas = []

def depositar(saldo, extrato, /):
    valor = float(input("Digite o valor do depósito: R$ "))
    while True:
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: \033[32mR${valor:.2f}\033[m\n"
            return saldo, extrato
        else:
            print("\n\033[31mDigite um valor válido.\033[m")

def sacar(*, saldo = saldo, extrato = extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES):
    erro = """
----------------------------------
 \033[31mLimite de saques diário atingido.\033[m
----------------------------------
"""
    if numero_saques < limite_saques:
        saque = float(input("Digite o valor do saque: R$ "))

        if saque > saldo:
            print("\n\033[31m[ERRO!] - Saldo insuficiente.\033[m")
        elif saque > limite:
            print("\n\033[31m[ERRO!] - Valor do saque ultaprassa o limite.\033[m")
        else:
            if saque > 0:
                saldo -= saque
                extrato += f"Saque: \033[31mR${saque:.2f}\033[m\n"
                numero_saques+=1
                # return saldo, extrato, numero_saques
            else:
                print("\n\033[31mDigite um valor válido.\033[m")
    else:
        print(erro)

    return saldo, extrato, numero_saques

def historico(saldo,/, *, extrato = extrato):
    print('''
-------------------------
         EXTRATO         
-------------------------
        ''')
    print("Não foram realizadas movimentações." if not extrato else extrato) #
    print(f"\n\nSaldo da conta: R$ {saldo:.2f}")
    print()
    print(f"-"*25)

def cadastrar_usuário(lista_usuarios):
    print('''
--------------------------
    CADASTRAR USUÁRIO         
--------------------------
        ''')
    cpf = int(input("Digite o CPF (apenas números): "))
    for usuario in lista_usuarios:
        if usuario["cpf"] == cpf:
            print(f"\033[31m\nO CPF nº {cpf} já cadastrado.\033[m")
            return
    novo_usuario = {
        "cpf" : cpf,
        "nome" : input("Nome: ").strip(),
        "nascimento" : input("Nascimento(dd/mm/aaaa): ").strip(),
        "endereco" : input("Endereço (logradouro, nº - bairro - cidade/sigla estado): ").strip()
    }
    print("\n\033[32mUsuário cadastrado com sucesso.\033[m")

    lista_usuarios.append(novo_usuario)

# essa sugestao usada pelo Guilherme para filtrar usuarios
# def filtrar_usuario(cpf, usuarios):
#     usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
#     return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, lista_usuarios):
    print('''
--------------------------
     CRIAR NOVA CONTA         
--------------------------
        ''')

    cpf = int(input(f"Informe o CPF do usuário: "))

    #inicializa variavel com valor padrao None 
    usuario_encontrado = None

    for usuario in lista_usuarios:
        if usuario["cpf"] == cpf:
            print("Conta vinculada ao usuario")
            usuario_encontrado = usuario["nome"]
            break
    
    if usuario_encontrado:
        return{"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario["nome"]}
    else:
        print(f"\033[31m\nNão foi localizado usuário com o CPF de nº {cpf}.\033[m\nCaso seja de interesse, cadastre esse usuário")

def listar_contas(contas):
    for conta in contas:
        linha = f'''
Agência: \t{conta['agencia']}
C/C:\t\t{conta['numero_conta']}
Titular:\t{conta['usuario']}
'''     
        print("=" * 30)
        print(linha)

#Começo do programa    
while True:
    opcao = int(input(menu))

    if opcao == 1:
        saldo, extrato = depositar(saldo, extrato)

    elif opcao == 2:
        saldo, extrato, numero_saques = sacar(saldo = saldo, extrato = extrato, limite = limite, numero_saques = numero_saques, limite_saques = LIMITE_SAQUES)

    elif opcao == 3:
        print(historico(saldo, extrato = extrato))

    elif opcao == 4:
        cadastrar_usuário(usuarios)

    elif opcao == 5:
        numero_conta = len(contas) + 1
        conta = criar_conta(AGENCIA, numero_conta, usuarios)

        if conta:
            contas.append(conta)

    elif opcao == 6:
        print(usuarios)
        listar_contas(contas)

    elif opcao == 0:
        break
    else:
        print("\nOpção inválida! Por favor selecione novamente a opção desejada.")
print(despedida)
