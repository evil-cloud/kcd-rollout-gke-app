# Etapa de construcción
FROM python:3.9-slim AS builder

WORKDIR /app

# Crear usuario no root
RUN groupadd -g 3000 app && useradd -m -u 10001 -g 3000 --no-log-init app

# Copiar dependencias y instalar en una ubicación temporal
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Etapa final
FROM python:3.9-slim

WORKDIR /app

# Crear usuario no root en la imagen final
RUN groupadd -g 3000 app && useradd -m -u 10001 -g 3000 --no-log-init app

# Copiar librerías instaladas desde el builder
COPY --from=builder /install /usr/local

# Copiar código fuente
COPY src /app/src

# Agregar la variable de entorno PYTHONPATH
ENV PYTHONPATH=/app/src

# Usar usuario no root
USER app

# Exponer el puerto de la aplicación
EXPOSE 8000

# Comando de ejecución de FastAPI con Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]