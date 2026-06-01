# Atividade DAO + Repository - WebStore

**Aluno:** Aaron Guerra Goldberg
**Aluno:** Ramon Couto Santos

**Disciplina:** Arquitetura de Software

## Introdução

Este README explica a atividade feita no projeto **DAO-Repository-WebStore**. A proposta foi analisar a aplicação WebStore e aplicar os padrões de projeto **DAO (Data Access Object)** e **Repository**.

Eu fiz a refatoração de uma forma simples, tentando deixar o código parecido com algo feito em aula: sem inventar uma arquitetura muito complexa, mas separando melhor cada responsabilidade.

A aplicação continua sendo a mesma WebStore, com cadastro de:

* **Categorias**;
* **Produtos**.

A diferença principal é que agora a `view` não fica mais cheia de SQL. A parte de banco foi colocada em arquivos separados.

## Objetivo da atividade

O objetivo foi melhorar a organização do código usando padrões de projeto. Antes, o arquivo `app/views.py` fazia praticamente tudo sozinho.

Depois da alteração, a ideia ficou assim:

```text
Tela / Rota -> View -> Repository -> DAO -> Banco SQLite
```

Ou seja:

* a **view** cuida da requisição e escolhe qual página renderizar;
* o **repository** organiza a regra de acesso que a view precisa usar;
* o **DAO** executa os comandos SQL no banco;
* o **SQLite** guarda os dados.

## Como estava antes

Antes da refatoração, o arquivo `app/views.py` misturava várias responsabilidades no mesmo lugar.

Ele fazia coisas como:

* receber a requisição do usuário;
* decidir se era listagem, inclusão, alteração ou exclusão;
* abrir conexão com o banco SQLite;
* escrever os comandos SQL dentro da própria view;
* executar `SELECT`, `INSERT`, `UPDATE` e `DELETE`;
* montar dicionários para preencher formulários;
* renderizar as páginas HTML.

Isso funciona, mas não é a melhor organização, porque a view fica responsável por muita coisa. Se eu precisasse mudar alguma consulta SQL, eu teria que mexer direto na view, que deveria ser mais ligada à parte da tela.

## Problema encontrado no código original

O principal problema era a falta de separação de responsabilidades.

Por exemplo, a view de categorias tinha SQL de listagem, SQL de insert, SQL de update e SQL de delete. A view de produtos também tinha esse mesmo tipo de lógica.

Então, em vez da view só controlar o fluxo da página, ela também estava controlando o banco de dados.

Na prática, isso deixa o código:

* maior;
* mais repetido;
* mais difícil de entender;
* mais difícil de manter;
* mais fácil de dar erro se mudar alguma coisa no banco.

## Padrão DAO

DAO significa **Data Access Object**, ou seja, Objeto de Acesso a Dados.

Na minha explicação simples, o DAO é a parte do código que conversa diretamente com o banco de dados.

No projeto, eu criei o arquivo:

```text
app/dao.py
```

Nesse arquivo ficam:

* a conexão com o banco SQLite;
* os comandos SQL;
* os métodos de listar, buscar, inserir, alterar e excluir.

### Por que usar DAO?

Usei DAO para tirar os comandos SQL de dentro da view.

Assim, se um dia eu precisar mudar uma consulta, eu vou direto no DAO e não preciso ficar procurando SQL misturado no meio da lógica da tela.

### DAOs criados

Foram criadas três classes principais:

```python
class BancoDAO:
    ...
```

```python
class CategoriaDAO(BancoDAO):
    ...
```

```python
class ProdutoDAO(BancoDAO):
    ...
```

A classe `BancoDAO` ficou como uma classe base, só para centralizar a conexão com o banco.

A classe `CategoriaDAO` ficou responsável pela tabela `Categoria`.

A classe `ProdutoDAO` ficou responsável pela tabela `Produto`.

## Padrão Repository

O Repository é uma camada que fica entre a view e o DAO.

Na minha explicação, ele é como um intermediário. A view pede algo para o Repository, e o Repository usa o DAO para buscar ou salvar no banco.

No projeto, eu criei o arquivo:

```text
app/repositories.py
```

Nesse arquivo ficam:

* `CategoriaRepository`;
* `ProdutoRepository`.

### Por que usar Repository?

Usei Repository para deixar a view ainda mais simples.

A view não precisa saber qual método do DAO chamar em cada caso. Ela chama o repository, e ele decide se deve inserir, alterar ou excluir.

Por exemplo, no método `salvar(form_data)`, o repository olha a ação que veio do formulário:

* se for `Inclusão`, ele chama o método de inserir;
* se for `Alteração`, ele chama o método de alterar;
* se for `Exclusão`, ele chama o método de excluir.

## Arquivos criados

## `app/dao.py`

Este arquivo foi criado para guardar a parte de acesso direto ao banco de dados.

### `BancoDAO`

A classe `BancoDAO` tem o método `conectar()`.

Esse método abre conexão com o banco `db_solid.sqlite3` e também ativa a regra de chave estrangeira com:

```python
PRAGMA foreign_keys = ON;
```

Isso é importante porque a tabela `Produto` depende da tabela `Categoria`.

### `CategoriaDAO`

A classe `CategoriaDAO` possui os métodos:

* `listar()` - busca todas as categorias ordenadas pela descrição;
* `buscar_por_id(id)` - busca uma categoria pelo id;
* `inserir(descricao)` - adiciona uma categoria;
* `alterar(id, descricao)` - altera a descrição de uma categoria;
* `excluir(id)` - exclui uma categoria.

### `ProdutoDAO`

A classe `ProdutoDAO` possui os métodos:

* `listar()` - busca todos os produtos com a descrição da categoria;
* `buscar_por_id(id)` - busca um produto específico pelo id;
* `inserir(descricao, preco_unitario, quantidade_estoque, categoria_id)` - adiciona um produto;
* `alterar(id, descricao, preco_unitario, quantidade_estoque, categoria_id)` - altera um produto;
* `excluir(id)` - exclui um produto.

Nos métodos de produto, eu mantive o `INNER JOIN` com `Categoria`, porque a tela de produto precisa mostrar também o nome da categoria.

## `app/repositories.py`

Este arquivo foi criado para ser a camada intermediária entre as views e os DAOs.

### `CategoriaRepository`

O `CategoriaRepository` usa o `CategoriaDAO` por baixo.

Ele tem métodos para:

* listar categorias;
* buscar categoria por id;
* salvar categoria de acordo com a ação do formulário.

Quando busca uma categoria por id, ele transforma o resultado em dicionário, porque isso facilita preencher o formulário do Django.

### `ProdutoRepository`

O `ProdutoRepository` usa o `ProdutoDAO` por baixo.

Ele tem métodos para:

* listar produtos;
* buscar produto por id;
* salvar produto de acordo com a ação do formulário.

No caso do produto, o dicionário tem mais campos, como preço, quantidade, categoria e categoria_id.

## Arquivo alterado

## `app/views.py`

O arquivo `app/views.py` foi simplificado.

Antes ele tinha os comandos SQL diretamente nele. Depois da refatoração, ele passou a importar:

```python
from app.repositories import CategoriaRepository, ProdutoRepository
```

Agora a view de categorias usa:

```python
categoria_repository = CategoriaRepository()
```

E a view de produtos usa:

```python
produto_repository = ProdutoRepository()
```

Com isso, a view ficou mais focada em:

* verificar qual ação foi chamada pela URL;
* chamar o repository correto;
* renderizar o template certo;
* redirecionar depois de salvar.

## Exemplo do fluxo de Categoria

### Listar categorias

Quando o usuário acessa:

```text
/categorias/
```

Acontece este fluxo:

1. A URL chama a função `categorias` em `views.py`.
2. A view cria um `CategoriaRepository`.
3. A view chama `categoria_repository.listar()`.
4. O repository chama `CategoriaDAO().listar()`.
5. O DAO executa o `SELECT` no banco.
6. A lista volta para a view.
7. A view renderiza `categorias_listar.html`.

### Salvar categoria

Quando o usuário salva uma categoria, acontece:

1. O formulário envia os dados por POST.
2. A view chama `categoria_repository.salvar(request.POST)`.
3. O repository verifica se a ação é inclusão, alteração ou exclusão.
4. O repository chama o método correto do DAO.
5. O DAO executa o SQL.
6. A view redireciona para a listagem de categorias.

## Exemplo do fluxo de Produto

### Listar produtos

Quando o usuário acessa:

```text
/produtos/
```

Acontece este fluxo:

1. A URL chama a função `produtos` em `views.py`.
2. A view cria um `ProdutoRepository`.
3. A view chama `produto_repository.listar()`.
4. O repository chama `ProdutoDAO().listar()`.
5. O DAO faz um `SELECT` com `INNER JOIN` entre produto e categoria.
6. Os dados voltam para a view.
7. A view renderiza `produtos_listar.html`.

### Salvar produto

Quando o usuário salva um produto:

1. O formulário envia os dados para a rota de salvar.
2. A view chama `produto_repository.salvar(request.POST)`.
3. O repository olha a ação do formulário.
4. O repository chama inserir, alterar ou excluir no DAO.
5. O DAO executa o comando SQL no SQLite.
6. A view redireciona para a listagem de produtos.

## Comparação antes e depois

| Antes                            | Depois                            |
| -------------------------------- | --------------------------------- |
| View tinha SQL direto            | SQL ficou no DAO                  |
| View abria conexão com banco     | DAO abre conexão com banco        |
| View fazia quase tudo            | Responsabilidades foram separadas |
| Código mais difícil de manter    | Código mais organizado            |
| Alterar SQL exigia mexer na view | Alterar SQL fica no DAO           |

## Estrutura final simplificada

A estrutura principal ficou assim:

```text
DAO-Repository-WebStore/
├── app/
│   ├── dao.py
│   ├── repositories.py
│   ├── views.py
│   └── templates/
├── db_solid.sqlite3
├── manage.py
└── README.md
```

## Observação sobre Codespace

Como eu uso Codespace, pode ser necessário ajustar configurações no `settings.py`, principalmente relacionadas a:

* `ALLOWED_HOSTS`;
* configurações de CSRF;
* host gerado pelo Codespace.

Essas configurações são mais relacionadas ao ambiente onde o Django está rodando. A parte da atividade de DAO e Repository ficou concentrada nos arquivos `dao.py`, `repositories.py` e `views.py`.

## Como executar o projeto

Entre na pasta do projeto:

```bash
cd DAO-Repository-WebStore
```

Se estiver usando ambiente virtual, ative ele antes. Depois execute:

```bash
python manage.py runserver
```

Depois acesse no navegador:

```text
http://127.0.0.1:8000/
```

No Codespace, normalmente o acesso acontece pela URL encaminhada na aba **Ports**.

## Como testar de forma simples

Um teste simples é abrir o sistema e verificar se as páginas continuam funcionando:

* página inicial;
* listagem de categorias;
* inclusão de categoria;
* alteração de categoria;
* exclusão de categoria;
* listagem de produtos;
* inclusão de produto;
* alteração de produto;
* exclusão de produto.

Também dá para rodar o comando:

```bash
python manage.py check
```

Esse comando verifica se o projeto Django possui algum erro básico de configuração.

## O que eu aprendi

Com essa atividade eu entendi melhor que um código fica mais fácil de manter quando cada parte tem sua responsabilidade.

Antes, a view fazia muita coisa. Depois, ficou mais separado:

* **View**: controla o que aparece na tela e o fluxo da requisição;
* **Repository**: organiza a comunicação entre view e DAO;
* **DAO**: acessa o banco de dados e executa SQL;
* **Banco SQLite**: armazena as informações.

Eu também percebi que aplicar padrão de projeto não significa deixar o código difícil. Dá para aplicar de um jeito simples, desde que a separação faça sentido.

## Conclusão

A atividade foi concluída aplicando os padrões **DAO** e **Repository** na aplicação WebStore.

O sistema manteve as mesmas funcionalidades, mas o código ficou melhor dividido. A view ficou menor e mais limpa, o acesso ao banco ficou no DAO, e o Repository ficou como camada intermediária.

Para mim, a parte mais importante foi entender que, quando o projeto cresce, separar responsabilidades ajuda bastante para não virar tudo um arquivo gigante e confuso.