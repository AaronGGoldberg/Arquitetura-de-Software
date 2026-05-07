class CategoriaDeleteHandler:
    def execute(self, conexao, form_data):
        sql = f"DELETE FROM Categoria WHERE id = {form_data['id']}"
        conexao.cursor().execute(sql)
        conexao.commit()