# Azure Deployment Setup Guide

This guide explains how to deploy the PyCon Davao Membership API to Azure using Container Apps and Supabase (PostgreSQL).

## Prerequisites

- Azure CLI installed: `brew install azure-cli` (macOS) or [download](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- Azure subscription
- GitHub repository with this code
- DockerHub account (free) - [Sign up here](https://hub.docker.com/signup)
- Supabase account (free) - [Sign up here](https://supabase.com)

## Supabase Database Setup

### 1. Create Supabase Project

1. Go to [https://supabase.com](https://supabase.com) and sign in
2. Click **"New Project"**
3. Fill in the details:
   - **Name**: `pycon-davao-membership`
   - **Database Password**: Create a strong password (save this!)
   - **Region**: Choose closest to your Azure region (e.g., East US)
   - **Pricing Plan**: Free tier (includes 500MB database, 2GB bandwidth)
4. Click **"Create new project"**
5. Wait for the project to finish setting up (~2 minutes)

### 2. Get Database Connection String

1. In your Supabase project dashboard, click **"Project Settings"** (gear icon)
2. Click **"Database"** in the left sidebar
3. Scroll down to **"Connection string"**
4. Select **"URI"** tab
5. Copy the connection string (it looks like this):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxxxxxxxxx.supabase.co:5432/postgres
   ```
6. Replace `[YOUR-PASSWORD]` with your actual database password
7. Add `?sslmode=require` to the end of the URL
8. Save this as your `SUPABASE_CONNECTION_STRING`

**Example:**
```bash
SUPABASE_CONNECTION_STRING="postgresql://postgres:your-password@db.abcdefghijklmnop.supabase.co:5432/postgres?sslmode=require"
```

### 3. (Optional) Initialize Database Tables

The FastAPI application will automatically create tables on first run. However, you can also run SQL manually:

1. In Supabase dashboard, click **"SQL Editor"**
2. The tables will be created automatically by SQLAlchemy when the app starts

## Azure Resources Setup

### 1. Login to Azure

```bash
az login
```

### 2. Set Variables

```bash
# Resource naming
RESOURCE_GROUP="pycon-davao-rg"
LOCATION="eastus"
CONTAINER_APP_ENV="pycon-davao-env"
CONTAINER_APP_NAME="pycon-davao-api"
DOCKERHUB_USERNAME="your-dockerhub-username"  # Replace with your DockerHub username

# Supabase connection string (from step 2 above)
SUPABASE_CONNECTION_STRING="postgresql://postgres:your-password@db.xxxxx.supabase.co:5432/postgres?sslmode=require"
```

### 3. Create Resource Group

```bash
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION
```

### 4. Create Container Apps Environment

```bash
az containerapp env create \
  --name $CONTAINER_APP_ENV \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION
```

### 5. Create Container App

```bash
# Note: Initial image is a placeholder. GitHub Actions will deploy your actual image.
az containerapp create \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $CONTAINER_APP_ENV \
  --image mcr.microsoft.com/azuredocs/containerapps-helloworld:latest \
  --target-port 8000 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 3 \
  --cpu 0.5 \
  --memory 1Gi \
  --secrets database-url="$SUPABASE_CONNECTION_STRING" \
  --env-vars DATABASE_URL=secretref:database-url

# Get the app URL
APP_URL=$(az containerapp show \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn \
  --output tsv)

echo "Container App URL: https://$APP_URL"
```

## GitHub Secrets Configuration

Configure the following secrets in your GitHub repository (Settings → Secrets and variables → Actions):

### Required Secrets:

1. **DOCKERHUB_USERNAME**
   - Your DockerHub username
   - Example: `myusername`

2. **DOCKERHUB_TOKEN**
   - Create a token at [DockerHub Account Settings → Security](https://hub.docker.com/settings/security)
   - Click "New Access Token"
   - Give it a description like "GitHub Actions"
   - Copy the token (you'll only see it once!)

3. **AZURE_CREDENTIALS**
   ```bash
   # Create service principal
   SUBSCRIPTION_ID=$(az account show --query id --output tsv)

   az ad sp create-for-rbac \
     --name "pycon-davao-github-actions" \
     --role contributor \
     --scopes /subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP \
     --sdk-auth

   # Copy the entire JSON output to GitHub secret
   ```

4. **SUPABASE_CONNECTION_STRING**
   - Your Supabase PostgreSQL connection string from step 2 of Supabase setup
   - Format: `postgresql://postgres:your-password@db.xxxxx.supabase.co:5432/postgres?sslmode=require`
   - Get this from Supabase Dashboard → Project Settings → Database → Connection string (URI)

### Add Secrets to GitHub:

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret with its corresponding value

## Deployment

Once the secrets are configured, the deployment will trigger automatically on:
- Push to `main` branch
- Manual workflow dispatch

### Manual Deployment:

1. Go to **Actions** tab in GitHub
2. Select **Deploy to Azure Container Apps** workflow
3. Click **Run workflow**

## Verify Deployment

```bash
# Check container app status
az containerapp show \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query properties.runningStatus

# View logs
az containerapp logs show \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --follow

# Test the API
curl https://$APP_URL/
curl https://$APP_URL/docs
```

## Cleanup Resources
To avoid charges, delete the resource group when done:

```bash
az group delete --name $RESOURCE_GROUP --yes --no-wait
```

## Troubleshooting

### Check deployment logs:
```bash
az containerapp revision list \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --output table
```

### View application logs:
```bash
az containerapp logs show \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --tail 100
```

## Additional Resources

- [Azure Container Apps Documentation](https://docs.microsoft.com/en-us/azure/container-apps/)
- [Azure Database for PostgreSQL](https://docs.microsoft.com/en-us/azure/postgresql/)
- [GitHub Actions for Azure](https://github.com/Azure/actions)