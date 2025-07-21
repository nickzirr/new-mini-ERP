# marketing/controller.py

from marketing.model import CampanhaMarketing
from marketing import view

def criar_campanha_para_produto(nome, descricao, preco):
    campanha = CampanhaMarketing(nome, descricao, preco)
    view.exibir_campanha(campanha)
    # Aqui você também poderia salvar num banco, gerar imagem etc.
