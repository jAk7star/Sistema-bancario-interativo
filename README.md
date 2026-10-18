# Sistema Bancário v1 🏦

Este é o projeto da primeira versão do Sistema Bancário em Python (simulador interativo de caixa eletrônico), desenvolvido como desafio de projeto para a **DIO (Digital Innovation One)**.

O diferencial deste projeto é que a lógica de negócio foi toda estruturada utilizando o paradigma de **Programação Orientada a Objetos (POO)**, garantindo um código mais limpo, organizado e seguro.

## 💻 Funcionalidades

O sistema conta com 3 operações principais acessadas via menu interativo no terminal:

- **Depósito (`[d]`)**: Permite adicionar valores positivos à conta. Os depósitos são registrados automaticamente no extrato.
- **Saque (`[s]`)**: Permite retirar valores da conta, respeitando as seguintes regras de negócio:
  - Limite de **3 saques diários**.
  - Limite máximo de **R\$ 500,00** por operação de saque.
  - Não é possível sacar se não houver saldo suficiente.
- **Extrato (`[e]`)**: Lista todas as movimentações (depósitos e saques) realizadas na conta e exibe o saldo atual formatado (ex.: `R$ 1500.45`).

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Conceitos aplicados:**
  - Variáveis e Tipos de Dados
  - Estruturas Condicionais (`if`, `elif`, `else`)
  - Laços de Repetição (`while`)
  - Formatação de Strings (`f-strings`)
  - Programação Orientada a Objetos (Classes, Objetos, Métodos, Atributos)

## 🚀 Como executar o projeto

1. Certifique-se de ter o Python instalado na sua máquina.
2. Clone este repositório ou baixe o arquivo `.py`:
   ```bash
   git clone https://github.com/jAk7star/Sistema-bancario-interativo.git
   cd Sistema-bancario-interativo
   ```
3. Abra o terminal na pasta do projeto e execute:
   ```bash
   python sistema_bancario.py
   ```
4. Interaja com o sistema através do menu exibido no terminal.

## 👨‍💻 Autor

**Jaques Nunes**
- [LinkedIn](https://www.linkedin.com/in/jaquesnunes-techdocs)
- [GitHub](https://github.com/jAk7star)

Projeto desenvolvido com as orientações do Bootcamp da DIO.
