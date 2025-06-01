# 🛒 StoreAPI

API RESTful para gerenciamento de uma loja virtual com funcionalidades completas de autenticação, produtos, carrinho de compras, checkout e histórico de compras.

---

## 🚀 Funcionalidades

- 🔐 Autenticação de usuários com JWT
- 📦 Cadastro e listagem de produtos
- 🛒 Adição de itens ao carrinho (usuário autenticado ou anônimo)
- 💳 Checkout do carrinho (finalização da compra)
- 🧾 Histórico de compras finalizadas
- 👤 Controle de permissões para usuários staff e autenticados

---

## 📂 Estrutura das Apps

- `products` – Gerenciamento de produtos
- `carts` – Lógica do carrinho de compras e checkout
- `buy` – Registro das compras finalizadas
- `users` – Autenticação e gerenciamento de usuários

---
## 🔐 Autenticação e Cadastro de Usuário

### 📌 Registro de Novo Usuário

Permite que qualquer pessoa crie uma conta no sistema.

- **Endpoint:** `POST /api/v1/accounts/register/`
- **Permissão:** Aberta (`AllowAny`)
- **Payload de exemplo:**

```json
{
  "username": "novousuario",
  "email": "usuario@email.com", (opcional)
  "password": "senha123"
}
```

## 🔐 Autenticação (JWT)

A autenticação da API é feita com o pacote `Simple JWT`.

### Obtenção do token:

`POST /api/token/`

```json
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

### Refresh token:

`POST /api/token/refresh/`

```json
{
  "refresh": "seu_refresh_token"
}
```

### Exemplo de uso no Postman:

Adicione no cabeçalho da requisição protegida:

```
Authorization: Bearer SEU_TOKEN
```

---

## 🔗 Documentação da API

A documentação completa com exemplos de uso está disponível no Postman:

👉 [Documentação no Postman](https://documenter.getpostman.com/view/32858190/2sB2qgeeGe)

---

## 🔧 Tecnologias Utilizadas

- Python 3.10+
- Django 4.x
- Django REST Framework
- SimpleJWT
- SQLite (pode ser adaptado para PostgreSQL)
- Postman (para testes e documentação)

---

## 📊 Endpoints Principais

| Método | Endpoint                         | Descrição                              |
|--------|----------------------------------|----------------------------------------|
| POST   | `/api/v1/accounts/register`      | Registro de novo usuário (cadastro)    |
| POST   | `/api/token/`                    | Geração de tokens (login)              |
| POST   | `/api/token/refresh/`            | Renovação de token                     |
| GET    | `/api/v1/products/`              | Lista de produtos                      |
| POST   | `/api/v1/cart/add/`              | Adiciona item ao carrinho              |
| GET    | `/api/v1/cart/`                  | Visualiza o carrinho atual             |
| POST   | `/api/v1/cart/checkout/`         | Finaliza compra (checkout)             |
| GET    | `/api/v1/cart/history/`          | Histórico de carrinhos finalizados     |

---

## 🛠️ Como rodar o projeto

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/storeapi.git
cd store_api
```

2. Crie e ative o ambiente virtual:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Rode as migrações:

```bash
python manage.py migrate
```

5. Cadastre os Produtos e Categorias via Django Command:

```bash
python manage.py load_products products.csv
```

6. Crie uma Superuser:

```bash
python manage.py createsuperuser
```

7. Inicie o servidor:

```bash
python manage.py runserver
```

8. Postman:

```
http://localhost:8000/api/v1/
```
9. DjangoAdmin:

```
http://127.0.0.1:8000/admin/
```
---

## 💡 Observações

- Carrinhos podem ser utilizados por usuários autenticados e anônimos.
- Usuários anônimos não conseguem fazer checkout.
- Após o checkout, o carrinho é desativado e salvo como histórico.
- O modelo `Buy` está relacionado ao `Cart`, registrando o total, produtos e data da compra.
- Usuários sem o staff (permissão de administrador) não podem fazer alterações nos products ou categories.

---

## 📁 Requisitos (requirements.txt)

```txt
Django>=4.2
djangorestframework>=3.14.0
djangorestframework-simplejwt>=5.2.2
```

---

## 📬 Contato

**Desenvolvedor:** Anailton Silva  
📧 francisco.anailton17@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/anailton-silva/)
