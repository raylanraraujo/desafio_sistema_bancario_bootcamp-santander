menu = '''

[1] - Depositar
[2] - Sacar
[3] - Extrato

[0] - Sair

>>> '''

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAAQUES = 3

while True:
    opcao = int(input(menu))

    if opcao == 1:
        deposito = float(input("Digite o valor do depósito: R$ "))
        saldo += deposito
        extrato += f"Depósito: \033[32mR${deposito:.2f}\033[m\n"
        
    
    elif opcao == 2:
        if numero_saques < 3:

            saque = float(input("Digite o valor do saque: R$ "))
        
            if saque > saldo:
                print("Saldo insuficiente.")
            elif saque > limite:
                print("Valor do saque ultaprassa o limite ")
            else:
                saldo -= saque
                extrato += f"Saque: \033[31mR${saque:.2f}\033[m\n"
            numero_saques+=1
        else:
            print("""
----------------------------------
 Limite de saques diário atingio.
----------------------------------
""")
    
    elif opcao == 3:
        print('''
-------------------------
         EXTRATO         
-------------------------
        ''')
        print(extrato)
        print(f"\n\nSaldo da conta: R$ {saldo:.2f}")
        print()
        print(f"-"*25)
    
    elif opcao == 0:
        break

    else:
        print("\nOpção inválida! Por favor selecione novamente a opção desejada.")

print('''
---------------------------------------------------
  Obrigado por usar nossos serviços. Volte sempre.
---------------------------------------------------
      
''')
