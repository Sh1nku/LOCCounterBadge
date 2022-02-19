FROM python:3.8-alpine
RUN apk add git cloc openssh
RUN addgroup -S python && adduser -S python -G python
COPY ./ /app
WORKDIR /app
RUN chown -R python:python /app
USER python
RUN pip3 install flask pybadges gunicorn --no-cache-dir

RUN mkdir ~/.ssh
RUN ssh-keygen -b 4096 -t rsa -f ~/.ssh/id_rsa -q -N ""
RUN echo "Host *" >> ~/.ssh/config && echo "  StrictHostKeyChecking no" >> ~/.ssh/config && chmod 600 ~/.ssh/config

CMD ["/home/python/.local/bin/gunicorn", "--bind", "0.0.0.0:80", "--preload", "--workers", "16", "wsgi:app"]