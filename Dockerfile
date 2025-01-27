FROM python:3.11-slim

RUN apt update &&  apt install -y gcc git

RUN pip install poetry

RUN python -m venv /opt/.venv
ENV PATH="/opt/.venv/bin:$PATH" VIRTUAL_ENV="/opt/.venv"

RUN mkdir /app
COPY pyproject.toml poetry.lock /app/
WORKDIR /app

RUN poetry install

EXPOSE 8000

RUN mkdir /root/.ssh
RUN ln -s /run/secrets/ssh_key /root/.ssh/id_rsa
RUN ln -s /run/secrets/gitconfig /root/.gitconfig

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]