FROM ghcr.io/astral-sh/uv:trixie-slim
RUN apt-get update && apt-get install -y build-essential curl libmariadb-dev pkg-config \
  && useradd --create-home --shell /usr/bin/bash trommelkreis

USER trommelkreis
WORKDIR /home/trommelkreis/app

# Copy deps first and cache layer:
COPY --chown=root:root --chmod=755 pyproject.toml uv.lock ./
RUN uv sync

# Copy rest of app:
COPY --chown=root:root --chmod=755 . .
RUN uv run collectstatic

HEALTHCHECK CMD curl -f http://localhost:8000/archiv/sessions
ENTRYPOINT ["uv", "run", "start"]
