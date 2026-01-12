# ============================
#            Builder
# ============================
FROM python:3.11-slim-bookworm AS builder

ENV DockerHOME=/home/app/webapp
WORKDIR $DockerHOME

# Install build deps (ONLY for building wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    default-libmysqlclient-dev \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf-2.0-dev \
    libffi-dev \
    pkg-config \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements first (cache optimization)
COPY requirements.txt .

RUN pip install --upgrade pip wheel \
 && pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels


# ============================
#          Runtime
# ============================
FROM python:3.11-slim-bookworm

ENV DockerHOME=/home/app/webapp
WORKDIR $DockerHOME

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install runtime-only deps (NO -dev)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    default-libmysqlclient-dev \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi8 \
    nano \
 && rm -rf /var/lib/apt/lists/*

# Install Python deps from wheels
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

# Copy project
COPY ./project $DockerHOME

# Create non-root user
RUN addgroup --system app && adduser --system --group app \
 && chown -R app:app $DockerHOME

USER app

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]
