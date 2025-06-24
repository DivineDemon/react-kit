# React Kit Monorepo

A **full-stack, type-safe monorepo** starter kit featuring a modern React frontend and an async Python FastAPI backend. This project is designed for rapid, scalable development with best practices for code quality, automation, and developer experience.

---

## Table of Contents

- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Backend Overview (`/backend`)](#backend-overview-backend)
  - [API Generation](#automatic-api-generation)
  - [Database & ORM](#database--orm)
  - [Linting & Formatting](#backend-linting--formatting)
  - [Environment Variables](#backend-environment-variables)
- [Frontend Overview (`/frontend`)](#frontend-overview-frontend)
  - [Routing](#routing)
  - [State Management](#state-management)
  - [API Integration & Type Safety](#api-integration--type-safety)
  - [Linting & Formatting](#frontend-linting--formatting)
- [Monorepo Tooling & Automation](#monorepo-tooling--automation)
  - [Pre-commit & Post-merge Hooks](#pre-commit--post-merge-hooks)
  - [Type Safety Across the Stack](#type-safety-across-the-stack)
- [Development Workflow](#development-workflow)
- [Special Features](#special-features)
- [FAQ](#faq)
- [Contributing](#contributing)

---

## Project Structure

```
react-kit/
│
├── backend/                # FastAPI backend (Python)
│   ├── app/                # Main backend application code
│   │   ├── core/           # Core config, DB, logger, etc.
│   │   ├── constants/      # Seed data and static files
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── routers/        # API route definitions
│   │   ├── schemas/        # Pydantic schemas for validation
│   │   ├── main.py         # FastAPI app entrypoint
│   │   └── ...             # Other backend modules
│   ├── requirements.txt    # Python dependencies
│   ├── .env                # Backend environment variables
│   └── ...                 # Lint config, cache, etc.
│
├── frontend/               # React frontend (TypeScript)
│   ├── src/                # Source code
│   │   ├── routes/         # Route components (file-based routing)
│   │   ├── store/          # Redux store & API services
│   │   ├── assets/         # Static assets (CSS, images)
│   │   └── main.tsx        # App entrypoint
│   ├── index.html          # HTML template
│   ├── package.json        # Frontend dependencies & scripts
│   ├── tsconfig*.json      # TypeScript configs
│   ├── vite.config.ts      # Vite build config
│   └── ...                 # Lint config, etc.
│
├── .husky/                 # Git hooks (pre-commit, post-merge, etc.)
├── README.md               # This file
└── ...
```

---

## Setup & Installation

### Prerequisites

- **Python 3.10+** (recommended: 3.12)
- **Node.js 18+** and **pnpm** (or npm/yarn)
- **PostgreSQL** (or your preferred DB, but defaults expect Postgres)
- **[Optional] Docker** for containerized development

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/react-kit.git
cd react-kit
```

### 2. Setup the Backend

```sh
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Edit .env for your DB and secrets
```

- **Database:** Ensure your `DATABASE_URL` in `.env` uses the async driver, e.g.:
  ```
  DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/reactkit
  ```

- **Seed Data:** The backend will auto-seed from `app/constants/seed_data.json` on first run.

### 3. Setup the Frontend

```sh
cd ../frontend
pnpm install
cp .env.example .env  # Set VITE_BASE_API_URL to your backend
```

### 4. Start Development Servers

- **Backend:**
  ```sh
  cd backend
  uvicorn app.main:app --reload
  ```
- **Frontend:**
  ```sh
  cd frontend
  pnpm run dev
  ```

---

## Backend Overview (`/backend`)

### FastAPI + SQLAlchemy + Pydantic

- **Async-first**: Uses `asyncpg` and SQLAlchemy's async engine for high concurrency.
- **Automatic API Generation**: All routers in `app/routers/` are auto-included.
- **Type-safe**: Pydantic v2 for request/response validation.
- **Seed Data**: On startup, seeds the database from `constants/seed_data.json` if empty.

#### Folder Details

- **`app/core/`**: Core utilities (DB, config, logger).
- **`app/models/`**: SQLAlchemy ORM models (e.g., `Item`).
- **`app/schemas/`**: Pydantic schemas for validation and serialization.
- **`app/routers/`**: All API endpoints (RESTful, modular).
- **`app/constants/`**: Static files and seed data.
- **`main.py`**: Entrypoint, includes all routers, sets up CORS, and runs DB init.

### Automatic API Generation

- All routers in `app/routers/` are auto-included in the FastAPI app.
- OpenAPI docs are available at `/docs` (Swagger) and `/redoc`.

### Database & ORM

- **SQLAlchemy** for ORM, with async support.
- **Seed logic**: On startup, checks for existing data and seeds if needed.

### Backend Linting & Formatting

- **Ruff** for linting (`ruff .`)
- **Black** for formatting (if configured)
- **Pre-commit hooks** ensure code quality before every commit.

### Backend Environment Variables

- `.env` file in `/backend` for secrets, DB URL, etc.
- Example:
  ```
  DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/reactkit
  JWT_SECRET_KEY=your-secret
  ```

---

## Frontend Overview (`/frontend`)

### React + TypeScript + Vite

- **File-based Routing**: Powered by [@tanstack/react-router](https://tanstack.com/router).
- **Redux Toolkit**: For state management and API queries.
- **Type-safe API Integration**: End-to-end types for API requests and responses.
- **Tailwind CSS**: For rapid, utility-first styling.
- **Vite**: Lightning-fast dev server and build.

#### Folder Details

- **`src/routes/`**: Route components, auto-registered.
- **`src/store/`**: Redux store, API services (RTK Query).
- **`src/assets/`**: Static assets (CSS, images).
- **`src/main.tsx`**: App entrypoint, sets up router and store.

### Routing

- File-based, zero-config routing with TanStack Router.
- Nested layouts and route-level code splitting.

### State Management

- **Redux Toolkit** for global state.
- **RTK Query** for API calls, with auto-caching and invalidation.

### API Integration & Type Safety

- **TypeScript** everywhere.
- **RTK Query** endpoints are typed.
- **Full-stack type safety**: Backend Pydantic schemas can be used to generate TypeScript types (see [Special Features](#special-features)).

### Frontend Linting & Formatting

- **ESLint** (with recommended and type-checked configs)
- **Prettier** for formatting
- **Pre-commit hooks** for code quality

---

## Monorepo Tooling & Automation

### Pre-commit & Post-merge Hooks

- Managed by **Husky** (`.husky/` directory)
- **Pre-commit**: Runs linting and formatting on staged files.
- **Post-merge**: Can auto-install dependencies or run migrations.
- Hooks are cross-platform and fast.

### Type Safety Across the Stack

- **Pydantic v2** on the backend for strict validation.
- **TypeScript** on the frontend.
- [Optional] Use tools like [datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator) or [openapi-typescript](https://github.com/drwpow/openapi-typescript) to generate TypeScript types from backend OpenAPI schemas for **end-to-end type safety**.

---

## Development Workflow

1. **Write code** in `/frontend` or `/backend`.
2. **Pre-commit hooks** ensure code is linted and formatted.
3. **Push/merge**: Post-merge hooks can run install or migration scripts.
4. **API changes**: Update backend schemas, regenerate frontend types if needed.
5. **Run tests** (add your own test setup for both frontend and backend).

---

## Special Features

- **Monorepo**: One repo, one install, one workflow for frontend and backend.
- **Automatic API docs**: FastAPI auto-generates OpenAPI docs.
- **Seed data**: Easily bootstrap your DB with initial data.
- **Full-stack type safety**: Reduce runtime bugs with strict types everywhere.
- **Modern tooling**: Vite, TanStack Router, RTK Query, Tailwind, FastAPI, SQLAlchemy, asyncpg.
- **Pre-configured linting/formatting**: Consistent codebase, enforced by hooks.
- **Easy environment management**: `.env` files for both frontend and backend.
- **CORS enabled**: Out-of-the-box support for frontend-backend communication.
- **Hot reload**: Both frontend and backend support instant reload on code changes.
- **Extensible**: Add more routers, models, or frontend routes as your app grows.

---

## FAQ

**Q: Can I use a different database?**  
A: Yes! Just update your `DATABASE_URL` and install the appropriate async driver.

**Q: How do I add a new API route?**  
A: Add a new file in `backend/app/routers/`, define your endpoints, and it will be auto-included.

**Q: How do I generate TypeScript types from my backend?**  
A: Use [openapi-typescript](https://github.com/drwpow/openapi-typescript) with your FastAPI OpenAPI schema.

**Q: How do I run tests?**  
A: Add your preferred test runner (e.g., pytest for backend, vitest/jest for frontend).

---

## Contributing

1. Fork the repo and create your branch.
2. Make your changes with clear, descriptive commits.
3. Ensure all linting and formatting checks pass.
4. Submit a pull request!

---

**Happy hacking!