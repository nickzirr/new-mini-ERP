# sistema_rh.py

funcionarios = []

def menu():
    print("\n==== SISTEMA RH - LOJA DE ROUPAS ====")
    print("1. Cadastrar Funcionário")
    print("2. Listar Funcionários")
    print("3. Buscar Funcionário por CPF")
    print("4. Atualizar Funcionário")
    print("5. Remover Funcionário")
    print("0. Sair")

def cadastrar_funcionario():
    print("\n--- Cadastro de Funcionário ---")
    nome = input("Nome: ")
    cpf = input("CPF: ")
    cargo = input("Cargo: ")
    salario = float(input("Salário: R$ "))
    
    # Verifica duplicidade de CPF
    if any(f['cpf'] == cpf for f in funcionarios):
        print("⚠️ CPF já cadastrado.")
        return

    funcionario = {
        "nome": nome,
        "cpf": cpf,
        "cargo": cargo,
        "salario": salario
    }
    funcionarios.append(funcionario)
    print("✅ Funcionário cadastrado com sucesso!")

def listar_funcionarios():
    print("\n--- Lista de Funcionários ---")
    if not funcionarios:
        print("Nenhum funcionário cadastrado.")
        return
    for f in funcionarios:
        print(f"- {f['nome']} | CPF: {f['cpf']} | Cargo: {f['cargo']} | Salário: R${f['salario']:.2f}")

def buscar_funcionario():
    cpf = input("\nDigite o CPF do funcionário: ")
    for f in funcionarios:
        if f["cpf"] == cpf:
            print(f"🔍 Encontrado: {f['nome']} | Cargo: {f['cargo']} | Salário: R${f['salario']:.2f}")
            return
    print("❌ Funcionário não encontrado.")

def atualizar_funcionario():
    cpf = input("\nCPF do funcionário que deseja atualizar: ")
    for f in funcionarios:
        if f["cpf"] == cpf:
            print(f"Atualizando dados de {f['nome']}")
            f["nome"] = input("Novo nome: ") or f["nome"]
            f["cargo"] = input("Novo cargo: ") or f["cargo"]
            salario_input = input("Novo salário: R$ ")
            if salario_input:
                f["salario"] = float(salario_input)
            print("✅ Funcionário atualizado!")
            return
    print("❌ Funcionário não encontrado.")

def remover_funcionario():
    cpf = input("\nCPF do funcionário que deseja remover: ")
    for i, f in enumerate(funcionarios):
        if f["cpf"] == cpf:
            del funcionarios[i]
            print("🗑️ Funcionário removido.")
            return
    print("❌ Funcionário não encontrado.")

def sistema_rh():
    while True:
        menu()
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            cadastrar_funcionario()
        elif opcao == "2":
            listar_funcionarios()
        elif opcao == "3":
            buscar_funcionario()
        elif opcao == "4":
            atualizar_funcionario()
        elif opcao == "5":
            remover_funcionario()
        elif opcao == "0":
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("⚠️ Opção inválida. Tente novamente.")

# Executar o sistema
if __name__ == "__main__":
    sistema_rh()

