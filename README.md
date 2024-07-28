# API para Gerenciamento de Cartões

Esta API permite a criação, busca e upload de cartões com criptografia usando `Fernet`. É implementada em Flask e utiliza SQLAlchemy para gerenciamento de banco de dados.

## Requisitos

- Python 3.8 ou superior
- Pip
- SQLite (ou outro banco de dados compatível)

## Configuração

### 1. Clonar o Repositório

```bash
git clone git@github.com:tensairod/desafio-hyperativa.git
```

### 2. Criar e Ativar um Ambiente Virtual

```bash
pipenv install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente

```env
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=sqlite:///db.sqlite3
FERNET_KEY=<sua-chave-fern>
JWT_SECRET_KEY=a179ffa9157658442dc86630f9c246275fd030764b8ee69f8096131338f7b010
```

### 4. Inicializar o Banco de Dados

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. Rodar a Aplicação

```bash
6. Rodar a Aplicação
```

## Endpoints

### 1. Register

Endpoint: /register
Método: POST
Descrição: Registra um novo usuário na aplicação.

Body:

```json
{
  "username": "user",
  "password": "password"
}

```

### 2. Login
Endpoint: /login
Método: POST
Descrição: Realiza o login do usuário e retorna um token de acesso.

Body:
```json
{
  "username": "user",
  "password": "password"
}

```

### 3. Adicionar Cartao
Endpoint: /cards
Método: POST
Descrição: Adiciona um novo cartão ao banco de dados.

Headers:

- Authorization: Bearer <token>

Body:
```json
{
  "number": "1234567812345678"
}
```

### 4. Upload de cartoes
Endpoint: /cards/upload
Método: POST
Descrição: Faz o upload de um arquivo TXT contendo números de cartões e adiciona-os ao banco de dados.

Headers:

- Authorization: Bearer <token>

Form Data:

- file - Arquivo TXT com números de cartões.
