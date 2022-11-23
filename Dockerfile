FROM python:3.10.8-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install 'poetry==1.2.2'
COPY pyproject.toml .
RUN poetry install --no-dev

COPY . app/

CMD [ "/app/entrypoint.sh" ]