# AgentImmo

## Objectif

AgentImmo est une application permettant aux promoteurs immobiliers d’analyser la pertinence d’un emplacement pour un projet immobilier en France. L'application doit :

- Collecter des données publiques : API DVF, API INSEE, Open Data locales.
- Analyser la concurrence et le marché : prix, typologie, projets existants.
- Générer des visualisations : graphes, cartes interactives.
- Produire un rapport PDF complet avec tous les résultats.

## Stack

- Backend : Python + FastAPI
- Workflow agentique : LangGraph
- Observabilité : LangSmith
- Frontend : Svelte + TailwindCSS
- Formatter : Ruff
- Gestionnaire de dépendances : Poetry
- Stockage : PostgreSQL / PostGIS

## Agents LangGraph

| Agent              | Input                          | Output           |
| ------------------ | ------------------------------ | ---------------- |
| DataCollectorAgent | adresse: str                   | dataset: dict    |
| AnalyzerAgent      | dataset: dict                  | indicators: dict |
| VisualizerAgent    | indicators: dict               | images: dict     |
| ReportBuilderAgent | indicators: dict, images: dict | rapport: PDF     |

## API

- POST `/analyze` : lance le workflow pour une adresse
- GET `/status/{workflow_id}` : état du workflow et résultats intermédiaires
- GET `/report/{workflow_id}` : récupère le PDF final

## Frontend

- Svelte + TailwindCSS
- Consomme les endpoints FastAPI
- Formulaire simple pour saisir une adresse et lancer l’analyse
- Affiche les résultats et les graphes interactifs, avec possibilité de télécharger le PDF

## Installation

### Prérequis

- Python 3.10+
- Poetry
- Node.js 18+ et npm

### Backend

1. Installer les dépendances avec Poetry :

```bash
poetry install
```

2. Configurer les variables d'environnement :

```bash
cp .env.example .env
# Éditer .env et configurer vos clés API (LangSmith, etc.)
```

3. Lancer le serveur FastAPI :

```bash
poetry run uvicorn backend.api.main:app --reload
```

L'API sera accessible sur `http://localhost:8000`

### Frontend

1. Installer les dépendances :

```bash
cd frontend
npm install
```

2. Configurer la clé API Mapbox :

Créez un fichier `.env` dans le dossier `frontend` avec votre clé d'accès Mapbox :

```bash
# Dans frontend/.env
VITE_MAPBOX_ACCESS_TOKEN=votre_clé_mapbox_ici
VITE_API_URL=http://localhost:8000
```

Pour obtenir une clé Mapbox :

- Créez un compte sur [https://account.mapbox.com/](https://account.mapbox.com/)
- Accédez à votre page d'accès (Access tokens)
- Copiez votre token public (commence par `pk.`)

3. Lancer le serveur de développement :

```bash
npm run dev
```

Le frontend sera accessible sur `http://localhost:5173`

## Utilisation

1. Accéder à l'interface web sur `http://localhost:5173`
2. Saisir une adresse dans le formulaire
3. Lancer l'analyse
4. Suivre la progression en temps réel
5. Télécharger le rapport PDF une fois l'analyse terminée

## Structure du projet

```
agent-immo/
├── backend/
│   ├── api/
│   │   ├── endpoints/     # Endpoints FastAPI
│   │   ├── models/        # Modèles Pydantic
│   │   └── main.py        # Application FastAPI
│   ├── agents/            # Agents LangGraph
│   ├── utils/             # Utilitaires (PDF, plotting)
│   ├── config.py          # Configuration
│   └── workflow.py        # Orchestrateur de workflow
├── frontend/              # Application Svelte
├── tests/                 # Tests unitaires
└── pyproject.toml         # Configuration Poetry
```

## Développement

### Formatage du code

Utiliser Ruff pour formater le code :

```bash
poetry run ruff format .
poetry run ruff check .
```

### Tests

Lancer les tests :

```bash
poetry run pytest
```

## Notes

- Les agents contiennent des stubs pour l'instant. L'implémentation complète des APIs externes (DVF, INSEE, Open Data) sera ajoutée ultérieurement.
- La configuration LangSmith est optionnelle mais recommandée pour le suivi des workflows.
