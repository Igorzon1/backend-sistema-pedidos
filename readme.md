# 🛡️ Robust FastAPI — API Resiliente, Testada e Monitorada com MongoDB

Projeto desenvolvido com o objetivo de demonstrar **boas práticas de desenvolvimento backend em Python**, utilizando **FastAPI**, **MongoDB**, **testes automatizados**, e **tratamento estruturado de erros e logs**.

A API simula um sistema real de **cadastro de usuários**, **criação de pedidos**, **upload de arquivos**, e **integrações externas** com tratamento de falhas — tudo dentro de um modelo de arquitetura robusto e preparado para ambientes reais.

---

## 🚀 Tecnologias Utilizadas

| Camada | Tecnologias |
|--------|--------------|
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) |
| **Banco de Dados** | [MongoDB](https://www.mongodb.com/) (driver motor) |
| **Testes** | Pytest + HTTPX (testes assíncronos) |
| **Logs & Monitoramento** | logging, logger customizado e alertas (core/monitor.py) |
| **Validações** | Pydantic Models & Settings |
| **Container (opcional)** | Docker |

---

## 🧩 Estrutura do Projeto

```
Robust-FastApi/
├── src/
│   ├── app/
│   │   ├── api/              # Rotas da aplicação
│   │   │   ├── users.py
│   │   │   ├── orders.py
│   │   │   └── uploads.py
│   │   ├── core/             # Configurações e componentes centrais
│   │   │   ├── config.py     # Variáveis do .env
│   │   │   ├── db.py         # Conexão MongoDB
│   │   │   ├── logger.py     # Sistema de logs estruturados
│   │   │   └── monitor.py    # Sistema de alerta para erros críticos
│   │   ├── models/           # Schemas e modelos Pydantic
│   │   ├── services/         # Integração externa simulada (ex: pagamento)
│   │   └── main.py           # Ponto de entrada da API
│   ├── tests/                # Testes automatizados com pytest
│   │   ├── conftest.py       # Fixtures da API e banco fake
│   │   ├── test_users.py
│   │   ├── test_orders.py
│   │   └── test_uploads.py (opcional)
│   └── .env                  # Configurações do ambiente
├── requirements.txt
└── README.md
```

---

## ⚙️ Instalação e Execução

### 1️⃣ Clonar o projeto

```bash
git clone https://github.com/seuusuario/robust-fastapi.git
cd robust-fastapi
```

### 2️⃣ Criar ambiente virtual

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar variáveis de ambiente

Crie o arquivo `src/.env` com o conteúdo sugerido:

```
MONGO_URI=mongodb://localhost:27017/robustdb
LOG_LEVEL=INFO
```

**Dica (MongoDB via Docker):**
```bash
docker run -d --name robust-mongo -p 27017:27017 mongo:6.0
```

### 5️⃣ Iniciar o servidor

```bash
cd src
uvicorn app.main:app --reload --port 8000
```

Acesse:
- **Swagger:** http://127.0.0.1:8000/docs
- **Health Check:** http://127.0.0.1:8000/health

---

## 🧪 Executando os Testes

Os testes utilizam **pytest** e **httpx.AsyncClient**, simulando requisições reais à API.

### Antes de rodar:

**PowerShell (Windows):**
```powershell
$env:PYTHONPATH="src"
```

**Linux/Mac:**
```bash
export PYTHONPATH=src
```

### Rodar testes:

```bash
pytest -q
```

### Exemplos do que é testado:

- ✔ Criação de usuários
- ✔ Evitar duplicidade de e-mail
- ✔ Criação de pedidos + mock de pagamento
- ✔ Falha simulada no serviço externo
- ✔ Logs e respostas corretas da API

---

## 🧰 Recursos de Robustez Implementados

### ✔ Health Check Inteligente

O endpoint `/health` verifica:
- Conexão com o MongoDB
- Status geral da API
- Retorna 503 automaticamente se o banco falhar

### ✔ Tratamento Global de Exceções

Nenhuma exceção "vaza". Tudo passa por um handler global que:
- Registra erro detalhado no log
- Envia alerta via `monitor.py`
- Retorna JSON amigável para o cliente

### ✔ Logs Estruturados (JSON-like)

Tudo é registrado com:
- Nível (INFO / WARNING / ERROR)
- Rota
- Método HTTP
- Mensagem contextual

Arquivo gerado: `robust.log`

### ✔ Integração externa simulada

O serviço `payment_client.py` emula uma API real:
- Sucesso
- Falha
- Tempo de resposta
- Mocks para testes

### ✔ Testes Automatizados

Cobrem:
- Regras de negócio
- Falhas simuladas
- Idempotência
- Comportamento assíncrono
- Response codes + payload

---

## 📈 Próximos Passos

- Adicionar testes para upload de arquivos
- Criar índice único (email) no MongoDB
- Dockerfile + docker-compose (API + Mongo + Logs)
- Middleware para correlação de requisições (Request ID)
- Rate limiting (limitar requisições suspeitas)
- Exportar logs em formato OpenTelemetry

---

## 🧠 Intuito do Projeto

Criar uma API robusta, resiliente e testada, ideal para:
- Portfolio profissional
- Estudo de boas práticas
- Simulação de ambientes reais de backend

---

## 👨‍💻 Autor

**Igorzon**  
Desenvolvedor Python — Backend & APIs

---

## 🧭 Licença

Uso livre para fins de aprendizado e portfólio.