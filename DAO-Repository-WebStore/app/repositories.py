from app.dao import CategoriaDAO, ProdutoDAO


class CategoriaRepository:
    """Repository de Categoria. Ele usa o DAO e entrega dados prontos para a view."""

    def __init__(self):
        self.dao = CategoriaDAO()

    def listar(self):
        return self.dao.listar()

    def buscar_por_id(self, id):
        registro = self.dao.buscar_por_id(id)
        if registro is None:
            raise Exception('Categoria não encontrada')

        return {
            'id': registro[0],
            'descricao': registro[1],
        }

    def salvar(self, form_data):
        acao = form_data['acao']

        if acao == 'Inclusão':
            self.dao.inserir(form_data['descricao'])
        elif acao == 'Exclusão':
            self.dao.excluir(form_data['id'])
        else:
            self.dao.alterar(form_data['id'], form_data['descricao'])


class ProdutoRepository:
    """Repository de Produto. Ele usa o DAO e deixa a view mais limpa."""

    def __init__(self):
        self.dao = ProdutoDAO()

    def listar(self):
        return self.dao.listar()

    def buscar_por_id(self, id):
        registro = self.dao.buscar_por_id(id)
        if registro is None:
            raise Exception('Produto não encontrado')

        return {
            'id': registro[0],
            'descricao': registro[1],
            'preco_unitario': registro[2],
            'quantidade_estoque': registro[3],
            'categoria_id': registro[4],
            'categoria': registro[5],
        }

    def salvar(self, form_data):
        acao = form_data['acao']

        if acao == 'Inclusão':
            self.dao.inserir(
                form_data['descricao'],
                form_data['preco_unitario'],
                form_data['quantidade_estoque'],
                form_data['categoria_id'],
            )
        elif acao == 'Exclusão':
            self.dao.excluir(form_data['id'])
        else:
            self.dao.alterar(
                form_data['id'],
                form_data['descricao'],
                form_data['preco_unitario'],
                form_data['quantidade_estoque'],
                form_data['categoria_id'],
            )