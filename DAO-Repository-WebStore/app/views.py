from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from app.repositories import CategoriaRepository, ProdutoRepository

# formulario utilizado para edicao de registros de categorias
class CategoriaForm(forms.Form):
    id = forms.IntegerField(label='ID', widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)
    descricao = forms.CharField(label='Descrição', max_length=30, required=True)

# Método responsavel por listar, incluir, alterar e excluir as Categorias.
def categorias(request, acao=None, id=None):
    '''
    Método responsavel por receber todas as rotas URL do cadastro de Categorias.

    Agora a view não conversa direto com SQL. Ela chama o Repository, e o
    Repository chama o DAO.
    '''

    try:
        categoria_repository = CategoriaRepository()

        # Listar registros
        if acao is None:
            registros = categoria_repository.listar()
            return render(request, 'categorias_listar.html', context={'registros': registros})
        
        # Salvar registro
        # 'categorias/salvar/': insere, altera ou exclui um registro
        elif acao == 'salvar':
            categoria_repository.salvar(request.POST)
            return HttpResponseRedirect(reverse('categorias'))
        
        # inserir registro
        elif acao == 'incluir':
            return render(request, 'categorias_editar.html',
                           context={'acao': 'Inclusão', 'form': CategoriaForm()})
        
        # Alterar ou excluir registro
        elif acao in ['alterar', 'excluir']:
            registro_dict = categoria_repository.buscar_por_id(id)
            nome_acao = 'Alteração' if acao == 'alterar' else 'Exclusão'            

            return render(request, 'categorias_editar.html',
                          context={'acao': nome_acao, 'form': CategoriaForm(initial=registro_dict)})
        
        # acao INVALIDA
        else:
            raise Exception('Ação inválida')

    # se ocorreu algum erro, insere a mensagem para ser exibida no contexto da página
    except Exception as err:
        return render(request, 'home.html', context={'ERRO': err})
    

# formulario utilizado para edicao de registros de produtos
class ProdutoForm(forms.Form):
    id = forms.IntegerField(label='ID', widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)
    descricao = forms.CharField(label='Descrição', max_length=30, required=True)
    preco_unitario = forms.DecimalField(label='Preço Unitário', max_digits=10, decimal_places=2, required=True)
    quantidade_estoque = forms.IntegerField(label='Qtd. Estoque', required=True)
    categoria_id = forms.ChoiceField(label='Categoria', required=True)

    # construtor do Formulario
    def __init__(self, *args, **kwargs):
        # chama construtor da classe-Pai
        super().__init__(*args, **kwargs)
        # carrega as categorias no <select> da página usando o Repository
        self.fields['categoria_id'].choices = CategoriaRepository().listar()

# Método responsavel por listar, incluir, alterar e excluir os Produtos.
def produtos(request, acao=None, id=None):
    '''
    Método responsavel por receber todas as rotas URL do cadastro de Produtos.

    A view ficou responsável só por receber a requisição e escolher a tela.
    A parte de banco de dados foi para DAO e Repository.
    '''

    try:
        produto_repository = ProdutoRepository() 

        # Listar registros
        if acao is None:
            registros = produto_repository.listar() 
            return render(request, 'produtos_listar.html', context={'registros': registros})
        
        # Salvar registro
        elif acao == 'salvar':
            produto_repository.salvar(request.POST)
            return HttpResponseRedirect(reverse('produtos'))

        # inserir registro
        elif acao == 'incluir':
            return render(request, 'produtos_editar.html',
                           context={'acao': 'Inclusão', 'form': ProdutoForm()})
        
        # Alterar ou excluir registro
        elif acao in ['alterar', 'excluir']:
            registro_dict = produto_repository.buscar_por_id(id)
            nome_acao = 'Alteração' if acao == 'alterar' else 'Exclusão'

            return render(request, 'produtos_editar.html',
                          context={'acao': nome_acao, 'form': ProdutoForm(initial=registro_dict)})
        
        # acao INVALIDA
        else:
            raise Exception('Ação inválida')

    # se ocorreu algum erro, insere a mensagem para ser exibida no contexto da página
    except Exception as err:
        return render(request, 'home.html', context={'ERRO': err})


# Exibe a página inicial da aplicação
def home(request):
    '''Exibe a pagina inicial da aplicação'''
    # define a página HTML (template) que deverá será carregada
    template = 'home.html'
    return render(request, template)