# Guía de Contribución

¡Gracias por tu interés en contribuir a este proyecto! Por favor, lea esta guía antes de comenzar a abrir Issues o realizar pull requests.

## Entorno de desarrollo

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

## Cómo contribuir

Para contribuir, por favor sigue estos pasos:

1. **Forkea el repositorio**: Haz un "fork" de este repositorio a tu cuenta de GitHub.
2. **Crea una rama**: Crea una nueva rama para tus cambios. Usa un nombre descriptivo para la rama (por ejemplo, `fix-bug-123` o `feature-add-login`).
3. **Haz tus cambios**: Realiza las modificaciones necesarias en tu rama para alcanzar el objetivo fijado.
4. **Escribe pruebas**: Escribe pruebas que permitan validar tus cambios.
5. **Haz un pull request**: Cuando estés listo para que tus cambios sean revisados, abre un pull request a la rama principal del repositorio.

## Reporte de errores (Issues)

Si encuentras un error o tienes una sugerencia, por favor abre un **issue** en el repositorio. Para ello:

1. Busca si el problema ya ha sido reportado.
2. Si no lo ha sido, abre un nuevo issue con una descripción detallada.

Asegúrate de proporcionar los siguientes detalles cuando sea posible:
- Descripción del error o sugerencia.
- Pasos para reproducir el error.
- Resultado esperado y actual.
- Entorno en el que fue encontrado el error (navegador,sistema operativo...).

## Normas de estilo

Por favor sigue las siguientes normas de estilo para asegurarte de que el código sea consistente:

- **Convenciones de nomenclatura**: Usa nombres de variables y funciones claros y descriptivos.
- **Comentarios**: Añade comentarios donde sea necesario para explicar por qué se hacen ciertos cambios y facilitar la revisión del pull request.

## Ejecución de tests

Por el momento el proyecto no tiene una suite de tests automatizados. Si estás añadiendo una funcionalidad importante, incluye los pasos de prueba manual en la descripción de tu pull request para que los revisores puedan verificar su comportamiento.

Cuando se añada una suite de tests, esta sección se actualizará con las instrucciones correspondientes.

## Proceso de Pull Request

1. **Crea la rama desde `main`** y usa un nombre descriptivo:
```bash
   git checkout -b fix/xlsx-none-error
   git checkout -b feat/microsoft-onedrive-sync
   git checkout -b docs/update-contributing
```

2. **Mantén los PRs enfocados** — una funcionalidad o fix por PR. Los PRs grandes son más difíciles de revisar y más propensos a introducir bugs.

3. **Rellena la descripción del PR** con:
   - Qué hace el cambio
   - Por qué es necesario
   - Cómo probarlo manualmente
   - Capturas de pantalla si hay cambios en la interfaz

4. **Asegúrate de que el proyecto sigue funcionando** antes de abrir el PR — construye los contenedores Docker y haz una prueba básica.

5. **Enlaza los issues relacionados** en la descripción del PR:
```
   Closes #12
   Related to #8
```

6. **No hagas force-push** a una rama que ya tiene un PR abierto — dificulta el seguimiento del historial de revisión.

## Commit conventions

Este proyecto sigue [Conventional Commits](https://www.conventionalcommits.org/).

### Formato

```
<type>(<scope>): <short description>
```

### Types

| Type | When to use |
|------|-------------|
| `fix` | A bug fix |
| `feat` | A new feature |
| `perf` | Performance improvement|
| `refactor` | Code change that is neither a fix nor a feature |
| `style` | Formatting, missing semicolons, etc — no logic change |
| `test` | Tests added/corrected |
| `docs` | Documentation changes only |
| `build` | Build Tools, dependencies, versions |
| `ops` | DevOps, infrastructure, or backups |
| `chore` | Build process, dependencies, config changes |

## Expectativas de revisión

### Para los contribuidores

- Sé receptivo al feedback — los comentarios de revisión son sobre el código, no sobre ti
- Responde a todos los comentarios, aunque sea solo para confirmar que los has visto
- Si no estás de acuerdo con una sugerencia, explica por qué — el debate es bienvenido
- Marca las conversaciones como resueltas una vez que las hayas atendido

### Para los revisores

- Revisa los PRs en un plazo de 2 días laborables cuando sea posible
- Sé específico y constructivo — explica qué cambiar y por qué
- Distingue entre problemas bloqueantes y sugerencias opcionales:
```
  # bloqueante
  Esto causará un KeyError si falta la extensión — necesita una comprobación.

  # sugerencia (opcional)
  nit: podrías simplificar esto con dict.get() en lugar de if/else
```
- Aprueba solo cuando estés seguro de que el cambio funciona y sigue los estándares del proyecto
- Se requiere al menos una aprobación antes de hacer merge

## Códigos de conducta

Este proyecto sigue un **Código de Conducta** para garantizar un entorno de trabajo inclusivo y respetuoso. Por favor, sigue las normas de conducta en tus interacciones.

Puedes leer el código de conducta completo aquí: [Código de Conducta](https://github.com/x-nunez/hackudc/blob/main/CODE_OF_CONDUCT.md).