#Sistema bancario para um usuario simples, com funcionalidades de deposito, saque e consulta de saldo
#Extrato: O banco pediu para listar todos os depósitos e saques realizados. No momento, você só mostra o saldo atual.
#Limite de valor por saque: O saque máximo permitido é de R$ 500,00.
#Limite de quantidade de saques: O cliente só pode fazer 3 saques por dia.

class ContaBancaria:
    def __init__(self, extrato="", numero_saques=0, saldo_inicial=0):
        # Oque é o titular? É o nome do dono da conta, que será passado como argumento ao criar a conta. O saldo_inicial é opcional e, se não for fornecido, será definido como 0.
        self.extrato = extrato
        self.numero_saques = numero_saques
        self.saldo = saldo_inicial

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato += f'Depósito de R${valor:.2f}\n'
        else:
            print('Valor de depósito inválido.')
        # aqui estamos verificando se o valor do depósito é maior que 0. Se for, adicionamos o valor ao saldo da conta e exibimos uma mensagem de sucesso. Caso contrário, exibimos uma mensagem de erro indicando que o valor do depósito é inválido.
    
    def sacar(self, valor):
        if self.numero_saques >= 3:
            print('Limite de saques diários atingido.')
        elif valor > 500:
            print('Valor de saque excede o limite de R$ 500,00.')
        elif valor > self.saldo or valor <= 0:
            print('Saldo insuficiente ou valor de saque inválido.')
        else:
           # 1. Subtraia o valor do self.saldo
            # 2. Adicione +1 ao self.numero_saques
            # 3. Concatene o registro na string self.extrato igual você fez no depósito
            self.saldo -= valor
            self.extrato += f'Saque de R${valor:.2f}\n'
            self.numero_saques += 1
            print(f'Saque de R${valor:.2f} realizado com sucesso.')

    def consultar_saldo(self):
        print(f'Saldo atual: R${self.saldo:.2f}')

    def consultar_extrato(self):
        print('---Extrato---')
       # Se o extrato estiver vazio, é legal mostrar uma mensagem dizendo que não há movimentações. Caso contrário, exiba o extrato.
        if not self.extrato:
            print('Não há movimentações.')
        else:
            print(self.extrato)
        # Moatrando o saldo atual no final do extrato
        print(f'Saldo atual: R${self.saldo:.2f}')
        print('-------------')



minha_conta = ContaBancaria()

menu = """
================
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
================
Escolha uma opção: """

while True:
    opcao = input(menu).lower()

    if opcao == 'd':
        valor = float(input("Informe o valor do depósito: R$ "))
        minha_conta.depositar(valor)

    elif opcao == 's':
        valor = float(input("Informe o valor do saque: R$ "))
        minha_conta.sacar(valor)

    elif opcao == 'e':
        minha_conta.consultar_extrato()

    elif opcao == 'q':
        print("Saindo do sistema... Obrigado!")
        break # O break encerra o 'while True'

    else:
        print("Opção inválida, por favor selecione novamente a operação desejada.")