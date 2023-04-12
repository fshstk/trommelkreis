################################################################################
# Base Setup
################################################################################

FROM nikolaik/python-nodejs:python3.10-nodejs17

USER pn
WORKDIR /home/pn/app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/pn/.local/bin:/home/pn/app/node_modules/.bin:${PATH}"

EXPOSE 5000
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5000", "trommelkreis.wsgi"]


################################################################################
# Python / Node
################################################################################

RUN pip install --no-cache-dir poetry==1.4.2
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt | pip install -r /dev/stdin

COPY package.json package-lock.json ./
RUN npm ci


################################################################################
# Django
################################################################################

COPY --chown=pn . .

RUN python manage.py collectstatic --noinput \
    && python manage.py compress --force
