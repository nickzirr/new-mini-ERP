import json
from datetime import datetime

ARQUIVO_DADOS = "funcionarios.json"
funcionarios = []

# ------------------ UTILIDADES ------------------ #

def carregar_dados():
    global funcionarios
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            funcionarios = json.load(f)
    except FileNotFoundError:
        funcionarios = []

def salvar_dados():
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(funcionarios, f, indent=4, ensure_ascii=False)

# ------------------ MENU PRINCIPAL ------------------ #

def menu():
    print("\n==== SISTEMA RH - LOJA DE ROUPAS ====")
    print("1. Cadastrar Funcionário")
    print("2. Listar Funcionários")
    print("3. Ver Detalhes de Funcionário")
    print("4. Atualizar Funcionário")
    print("5. Remover Funcionário")
    print("6. Registrar Férias")
    print("7. Registrar Afastamento")
    print("8. Relatório de Cargos e Salários")
    print("0. Sair")

# ------------------ FUNÇÕES DE RH ------------------ #

def cadastrar_funcionario():
    print("\n--- Cadastro de Funcionário ---")
    nome = input("Nome: ")
    cpf = input("CPF: ")
    cargo = input("Cargo: ")
    salario = float(input("Salário: R$ "))
    data_admissao = input("Data de admissão (dd/mm/aaaa): ")
    try:
        datetime.strptime(data_admissao, "%d/%m/%Y")
    except:
        print("⚠️ Data inválida. Use o formato dd/mm/aaaa.")
        return

    if any(f['cpf'] == cpf for f in funcionarios):
        print("⚠️ CPF já cadastrado.")
        return

    funcionario = {
        "nome": nome,
        "cpf": cpf,
        "cargo": cargo,
        "salario": salario,
        "data_admissao": data_admissao,
        "ferias_disponiveis": 30,
        "afastamentos": []
    }
    funcionarios.append(funcionario)
    salvar_dados()
    print("✅ Funcionário cadastrado com sucesso!")

def listar_funcionarios():
    print("\n--- Lista de Funcionários ---")
    if not funcionarios:
        print("Nenhum funcionário cadastrado.")
        return
    for f in funcionarios:
        print(f"- {f['nome']} | CPF: {f['cpf']} | Cargo: {f['cargo']} | Salário: R${f['salario']:.2f}")

def ver_detalhes_funcionario():
    cpf = input("\nDigite o CPF do funcionário: ")
    for f in funcionarios:
        if f["cpf"] == cpf:
            print(f"\n🧾 Detalhes de {f['nome']}:")
            print(f"Cargo: {f['cargo']}")
            print(f"Salário: R${f['salario']:.2f}")
            print(f"Admissão: {f['data_admissao']}")
            print(f"Férias disponíveis: {f['ferias_disponiveis']} dias")
            if f["afastamentos"]:
                print("Afastamentos:")
                for afast in f["afastamentos"]:
                    print(f"  - {afast['motivo']} ({afast['inicio']} até {afast['fim']})")
            else:
                print("Sem afastamentos registrados.")
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
            salvar_dados()
            print("✅ Funcionário atualizado!")
            return
    print("❌ Funcionário não encontrado.")

def remover_funcionario():
    cpf = input("\nCPF do funcionário que deseja remover: ")
    for i, f in enumerate(funcionarios):
        if f["cpf"] == cpf:
            del funcionarios[i]
            salvar_dados()
            print("🗑️ Funcionário removido.")
            return
    print("❌ Funcionário não encontrado.")

def registrar_ferias():
    cpf = input("\nCPF do funcionário: ")
    for f in funcionarios:
        if f["cpf"] == cpf:
            print(f"{f['nome']} tem {f['ferias_disponiveis']} dias disponíveis.")
            dias = int(input("Quantos dias deseja tirar de férias? "))
            if dias <= 0 or dias > f["ferias_disponiveis"]:
                print("❌ Quantidade de dias inválida.")
                return
            f["ferias_disponiveis"] -= dias
            salvar_dados()
            print(f"✅ Férias registradas. Dias restantes: {f['ferias_disponiveis']}")
            return
    print("❌ Funcionário não encontrado.")

def registrar_afastamento():
    cpf = input("\nCPF do funcionário: ")
    for f in funcionarios:
        if f["cpf"] == cpf:
            motivo = input("Motivo do afastamento: ")
            inicio = input("Data de início (dd/mm/aaaa): ")
            fim = input("Data de fim (dd/mm/aaaa): ")
            try:
                datetime.strptime(inicio, "%d/%m/%Y")
                datetime.strptime(fim, "%d/%m/%Y")
            except:
                print("⚠️ Datas inválidas.")
                return
            afastamento = {"motivo": motivo, "inicio": inicio, "fim": fim}
            f["afastamentos"].append(afastamento)
            salvar_dados()
            print("✅ Afastamento registrado.")
            return
    print("❌ Funcionário não encontrado.")

def relatorio_cargos_salarios():
    print("\n📊 Relatório de Cargos e Salários:")
    cargos = {}
    for f in funcionarios:
        cargo = f["cargo"]
        if cargo not in cargos:
            cargos[cargo] = []
        cargos[cargo].append(f["salario"])

    for cargo, salarios in cargos.items():
        media = sum(salarios) / len(salarios)
        print(f"- {cargo}: {len(salarios)} funcionário(s) | Salário médio: R${media:.2f}")

# ------------------ EXECUÇÃO ------------------ #

def sistema_rh():
    carregar_dados()
    while True:
        menu()
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            cadastrar_funcionario()
        elif opcao == "2":
            listar_funcionarios()
        elif opcao == "3":
            ver_detalhes_funcionario()
        elif opcao == "4":
            atualizar_funcionario()
        elif opcao == "5":
            remover_funcionario()
        elif opcao == "6":
            registrar_ferias()
        elif opcao == "7":
            registrar_afastamento()
        elif opcao == "8":
            relatorio_cargos_salarios()
        elif opcao == "0":
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("⚠️ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    sistema_rh()
