import sqlite3


class DatabaseConnection:
    """Responsável exclusivamente por abrir conexão com o SQLite."""

    def connect(self):
        conexao = sqlite3.connect('db_solid.sqlite3')
        conexao.execute('PRAGMA foreign_keys = ON;')
        return conexao