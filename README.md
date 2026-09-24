# AccessBuild API

AI-powered accessibility audit tool for mobile apps.

## The Problem
100% of Nigerian banking apps are completely inaccessible to visually impaired users.

## Endpoints
- `GET /` — Health check
- `POST /audit` — Manual audit from element list
- `POST /scan` — Auto-scan from Android UI tree XML
- `GET /audits/recent` — Recent audits
- `GET /stats` — Aggregate statistics
- `GET /grades` — Grading system explanation

## Scoring
- A: 90%+ labeled. Fully accessible.
- B: 70-89% labeled. Mostly accessible.
- C: 50-69% labeled. Needs work.
- D: 25-49% labeled. Mostly inaccessible.
- F: Below 25% labeled. Completely inaccessible.

## Environment Variables
- `SUPABASE_URL`
- `SUPABASE_KEY`

## Deploy
Hosted on Render. Free tier.
