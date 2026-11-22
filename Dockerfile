# PyBank Core Transaction Engine
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements-dev.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .

# Run test suite verifying thread-safety and ledger integrity
CMD ["pytest", "-v"]
