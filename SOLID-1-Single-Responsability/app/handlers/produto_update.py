class ProdutoUpdateHandler:
    def execute(self, conexao, form_data):
        sql = f"""
            UPDATE Produto
            SET descricao = '{form_data['descricao']}',
                preco_unitario = {form_data['preco_unitario']},
                quantidade_estoque = {form_data['quantidade_estoque']},
                categoria_id = {form_data['categoria_id']}
            WHERE id = {form_data['id']}
        """
        conexao.cursor().execute(sql)
        conexao.commit()