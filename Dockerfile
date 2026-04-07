FROM python:3.9-slim

WORKDIR /app

COPY . /app

# The baseline depends only on standard libraries, but we might want useful extensions.
# Since OpenEnv usually deals with numpy or RL stuff, we install some basics.
RUN pip install --no-cache-dir numpy

CMD ["python", "inference.py", "--all"]
