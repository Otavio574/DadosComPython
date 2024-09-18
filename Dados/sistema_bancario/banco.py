def deposito(saldo, valor):
    saldo += valor
    
    return saldo


def saque(saldo, valor, num_saques, limite):
    if saldo < valor:
        print("Saldo insuficiente para realizar a transação")
    
    elif valor > limite:
        print("Valor máximo permitido de R$ 500,00")
    
    elif num_saques > LIMITE_SAQUES:
        print("Número de saques diários máximos já atingido")
    
    else:
        saldo -= valor
    
    return saldo


menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

"""

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu).lower()

    if opcao == 'd':
        print("Depósito")
        valor = int(input("Digite o valor do depósito: "))
        extrato += f"\nDepósito: R$ {valor:.2f}"
        saldo = deposito(saldo, valor)
    
    elif opcao == 's':
        print('Saque')
        valor = int(input(f"Digite o valor do saque: "))
        extrato += f"\nSaque: R$ {valor:.2f}"
        numero_saques += 1
        saldo = saque(saldo, valor, numero_saques, limite)
    
    elif opcao == 'e':
        print("\n================= EXTRATO =================")
        if not extrato:
            print("Não foram realizadas movimentações")
        else:
            print(f"{extrato}\n")
            print(f"\nSaldo: R$ {saldo:.2f}")
        print("===========================================")
    
    elif opcao == 'q':
        break

    else:
        print('Erro: resposta inválida')