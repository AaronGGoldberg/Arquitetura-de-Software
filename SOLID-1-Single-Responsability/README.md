# SOLID 1 - Single Responsibility (Responsabilidade Única)

## Objetivo da refatoração

Esta refatoração separa as responsabilidades que estavam concentradas em `app/views.py`.
A ideia é aplicar o princípio **S (Single Responsibility)** do SOLID: **cada classe deve ter um único motivo para mudar**.

## O que foi feito

### 1) Responsabilidade de banco isolada
- Criado `app/database.py` com a classe `DatabaseConnection`.
- Essa classe agora é responsável **somente** por abrir a conexão com o SQLite e habilitar `foreign_keys`.

### 2) Formulários em arquivo próprio
- Criado `app/forms.py` com:
  - `CategoriaForm`
  - `ProdutoForm`
- A responsabilidade desse arquivo é exclusivamente de **definição de formulários**.

### 3) CRUD de Categorias separado por responsabilidade
Na pasta `app/handlers/`, cada ação do CRUD virou uma classe independente:
- `categoria_create.py` → `CategoriaCreateHandler`
- `categoria_read.py` → `CategoriaReadHandler`
- `categoria_update.py` → `CategoriaUpdateHandler`
- `categoria_delete.py` → `CategoriaDeleteHandler`

### 4) CRUD de Produtos separado por responsabilidade
Também em `app/handlers/`, cada ação tem sua própria classe:
- `produto_create.py` → `ProdutoCreateHandler`
- `produto_read.py` → `ProdutoReadHandler`
- `produto_update.py` → `ProdutoUpdateHandler`
- `produto_delete.py` → `ProdutoDeleteHandler`

### 5) `views.py` ficou como orquestrador
- `app/views.py` continua recebendo as rotas HTTP (Django views),
- mas agora apenas delega cada tarefa para as classes corretas usando `from ... import ...`.

## Benefícios práticos

- Redução de acoplamento e do “arquivo monolítico”.
- Código mais fácil de testar e manter.
- Reuso mais simples com `from/import` de classes específicas.
- Mudanças de regra em Create/Read/Update/Delete afetam arquivos isolados.

## Estrutura final

```text
app/
  database.py
  forms.py
  views.py
  handlers/
    __init__.py
    categoria_create.py
    categoria_read.py
    categoria_update.py
    categoria_delete.py
    produto_create.py
    produto_read.py
    produto_update.py
    produto_delete.py
```

## Observação

A interface e as rotas da aplicação foram preservadas, mas a implementação interna foi reorganizada para seguir o princípio de responsabilidade única.

## Resolução de Problemas - Configuração Django

### Problema 1: Arquivo Estático Não Encontrado

```python
# Antes (apontava para pasta raiz)
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Depois (aponta para pasta correta dentro de app/)
STATICFILES_DIRS = [
    BASE_DIR / 'app' / 'static',
]
```

### Problema 2: Erro CSRF 403 - Origin Checking Failed

```python
# Adicionar hosts permitidos
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Adicionar origens confiáveis (HTTP e HTTPS)
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://localhost:8000',
    'https://127.0.0.1:8000',
]
```

**Por que isso resolve?**
- Django valida a origem das requisições POST para evitar ataques CSRF
- O ambiente de dev container usa HTTPS mesmo em localhost
- Agora o servidor aceita requisições de localhost e 127.0.0.1 tanto em HTTP quanto HTTPS