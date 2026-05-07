class CategoriaCreateHandler:
    def execute(self, conexao, form_data):
        sql = f"INSERT INTO Categoria(descricao) VALUES('{form_data['descricao']}')"
        conexao.cursor().execute(sql)
        conexao.commit()