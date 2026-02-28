# hackudc - Docker deployment guide

This project runs with 4 containers:

- `postgresql` (database)
- `qdrant` (vector database)
- `backend` (FastAPI on port `8000`)
- `frontend` (Next.js on port `3000`)

## Prerequisites

- Docker and Docker Compose/Engine installed (Docker Desktop on macOS is fine)
- Ports available: `3000`, `5432`, `6333`, `8000`

## 1) Configure environment files

Create a `.env` file inside `postgresql/`:

```env
POSTGRES_USER=<postgres_user>
POSTGRES_PASSWORD=<postgres_password>
POSTGRES_DB=<postgres_database>
```

Create a `.env` file inside `backend/`:

```env
POSTGRES_USER=<postgres_user>
POSTGRES_PASSWORD=<postgres_password>
POSTGRES_DB=<postgres_database>

GOOGLE_CLIENT_ID=<google_client_id>
GOOGLE_CLIENT_SECRET=<google_client_secret>
GOOGLE_REDIRECT_URI=<google_redirect_uri>

# Optional (defaults are used if omitted)
POSTGRES_PORT=<postgres_port>
QDRANT_PORT=<qdrant_port>
```

## 2) Build images

Run from the project root:

```bash
cd qdrant
# qdrant uses official image; no build required

cd ../postgresql
./buildImage.sh

cd ../backend
./buildImage.sh

cd ../frontend
./buildImage.sh
```

## 3) Deploy (run) containers

Start in this order (from project root):

```bash
cd qdrant
./startContainer.sh

cd ../postgresql
./startContainer.sh

cd ../backend
./startContainer.sh

cd ../frontend
./startContainer.sh
```

This creates/uses the Docker network `hackudc-net` and exposes:

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- PostgreSQL: `localhost:5432`
- Qdrant: `http://localhost:6333`

## 4) Access the web portal

Open:

```text
http://localhost:3000
```

The frontend calls the backend on `http://localhost:8000`.

## Useful commands

Check running containers:

```bash
docker ps
```

View logs:

```bash
docker logs -f frontend-hudc
docker logs -f backend-hudc
docker logs -f postgres-hudc
docker logs -f qdrant
```

Stop containers:

```bash
docker stop frontend-hudc backend-hudc postgres-hudc qdrant
```

Remove containers:

```bash
docker rm frontend-hudc backend-hudc postgres-hudc qdrant
```

If you need a clean PostgreSQL start (deletes DB data):

```bash
docker volume rm pgdata
```
