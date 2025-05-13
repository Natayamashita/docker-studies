FROM python:3.6

LABEL maintainer="Aluno Cod3r <aluno@cod3r.com.br>"

ENV PYTHONUNBUFFERED=1

WORKDIR /worker

COPY . /worker

RUN pip install redis==2.10.5

ENTRYPOINT [ "python", "worker.py" ]
