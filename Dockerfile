FROM python:3.10-slim-buster

WORKDIR /

COPY employee_service/ /employee_service
COPY pyproject.toml .
COPY poetry.lock .
COPY README.md .

RUN pip install poetry
RUN poetry install --no-dev

CMD ["poetry", "run", "python", "employee_service/main.py", "--is-testing"]
