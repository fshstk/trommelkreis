FROM nikolaik/python-nodejs:python3.12-nodejs23 AS develop
USER pn
EXPOSE 8000
ENTRYPOINT ["bash"]

FROM develop AS deploy
WORKDIR /home/pn/app
COPY --chown=pn . .
RUN npm ci
ENTRYPOINT ["npm", "start"]
