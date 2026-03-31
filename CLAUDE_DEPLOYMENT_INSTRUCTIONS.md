# Claude Deployment Instructions

Use this file when you want to ask an AI chat assistant like Claude to help you deploy this project.

## What This Project Is

This is a Python FastAPI project with:

- a backend API
- a simple frontend HTML page
- sample CSV files for reconciliation

## Important Architecture Detail

In the current codebase, the **frontend and backend are already connected in one FastAPI app**.

That means:

- backend API is served by FastAPI
- frontend HTML is also served by FastAPI at `/`
- the easiest deployment is to deploy them **together as one service**

Relevant files:

- Project root: `D:\OneLab\reconciler`
- Backend entry point: `D:\OneLab\reconciler\api\main.py`
- Frontend file: `D:\OneLab\reconciler\ui\index.html`
- Requirements: `D:\OneLab\reconciler\requirements.txt`
- Sample transactions CSV: `D:\OneLab\reconciler\data\transactions.csv`
- Sample settlements CSV: `D:\OneLab\reconciler\data\settlements.csv`

## Recommended Deployment Strategy

Ask Claude to help you deploy this as **one combined FastAPI service** on Render.

Why:

- simplest setup
- frontend and backend stay on the same domain
- no CORS setup needed
- current code already supports this structure

## Copy-Paste Prompt For Claude

Paste this entire prompt into Claude:

```text
I have a FastAPI project I want to deploy.

Project details:
- The project folder is: D:\OneLab\reconciler
- Backend entry point is: api/main.py
- Frontend file is: ui/index.html
- The frontend is served by FastAPI at GET /
- The backend exposes:
  - GET /
  - GET /health
  - GET /report
  - POST /reconcile
- Dependencies are in requirements.txt
- The app should be deployed so both frontend and backend work together

Important:
- This is not a separate React/Vue frontend
- The frontend is plain HTML/JS already served by FastAPI
- I want the easiest deployment path

Please help me deploy this project on Render as a single web service.

Use these expected commands:
- Build command: python -m pip install -r requirements.txt
- Start command: python -m uvicorn api.main:app --host 0.0.0.0 --port $PORT

Please give me:
1. exact step-by-step deployment instructions
2. what to click in Render
3. what to set as Root Directory
4. how to verify the deployment after it goes live
5. common mistakes to avoid
```

## If Your GitHub Repo Root Is Different

If your GitHub repository root is `D:\OneLab` and the app is inside `reconciler`, tell Claude this too:

```text
My GitHub repo root contains the folder reconciler/, and the actual app lives inside that folder. So the Root Directory in Render may need to be set to reconciler.
```

## Expected Deployment Settings

Claude should guide you toward settings like these:

- Platform: Render
- Service type: Web Service
- Environment: Python
- Root Directory: `reconciler` if the repository root is `D:\OneLab`
- Build Command:

```bash
python -m pip install -r requirements.txt
```

- Start Command:

```bash
python -m uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

- Health Check Path:

```text
/health
```

## How To Ask Claude To Verify Frontend And Backend

Paste this follow-up prompt after deployment:

```text
My app is now deployed. Help me verify both frontend and backend.

I want to confirm:
- the frontend page loads at /
- /health returns {"status":"ok"}
- /report returns sample reconciliation JSON
- the upload flow for /reconcile still works

Please tell me exactly what URLs and behaviors I should test.
```

## If You Want Separate Frontend And Backend Deployments

This project does **not** currently need separate deployments, but if you want Claude to help split them, use this prompt:

```text
I want to split this app into two deployments:
- backend on Render
- frontend on a static host like Netlify or Vercel

Current project details:
- backend is FastAPI
- frontend is plain HTML/JS in ui/index.html
- frontend currently calls relative API paths like /report and /reconcile

Please tell me what code changes are required to split deployment cleanly.

I expect you to cover:
1. CORS setup in FastAPI
2. replacing relative API calls with a configurable backend base URL
3. frontend deployment options
4. backend deployment settings
5. how to test the split deployment
```

## What Claude Should Understand About This Codebase

If Claude seems confused, give it this summary:

```text
This project is a monolithic FastAPI app that serves both the UI and the API.

Backend:
- api/main.py
- engine/loader.py
- engine/detectors.py
- engine/matcher.py

Frontend:
- ui/index.html

Data files:
- data/transactions.csv
- data/settlements.csv

Main endpoints:
- GET /
- GET /health
- GET /report
- POST /reconcile
```

## Best Prompt To Use

If you want just one clean message to Claude, use this:

```text
Help me deploy my FastAPI project to Render.

This project already serves both frontend and backend from the same FastAPI app, so I want a single-service deployment.

Project structure:
- api/main.py is the app entry point
- ui/index.html is the frontend served by GET /
- requirements.txt contains dependencies
- data/ contains sample CSV files used by /report

I want:
1. deployment steps
2. Render configuration values
3. Root Directory guidance
4. post-deploy verification steps
5. common deployment mistakes

Expected commands:
- Build: python -m pip install -r requirements.txt
- Start: python -m uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

## Final Recommendation

For this project, ask Claude to deploy **frontend and backend together as one FastAPI service** first.

Only ask for split frontend/backend deployment if you specifically need:

- a separate frontend domain
- static frontend hosting
- a more production-style architecture
