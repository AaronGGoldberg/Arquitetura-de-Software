class ProdutoCreateHandler:
    def execute(self, conexao, form_data):
        sql = f"""
            INSERT INTO Produto (
                descricao,
                preco_unitario,
                quantidade_estoque,
                categoria_id
            )
            VALUES(
                '{form_data['descricao']}',
                {form_data['preco_unitario']},
                {form_data['quantidade_estoque']},
                {form_data['categoria_id']}
            );
        """
        conexao.cursor().execute(sql)
        conexao.commit()