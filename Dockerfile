#Pull base image
FROM python:3.8-slim

###########################################################################
# User Aliases
###########################################################################
USER root

ARG PUID=1000
ENV PUID ${PUID}
ARG PGID=1000
ENV PGID ${PGID}

# Añadir user devuser como non-root. Si todo se ejecuta como usuario root,
# los archivos no son modificables desde el host
RUN groupadd -g ${PGID} devuser && \
  useradd -u ${PUID} -g devuser -m devuser && \
  usermod -p "*" devuser -s /bin/bash 

WORKDIR /app/src

COPY Pipfile Pipfile.lock /app/
RUN pip install --upgrade pip \
    && pip install pipenv \ 
    && pipenv install --system \
    && rm -rf /root/.cache \
    && chown -R devuser:devuser /app

COPY . /app/
