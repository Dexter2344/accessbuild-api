# AccessBuild API

AI-powered accessibility audit tool for mobile apps.

## The Problem
100% of Nigerian banking apps are completely inaccessible to visually impaired users. Millions are locked out of essential services.

## What It Does
Accepts a list of UI elements from any mobile app and returns an accessibility score from A to F.

## Scoring
- A: 90%+ labeled. Fully accessible.
- B: 70-89% labeled. Mostly accessible.
- C: 50-69% labeled. Needs work.
- D: 25-49% labeled. Mostly inaccessible.
- F: Below 25% labeled. Completely inaccessible.

## Endpoints
- GET / — Health check
- POST /audit — Submit UI elements for scoring
- GET /grades — Get grading system explanation

## Deploy
Hosted on Render. Free tier.