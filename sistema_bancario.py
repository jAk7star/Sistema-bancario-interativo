# Sistema bancário para um usuário simples, com funcionalidades de depósito, saque e consulta de extrato.
# Regras de negócio:
# - Limite de valor por saque: R$ 500,00
# - Limite de quantidade de saques: 3 saques diários


class ContaBancaria:
    def __init__(self, extrato="", numero_saques=0, saldo_inicial=0):
        self.extrato = extrato
        self.numero_saques = numero_saques
        self.saldo = saldo_inicial

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato += f'Depósito de R${valor:.2f}\n'
            print(f'Depósito de R${valor:.2f} realizado com sucesso.')
        else:
            print('Valor de depósito inválido.')

    def sacar(self, valor):
        if self.numero_saques >= 3:
            print('Limite de saques diários atingido.')
        elif valor > 500:
            print('Valor de saque excede o limite de R$ 500,00.')
        elif valor > self.saldo or valor <= 0:
            print('Saldo insuficiente ou valor de saque inválido.')
        else:
            self.saldo -= valor
            self.extrato += f'Saque de R${valor:.2f}\n'
            self.numero_saques += 1
            print(f'Saque de R${valor:.2f} realizado com sucesso.')

    def consultar_saldo(self):
        print(f'Saldo atual: R${self.saldo:.2f}')

    def consultar_extrato(self):
        print('---Extrato---')
        if not self.extrato:
            print('Não há movimentações.')
        else:
            print(self.extrato, end='')
        print(f'Saldo atual: R${self.saldo:.2f}')
        print('-------------')


if __name__ == "__main__":
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
            break

        else:
            print("Opção inválida, por favor selecione novamente a operação desejada.")