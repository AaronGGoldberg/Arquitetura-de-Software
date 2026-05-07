class ProdutoReadHandler:
    def execute(self, conexao):
        sql = '''
            SELECT  pro.id,
                    pro.descricao,
                    pro.preco_unitario,
                    pro.quantidade_estoque,
                    pro.categoria_id,
                    cat.descricao as categoria
            FROM Produto pro
            INNER JOIN Categoria cat ON cat.id = pro.categoria_id
            ORDER BY pro.descricao
        '''
        return conexao.cursor().execute(sql).fetchall()

    def execute_by_id(self, conexao, registro_id):
        sql = f'''
            SELECT  pro.id,
                    pro.descricao,
                    pro.preco_unitario,
                    pro.quantidade_estoque,
                    pro.categoria_id,
                    cat.descricao as categoria
            FROM Produto pro
            INNER JOIN Categoria cat ON cat.id = pro.categoria_id
            WHERE pro.id={registro_id}
        '''
        return conexao.cursor().execute(sql).fetchone()