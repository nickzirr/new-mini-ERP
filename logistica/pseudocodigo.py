# Estoque simulado (produto_id: quantidade)
estoque = {
    1: 50,
    2: 30,
}

# Lista para armazenar devoluções
devolucoes = []

# Lista para armazenar movimentações
movimentacoes = []

def registrar_movimentacao(produto_id, tipo, quantidade):
    movimentacoes.append({
        'produto_id': produto_id,
        'tipo': tipo,
        'quantidade': quantidade
    })

def registrar_entrada(produto_id, quantidade):
    estoque[produto_id] = estoque.get(produto_id, 0) + quantidade
    registrar_movimentacao(produto_id, 'Entrada', quantidade)

def registrar_saida(produto_id, quantidade):
    if estoque.get(produto_id, 0) >= quantidade:
        estoque[produto_id] -= quantidade
        registrar_movimentacao(produto_id, 'Saída', quantidade)
    else:
        raise Exception("Estoque insuficiente")

def registrar_devolucao(produto_id, quantidade, motivo):
    devolucao = {
        'produto_id': produto_id,
        'quantidade': quantidade,
        'motivo': motivo,
        'status': 'Em avaliação'
    }
    devolucoes.append(devolucao)
    return len(devolucoes) - 1  # Retorna o índice da devolução criada

def aceitar_devolucao(devolucao_id):
    devolucao = devolucoes[devolucao_id]
    devolucao['status'] = 'Aceita'
    estoque[devolucao['produto_id']] = estoque.get(devolucao['produto_id'], 0) + devolucao['quantidade']

def registrar_troca(produto_dev_id, produto_rec_id, qtde):
    devolucao_id = registrar_devolucao(produto_dev_id, qtde, 'Troca')
    aceitar_devolucao(devolucao_id)
    registrar_entrada(produto_rec_id, qtde)


# Testando o código
print("Estoque inicial:", estoque)

registrar_troca(produto_dev_id=1, produto_rec_id=2, qtde=3)

print("Estoque após troca:", estoque)
print("Devoluções:", devolucoes)
print("Movimentações:", movimentacoes)
