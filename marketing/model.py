# marketing/model.py

class CampanhaMarketing:
    def __init__(self, nome_produto, descricao, preco):
        self.nome_produto = nome_produto
        self.descricao = descricao
        self.preco = preco
        self.mensagem = self.gerar_mensagem_promocional()

    def gerar_mensagem_promocional(self):
        return f"🔥 NOVO PRODUTO: {self.nome_produto.upper()} por apenas R${self.preco:.2f}! Confira já! 🔥"
