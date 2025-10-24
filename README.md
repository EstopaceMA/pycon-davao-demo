# PyCon Davao Membership API (Demo)

A modern FastAPI REST API for managing PyCon Davao conference memberships with cloud-first architecture using Supabase (PostgreSQL) and Azure Container Apps.

## Features

- 🚀 **RESTful API** - Complete CRUD operations with FastAPI
- 📊 **Free Database** - Supabase PostgreSQL (500MB, unlimited requests)
- 🐳 **Docker Ready** - Single-container development setup
- ☁️ **Production Ready** - GitHub Actions CI/CD to Azure Container Apps
- 📖 **Interactive Docs** - Auto-generated Swagger UI and ReDoc
- 🔒 **Secure** - SSL/TLS connections, environment-based secrets

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- [Supabase account](https://supabase.com) (free tier)

### Setup (5 minutes)

1. **Create Supabase Project**
   - Sign up at [supabase.com](https://supabase.com)
   - Create a new project (takes ~2 minutes to provision)
   - Go to Project Settings → Database
   - Copy the connection string (use "Transaction Pooler" mode)

2. **Configure Environment**
   ```bash
   # Copy environment template
   cp .env.example .env

   # Edit .env and paste your Supabase connection string
   # DATABASE_URL=postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-us-west-1.pooler.supabase.com:6543/postgres
   ```

3. **Start the Application**
   ```bash
   docker-compose up -d

   # View logs
   docker-compose logs -f web

   # Stop
   docker-compose down
   ```

4. **Access the API**
   - **API Base**: http://localhost:8000
   - **Swagger UI**: http://localhost:8000/docs (interactive testing)
   - **ReDoc**: http://localhost:8000/redoc (clean documentation)

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/members/` | Create a new member |
| GET | `/members/` | List all members (with pagination) |
| GET | `/members/{id}` | Get member by ID |
| PUT | `/members/{id}` | Update member |
| DELETE | `/members/{id}` | Delete member |

### Try It Out

**Option 1: Interactive Swagger UI** (Recommended)
- Open http://localhost:8000/docs
- Click "Try it out" on any endpoint
- Fill in the request body and click "Execute"

**Option 2: Command Line**
```bash
# Create a member
curl -X POST http://localhost:8000/members/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Juan",
    "last_name": "Dela Cruz",
    "email": "juan@pycon.ph",
    "membership_type": "professional",
    "is_active": true
  }'

# Get all members
curl http://localhost:8000/members/

# Get member by ID
curl http://localhost:8000/members/1

# Update member
curl -X PUT http://localhost:8000/members/1 \
  -H "Content-Type: application/json" \
  -d '{"membership_type": "speaker"}'

# Delete member
curl -X DELETE http://localhost:8000/members/1
```

**Option 3: Supabase Dashboard**
- Visit https://supabase.com/dashboard
- Select your project → Table Editor
- View and edit the `members` table directly

## Project Structure

```
.
├── app/
│   ├── main.py          # FastAPI application & endpoints
│   ├── models.py        # SQLAlchemy database models
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── crud.py          # Database operations
│   └── database.py      # Database configuration
├── .github/
│   └── workflows/
│       └── azure-deploy.yml    # Azure deployment workflow
├── docker-compose.yml   # Docker setup (web app only)
├── Dockerfile          # Container image definition
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── AZURE_SETUP.md     # Azure deployment guide
└── LOCAL_SETUP.md     # Local development guide
```

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) | Latest |
| **Database** | [Supabase PostgreSQL](https://supabase.com) | 15 |
| **ORM** | SQLAlchemy | 2.0+ |
| **Validation** | Pydantic | v2 |
| **Server** | Uvicorn (ASGI) | Latest |
| **Container** | Docker & Docker Compose | Latest |
| **Cloud Hosting** | Azure Container Apps | Latest |
| **Cloud Database** | Supabase (free tier) | Latest |
| **CI/CD** | GitHub Actions | Latest |
| **Registry** | DockerHub | Free |

**Architecture Pattern**: Layered architecture with strict separation of concerns (Presentation → Validation → Repository → ORM → Data)

## Cloud Deployment to Azure

### Production Setup (10 minutes total)

Deploy to production with GitHub Actions automated CI/CD:

| Step | Task | Time | Cost |
|------|------|------|------|
| 1 | [Create Supabase project](SUPABASE_QUICKSTART.md) |
| 2 | [Setup Azure Container Apps](AZURE_SETUP.md) | 5 min |
| 3 | [Configure GitHub secrets](.github/SECRETS_SETUP.md) |
| 4 | Push to `main` branch |

### Deployment Architecture

```
GitHub Push → GitHub Actions → Build Docker Image → Push to DockerHub
                    ↓
              Deploy to Azure Container Apps (with secrets)
                    ↓
              Connect to Supabase PostgreSQL (SSL)
                    ↓
              Production API Ready 🚀
```

## Development

### Local Setup (without Docker)

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Configure environment (option A: export)
export DATABASE_URL="postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-us-west-1.pooler.supabase.com:6543/postgres"

# 2. Configure environment (option B: .env file - recommended)
cp .env.example .env
# Edit .env with your Supabase connection string

# 3. Run with hot reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

See [LOCAL_SETUP.md](LOCAL_SETUP.md) for detailed setup instructions.

## Testing

### Interactive Testing (Recommended)

**Swagger UI**: http://localhost:8000/docs
- Try out all endpoints with a user-friendly interface
- Auto-filled request examples
- See responses in real-time

**Supabase Dashboard**: https://supabase.com/dashboard
- **Table Editor** - View and edit data with spreadsheet-like interface
- **SQL Editor** - Run custom SQL queries
- **Database Logs** - Monitor queries and performance
- **API Logs** - Track API requests to your database

## Architecture

This project follows a **5-layer architecture pattern** with strict separation of concerns:

1. **Presentation Layer** (`app/main.py`) - FastAPI route handlers
2. **Validation Layer** (`app/schemas.py`) - Pydantic request/response models
3. **Repository Layer** (`app/crud.py`) - Database operations
4. **ORM Layer** (`app/models.py`) - SQLAlchemy database models
5. **Data Layer** (`app/database.py`) - Database connection & session management

**Benefits:**
- Clean code organization
- Easy to test each layer independently
- Simple to add new features
- Clear data flow from HTTP request to database

## Contributing

This is a demo project for PyCon Davao. Feel free to fork and customize for your own use!

**Key Technologies to Learn:**
- [FastAPI](https://fastapi.tiangolo.com/tutorial/) - Modern Python web framework
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) - SQL toolkit and ORM
- [Supabase](https://supabase.com/docs) - Open source Firebase alternative
- [Azure Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/) - Serverless containers

## License

MIT License - See LICENSE file for details

---

Built with ❤️ by [anth.dev](https://web.facebook.com/AnthDotDev/) for [PyCon Davao](https://pycon-davao.durianpy.org/) | [Report Issues](https://github.com/EstopaceMA/pycon-davao-demo/issues)
