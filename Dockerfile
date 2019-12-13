FROM openjdk:8-alpine

ENV DIGDAG_VERSION=0.9.39 \
    EMBULK_VERSION=0.9.18 \
    AWSCLI_VERSION=1.16.139 \
    BIND=0.0.0.0 \
    PORT=65432

WORKDIR /var/lib/digdag

COPY server.properties /etc/server.properties
COPY Gemfile Gemfile.lock ./

RUN apk add --no-cache curl && \
    curl -o /usr/bin/digdag --create-dirs -L "https://dl.digdag.io/digdag-$DIGDAG_VERSION" && \
    chmod +x /usr/bin/digdag && \
    apk del curl && \
    adduser -h /var/lib/digdag -g 'digdag user' -s /sbin/nologin -D digdag && \
    mkdir -p /var/lib/digdag/logs/tasks /var/lib/digdag/logs/server && \
    chown -R digdag.digdag /var/lib/digdag && \
    apk --no-cache update && \
    apk --no-cache add ruby-dev ruby-bundler ruby-json && \
    apk --no-cache add python3 py-pip py-setuptools ca-certificates curl groff less gettext && \
    apk --no-cache add bash jq && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    pip3 install --no-cache awscli==${AWSCLI_VERSION} && \
    rm -rf /var/cache/apk/*

ADD requirements.txt ./
RUN pip3 install -r ./requirements.txt

USER digdag
WORKDIR /var/lib/digdag

EXPOSE 65432
CMD exec digdag server --bind $BIND \
                       --port $PORT \
                       --config /etc/server.properties \
                       --log /var/lib/digdag/logs/server \
                       --task-log /var/lib/digdag/logs/tasks

