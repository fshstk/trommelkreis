FROM ghcr.io/astral-sh/uv:trixie-slim
RUN apt-get update && apt-get install -y build-essential curl libmariadb-dev pkg-config

RUN useradd --create-home --shell /usr/bin/bash trommelkreis
USER trommelkreis
WORKDIR /home/trommelkreis/app

# Copy deps first and cache layer:
COPY --chown=trommelkreis pyproject.toml uv.lock ./
RUN uv sync

# Copy rest of app:
COPY --chown=trommelkreis . .
RUN uv run collectstatic

HEALTHCHECK CMD curl -f http://localhost:8000/archiv/sessions
ENTRYPOINT ["uv", "run", "start"]
