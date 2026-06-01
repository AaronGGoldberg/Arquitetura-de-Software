from pathlib import Path
import sqlite3


# Caminho do banco. Assim o sistema acha o arquivo mesmo rodando de outra pasta.
CAMINHO_BANCO = Path(__file__).resolve().parent.parent / 'db_solid.sqlite3'


class BancoDAO:
    """Classe base só para não repetir a conexão com o banco."""

    def conectar(self):
        conexao = sqlite3.connect(CAMINHO_BANCO)
        conexao.execute('PRAGMA foreign_keys = ON;')
        return conexao


class CategoriaDAO(BancoDAO):
    """DAO da tabela Categoria. Aqui ficam os comandos SQL da categoria."""

    def listar(self):
        sql = '''
            SELECT id,
                   descricao
            FROM Categoria
            ORDER BY descricao
        '''

        with self.conectar() as conexao:
            return conexao.cursor().execute(sql).fetchall()

    def buscar_por_id(self, id):
        sql = '''
            SELECT id,
                   descricao
            FROM Categoria
            WHERE id = ?
        '''

        with self.conectar() as conexao:
            return conexao.cursor().execute(sql, (id,)).fetchone()

    def inserir(self, descricao):
        sql = 'INSERT INTO Categoria(descricao) VALUES(?)'

        with self.conectar() as conexao:
            conexao.cursor().execute(sql, (descricao,))
            conexao.commit()

    def alterar(self, id, descricao):
        sql = '''
            UPDATE Categoria
            SET descricao = ?
            WHERE id = ?
        '''

        with self.conectar() as conexao:
            conexao.cursor().execute(sql, (descricao, id))
            conexao.commit()

    def excluir(self, id):
        sql = 'DELETE FROM Categoria WHERE id = ?'

        with self.conectar() as conexao:
            conexao.cursor().execute(sql, (id,))
            conexao.commit()


class ProdutoDAO(BancoDAO):
    """DAO da tabela Produto. Aqui ficam os comandos SQL do produto."""

    def listar(self):
        sql = '''
            SELECT pro.id,
                   pro.descricao,
                   pro.preco_unitario,
                   pro.quantidade_estoque,
                   pro.categoria_id,
                   cat.descricao as categoria
            FROM Produto pro
            INNER JOIN Categoria cat ON cat.id = pro.categoria_id
            ORDER BY pro.descricao
        '''

        with self.conectar() as conexao:
            return conexao.cursor().execute(sql).fetchall()

    def buscar_por_id(self, id):
        sql = '''
            SELECT pro.id,
                   pro.descricao,
                   pro.preco_unitario,
                   pro.quantidade_estoque,
                   pro.categoria_id,
                   cat.descricao as categoria
            FROM Produto pro
            INNER JOIN Categoria cat ON cat.id = pro.categoria_id
            WHERE pro.id = ?
        '''

        with self.conectar() as conexao:
            return conexao.cursor().execute(sql, (id,)).fetchone()

    def inserir(self, descricao, preco_unitario, quantidade_estoque, categoria_id):
        sql = '''
            INSERT INTO Produto (
                descricao,
                preco_unitario,
                quantidade_estoque,
                categoria_id
            )
            VALUES (?, ?, ?, ?)
        '''

        with self.conectar() as conexao:
            conexao.cursor().execute(
                sql,
                (descricao, preco_unitario, quantidade_estoque, categoria_id),
            )
            conexao.commit()

    def alterar(self, id, descricao, preco_unitario, quantidade_estoque, categoria_id):
        sql = '''
            UPDATE Produto
            SET descricao = ?,
                preco_unitario = ?,
                quantidade_estoque = ?,
                categoria_id = ?
            WHERE id = ?
        '''

        with self.conectar() as conexao:
            conexao.cursor().execute(
                sql,
                (descricao, preco_unitario, quantidade_estoque, categoria_id, id),
            )
            conexao.commit()

    def excluir(self, id):
        sql = 'DELETE FROM Produto WHERE id = ?'

        with self.conectar() as conexao:
            conexao.cursor().execute(sql, (id,))
            conexao.commit()