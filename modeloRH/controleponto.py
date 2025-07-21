import json
from datetime import datetime, timedelta

ARQUIVO_FUNC = "funcionarios_ponto.json"
ARQUIVO_ADVERTENCIAS = "advertencias.json"

funcionarios = {}
advertencias = {}

# ------------------ UTILIDADES ------------------ #

def carregar_dados():
    global funcionarios, advertencias
    try:
        with open(ARQUIVO_FUNC, "r", encoding="utf-8") as f:
            funcionarios = json.load(f)
    except FileNotFoundError:
        funcionarios = {}

    try:
        with open(ARQUIVO_ADVERTENCIAS, "r", encoding="utf-8") as f:
            advertencias = json.load(f)
    except FileNotFoundError:
        advertencias = {}

def salvar_dados():
    with open(ARQUIVO_FUNC, "w", encoding="utf-8") as f:
        json.dump(funcionarios, f, indent=4, ensure_ascii=False)
    with open(ARQUIVO_ADVERTENCIAS, "w", encoding="utf-8") as f:
        json.dump(advertencias, f, indent=4, ensure_ascii=False)

def menu():
    print("\n==== RH - CONTROLE DE PONTO E CONDUTA ====")
    print("1. Registrar Entrada")
    print("2. Registrar Saída")
    print("3. Ver Banco de Horas")
    print("4. Histórico de Presença")
    print("5. Registrar Advertência")
    print("6. Relatório Disciplinar")
    print("0. Sair")

# ------------------ FUNÇÕES DE PONTO ------------------ #

def registrar_entrada():
    cpf = input("CPF do funcionário: ")
    data_hoje = datetime.now().strftime("%Y-%m-%d")

    if cpf not in funcionarios:
        nome = input("Nome do funcionário: ")
        funcionarios[cpf] = {
            "nome": nome,
            "presencas": {}
        }

    if data_hoje not in funcionarios[cpf]["presencas"]:
        funcionarios[cpf]["presencas"][data_hoje] = {"entrada": None, "saida": None}

    if funcionarios[cpf]["presencas"][data_hoje]["entrada"]:
        print("⚠️ Entrada já registrada hoje.")
        return

    hora = datetime.now().strftime("%H:%M:%S")
    funcionarios[cpf]["presencas"][data_hoje]["entrada"] = hora
    salvar_dados()
    print(f"✅ Entrada registrada para {funcionarios[cpf]['nome']} às {hora}")

def registrar_saida():
    cpf = input("CPF do funcionário: ")
    data_hoje = datetime.now().strftime("%Y-%m-%d")

    if cpf not in funcionarios or data_hoje not in funcionarios[cpf]["presencas"]:
        print("⚠️ Nenhuma entrada registrada hoje.")
        return

    if funcionarios[cpf]["presencas"][data_hoje]["saida"]:
        print("⚠️ Saída já registrada hoje.")
        return

    hora = datetime.now().strftime("%H:%M:%S")
    funcionarios[cpf]["presencas"][data_hoje]["saida"] = hora
    salvar_dados()
    print(f"✅ Saída registrada para {funcionarios[cpf]['nome']} às {hora}")

def ver_banco_horas():
    cpf = input("CPF do funcionário: ")

    if cpf not in funcionarios:
        print("Funcionário não encontrado.")
        return

    total_minutos = 0
    for data, registro in funcionarios[cpf]["presencas"].items():
        if registro["entrada"] and registro["saida"]:
            entrada = datetime.strptime(f"{data} {registro['entrada']}", "%Y-%m-%d %H:%M:%S")
            saida = datetime.strptime(f"{data} {registro['saida']}", "%Y-%m-%d %H:%M:%S")
            minutos = (saida - entrada).total_seconds() / 60
            total_minutos += minutos

    horas_trabalhadas = total_minutos / 60
    horas_esperadas = len(funcionarios[cpf]["presencas"]) * 8  # 8 horas por dia
    banco = horas_trabalhadas - horas_esperadas

    print(f"\n🕒 Banco de horas de {funcionarios[cpf]['nome']}: {banco:.2f}h")
    if banco < 0:
        print("⚠️ Débito de horas")
    elif banco > 0:
        print("✅ Horas extras acumuladas")

# ------------------ CONDUTA E DISCIPLINA ------------------ #

def registrar_advertencia():
    cpf = input("CPF do funcionário: ")
    if cpf not in funcionarios:
        print("Funcionário não encontrado.")
        return
    motivo = input("Motivo da advertência: ")
    data = datetime.now().strftime("%d/%m/%Y")
    registro = {"data": data, "motivo": motivo}

    if cpf not in advertencias:
        advertencias[cpf] = []

    advertencias[cpf].append(registro)
    salvar_dados()
    print("⚠️ Advertência registrada.")

def relatorio_disciplina():
    print("\n📋 Relatório Disciplinar:")
    if not advertencias:
        print("Nenhuma advertência registrada.")
        return

    for cpf, lista in advertencias.items():
        nome = funcionarios[cpf]["nome"] if cpf in funcionarios else "Desconhecido"
        print(f"- {nome} ({cpf}): {len(lista)} advertência(s)")
        for adv in lista:
            print(f"   • {adv['data']}: {adv['motivo']}")

# ------------------ HISTÓRICO ------------------ #

def historico_presenca():
    cpf = input("CPF do funcionário: ")
    if cpf not in funcionarios:
        print("Funcionário não encontrado.")
        return

    print(f"\n📆 Histórico de presença de {funcionarios[cpf]['nome']}:")
    for data, registro in sorted(funcionarios[cpf]["presencas"].items()):
        entrada = registro["entrada"] or "--:--"
        saida = registro["saida"] or "--:--"
        print(f"{data}: Entrada: {entrada} | Saída: {saida}")

# ------------------ EXECUÇÃO ------------------ #

def sistema_rh_ponto():
    carregar_dados()
    while True:
        menu()
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            registrar_entrada()
        elif opcao == "2":
            registrar_saida()
        elif opcao == "3":
            ver_banco_horas()
        elif opcao == "4":
            historico_presenca()
        elif opcao == "5":
            registrar_advertencia()
        elif opcao == "6":
            relatorio_disciplina()
        elif opcao == "0":
            print("Saindo do sistema.")
            break
        else:
            print("⚠️ Opção inválida.")

if __name__ == "__main__":
    sistema_rh_ponto()
