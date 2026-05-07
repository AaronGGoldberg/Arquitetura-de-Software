class CategoriaReadHandler:
    def execute(self, conexao):
        sql = '''
            SELECT id, descricao
            FROM Categoria
            ORDER BY descricao
        '''
        return conexao.cursor().execute(sql).fetchall()

    def execute_by_id(self, conexao, registro_id):
        sql = f'''
            SELECT id, descricao
            FROM Categoria
            WHERE id={registro_id}
        '''
        return conexao.cursor().execute(sql).fetchone()