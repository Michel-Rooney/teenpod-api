# 🎙️ TeenPod API

API REST para uma plataforma de gerenciamento de podcasts. Permite que usuários ouçam, curtam, comentem e interajam com podcasts, enquanto administradores gerenciam o catálogo de conteúdo.

### 📋 Documentação Postman
[TeenPod API - DOCS](https://documenter.getpostman.com/view/23133439/2s9Xy5LW2t)

### 🌐 Deploy
[teenpod.pythonanywhere.com](https://teenpod.pythonanywhere.com/)

---

## 🚀 Tecnologias

| Tecnologia | Versão |
|---|---|
| Python | 3.x |
| Django | 4.2.17 |
| Django REST Framework | 3.15.2 |
| SimpleJWT | 5.3.0 |
| Pillow | 10.3.0 |
| SQLite (dev) / PostgreSQL (prod) | via dj-database-url |
| WhiteNoise | 6.5.0 |
| django-cors-headers | 4.2.0 |
| pytest / pytest-django | 7.4.1 / 4.5.2 |

---

## 🗂️ Estrutura do Projeto

```
teenpod-api/
├── core/               # Configurações principais (settings, urls, wsgi/asgi)
├── app/
│   ├── models.py       # User, Podcast, Comment
│   ├── views.py        # ViewSets de usuário, podcast e comentário
│   ├── serializers.py  # Serializers DRF
│   ├── urls.py         # Roteamento da API
│   ├── permissions.py  # Permissões customizadas
│   ├── utils.py        # Queries otimizadas
│   └── tests/          # Testes automatizados
├── manage.py
├── requirements.txt
├── build.sh            # Script de build para deploy
└── .env-example        # Exemplo de variáveis de ambiente
```

---

## ⚙️ Configuração do Ambiente

### 1. Clone o repositório

```bash
git clone https://github.com/Michel-Rooney/teenpod-api.git
cd teenpod-api
```

### 2. Crie e ative um ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
cp .env-example .env
```

Edite o arquivo `.env` com seus valores:

```env
# Gerar a SECRET_KEY com:
# python -c "import string as s;from random import SystemRandom as sr;print(''.join(sr().choices(s.ascii_letters + s.punctuation, k=64)))"
SECRET_KEY='sua-chave-secreta'

# 0 = False | 1 = True
DEBUG=1

# Separados por vírgula
ALLOWED_HOSTS=127.0.0.1
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000
CORS_ALLOWED_ORIGINS=http://127.0.0.1:3000

# Banco de dados externo (0 = SQLite local, 1 = URL externa)
USE_EXTERNAL_DATABASE=0
DATABASE_URL=
```

### 5. Execute as migrações

```bash
python manage.py migrate
```

### 6. Inicie o servidor

```bash
python manage.py runserver
```

---

## 🔑 Autenticação

A API usa **JWT (JSON Web Token)**. Rotas protegidas exigem o header:

```
Authorization: Bearer <access_token>
```

| Endpoint | Método | Descrição |
|---|---|---|
| `/api/token/` | POST | Obter access + refresh token |
| `/api/token/refresh/` | POST | Renovar o access token |
| `/api/token/verify/` | POST | Verificar validade do token |

---

## 📡 Endpoints

### 👤 Usuários — `/api/users/`

| Método | URL | Descrição | Auth | Admin |
|---|---|---|---|---|
| POST | `/api/users/` | Criar conta | ❌ | ❌ |
| GET | `/api/users/me/` | Dados do usuário logado | ✅ | ❌ |
| GET | `/api/users/{id}/` | Detalhar usuário | ✅ | ❌ |
| PUT/PATCH | `/api/users/{id}/` | Atualizar perfil | ✅ | ❌ |
| DELETE | `/api/users/{id}/` | Deletar conta | ✅ | ❌ |
| GET | `/api/users/` | Listar todos os usuários | ✅ | ✅ |

**Campos:**

| Campo | Tipo | Descrição |
|---|---|---|
| `username` | string | Nome de usuário |
| `password` | string | Senha |
| `email` | string | E-mail |
| `avatar` | image | Foto de perfil (opcional) |

> Ao atualizar ou deletar o perfil, o arquivo de avatar anterior é removido automaticamente do servidor.

---

### 🎙️ Podcasts — `/api/podcast/`

| Método | URL | Descrição | Auth | Admin |
|---|---|---|---|---|
| GET | `/api/podcast/` | Listar todos os podcasts | ✅ | ❌ |
| GET | `/api/podcast/{id}/` | Detalhar podcast | ✅ | ❌ |
| GET | `/api/podcast/{id}/like/` | Curtir podcast | ✅ | ❌ |
| GET | `/api/podcast/{id}/dislike/` | Descurtir podcast | ✅ | ❌ |
| POST | `/api/podcast/` | Criar podcast | ✅ | ✅ |
| PUT/PATCH | `/api/podcast/{id}/` | Atualizar podcast | ✅ | ✅ |
| DELETE | `/api/podcast/{id}/` | Deletar podcast | ✅ | ✅ |

**Campos:**

| Campo | Tipo | Descrição |
|---|---|---|
| `title` | string | Título do podcast |
| `description` | string | Descrição (opcional) |
| `audio` | file | Arquivo de áudio |
| `cover` | image | Capa do podcast (opcional) |
| `authors` | array | Lista de IDs de autores |
| `likes` | int | Contador de curtidas (leitura) |

> Ao atualizar ou deletar um podcast, os arquivos de capa e áudio anteriores são removidos do servidor automaticamente.

---

### 💬 Comentários — `/api/comment/`

| Método | URL | Descrição | Auth |
|---|---|---|---|
| GET | `/api/comment/` | Listar comentários | ✅ |
| POST | `/api/comment/?comment=False&entity={id}` | Comentar em um podcast | ✅ |
| POST | `/api/comment/?comment=True&entity={id}` | Responder a um comentário | ✅ |
| GET | `/api/comment/{id}/like/` | Curtir comentário | ✅ |
| GET | `/api/comment/{id}/dislike/` | Descurtir comentário | ✅ |
| PUT/PATCH | `/api/comment/{id}/` | Editar comentário | ✅ |
| DELETE | `/api/comment/{id}/` | Deletar comentário | ✅ |

**Parâmetros de criação:**

| Query Param | Valor | Descrição |
|---|---|---|
| `comment` | `False` | Comentar diretamente no podcast |
| `comment` | `True` | Responder a um comentário existente |
| `entity` (body) | `int` | ID do podcast ou comentário alvo |

**Campos:**

| Campo | Tipo | Descrição |
|---|---|---|
| `content` | string | Texto do comentário |
| `likes` | int | Contador de curtidas (leitura) |

> Um usuário não pode curtir ou descurtir o mesmo item mais de uma vez. Curtir remove o dislike anterior e vice-versa.

---

## 🔐 Permissões

| Permissão | Descrição |
|---|---|
| `IsOwner` | Usuário só pode editar/deletar sua própria conta. Superusuários têm acesso irrestrito. |
| `IsOwnerComment` | Usuário só pode editar/deletar comentários que ele próprio criou. Superusuários têm acesso irrestrito. |

---

## 🗄️ Banco de Dados

O projeto suporta dois modos, configurados via `.env`:

- **SQLite** (padrão para desenvolvimento): `USE_EXTERNAL_DATABASE=0`
- **Banco externo via URL** (PostgreSQL, etc.): `USE_EXTERNAL_DATABASE=1` e `DATABASE_URL=<url>`

---

## 🧪 Testes

```bash
# Rodar todos os testes
pytest

# Com relatório de cobertura
coverage run -m pytest
coverage report
```

Os testes cobrem fluxos de usuários, podcasts e comentários, incluindo autenticação JWT e validações de permissão.

---

## 🚢 Deploy

O projeto inclui `build.sh` para deploy em plataformas como Render ou PythonAnywhere:

```bash
./build.sh
```

Executa automaticamente:
1. `pip install -r requirements.txt`
2. `python manage.py collectstatic --no-input`
3. `python manage.py migrate`

Para produção com Gunicorn:

```bash
gunicorn core.wsgi:application
```

---

## ✒️ Autor

* [Michel-Rooney](https://github.com/Michel-Rooney/) — Dev. Backend
