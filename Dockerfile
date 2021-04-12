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

COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt

COPY --chown=pn package.json package-lock.json ./
RUN npm install


################################################################################
# Django
################################################################################

COPY --chown=pn . .

RUN python manage.py collectstatic --noinput \
    && python manage.py compress --force
