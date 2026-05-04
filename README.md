# Tokenizer util
just a util to load any tokenizer(dummy or from HF or ...) and use it for chuncking and tokenizing

## what you must add to docker file
```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy tokenizer archive
COPY tokenizers.tar.gz .

# Extract tokenizers
RUN mkdir -p /app/tokenizers && \
    tar -xzf tokenizers.tar.gz -C /app/tokenizers

# Set env so code knows where to look
ENV TOKENIZER_DIR=/app/tokenizers

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```