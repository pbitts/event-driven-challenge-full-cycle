FROM python:3.11-slim

RUN python -m pip install --upgrade pip

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

RUN rm /app/requirements.txt

COPY src/ app/

WORKDIR /app

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3003"]
