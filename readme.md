## Propósito
Este proyecto es una solución diseñada para facilitar la gestión, búsqueda y organización de documentos. Este proyecto permite a los usuarios indexar documentos tanto de Google Drive como de OneDrive y realizar búsquedas avanzadas utilizando filtros y consultas vectoriales. Resuelve el problema de encontrar información relevante en grandes volúmenes de datos de manera eficiente.

## Características
- **Indexación de documentos**: Soporte para múltiples formatos como PDF, DOCX, XLSX, PPTX, TXT, e imágenes.
- **Búsqueda avanzada**: Filtros por nombre, extensión, tamaño, fechas y consultas vectoriales.
- **Integración en la nube**: Sincronización con Google Drive y OneDrive.
- **Procesamiento de texto**: Permite extracción de texto para múltiples formatos como PDF, DOCX, XLSX o PPTX.
- **Interfaz intuitiva**: Frontend moderno construido con Next.js.
- **Base de datos híbrida**: PostgreSQL para datos estructurados y Qdrant para búsquedas vectoriales.

## Instalación
1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/hackudc.git
   cd hackudc

2. **Configura los archivos .env**:
    En postgresql/.env:
    POSTGRES_USER=usuario
    POSTGRES_PASSWORD=contraseña
    POSTGRES_DB=base_de_datos

    En backend/.env:
    # Google OAuth
    GOOGLE_CLIENT_ID=<your_google_client_id>
    GOOGLE_CLIENT_SECRET=<your_google_client_secret>
    GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

    # Microsoft OAuth
    MICROSOFT_CLIENT_ID=<your_microsoft_client_id>
    MICROSOFT_TENANT_ID=<your_microsoft_tenant_id>
    MICROSOFT_REDIRECT_URI=http://localhost:8000/auth/microsoft/callback
    MICROSOFT_CLIENT_SECRET=<your_microsoft_client_secret>

    # Postgres
    POSTGRES_USER=<postgres_user>
    POSTGRES_PASSWORD=<postgres_password>
    POSTGRES_DB=<postgres_database>

    # Gemini
    GEMINI_API_KEY=<your_gemini_api_key>

3. **Construye las imágenes Docker:**
    bash launch.sh

4. **Accede a la aplicación:**
    - Frontend: http://localhost:3000
    - Backend API: http://localhost:8000

## Uso
### Ejemplo de búsqueda exacta
1. Accede al frontend en http://localhost:3000.
2. Introduce un término de búsqueda en la barra de búsqueda.
3. Aplica filtros avanzados como extensión, tamaño o fechas.
4. Haz clic en "Buscar" para obtener resultados.

### Ejemplo de búsqueda vectorial
1. Escribe una consulta en lenguaje natural en la barra de búsqueda.
2. Haz clic en "Buscar" para obtener documentos relevantes basados en similitud semántica.

## Configuración
- Google Drive: Configura las credenciales de la API de Google en el archivo .env del backend.
- OneDrive: Configura las credenciales de la API de Microsoft en el archivo .env del backend.
- Base de datos: PostgreSQL y Qdrant deben estar configurados correctamente en sus respectivos contenedores.

## Compatibilidad
    - Frontend: Compatible con navegadores modernos (Chrome, Firefox, Edge).
    - Backend: Requiere Python 3.11 y Docker.
    - Bases de datos: PostgreSQL 16 y Qdrant.

## Solución de problemas
### Error de conexión a la base de datos:
    1. Verifica que los contenedores de PostgreSQL y Qdrant estén en ejecución.
    2. Asegúrate de que las credenciales en .env sean correctas.
### Problemas con OCR:
    1. Asegúrate de que tesseract-ocr esté instalado en el contenedor del backend.
### Errores de sincronización con Google Drive o OneDrive:
    1. Verifica que los tokens de acceso sean válidos y que las credenciales estén configuradas correctamente.

## Canales de soporte
    - Correo electrónico: monterrosocernadasizan@gmail.com
    - Issues en GitHub: https://github.com/x-nunez/hackudc/issues
    - Documentación oficial: Consulta los archivos [CONTRIBUTING.md] (https://github.com/x-nunez/hackudc/blob/main/CONTRIBUTING.md) y [CODE_OF_CONDUCT.md] (https://github.com/x-nunez/hackudc/blob/main/CODE_OF_CONDUCT.md) para más detalles.