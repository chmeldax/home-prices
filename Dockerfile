FROM python:3.7.0

# System-wide dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
    postgresql-client \
    curl

# Upgrade pip3
RUN pip3 install --upgrade 'pip==20.3b1'

# Install requirements for the `paysure` project
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Environment
RUN mkdir /app
WORKDIR /app

# Docker configuration
COPY docker docker

# Supervisor
RUN ln -s /app/docker/supervisord/server.conf /etc/supervisor/conf.d/server.conf
# Forcing it not to run as a daemon. Docker needs some long-running process.
RUN sed -i 's/^\(\[supervisord\]\)$/\1\nnodaemon=true/' /etc/supervisor/supervisord.conf

# Nginx
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /app/docker/nginx/server.conf /etc/nginx/sites-available/server.conf
RUN ln -s /etc/nginx/sites-available/server.conf /etc/nginx/sites-enabled/server.conf

ENTRYPOINT ["/app/docker/scripts/docker-entrypoint.sh"]

EXPOSE 80
