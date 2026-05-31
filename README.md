# Backend

[🇺🇸 English](#english) | [🇧🇷 Português](#português)

---

## English

### Overview

RoadUSP backend is a Flask-based REST API that serves USP curriculum data from Supabase to the frontend. It provides endpoints for course listing, discipline fetching, and transforms database records into D3-compatible graph format.

### Quick Start

```bash
cd roadusp-backend
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add: SUPABASE_URL, SUPABASE_KEY, JWT_SECRET_KEY

python server.py    # Development
make run           # Production (Gunicorn)
```

Runs at http://localhost:3010

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SUPABASE_URL` | Yes | Supabase project URL |
| `SUPABASE_KEY` | Yes | Supabase anon key |
| `JWT_SECRET_KEY` | Yes | JWT signing secret |

### Tech Stack

| Technology | Purpose |
|------------|---------|
| Flask | Web framework |
| Flask-CORS | Cross-origin requests |
| Flask-JWT-Extended | JWT authentication |
| Supabase | PostgreSQL client |
| Gunicorn | WSGI server |
| pdfplumber | PDF parsing |

### Project Structure

```
src/
├── api/v1/endpoints/
│   ├── cursos.py          # Course endpoints
│   └── conta.py           # Account + history endpoints
├── core/
│   └── config.py          # Settings, Supabase client
├── database/
│   ├── setup.py           # Migration runner
│   ├── 000_create_usuarios.sql
│   ├── 001_create_historico_disciplinas.sql
│   └── 002_create_processamentos_historico.sql
├── repositories/
│   ├── cursos_db.py       # Course/discipline queries
│   ├── usuarios_db.py     # User CRUD
│   ├── historico_db.py    # User history CRUD
│   └── processamento_db.py # Async processing tracking
├── services/
│   ├── grafos.py          # Graph transformation
│   ├── pdf_parsing.py     # PDF parsing
│   └── processamento.py   # Async background processing
└── utils/
    └── senha_servicos.py  # Password hashing
```

### API Endpoints

| Endpoint | Method | Auth | Parameters | Description |
|----------|--------|------|------------|-------------|
| `/ping` | GET | - | - | Health check |
| `/api/v1/cursos/lista` | GET | - | `unidade` | List courses for campus |
| `/api/v1/cursos/disciplinas` | GET | - | `unidade`, `curso` | Get graph nodes/links |
| `/api/v1/conta/criar` | POST | - | `email`, `senha` | Create account |
| `/api/v1/conta/login` | POST | - | `email`, `senha` | Login, returns JWT |
| `/api/v1/conta/deletar` | DELETE | JWT | `email` | Delete account |
| `/api/v1/conta/alterar` | UPDATE | JWT | `email`, `senha_antiga`, `nova_senha` | Change password |
| `/api/v1/conta/upload/historico` | POST | JWT | `arquivo` (PDF) | Upload history (async) |
| `/api/v1/conta/processamento/<id>` | GET | JWT | - | Check upload processing status |

### Database Schema

**unidades:** id (uuid), nome (text)  
**cursos:** id, nome, id_unidade, duracao_ideal, duracao_minima, duracao_maxima  
**disciplinas:** id, codigo, nome, id_curso, semestre, obrigatoria, eletiva, livre, cred_aula, cred_trabalho, ch  
**requisitos:** id, id_disciplina, id_requisito  
**usuarios:** id (uuid), email (unique), senha (hash)  
**historico_disciplinas:** id (serial), id_usuario (fk), codigo_disciplina (text), status (aprovada|cursando), created_at  
**processamentos_historico:** id (uuid), id_usuario (fk), status (processando|concluido|erro), resultado (jsonb), erro (text), created_at, updated_at

### Known Limitations

- No pagination
- No caching
- Course/unidade names must match exactly

---

## Português

### Visão Geral

O backend do RoadUSP é uma API REST baseada em Flask que serve dados curriculares da USP do Supabase para o frontend. Fornece endpoints para listagem de cursos, busca de disciplinas e transforma registros do banco em formato compatível com D3.

### Início Rápido

```bash
cd roadusp-backend
pip install -r requirements.txt

# Criar arquivo .env
cp .env.example .env
# Adicionar: SUPABASE_URL, SUPABASE_KEY, JWT_SECRET_KEY

python server.py    # Desenvolvimento
make run           # Produção (Gunicorn)
```

Executa em http://localhost:3010

### Variáveis de Ambiente

| Variável | Requerido | Descrição |
|----------|----------|-------------|
| `SUPABASE_URL` | Sim | URL do projeto Supabase |
| `SUPABASE_KEY` | Sim | Chave anon do Supabase |
| `JWT_SECRET_KEY` | Sim | Segredo para assinatura JWT |

### Stack Tecnológica

| Tecnologia | Propósito |
|------------|-----------|
| Flask | Framework web |
| Flask-CORS | Requisições cross-origin |
| Flask-JWT-Extended | Autenticação JWT |
| Supabase | Cliente PostgreSQL |
| Gunicorn | Servidor WSGI |
| pdfplumber | Parsing de PDF |

### Estrutura do Projeto

```
src/
├── api/v1/endpoints/
│   ├── cursos.py          # Endpoints de cursos
│   └── conta.py           # Endpoints de conta + histórico
├── core/
│   └── config.py          # Configurações, cliente Supabase
├── database/
│   ├── setup.py           # Gerenciador de migrações
│   ├── 000_create_usuarios.sql
│   ├── 001_create_historico_disciplinas.sql
│   └── 002_create_processamentos_historico.sql
├── repositories/
│   ├── cursos_db.py       # Consultas de cursos/disciplinas
│   ├── usuarios_db.py     # CRUD de usuários
│   ├── historico_db.py    # CRUD do histórico do usuário
│   └── processamento_db.py # Tracking de processamento assíncrono
├── services/
│   ├── grafos.py          # Transformação do grafo
│   ├── pdf_parsing.py     # Parsing de PDF
│   └── processamento.py   # Processamento assíncrono em background
└── utils/
    └── senha_servicos.py  # Hash de senhas
```

### Endpoints da API

| Endpoint | Método | Auth | Parâmetros | Descrição |
|----------|--------|------|------------|-------------|
| `/ping` | GET | - | - | Health check |
| `/api/v1/cursos/lista` | GET | - | `unidade` | Lista cursos da unidade |
| `/api/v1/cursos/disciplinas` | GET | - | `unidade`, `curso` | Get nós/links do grafo |
| `/api/v1/conta/criar` | POST | - | `email`, `senha` | Criar conta |
| `/api/v1/conta/login` | POST | - | `email`, `senha` | Login, retorna JWT |
| `/api/v1/conta/deletar` | DELETE | JWT | `email` | Deletar conta |
| `/api/v1/conta/alterar` | UPDATE | JWT | `email`, `senha_antiga`, `nova_senha` | Alterar senha |
| `/api/v1/conta/upload/historico` | POST | JWT | `arquivo` (PDF) | Upload de histórico (assíncrono) |
| `/api/v1/conta/processamento/<id>` | GET | JWT | - | Status do processamento |

### Esquema do Banco de Dados

**unidades:** id (uuid), nome (text)  
**cursos:** id, nome, id_unidade, duracao_ideal, duracao_minima, duracao_maxima  
**disciplinas:** id, codigo, nome, id_curso, semestre, obrigatoria, eletiva, livre, cred_aula, cred_trabalho, ch  
**requisitos:** id, id_disciplina, id_requisito  
**usuarios:** id (uuid), email (único), senha (hash)  
**historico_disciplinas:** id (serial), id_usuario (fk), codigo_disciplina (text), status (aprovada|cursando), created_at  
**processamentos_historico:** id (uuid), id_usuario (fk), status (processando|concluido|erro), resultado (jsonb), erro (text), created_at, updated_at

### Limitações Conhecidas

- Sem paginação
- Sem cache
- Nomes de curso/unidade devem corresponder exatamente