FROM python:3.10

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install numpy fastapi uvicorn

CMD ["python", "inference.py", "--all"]