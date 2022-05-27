# syntax=docker/dockerfile:1
FROM dahanna/python.3.7-pandas-alpine
# Sane defaults for pip
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on

RUN apk add --update build-base linux-headers pcre pcre-dev

COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt
RUN apk add --no-cache libstdc++


RUN addgroup -g 1000 -S uwsgi && \
    adduser -u 1000 -S uwsgi -G uwsgi



COPY ./app /app


WORKDIR /app/

# Logging
RUN mkdir -p /var/log/uwsgi/app/

# Cleanups
RUN apk del build-base linux-headers pcre-dev

RUN chown -R uwsgi:uwsgi /app
RUN chmod u+w /app
#trying to enable access to write in the encryption.bin file

USER uwsgi

EXPOSE 5050

CMD ["/usr/local/bin/uwsgi", "--ini", "uwsgi.ini"]