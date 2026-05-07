class ProdutoDeleteHandler:
    def execute(self, conexao, form_data):
        sql = f"DELETE FROM Produto WHERE id = {form_data['id']}"
        conexao.cursor().execute(sql)
        conexao.commit()