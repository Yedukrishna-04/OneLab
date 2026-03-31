# Deployment Guide

This file explains how to deploy the OneLab payments reconciler project.

## Recommended Option

Use **Render** for deployment. It works well for a small FastAPI app and does not require changing the project structure.

## Project Location

The app code is inside:

- [reconciler](D:/OneLab/reconciler)

Important:

- If your Git repository root is `D:\OneLab`, then the **Root Directory** in Render should be `reconciler`
- If you upload only the `reconciler` folder as the repo root, then the Root Directory can be left empty

## Files Used In Deployment

- API entry point: [main.py](D:/OneLab/reconciler/api/main.py)
- Requirements: [requirements.txt](D:/OneLab/reconciler/requirements.txt)
- Health endpoint: [main.py](D:/OneLab/reconciler/api/main.py#L29)

## Local Run Before Deployment

Install dependencies:

```powershell
cd D:\OneLab\reconciler
python -m pip install -r requirements.txt
```

Run locally:

```powershell
cd D:\OneLab\reconciler
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Verify locally:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/report`

## Deploy To Render

### 1. Push the project to GitHub

Push either:

- the full `D:\OneLab` folder as a repository, or
- the `D:\OneLab\reconciler` folder as its own repository

### 2. Create a new Web Service in Render

In Render:

1. Sign in to https://render.com
2. Click `New`
3. Click `Web Service`
4. Connect your GitHub repository
5. Select the repository that contains this project

### 3. Configure the service

Use these settings:

- **Environment**: `Python 3`
- **Root Directory**: `reconciler` if your repo root is `D:\OneLab`
- **Build Command**:

```bash
python -m pip install -r requirements.txt
```

- **Start Command**:

```bash
python -m uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

### 4. Optional settings

Recommended:

- **Health Check Path**: `/health`
- **Auto Deploy**: enabled

### 5. Deploy

Click `Create Web Service`.

Render will:

- install dependencies from `requirements.txt`
- start the FastAPI app using `uvicorn`
- expose a public URL

## How To Verify After Deployment

Once deployed, test these URLs:

- `https://your-render-url/`
- `https://your-render-url/health`
- `https://your-render-url/report`

Expected results:

- `/` should load the upload UI
- `/health` should return `{"status":"ok"}`
- `/report` should return JSON with sample reconciliation results

## What To Include In Submission

After deployment, include:

- the deployed Render URL
- a demo video showing the app working
- the project zip

## Troubleshooting

### Problem: App starts locally but fails on Render

Check:

- the Root Directory is correct
- the Build Command uses `requirements.txt`
- the Start Command includes `--host 0.0.0.0 --port $PORT`

### Problem: Browser opens but page is blank

Check:

- the app root endpoint `/` is reachable
- [index.html](D:/OneLab/reconciler/ui/index.html) exists
- the deployment logs do not show import errors

### Problem: `/report` fails

Check:

- [transactions.csv](D:/OneLab/reconciler/data/transactions.csv) exists
- [settlements.csv](D:/OneLab/reconciler/data/settlements.csv) exists
- the project was deployed with the full `reconciler` folder contents

## Alternative Platforms

If you deploy somewhere other than Render, keep the same startup command pattern:

```bash
python -m uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

This works for most Python app hosting platforms such as Railway and similar services.
