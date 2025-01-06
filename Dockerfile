FROM python:3.12 AS develop
ENV POETRY_HOME=/usr/local
RUN curl -sSL https://install.python-poetry.org | python
RUN useradd --create-home --shell /usr/bin/bash trommelkreis
USER trommelkreis
WORKDIR /home/trommelkreis/app
EXPOSE 8000
ENTRYPOINT ["bash"]

FROM develop AS deploy
COPY . .
RUN poetry install && poetry run collectstatic
ENTRYPOINT ["poetry", "run", "start"]
