# Dockerfile
FROM python:3.11-slim

# Instala dependências do sistema (ex: build para torch/docling)
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Cria diretório da app
WORKDIR /app

# Copia arquivos
COPY . /app

# Instala dependências Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expõe a porta da API
EXPOSE 8000

# Comando para rodar a API FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
