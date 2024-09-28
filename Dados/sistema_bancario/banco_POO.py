import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = list()
    
    def realizar_transacao (self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta (self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo (self):
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
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    def sacar(self, valor):
        saldo = self._saldo
        
        if valor > saldo:
            print("\n@@@ Falha na operação! Saldo insuficiente! @@@")
        
        elif valor < 0:
            print("\n@@@ Falha na operação! Digite um valor válido! @@@")
        
        else:
            self._saldo -= valor
            print("\n@@@ Transação bem sucedida! @@@")
            return True

        return False
    
    def depositar(self, valor):
        if valor < 0:
            print("\n@@@ Falha na operação! Digite um valor válido! @@@")
            return False

        else:
            self._saldo += valor
            print("\n@@@ Transação bem sucedida! @@@")
            return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor):
        transacoes = self.historico.transacoes
        saques = list()

        for transacao in transacoes:
            if transacao["tipo"] == Saque.__name__:
                saques.append(transacao)
        
        numero_saques = len(saques)
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques > self.limite_saques

        if excedeu_limite:
            print("\n@@@ Falha na operação! Valor do saque excede limite! @@@")
        
        elif excedeu_saques:
            print("\n@@@ Falha na operação! Número de saques excedeu o limite! @@@")
        
        else:
            return super().sacar(valor)
        
        return False

    def __str__(self):
        return f"""\
            Agência: \t\t{self.agencia}
            C/C: \t\t\t{self.numero}
            Titular: \t\t{self.cliente.nome}
        """


class Historico:
    def __init__ (self):
        self._transacoes = list()
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @classmethod
    @abstractmethod
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
            conta.historico.adicionar_transacao(self)


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


def operar(clientes, opcao):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float (input("Informe o valor do depósito: "))
    
    if opcao == 'd':
        transacao = Deposito(valor)
    elif opcao == 's':
        transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n ====================== EXTRATO ======================")
    transacoes = conta.historico.transacoes

    extrato = ""
    
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
        
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("="*30)


def criar_cliente(clientes):
    cpf = input("Informe o CPF (apenas números): ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if cliente:
        print("\n@@@ Já existe cliente com esse CPF. @@@")
        return
    
    nome = input("Digite o nome: ")
    data_de_nascimento = input("Data de nascimento(dd-mm-aaaa): ")
    endereco = input(("Digite o endereço(Logradouro, número, bairro, cidade/estado(sigla)): "))
    
    cliente = PessoaFisica(cpf=cpf, nome=nome, data_nascimento=data_de_nascimento, endereco=endereco)
    clientes.append(cliente)

    print("\n ==== Cliente criado com sucesso! ====")


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]

    if clientes_filtrados:
        return clientes_filtrados[0] 
    else:
        return None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n @@@ Cliente não possui conta! @@@")
        return

    # FIX ME: cliente não pode escolher conta
    return cliente.contas[0]


def formatar_endereco(logradouro, numero, bairro, cidade, estado):
    logradouro = logradouro.title()
    bairro = bairro.title()
    cidade = cidade.title()
    estado = estado.upper()

    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}"
    return endereco


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do usuário: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
        contas.append(conta)
        cliente.contas.append(conta)
        print("\n========= Conta criada com sucesso! =======")
    else:
        print("@@@ Cliente não encontrado. Fluxo de conta encerrado. @@@")


def listar_conta(contas):
    for conta in contas:
        print("="*100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = list()
    contas = list()

    while True:
        opcao = menu()

        if opcao == 'd':
            operar(clientes, opcao)
        
        elif opcao == 's':
            operar(clientes, opcao)
        
        elif opcao == 'e':
            exibir_extrato(clientes)
        
        elif opcao == 'q':
            break
        
        elif opcao == 'nu':
            criar_cliente(clientes)
        
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        
        elif opcao == "lc":
            listar_conta(contas)

        else:
            print('Erro: resposta inválida')

main()