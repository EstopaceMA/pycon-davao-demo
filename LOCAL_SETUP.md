# Local Development Setup

This guide shows you how to run the PyCon Davao Membership API locally using Supabase.

## Prerequisites

- Docker and Docker Compose installed
- Supabase account (free) - [Sign up here](https://supabase.com)

## Quick Start (5 minutes)

### Step 1: Create Supabase Project

1. Go to [https://supabase.com](https://supabase.com) and sign in
2. Click **"New Project"**
3. Fill in:
   - **Name**: `pycon-davao-membership`
   - **Database Password**: Create and save a strong password
   - **Region**: Choose closest to you
4. Click **"Create new project"**
5. Wait ~2 minutes for setup

### Step 2: Get Connection String

1. In Supabase dashboard, click **Settings** (gear icon)
2. Click **Database**
3. Find **"Connection string"** section
4. Copy the **URI** format
5. Replace `[YOUR-PASSWORD]` with your actual password
6. Add `?sslmode=require` at the end

**Example:**
```
postgresql://postgres:YourPassword123@db.xxxxx.supabase.co:5432/postgres?sslmode=require
```

### Step 3: Setup Environment File

```bash
# In the project directory
cp .env.example .env

# Edit .env file and paste your Supabase connection string
# DATABASE_URL=postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres?sslmode=require
```

### Step 4: Start the Application

```bash
# Build and start
docker-compose up --build

# Or in detached mode (runs in background)
docker-compose up -d --build
```

### Step 5: Test the API

Open your browser:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Create a test member:
```bash
curl -X POST http://localhost:8000/members/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@pycon.ph",
    "membership_type": "professional",
    "is_active": true
  }'
```

## Common Commands

```bash
# View logs
docker-compose logs -f web

# Restart application
docker-compose restart web

# Rebuild after code changes
docker-compose up --build

# Stop everything
docker-compose down

# Stop and start without rebuilding
docker-compose stop
docker-compose start
```
