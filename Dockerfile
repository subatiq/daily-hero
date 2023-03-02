FROM python:3.10-slim-buster
ENV PYTHONUNBUFFERED 1

RUN pip3 install pipenv==2022.7.4

WORKDIR /app

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --deploy --clear --system --ignore-pipfile;

COPY ./src /app/src

ENTRYPOINT ["python", "-m", "src.api"]
