FROM nikolaik/python-nodejs:python3.12-nodejs23 AS develop
ARG POETRY_VERSION=1.8.5
USER pn
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/pn/.local/bin:/home/pn/app/node_modules/.bin:${PATH}"
EXPOSE 8000
RUN pip install --no-cache-dir poetry==${POETRY_VERSION}
ENTRYPOINT ["bash"]

FROM develop AS deploy
WORKDIR /home/pn/app
COPY --chown=pn . .
RUN npm ci
ENTRYPOINT ["npm", "start"]
