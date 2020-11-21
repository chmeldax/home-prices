#!/bin/bash

set -e

DIR=$(cd `dirname $0` && pwd)

# Upstream services
echo "Waiting for upstream services."
${DIR}/wait-for-upstream-services.sh
echo "Upstream services are ready."

# Django init
python3 /app/manage.py collectstatic --no-input

# Gunicorn
mkdir -p /app/tmp/

case "$1" in
    test)
        ${DIR}/test.sh
    ;;
    "")
        # Nginx
        echo Starting nginx.
        service nginx start

        # Supervisord
        echo Starting supervisord
        supervisord -c /etc/supervisor/supervisord.conf
    ;;
    *)
        exec "${@:1}"
esac
