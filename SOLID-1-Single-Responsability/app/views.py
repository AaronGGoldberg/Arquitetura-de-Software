from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Classe responsável por criar a conexão com o banco de dados
from app.database import DatabaseConnection

# Forms utilizados nas telas
from app.forms import CategoriaForm, ProdutoForm

# Handlers(Manipuladores) de Categoria
from app.handlers.categoria_create import CategoriaCreateHandler
from app.handlers.categoria_delete import CategoriaDeleteHandler
from app.handlers.categoria_read import CategoriaReadHandler
from app.handlers.categoria_update import CategoriaUpdateHandler

# Handlers(Manipuladores) de Produto
from app.handlers.produto_create import ProdutoCreateHandler
from app.handlers.produto_delete import ProdutoDeleteHandler
from app.handlers.produto_read import ProdutoReadHandler
from app.handlers.produto_update import ProdutoUpdateHandler

# VIEW DE CATEGORIAS
def categorias(request, acao=None, id=None):

    try:
        # Faz conexão com o banco
        conexao = DatabaseConnection().connect()

        # Lista todas as categorias
        if acao is None:
            registros = CategoriaReadHandler().execute(conexao)

            return render(
                request,
                'categorias_listar.html',
                context={'registros': registros}
            )

        # Salvar dados do formulário
        if acao == 'salvar':

            # Pega os dados enviados pelo form
            form_data = request.POST

            # Verifica qual ação foi feita
            acao_form = form_data['acao']

            # Inclusão
            if acao_form == 'Inclusão':
                CategoriaCreateHandler().execute(conexao, form_data)

            # Exclusão
            elif acao_form == 'Exclusão':
                CategoriaDeleteHandler().execute(conexao, form_data)

            # Alteração
            else:
                CategoriaUpdateHandler().execute(conexao, form_data)

            # Depois de salvar, volta para listagem
            return HttpResponseRedirect(reverse('categorias'))

        # Tela de inclusão
        if acao == 'incluir':

            return render(
                request,
                'categorias_editar.html',
                context={
                    'acao': 'Inclusão',
                    'form': CategoriaForm()
                }
            )

        # Tela de alteração ou exclusão
        if acao in ['alterar', 'excluir']:

            # Busca categoria pelo id
            registro = CategoriaReadHandler().execute_by_id(conexao, id)

            # Organiza os dados para preencher o form
            registro_dict = {
                'id': registro[0],
                'descricao': registro[1]
            }

            # Define texto da tela
            if acao == 'alterar':
                acao_tela = 'Alteração'
            else:
                acao_tela = 'Exclusão'

            return render(
                request,
                'categorias_editar.html',
                context={
                    'acao': acao_tela,
                    'form': CategoriaForm(initial=registro_dict)
                }
            )

        # Caso a ação não exista
        raise Exception('Ação inválida')

    except Exception as err:

        # Mostra erro na home
        return render(
            request,
            'home.html',
            context={'ERRO': err}
        )

# VIEW DE PRODUTOS
def produtos(request, acao=None, id=None):

    try:
        # Conexão com o banco
        conexao = DatabaseConnection().connect()

        # Lista os produtos
        if acao is None:

            registros = ProdutoReadHandler().execute(conexao)

            return render(
                request,
                'produtos_listar.html',
                context={'registros': registros}
            )

        # Salvar formulário
        if acao == 'salvar':

            form_data = request.POST

            # Descobre qual ação foi feita
            acao_form = form_data['acao']

            # Inclusão
            if acao_form == 'Inclusão':
                ProdutoCreateHandler().execute(conexao, form_data)

            # Exclusão
            elif acao_form == 'Exclusão':
                ProdutoDeleteHandler().execute(conexao, form_data)

            # Alteração
            else:
                ProdutoUpdateHandler().execute(conexao, form_data)

            return HttpResponseRedirect(reverse('produtos'))

        # Tela de inclusão
        if acao == 'incluir':

            return render(
                request,
                'produtos_editar.html',
                context={
                    'acao': 'Inclusão',
                    'form': ProdutoForm()
                }
            )

        # Tela de alterar ou excluir
        if acao in ['alterar', 'excluir']:

            # Busca produto pelo id
            registro = ProdutoReadHandler().execute_by_id(conexao, id)

            # Organiza os dados do produto
            registro_dict = {
                'id': registro[0],
                'descricao': registro[1],
                'preco_unitario': registro[2],
                'quantidade_estoque': registro[3],
                'categoria_id': registro[4],
                'categoria': registro[5],
            }

            # Define texto da ação
            if acao == 'alterar':
                acao_tela = 'Alteração'
            else:
                acao_tela = 'Exclusão'

            return render(
                request,
                'produtos_editar.html',
                context={
                    'acao': acao_tela,
                    'form': ProdutoForm(initial=registro_dict)
                }
            )

        raise Exception('Ação inválida')

    except Exception as err:

        return render(
            request,
            'home.html',
            context={'ERRO': err}
        )


def home(request):

    # Carrega página inicial
    return render(request, 'home.html')