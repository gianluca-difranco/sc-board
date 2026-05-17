# Usa un'immagine base di Python ufficiale (slim per ridurre le dimensioni)
FROM python:3.11-slim

# Imposta variabili d'ambiente:
# - PYTHONDONTWRITEBYTECODE: evita che Python scriva i file .pyc sul disco
# - PYTHONUNBUFFERED: assicura che l'output del log sia inviato direttamente al terminale senza bufferizzazione
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directory di lavoro all'interno del container
WORKDIR /app

# Installa le dipendenze di sistema necessarie per psycopg2 (driver PostgreSQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia il file dei requisiti e installa le dipendenze Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn whitenoise

# Copia tutto il contenuto del progetto nella directory /app del container
COPY . /app/

# Raccoglie i file statici per la produzione. 
# Nota: Whitenoise deve essere configurato in settings.py per servirli.
RUN python manage.py collectstatic --noinput || true

# Espone la porta 8080
EXPOSE 8080

# Rendi lo script di entrypoint eseguibile
RUN chmod +x /app/entrypoint.sh

# Comando per avviare l'applicazione.
CMD ["/app/entrypoint.sh"]
