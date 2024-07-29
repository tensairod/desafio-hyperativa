# API para Gerenciamento de Cartões

Esta API permite a criação, busca e upload de cartões com criptografia usando `AES`. É implementada em Flask e utiliza SQLAlchemy para gerenciamento de banco de dados.

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
FLASK_ENV=development
JWT_SECRET_KEY=a179ffa9157658442dc86630f9c246275fd030764b8ee69f8096131338f7b010
DATABASE_URL=sqlite:///app.db
AES_KEY=YCDbWQb1NMI59mrka3G6ybxjpHCitK2rAYQkqtv/VpA\=
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
Descrição: Adiciona um novo cartão ao banco de dados. O numero do cartao precisa ser encriptado, usando a nossa chave 
publica e encodificando em base64.

Headers:

- Authorization: Bearer <token>

Body:
```json
{
  "number": "OXZUBk07brjrn0HhJq58ggUYqJETPF78u8u+8SzzBPVImyRZ1BwQr4lDlcpTD1bd+NiVfBczx3ShrW4yNG+BexTITuDPbPr4MAaBHg0m9mMkEBffqZ8aWXBhTrGz4M0uxF7xEga7/0xQi9tWF8x6GkpOXEVhoAniHa94AE47xhCLZsEHUG1NAqTn9wDtyl7JOeC74Kj18gsKXc246GisWrcaz1tSuAFGN0WP0YDZ21iMBJMDykXg614tznh88qUH0dcn8nXdb4/AbRZ42G31cnlX6WtkGmDhTpWgd9C1YP0lkM8mo7b6Y1gRYsVGHYB0lNPVNV/avrY6CGvnwSugMQ=="
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


### 5. Buscar cartao
Endpoint: /get_card
Método: GET
Descrição: Busca o cartao pelo numero encriptado que é mandado via JSON. Encriptação deve seguir o mesmo padrão da
requisição de adicionar cartao.

Headers:

- Authorization: Bearer <token>

Body:
```json
{
  "number": "OXZUBk07brjrn0HhJq58ggUYqJETPF78u8u+8SzzBPVImyRZ1BwQr4lDlcpTD1bd+NiVfBczx3ShrW4yNG+BexTITuDPbPr4MAaBHg0m9mMkEBffqZ8aWXBhTrGz4M0uxF7xEga7/0xQi9tWF8x6GkpOXEVhoAniHa94AE47xhCLZsEHUG1NAqTn9wDtyl7JOeC74Kj18gsKXc246GisWrcaz1tSuAFGN0WP0YDZ21iMBJMDykXg614tznh88qUH0dcn8nXdb4/AbRZ42G31cnlX6WtkGmDhTpWgd9C1YP0lkM8mo7b6Y1gRYsVGHYB0lNPVNV/avrY6CGvnwSugMQ=="
}
```


## Chaves .pem

As chaves .pem publica e privada foram adicionadas no git tambem para maior facilidade nos testes
