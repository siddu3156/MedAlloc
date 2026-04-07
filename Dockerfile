FROM python:3.10

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install numpy

# keep container alive (VERY IMPORTANT)
CMD ["tail", "-f", "/dev/null"]