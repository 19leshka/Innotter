FROM python:3.10

WORKDIR app/

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential libpq-dev

RUN apt install -y netcat
# System deps:
RUN pip install "poetry==1.2.2"

# Copy only requirements to cache them in docker layer
COPY poetry.lock pyproject.toml ./

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]