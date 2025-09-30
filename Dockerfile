FROM python:3.12-slim
WORKDIR /app

# Copiar requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar projeto
COPY . .

# Comando API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000