import textwrap

def menu():
    menu = """\n
    ==================== MENU ====================
    [d] \tDepositar
    [s] \tSacar
    [e] \tExtrato
    [nc] \tNova conta
    [lc] \tListar contas
    [nu] \tNovo usuário
    [lu] \tListar usuários
    [q] \tSair

    """
    return input(textwrap.dedent(menu))


def deposito(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"\nDepósito: \t\tR$ {valor:.2f}\n"
        print("=== Depósito Realizado com sucesso! ===")
    else:
        print ("\n@@@Operação falhou! Valor digitado inválido!@@@")
    
    return saldo, extrato


def saque(saldo, valor, extrato, num_saques, limite, LIMITE_SAQUES):
    if valor > 0:
        if saldo < valor:
            print("Saldo insuficiente para realizar a transação")
        
        elif valor > limite:
            print("Valor máximo permitido de R$ 500,00")
        
        elif num_saques > LIMITE_SAQUES:
            print("Número de saques diários máximos já atingido")
        
        else:
            saldo -= valor
            extrato += f"\nSaque:\t\t\tR$ {valor:.2f}\n"
 
    return saldo, extrato


def exibir_extrato(saldo,/, *, extrato):
    print("\n================= EXTRATO =================")
    if not extrato:
        print("Não foram realizadas movimentações")
    else:
        print(f"{extrato}\n")
        print(f"\nSaldo: \t\t\tR$ {saldo:.2f}\n")
    print("===========================================")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (apenas números): ")
    
    if checar_CPF(cpf, usuarios):
        print("Usuário já cadastrado")
    
    if not checar_CPF(cpf, usuarios):
        nome = input("Digite o nome: ")
        nome = nome.title()
        data_de_nascimento = input("Data de nascimento: ")
        
        print("Digite o endereço: ")
        logradouro = input("Logradouro: ")
        numero = int(input("Número: "))
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        estado = input("Estado(sigla): ")
        endereco = formatar_endereco(logradouro, numero, bairro, cidade, estado)
        
        usuario = {
            cpf: {    
                "Nome": nome,
                "Data de nascimento": data_de_nascimento,
                "Endereço": endereco
            }
        }
        
        usuarios.append(usuario)
    
    return usuarios


def listar_usuarios(usuarios):
    for usuario in usuarios:
         for cpf, detalhes in usuario.items():
            print(f"CPF: {cpf}")
            print(f"Nome: {detalhes['Nome']}")
            print(f"Data de nascimento: {detalhes['Data de nascimento']}")
            print(f"Endereço: {detalhes['Endereço']}")
            print("-" * 40)  # Separador entre usuários


def checar_CPF(cpf, usuarios):
    for usuario in usuarios:
        if cpf in usuario:
            return usuario[cpf]
    return None


def formatar_endereco(logradouro, numero, bairro, cidade, estado):
    logradouro = logradouro.title()
    bairro = bairro.title()
    cidade = cidade.title()
    estado = estado.upper()

    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}"
    return endereco


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = checar_CPF(cpf, usuarios)

    if usuario:
        print("\n========= Conta criada com sucesso! =======")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("@@@ Usuário não encontrado. Fluxo de conta encerrado. @@@")


def listar_conta(contas):
    for conta in contas:
        nome_usuario = conta['usuario']['Nome']
        
        linha = f"""\
            Agência: \t\t{conta['agencia']}
            C/C: \t\t{conta['numero_conta']}
            Titular: \t\t{nome_usuario}
        """
    
    print("="*100)
    print(textwrap.dedent(linha))


def main():
    AGENCIA = "0001"
    LIMITE_SAQUES = 3
    
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = list()
    contas = list()

    while True:
        opcao = menu()

        if opcao == 'd':
            valor = float(input("Digite o valor do depósito: "))
            saldo, extrato = deposito(saldo, valor, extrato)
        
        elif opcao == 's':
            valor = float(input(f"Digite o valor do saque: "))
            numero_saques += 1
            saldo, extrato = saque(saldo, valor, extrato, numero_saques, limite, LIMITE_SAQUES)
        
        elif opcao == 'e':
            exibir_extrato(saldo, extrato=extrato)
        
        elif opcao == 'q':
            break
        
        elif opcao == 'nu':
            criar_usuario(usuarios)
        
        elif opcao == "lu":
            listar_usuarios(usuarios)
        
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta (AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
        
        elif opcao == "lc":
            listar_conta(contas)

        else:
            print('Erro: resposta inválida')

main()