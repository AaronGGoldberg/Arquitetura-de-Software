class CategoriaUpdateHandler:
    def execute(self, conexao, form_data):
        sql = f"""
            UPDATE Categoria
            SET descricao = '{form_data['descricao']}'
            WHERE id = {form_data['id']}
        """
        conexao.cursor().execute(sql)
        conexao.commit()